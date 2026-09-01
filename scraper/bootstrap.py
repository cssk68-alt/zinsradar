"""Einmal-Skript: Was funktioniert an den Quellen wirklich?

Prueft fuer jede Quelle aus sources.yaml:
  * robots.txt - wird die Seite ueberhaupt erlaubt?
  * HTTP-Status der Seiten-URL (404/403/Timeout ...)
  * json_endpoint - erreichbar? JSON? Produkte erkennbar?
  * JSON-LD - vorhanden? verwertbar?
  * container_selector - wie viele Knoten trifft er?
  * jeder Feldselektor - trifft er im ersten Container etwas?
  * generische Heuristik - wieviel findet sie ohne Selektoren?

Das ist die Antwort auf "die Selektoren sind ungeprueft und teilweise
erfunden": Nach einem Lauf steht in docs/quellen_status.md schwarz auf
weiss, welche stimmen und welche nicht.

Aufruf:
    python scraper/bootstrap.py
    python scraper/bootstrap.py --nur biallo --speichern
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Any

import normalize
from extract import (
    FELDER, _css, _feldwert_aus_knoten, _literal, _parse, html_zu_fliesstext,
    parser_name, stufe1_json_endpoint, stufe1_jsonld, stufe2_css, stufe2_heuristik,
    html_holen,
)
from fetch import Fetcher
from util import (
    QUELLEN_STATUS_PFAD, ROOT, heute_iso, jetzt_iso, lade_quellen, log, log_einrichten,
)

SNAPSHOT_DIR = ROOT / "docs" / "snapshots"


def _argumente() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Quellen-Diagnose")
    p.add_argument("--nur", action="append", default=[], help="Nur diese Quelle(n)")
    p.add_argument("--speichern", action="store_true",
                   help="HTML-Snapshots nach docs/snapshots/ schreiben (zum Selektoren-Basteln)")
    p.add_argument("--mit-llm", action="store_true",
                   help="Auch Stufe 3 testen (kostet API-Aufrufe, braucht GEMINI_API_KEY)")
    return p.parse_args()


def pruefe_quelle(q: dict[str, Any], fetcher: Fetcher, *, speichern: bool = False,
                  mit_llm: bool = False) -> dict[str, Any]:
    ergebnis: dict[str, Any] = {
        "id": q.get("id"), "url": q.get("url"), "land": q.get("land"),
        "typ": q.get("typ"), "rendering": q.get("rendering"),
        "robots_yaml": q.get("robots_txt_erlaubt"),
        "fallstricke": q.get("fallstricke"),
        "probleme": [], "felder": {}, "empfehlung": "-",
    }

    # ---------------------------------------------------------- robots.txt
    info = fetcher.robots_pruefen(q["url"])
    ergebnis["robots_live"] = "erlaubt" if info.erlaubt else "VERBOTEN"
    ergebnis["robots_grund"] = info.grund
    ergebnis["crawl_delay"] = info.crawl_delay
    if not info.erlaubt:
        ergebnis["probleme"].append(f"robots.txt verbietet den Abruf ({info.grund})")
        ergebnis["empfehlung"] = "Quelle wird im Lauf uebersprungen"
        return ergebnis
    if str(q.get("robots_txt_erlaubt", "")).lower() == "nein":
        ergebnis["probleme"].append("YAML sagt 'nein', live-robots.txt erlaubt es - YAML ist veraltet")

    # ---------------------------------------------------------- json_endpoint
    if q.get("json_endpoint"):
        treffer, versuch = stufe1_json_endpoint(q, fetcher)
        ergebnis["json_endpoint"] = {
            "url": q["json_endpoint"], "treffer": len(treffer), "fehler": versuch.fehler,
        }
        if not treffer:
            ergebnis["probleme"].append(f"json_endpoint unbrauchbar: {versuch.fehler}")
        else:
            ergebnis["empfehlung"] = "Stufe 1 (json_endpoint)"
    else:
        ergebnis["json_endpoint"] = None

    # ---------------------------------------------------------- Seite holen
    t0 = time.monotonic()
    ant = html_holen(q, fetcher)
    ergebnis["http_status"] = ant.status
    ergebnis["http_dauer_s"] = round(time.monotonic() - t0, 1)
    ergebnis["gerendert"] = ant.gerendert
    ergebnis["bytes"] = ant.laenge

    if not ant.ok:
        ergebnis["probleme"].append(f"Seite nicht abrufbar: {ant.fehler or ('HTTP ' + str(ant.status))}")
        if ergebnis["empfehlung"] == "-":
            ergebnis["empfehlung"] = "URL pruefen / ersetzen"
        return ergebnis

    if ant.status and ant.status >= 400:
        ergebnis["probleme"].append(f"HTTP {ant.status}")

    html = ant.text
    if speichern:
        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
        ziel = SNAPSHOT_DIR / f"{q.get('id', 'quelle')}.html"
        ziel.write_text(html, encoding="utf-8", errors="replace")
        ergebnis["snapshot"] = str(ziel.relative_to(ROOT)).replace("\\", "/")

    # Bot-Schutz erkennen
    kurz = normalize.entschaerfe(html[:6000])
    for marker, name in (("just a moment", "Cloudflare"), ("cf-browser-verification", "Cloudflare"),
                         ("datadome", "DataDome"), ("captcha", "Captcha"),
                         ("access denied", "Access denied"), ("_incapsula_", "Imperva")):
        if marker in kurz:
            ergebnis["probleme"].append(f"Bot-Schutz erkannt ({name})")
            break

    # ---------------------------------------------------------- JSON-LD
    treffer_ld, versuch_ld = stufe1_jsonld(html, q)
    ergebnis["jsonld"] = {"treffer": len(treffer_ld), "detail": versuch_ld.detail,
                          "fehler": versuch_ld.fehler}
    if treffer_ld and ergebnis["empfehlung"] == "-":
        ergebnis["empfehlung"] = "Stufe 1 (JSON-LD)"

    # ---------------------------------------------------------- Selektoren
    baum = _parse(html)
    container_sel = q.get("container_selector") or ""
    container = _css(baum, container_sel) if baum else []
    ergebnis["container"] = {"selektor": container_sel, "treffer": len(container)}
    if not container:
        ergebnis["probleme"].append(f"container_selector trifft nichts: {container_sel}")

    felder_cfg = dict(q.get("felder") or {})
    basis = container[0] if container else baum
    for feld in FELDER:
        sel = felder_cfg.get(feld)
        if not sel:
            ergebnis["felder"][feld] = {"selektor": None, "status": "nicht konfiguriert"}
            continue
        lit = _literal(sel)
        if lit is not None:
            ergebnis["felder"][feld] = {"selektor": sel, "status": "literal", "beispiel": lit}
            continue
        knoten = _css(basis, sel) if basis is not None else []
        if knoten:
            beispiel = _feldwert_aus_knoten(knoten[0])[:70]
            ergebnis["felder"][feld] = {"selektor": sel, "status": "OK",
                                        "treffer": len(knoten), "beispiel": beispiel}
        else:
            ergebnis["felder"][feld] = {"selektor": sel, "status": "0 Treffer"}

    kaputte = [f for f, v in ergebnis["felder"].items() if v.get("status") == "0 Treffer"]
    if kaputte:
        ergebnis["probleme"].append(f"Feldselektoren ohne Treffer: {', '.join(kaputte)}")

    treffer_css, versuch_css = stufe2_css(html, q)
    ergebnis["stufe2_css"] = {"treffer": len(treffer_css), "fehler": versuch_css.fehler,
                              "detail": versuch_css.detail}
    if treffer_css and ergebnis["empfehlung"] == "-":
        ergebnis["empfehlung"] = "Stufe 2 (konfigurierte Selektoren)"

    # ---------------------------------------------------------- Heuristik
    treffer_h, versuch_h = stufe2_heuristik(html, q)
    ergebnis["heuristik"] = {"treffer": len(treffer_h), "detail": versuch_h.detail,
                             "fehler": versuch_h.fehler}
    if treffer_h and ergebnis["empfehlung"] == "-":
        ergebnis["empfehlung"] = "Stufe 2b (Heuristik, ohne YAML-Selektoren)"
    if treffer_h:
        ergebnis["heuristik_beispiele"] = [
            f"{t.get('bank')} - {t.get('zinssatz_pct')} %" for t in treffer_h[:4]
        ]

    # ---------------------------------------------------------- Textlaenge / LLM
    text = html_zu_fliesstext(html)
    ergebnis["fliesstext_zeichen"] = len(text)
    if len(text) < 200:
        ergebnis["probleme"].append("Fliesstext nach Reduktion sehr kurz - LLM-Stufe waere blind")

    if mit_llm and ergebnis["empfehlung"] == "-":
        from extract import stufe3_llm
        treffer_llm, versuch_llm = stufe3_llm(html, q)
        ergebnis["llm"] = {"treffer": len(treffer_llm), "fehler": versuch_llm.fehler}
        if treffer_llm:
            ergebnis["empfehlung"] = "Stufe 3 (LLM)"
            ergebnis["llm_beispiele"] = [
                f"{t.get('bank')} - {t.get('zinssatz')}" for t in treffer_llm[:4]
            ]

    if ergebnis["empfehlung"] == "-":
        ergebnis["empfehlung"] = "KEINE Stufe greift"
    return ergebnis


# ------------------------------------------------------------------ Bericht

def _ampel(e: dict[str, Any]) -> str:
    if e.get("robots_live") == "VERBOTEN":
        return "gesperrt"
    if e["empfehlung"].startswith("Stufe 1"):
        return "gut"
    if e["empfehlung"].startswith("Stufe 2 "):
        return "gut"
    if e["empfehlung"].startswith("Stufe 2b"):
        return "notduerftig"
    if e["empfehlung"].startswith("Stufe 3"):
        return "notduerftig"
    return "kaputt"


def bericht_schreiben(ergebnisse: list[dict[str, Any]]) -> str:
    z: list[str] = []
    a = z.append

    zaehler: dict[str, int] = {}
    for e in ergebnisse:
        s = _ampel(e)
        zaehler[s] = zaehler.get(s, 0) + 1

    a("# Quellen-Status")
    a("")
    a(f"Erzeugt: {jetzt_iso()} | HTML-Parser: {parser_name()}")
    a("")
    a("Erzeugt von `python scraper/bootstrap.py`. Dieser Bericht sagt, welche")
    a("Angaben aus `sources.yaml` der Realitaet standhalten. Die Selektoren dort")
    a("stammen aus einer LLM-Recherche und sind ungeprueft - hier steht das Ergebnis")
    a("der Pruefung.")
    a("")
    a("| Bewertung | Anzahl | Bedeutung |")
    a("| --- | ---: | --- |")
    a(f"| gut | {zaehler.get('gut', 0)} | Stufe 1 oder konfigurierte Selektoren greifen |")
    a(f"| notduerftig | {zaehler.get('notduerftig', 0)} | Nur Heuristik oder LLM liefert etwas |")
    a(f"| kaputt | {zaehler.get('kaputt', 0)} | Keine Stufe liefert Daten |")
    a(f"| gesperrt | {zaehler.get('gesperrt', 0)} | robots.txt verbietet den Abruf |")
    a("")

    a("## Uebersicht")
    a("")
    a("| Quelle | Land | HTTP | robots | Container | Felder OK | Heuristik | Greift |")
    a("| --- | :-: | :-: | :-: | ---: | :-: | ---: | --- |")
    for e in ergebnisse:
        felder = e.get("felder") or {}
        ok = sum(1 for v in felder.values() if v.get("status") in ("OK", "literal"))
        gesamt = sum(1 for v in felder.values() if v.get("status") != "nicht konfiguriert")
        a("| {id} | {land} | {http} | {rob} | {cont} | {ok}/{ges} | {heur} | {emp} |".format(
            id=e.get("id"), land=e.get("land"),
            http=e.get("http_status") or "-",
            rob="ja" if e.get("robots_live") == "erlaubt" else "NEIN",
            cont=(e.get("container") or {}).get("treffer", "-"),
            ok=ok, ges=gesamt,
            heur=(e.get("heuristik") or {}).get("treffer", "-"),
            emp=e.get("empfehlung"),
        ))
    a("")

    kaputte_urls = [e for e in ergebnisse
                    if e.get("http_status") in (403, 404, 410, 500, 502, 503) or e.get("http_status") is None]
    if kaputte_urls:
        a("## URLs mit Problem (404 / 403 / nicht erreichbar)")
        a("")
        for e in kaputte_urls:
            grund = "; ".join(p for p in e.get("probleme", []) if "abrufbar" in p or "HTTP" in p) \
                or f"HTTP {e.get('http_status')}"
            a(f"- `{e.get('id')}` -> {e.get('url')} : **{grund}**")
        a("")

    leere_sel = [e for e in ergebnisse if (e.get("container") or {}).get("treffer") == 0]
    if leere_sel:
        a("## container_selector ohne Treffer")
        a("")
        for e in leere_sel:
            a(f"- `{e.get('id')}`: `{(e.get('container') or {}).get('selektor')}`")
        a("")

    a("## Details je Quelle")
    a("")
    for e in ergebnisse:
        a(f"### {e.get('id')}  ({_ampel(e)})")
        a("")
        a(f"- URL: {e.get('url')}")
        a(f"- Land/Typ/Rendering: {e.get('land')} / {e.get('typ')} / {e.get('rendering')}"
          + (" (gerendert)" if e.get("gerendert") else ""))
        a(f"- robots.txt live: **{e.get('robots_live')}** ({e.get('robots_grund')})"
          + (f", crawl-delay {e.get('crawl_delay')}s" if e.get("crawl_delay") else ""))
        a(f"- YAML behauptet robots: `{e.get('robots_yaml')}`")
        a(f"- HTTP: {e.get('http_status')} , {e.get('bytes', 0)} Zeichen, {e.get('http_dauer_s', 0)}s")
        if e.get("json_endpoint"):
            je = e["json_endpoint"]
            a(f"- json_endpoint: {je['treffer']} Treffer"
              + (f" - {je['fehler']}" if je.get("fehler") else ""))
        if e.get("jsonld"):
            jl = e["jsonld"]
            a(f"- JSON-LD: {jl['treffer']} Treffer ({jl.get('detail') or jl.get('fehler')})")
        if e.get("container"):
            a(f"- container_selector `{e['container']['selektor']}`: **{e['container']['treffer']} Knoten**")
        if e.get("stufe2_css"):
            s2 = e["stufe2_css"]
            a(f"- Stufe 2 (konfiguriert): {s2['treffer']} Angebote"
              + (f" - {s2['fehler']}" if s2.get("fehler") else ""))
        if e.get("heuristik"):
            h = e["heuristik"]
            a(f"- Stufe 2b (Heuristik): {h['treffer']} Angebote"
              + (f" ueber {h['detail']}" if h.get("detail") else "")
              + (f" - {h['fehler']}" if h.get("fehler") else ""))
        for bsp in e.get("heuristik_beispiele", [])[:4]:
            a(f"    - {bsp}")
        if e.get("llm"):
            a(f"- Stufe 3 (LLM): {e['llm']['treffer']} Angebote"
              + (f" - {e['llm'].get('fehler')}" if e["llm"].get("fehler") else ""))
        a(f"- Fliesstext fuer LLM: {e.get('fliesstext_zeichen', 0)} Zeichen")
        if e.get("snapshot"):
            a(f"- Snapshot: `{e['snapshot']}`")
        a("")

        felder = e.get("felder") or {}
        if felder:
            a("| Feld | Selektor | Status | Beispielwert |")
            a("| --- | --- | :-: | --- |")
            for feld, v in felder.items():
                sel = (v.get("selektor") or "-").replace("|", "/")
                beispiel = str(v.get("beispiel") or "").replace("|", "/")[:60]
                a(f"| {feld} | `{sel}` | {v.get('status')} | {beispiel} |")
            a("")

        if e.get("probleme"):
            a("**Probleme:**")
            a("")
            for p in e["probleme"]:
                a(f"- {p}")
            a("")
        if e.get("fallstricke"):
            a(f"> Notiz aus sources.yaml: {e['fallstricke']}")
            a("")
        a(f"**Greift:** {e.get('empfehlung')}")
        a("")
        a("---")
        a("")

    text = "\n".join(z)
    QUELLEN_STATUS_PFAD.parent.mkdir(parents=True, exist_ok=True)
    QUELLEN_STATUS_PFAD.write_text(text, encoding="utf-8")
    return text


def main() -> int:
    args = _argumente()
    log_einrichten()

    quellen = lade_quellen()
    if args.nur:
        quellen = [q for q in quellen
                   if any(f.lower() in f"{q.get('id','')} {q.get('url','')}".lower() for f in args.nur)]
    if not quellen:
        log().error("Keine Quellen ausgewaehlt.")
        return 1

    log().info("Bootstrap-Check %s | %d Quellen | Parser: %s", heute_iso(), len(quellen), parser_name())
    ergebnisse: list[dict[str, Any]] = []

    with Fetcher() as fetcher:
        for i, q in enumerate(quellen, 1):
            log().info("[%2d/%2d] %s", i, len(quellen), q["url"])
            try:
                e = pruefe_quelle(q, fetcher, speichern=args.speichern, mit_llm=args.mit_llm)
            except Exception as ex:
                log().exception("  Fehler bei %s", q.get("id"))
                e = {"id": q.get("id"), "url": q.get("url"), "land": q.get("land"),
                     "probleme": [f"Ausnahme: {type(ex).__name__}: {ex}"],
                     "empfehlung": "KEINE Stufe greift", "felder": {}}
            ergebnisse.append(e)
            log().info("        -> %s", e.get("empfehlung"))

    bericht_schreiben(ergebnisse)
    log().info("Bericht geschrieben: %s", QUELLEN_STATUS_PFAD)

    gut = sum(1 for e in ergebnisse if _ampel(e) == "gut")
    log().info("Ergebnis: %d/%d Quellen liefern ueber Stufe 1 oder konfigurierte Selektoren.",
               gut, len(ergebnisse))
    return 0


if __name__ == "__main__":
    sys.exit(main())
