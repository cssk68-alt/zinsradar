"""Plausibilitaetspruefung gegen den Vortag und gegen die EZB.

Regeln aus der Aufgabenstellung:
  * 0 Treffer insgesamt              -> kompletten Vortagsstand behalten, stale
  * Zins > 10 %                      -> alten Wert behalten, stale
  * Abweichung > 2 pp zum Vortag     -> alten Wert behalten, stale
  * Zins > 3 pp ueber EZB-Schnitt    -> flag "pruefen" (Wert bleibt stehen)
Alles davon landet in docs/report.md.

Zwei Ergaenzungen, die sich aus der Regel "alten Wert behalten" ergeben
und in der README als Annahme stehen:
  * Ein Angebot, das gestern da war und heute fehlt, verschwindet nicht
    sofort, sondern bleibt `stale` - sonst wuerde ein einziger
    Netzwerkfehler die halbe Liste leeren. Nach `max_stale_tage`
    (Default 14) faellt es raus.
  * Ein neuer Eintrag mit unplausiblem Zins hat keinen "alten Wert", den
    man behalten koennte. Er wird verworfen und im Report genannt.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from util import cfg_get, heute_iso, log


def _zins(a: dict[str, Any]) -> float | None:
    w = a.get("zinssatz_pct")
    try:
        return float(w) if w is not None else None
    except (TypeError, ValueError):
        return None


def _tage_seit(datum_str: str | None) -> int:
    if not datum_str:
        return 0
    try:
        d = datetime.fromisoformat(str(datum_str)[:10]).date()
    except ValueError:
        return 0
    return (date.today() - d).days


def validiere(neue: list[dict[str, Any]],
              alter_stand: dict[str, Any] | None,
              referenz: dict[str, Any] | None = None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Neue Angebote pruefen. Gibt (gepruefte Liste, Pruefbericht) zurueck."""
    max_zins = float(cfg_get("validierung.max_zins_pct", 10.0))
    max_abweichung = float(cfg_get("validierung.max_abweichung_vortag_pp", 2.0))
    ezb_flag_pp = float(cfg_get("validierung.ezb_abstand_flag_pp", 3.0))
    min_treffer = int(cfg_get("validierung.min_treffer_gesamt", 1))
    max_stale = int(cfg_get("validierung.max_stale_tage", 14))
    heute = heute_iso()

    alte_liste: list[dict[str, Any]] = list((alter_stand or {}).get("angebote") or [])
    alt_nach_key: dict[str, dict[str, Any]] = {
        a.get("dedupe_key", ""): a for a in alte_liste if a.get("dedupe_key")
    }

    bericht: dict[str, Any] = {
        "datum": heute,
        "neu_gefunden": len(neue),
        "vortag_bestand": len(alte_liste),
        "komplettausfall": False,
        "zins_zu_hoch": [],
        "sprung_zum_vortag": [],
        "ezb_abweichung": [],
        "verschwunden_stale": [],
        "ausgelaufen_entfernt": [],
        "neu_hinzugekommen": [],
        "stale_gesamt": 0,
    }

    # ---------------------------------------------------------- Komplettausfall
    if len(neue) < min_treffer:
        bericht["komplettausfall"] = True
        log().error("VALIDIERUNG: %d Treffer (< %d) - kompletter Vortagsstand wird behalten.",
                    len(neue), min_treffer)
        behalten: list[dict[str, Any]] = []
        for alt in alte_liste:
            a = dict(alt)
            a["stale"] = True
            a["stale_seit"] = a.get("stale_seit") or a.get("stand") or heute
            a["stale_grund"] = "Lauf ohne Treffer - Vortagswert behalten"
            if _tage_seit(a.get("stale_seit")) <= max_stale:
                behalten.append(a)
            else:
                bericht["ausgelaufen_entfernt"].append(a.get("bank"))
        bericht["stale_gesamt"] = len(behalten)
        return behalten, bericht

    # ---------------------------------------------------------- Einzelpruefung
    geprueft: list[dict[str, Any]] = []
    gesehene_keys: set[str] = set()

    for a in neue:
        key = a.get("dedupe_key", "")
        gesehene_keys.add(key)
        alt = alt_nach_key.get(key)
        zins_neu = _zins(a)
        zins_alt = _zins(alt) if alt else None

        a.setdefault("stand", heute)
        a["stale"] = False
        a.pop("stale_grund", None)

        # --- Regel: Zins > 10 %
        if zins_neu is None or zins_neu > max_zins:
            eintrag = {
                "bank": a.get("bank"), "land": a.get("land"),
                "wert": zins_neu, "grenze": max_zins,
                "quelle": (a.get("quellen") or [{}])[0].get("id"),
            }
            bericht["zins_zu_hoch"].append(eintrag)
            if alt and zins_alt is not None:
                ersatz = _als_stale(alt, heute, f"Neuer Zins {zins_neu} % > {max_zins} % - Vortagswert behalten")
                geprueft.append(ersatz)
                log().warning("  %s: Zins %.2f%% unplausibel - Vortagswert %.2f%% behalten",
                              a.get("bank"), zins_neu or -1, zins_alt)
            else:
                log().warning("  %s: Zins %.2f%% unplausibel und kein Vortagswert - verworfen",
                              a.get("bank"), zins_neu or -1)
                eintrag["verworfen"] = True
            continue

        # --- Regel: Sprung > 2 pp zum Vortag
        if zins_alt is not None and abs(zins_neu - zins_alt) > max_abweichung:
            bericht["sprung_zum_vortag"].append({
                "bank": a.get("bank"), "land": a.get("land"),
                "alt": zins_alt, "neu": zins_neu,
                "differenz_pp": round(zins_neu - zins_alt, 3),
                "quelle": (a.get("quellen") or [{}])[0].get("id"),
            })
            ersatz = _als_stale(
                alt, heute,
                f"Sprung {zins_alt} % -> {zins_neu} % ({zins_neu - zins_alt:+.2f} pp) groesser als {max_abweichung} pp",
            )
            ersatz["verworfener_neuwert_pct"] = zins_neu
            geprueft.append(ersatz)
            log().warning("  %s: Sprung %+.2f pp - Vortagswert behalten", a.get("bank"), zins_neu - zins_alt)
            continue

        # --- Regel: mehr als 3 pp ueber EZB-Landesdurchschnitt -> pruefen
        ezb = a.get("ezb_landesdurchschnitt_pct")
        if ezb is not None and (zins_neu - float(ezb)) > ezb_flag_pp:
            a["flag"] = "pruefen"
            a["flag_grund"] = (f"{zins_neu:.2f} % liegt {zins_neu - float(ezb):.2f} pp ueber dem "
                               f"EZB-Landesdurchschnitt ({float(ezb):.2f} %, {a.get('ezb_periode')})")
            bericht["ezb_abweichung"].append({
                "bank": a.get("bank"), "land": a.get("land"),
                "zins": zins_neu, "ezb": float(ezb),
                "differenz_pp": round(zins_neu - float(ezb), 3),
            })
            log().info("  %s: %+.2f pp ueber EZB-Schnitt - Flag 'pruefen'", a.get("bank"), zins_neu - float(ezb))

        if alt is None:
            bericht["neu_hinzugekommen"].append({"bank": a.get("bank"), "land": a.get("land"), "zins": zins_neu})
        else:
            a["vortag_zins_pct"] = zins_alt
            if zins_alt is not None:
                a["veraenderung_pp"] = round(zins_neu - zins_alt, 4)

        geprueft.append(a)

    # ---------------------------------------------------------- Verschwundene
    from normalize import bank_plausibel

    for key, alt in alt_nach_key.items():
        if key in gesehene_keys:
            continue
        # Wurde der Namensfilter seit dem letzten Lauf verschaerft, darf ein
        # frueher faelschlich aufgenommener Eintrag nicht als "stale"
        # weiterleben - er waere sonst 14 Tage lang in der Liste.
        if not bank_plausibel(alt.get("bank")):
            bericht["ausgelaufen_entfernt"].append(str(alt.get("bank")) + " (Name nicht plausibel)")
            continue
        a = _als_stale(alt, heute, "In diesem Lauf nicht mehr gefunden")
        if _tage_seit(a["stale_seit"]) > max_stale:
            bericht["ausgelaufen_entfernt"].append(a.get("bank"))
            continue
        bericht["verschwunden_stale"].append({
            "bank": a.get("bank"), "land": a.get("land"),
            "seit": a["stale_seit"], "tage": _tage_seit(a["stale_seit"]),
        })
        geprueft.append(a)

    bericht["stale_gesamt"] = sum(1 for a in geprueft if a.get("stale"))
    bericht["ergebnis_gesamt"] = len(geprueft)
    return geprueft, bericht


def _als_stale(alt: dict[str, Any], heute: str, grund: str) -> dict[str, Any]:
    a = dict(alt)
    a["stale"] = True
    a["stale_seit"] = a.get("stale_seit") or a.get("stand") or heute
    a["stale_grund"] = grund
    a["stand"] = a.get("stand") or heute
    return a


# ------------------------------------------------------------------ Report

def report_schreiben(pfad, bericht: dict[str, Any], lauf_meta: dict[str, Any]) -> str:
    """docs/report.md erzeugen. Gibt den Text auch zurueck."""
    z: list[str] = []
    a = z.append

    a(f"# Lauf-Report {bericht.get('datum')}")
    a("")
    a(f"Erstellt: {lauf_meta.get('stand', '')}")
    a("")

    a("## Zusammenfassung")
    a("")
    a("| Kennzahl | Wert |")
    a("| --- | ---: |")
    a(f"| Quellen gesamt | {lauf_meta.get('quellen_gesamt', 0)} |")
    a(f"| Quellen mit Treffer | {lauf_meta.get('quellen_erfolg', 0)} |")
    a(f"| Quellen durch robots.txt uebersprungen | {lauf_meta.get('quellen_robots', 0)} |")
    a(f"| Quellen ohne Treffer | {lauf_meta.get('quellen_leer', 0)} |")
    a(f"| Rohtreffer | {lauf_meta.get('rohtreffer', 0)} |")
    a(f"| Angebote nach Dedupe | {lauf_meta.get('angebote_dedupe', 0)} |")
    a(f"| Angebote im Ergebnis | {bericht.get('ergebnis_gesamt', bericht.get('stale_gesamt', 0))} |")
    a(f"| davon stale | {bericht.get('stale_gesamt', 0)} |")
    a(f"| Laufzeit (s) | {lauf_meta.get('dauer_s', 0)} |")
    a("")

    tiers = lauf_meta.get("tier_verteilung") or {}
    if tiers:
        a("### Extraktionsstufen")
        a("")
        a("| Stufe | Angebote |")
        a("| --- | ---: |")
        for stufe in sorted(tiers):
            a(f"| Stufe {stufe} | {tiers[stufe]} |")
        a("")

    quellen_zeilen = lauf_meta.get("quellen_detail") or []
    if quellen_zeilen:
        a("### Welche Quelle lief auf welcher Stufe")
        a("")
        a("| Quelle | Stufe | Methode | Treffer | Hinweis |")
        a("| --- | :-: | --- | ---: | --- |")
        for q in quellen_zeilen:
            hinweis = (q.get("fehler") or "").replace("|", "/")[:110]
            a(f"| {q.get('id')} | {q.get('tier') or '-'} | {q.get('methode') or '-'} "
              f"| {q.get('treffer', 0)} | {hinweis} |")
        a("")

    if bericht.get("komplettausfall"):
        a("## ACHTUNG: Lauf ohne Treffer")
        a("")
        a("Es wurde kein einziges Angebot gefunden. Der komplette Vortagsstand ")
        a("wurde uebernommen und als `stale` markiert.")
        a("")

    def block(titel: str, schluessel: str, formatierer) -> None:
        eintraege = bericht.get(schluessel) or []
        if not eintraege:
            return
        a(f"## {titel} ({len(eintraege)})")
        a("")
        for e in eintraege:
            a(f"- {formatierer(e)}")
        a("")

    block("Zins ueber Grenzwert - Vortagswert behalten", "zins_zu_hoch",
          lambda e: (f"**{e.get('bank')}** ({e.get('land')}): {e.get('wert')} % > {e.get('grenze')} %"
                     f"{' - VERWORFEN, kein Vortagswert' if e.get('verworfen') else ''}"
                     f" [Quelle: {e.get('quelle')}]"))

    block("Sprung zum Vortag groesser als erlaubt - Vortagswert behalten", "sprung_zum_vortag",
          lambda e: (f"**{e.get('bank')}** ({e.get('land')}): {e.get('alt')} % -> {e.get('neu')} % "
                     f"({e.get('differenz_pp'):+} pp) [Quelle: {e.get('quelle')}]"))

    block("Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen'", "ezb_abweichung",
          lambda e: (f"**{e.get('bank')}** ({e.get('land')}): {e.get('zins')} % vs. EZB "
                     f"{e.get('ezb')} % ({e.get('differenz_pp'):+} pp)"))

    block("Heute nicht gefunden - als stale behalten", "verschwunden_stale",
          lambda e: f"**{e.get('bank')}** ({e.get('land')}), stale seit {e.get('seit')} ({e.get('tage')} Tage)")

    block("Zu lange stale - entfernt", "ausgelaufen_entfernt", lambda e: f"**{e}**")

    block("Neu hinzugekommen", "neu_hinzugekommen",
          lambda e: f"**{e.get('bank')}** ({e.get('land')}): {e.get('zins')} %")

    fehler = lauf_meta.get("referenz_fehler") or []
    if fehler:
        a("## Referenzdaten unvollstaendig")
        a("")
        for f in fehler:
            a(f"- {f}")
        a("")

    a("---")
    a("")
    a("Angaben ohne Gewaehr. Keine Anlageberatung.")
    a("")

    text = "\n".join(z)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(text, encoding="utf-8")
    log().info("Report geschrieben: %s", pfad)
    return text
