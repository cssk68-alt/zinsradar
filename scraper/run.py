"""Taeglicher Lauf: Quellen -> Angebote -> data/zinsen.json.

Ablauf:
    1. Referenzdaten von der EZB (MIR, €STR, FX)      -> data/referenz.json
    2. Jede Quelle durch die dreistufige Extraktion
    3. Normalisieren, Dedupe, Multi-Quellen-Merge
    4. Manuelle Overrides (gewinnen immer)
    5. Score rechnen
    6. Gegen den Vortag validieren
    7. Schreiben: data/zinsen.json, data/history/<datum>.json, docs/report.md

Aufruf:
    python scraper/run.py
    python scraper/run.py --nur biallo.de --nur ing.de
    python scraper/run.py --kein-llm --dry-run
    python scraper/run.py --keys
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Any

import ecb
import normalize
import score as score_mod
import validate
from extract import extrahiere, parser_name
from fetch import Fetcher
from util import (
    DOCS_DIR, HISTORY_DIR, OVERRIDES_PFAD, REFERENZ_PFAD, REPORT_PFAD, ZINSEN_PFAD,
    cfg_get, heute_iso, jetzt_iso, lade_config, lade_json, lade_quellen,
    log, log_einrichten, schreibe_json,
)

HINWEIS = ("Keine Anlageberatung. Alle Angaben ohne Gewaehr. "
           "Zinssaetze koennen sich jederzeit aendern - vor Abschluss beim Anbieter pruefen.")


def _argumente() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Tagesgeld-Aggregator: taeglicher Lauf")
    p.add_argument("--nur", action="append", default=[],
                   help="Nur diese Quelle(n) laufen lassen (ID oder Teil der URL). Mehrfach moeglich.")
    p.add_argument("--kein-llm", action="store_true", help="Stufe 3 (LLM) ueberspringen")
    p.add_argument("--keine-referenz", action="store_true", help="EZB-Abruf ueberspringen")
    p.add_argument("--dry-run", action="store_true", help="Nichts schreiben, nur berichten")
    p.add_argument("--keys", action="store_true",
                   help="Override-Schluessel des letzten Standes ausgeben und beenden")
    p.add_argument("--debug", action="store_true")
    return p.parse_args()


def _keys_ausgeben() -> int:
    stand = lade_json(ZINSEN_PFAD, default={}) or {}
    angebote = stand.get("angebote") or []
    if not angebote:
        print("Kein Stand in data/zinsen.json - erst einen Lauf machen.")
        return 1
    print(f"{len(angebote)} Angebote. Schluessel fuer data/overrides.json:\n")
    for a in sorted(angebote, key=lambda x: x.get("bank", "")):
        print(f'  "{a.get("override_key")}"   # {a.get("bank")} / {a.get("land")} / {a.get("zinssatz_pct")} %')
    return 0


def _quellen_filtern(quellen: list[dict], filter_liste: list[str]) -> list[dict]:
    if not filter_liste:
        return quellen
    gewaehlt = []
    for q in quellen:
        haystack = f"{q.get('id', '')} {q.get('url', '')}".lower()
        if any(f.lower() in haystack for f in filter_liste):
            gewaehlt.append(q)
    return gewaehlt


def lauf(args: argparse.Namespace) -> int:
    start = time.monotonic()
    log_einrichten()
    lade_config(neu=True)

    if args.kein_llm:
        lade_config()["extraktion"]["llm_aktiv"] = False

    quellen = lade_quellen()
    quellen = _quellen_filtern(quellen, args.nur)
    if not quellen:
        log().error("Keine Quellen ausgewaehlt.")
        return 1

    log().info("=" * 74)
    log().info("Zinsradar-Lauf %s | %d Quellen | HTML-Parser: %s", heute_iso(), len(quellen), parser_name())
    log().info("=" * 74)

    fetcher = Fetcher()
    quellen_detail: list[dict[str, Any]] = []
    rohtreffer: list[dict[str, Any]] = []
    referenz: dict[str, Any] = {}

    try:
        # ---------------------------------------------------- 1. Referenzdaten
        if args.keine_referenz:
            referenz = lade_json(REFERENZ_PFAD, default={}) or {}
            log().info("Referenzdaten uebersprungen - alter Stand wird benutzt.")
        else:
            referenz = ecb.referenzdaten(fetcher)
            if not args.dry_run:
                schreibe_json(REFERENZ_PFAD, referenz)

        fx = ((referenz.get("fx") or {}).get("kurse")) or {}

        # ---------------------------------------------------- 2. Extraktion
        log().info("-" * 74)
        log().info("Extraktion")
        for i, q in enumerate(quellen, 1):
            log().info("[%2d/%2d] %s (%s, %s)", i, len(quellen), q["url"], q.get("land"), q.get("rendering"))
            try:
                erg = extrahiere(q, fetcher)
            except Exception as e:  # eine kaputte Quelle darf den Lauf nicht killen
                log().exception("  Quelle %s wirft Ausnahme: %s", q.get("id"), e)
                quellen_detail.append({
                    "id": q.get("id"), "url": q.get("url"), "tier": None,
                    "methode": None, "treffer": 0, "fehler": f"{type(e).__name__}: {e}",
                })
                continue

            quellen_detail.append({
                "id": erg.quelle_id, "url": erg.url, "tier": erg.tier,
                "methode": erg.methode, "treffer": len(erg.treffer),
                "gesperrt": erg.gesperrt, "http_status": erg.http_status,
                "fehler": erg.fehler,
                "stufen": [{"stufe": v.stufe, "methode": v.methode, "treffer": v.treffer,
                            "fehler": v.fehler, "detail": v.detail} for v in erg.versuche],
            })

            for roh in erg.treffer:
                angebot = normalize.normalisiere(roh, q, fx)
                if angebot:
                    rohtreffer.append(angebot)
    finally:
        fetcher.schliessen()

    log().info("-" * 74)
    log().info("Rohtreffer nach Normalisierung: %d", len(rohtreffer))

    # ---------------------------------------------------- 3. Merge
    angebote = normalize.merge(rohtreffer)
    log().info("Nach Dedupe/Merge: %d Angebote", len(angebote))

    # ---------------------------------------------------- 4. Overrides
    overrides = lade_json(OVERRIDES_PFAD, default={}) or {}
    angebote, override_log = normalize.overrides_anwenden(angebote, overrides)
    for zeile in override_log:
        log().info("Override: %s", zeile)

    # ---------------------------------------------------- 5. Score
    angebote = score_mod.berechne_alle(angebote, referenz)

    # ---------------------------------------------------- 6. Validierung
    alter_stand = lade_json(ZINSEN_PFAD, default={}) or {}
    angebote, bericht = validate.validiere(angebote, alter_stand, referenz)

    # Nach der Validierung, weil erst dort die uebernommenen Vortagseintraege
    # dazukommen: die haben die Qualitaetsfilter dieses Laufs noch nie gesehen.
    angebote, saeuberung = normalize.altbestand_saeubern(angebote)
    for zeile in saeuberung:
        log().info("Altbestand: %s", zeile)
    bericht["altbestand_saeuberung"] = saeuberung
    # Der Report zaehlt sonst den Stand VOR der Saeuberung.
    bericht["ergebnis_gesamt"] = len(angebote)
    bericht["stale_gesamt"] = sum(1 for a in angebote if a.get("stale"))
    angebote.sort(key=lambda a: (-(a.get("score_mit_erstattung") or -99), a.get("bank", "")))

    # ---------------------------------------------------- 7. Schreiben
    tier_verteilung: dict[str, int] = {}
    for a in angebote:
        t = str(a.get("extraction_tier") or "?")
        tier_verteilung[t] = tier_verteilung.get(t, 0) + 1

    dauer = round(time.monotonic() - start, 1)
    lauf_meta = {
        "stand": jetzt_iso(),
        "quellen_gesamt": len(quellen),
        "quellen_erfolg": sum(1 for q in quellen_detail if q.get("treffer")),
        "quellen_robots": sum(1 for q in quellen_detail if q.get("gesperrt")),
        "quellen_leer": sum(1 for q in quellen_detail if not q.get("treffer") and not q.get("gesperrt")),
        "rohtreffer": len(rohtreffer),
        "angebote_dedupe": len(angebote),
        "tier_verteilung": tier_verteilung,
        "quellen_detail": quellen_detail,
        "referenz_fehler": referenz.get("fehler") or [],
        "dauer_s": dauer,
    }

    ausgabe = {
        "version": 1,
        "stand": jetzt_iso(),
        "stand_datum": heute_iso(),
        "erzeugt_von": "scraper/run.py",
        "hinweis": HINWEIS,
        "statistik": {
            "angebote": len(angebote),
            "stale": bericht.get("stale_gesamt", 0),
            "quellen_gesamt": lauf_meta["quellen_gesamt"],
            "quellen_erfolg": lauf_meta["quellen_erfolg"],
            "tier_verteilung": tier_verteilung,
            "dauer_s": dauer,
        },
        "berechnung": {
            "risiko_abschlag_pp": cfg_get("score.risiko_abschlag_pp", {}),
            "abgeltungssteuer_de_pct": cfg_get("score.abgeltungssteuer_de_pct", 26.375),
            "formel_brutto": "(aktionszins * min(aktionsdauer,12) + folgezins * max(0, 12-aktionsdauer)) / 12",
            "formel_netto": "brutto_12m * (1 - qst_effektiv)",
            "formel_score": "netto_12m - risiko_abschlag[staatsrating_sp]",
        },
        "referenz": {
            "stand": referenz.get("stand"),
            "ezb_mir": referenz.get("ezb_mir") or {},
            "estr": {k: v for k, v in (referenz.get("estr") or {}).items() if k != "reihe"},
            "estr_reihe": ((referenz.get("estr") or {}).get("reihe") or [])[-30:],
            "fx_datum": (referenz.get("fx") or {}).get("datum"),
            "fx_kurse": (referenz.get("fx") or {}).get("kurse") or {},
        },
        "quellen_status": [
            {"id": q["id"], "url": q["url"], "tier": q.get("tier"),
             "methode": q.get("methode"), "treffer": q.get("treffer", 0),
             "fehler": (q.get("fehler") or "")[:200]}
            for q in quellen_detail
        ],
        "angebote": angebote,
    }

    if args.dry_run:
        log().info("--dry-run: nichts geschrieben. %d Angebote waeren gespeichert worden.", len(angebote))
    else:
        schreibe_json(ZINSEN_PFAD, ausgabe)
        schreibe_json(HISTORY_DIR / f"{heute_iso()}.json", ausgabe)
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        validate.report_schreiben(REPORT_PFAD, bericht, lauf_meta)
        log().info("Geschrieben: %s (%d Angebote)", ZINSEN_PFAD, len(angebote))

    log().info("=" * 74)
    log().info("Fertig in %.1fs | %d Angebote | %d stale | Quellen mit Treffer: %d/%d",
               dauer, len(angebote), bericht.get("stale_gesamt", 0),
               lauf_meta["quellen_erfolg"], lauf_meta["quellen_gesamt"])
    for stufe in sorted(tier_verteilung):
        log().info("   Stufe %s: %d Angebote", stufe, tier_verteilung[stufe])
    log().info("=" * 74)

    # Exit 0 auch bei mageren Laeufen - der Workflow soll trotzdem committen.
    # Nur ein Totalausfall ohne jeden Vortagsstand ist ein Fehler.
    if not angebote:
        log().error("Keine Angebote und kein Vortagsstand - das ist ein Fehler.")
        return 2
    return 0


def main() -> int:
    args = _argumente()
    if args.keys:
        log_einrichten()
        return _keys_ausgeben()
    try:
        return lauf(args)
    except KeyboardInterrupt:
        log().warning("Abgebrochen.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
