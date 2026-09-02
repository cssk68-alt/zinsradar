"""Berechnung: Bruttozins ueber 12 Monate, Quellensteuer, Risiko, Score.

Formeln aus der Aufgabenstellung:

    brutto_12m = (aktionszins * min(aktionsdauer, 12)
                  + folgezins * max(0, 12 - aktionsdauer)) / 12

    netto_12m  = brutto_12m * (1 - qst_effektiv)

    qst_effektiv = 0, wenn rueckerstattung_aufwand in ("keiner","niedrig")
                      UND Setting "Rueckerstattung selbst machen" = an,
                   sonst quellensteuer_mit_dba_pct

    score = netto_12m - risiko_abschlag[staatsrating_sp]

Weil das Setting in der App sitzt und nicht im Scraper, werden BEIDE
Varianten vorberechnet und mitgeliefert:
    netto_12m_mit_erstattung / score_mit_erstattung
    netto_12m_ohne_erstattung / score_ohne_erstattung
Die App schaltet nur zwischen zwei fertigen Zahlen um.

Zwei dokumentierte Annahmen (siehe README, Abschnitt "Annahmen"):
  A) Inlandsfall DE: withholding.json fuehrt fuer DE 25 % - das ist die
     deutsche Abgeltungssteuer, keine auslaendische Quellensteuer. Die
     Vorgabe sagt ausdruecklich, die Abgeltungssteuer gehoert NICHT in
     den Score. qst_effektiv ist fuer DE daher immer 0; die 25 % (bzw.
     26,375 % mit Soli) erscheinen nur im Anzeige-Toggle.
  B) Fehlt der Folgezins bei einer befristeten Aktion, wird der
     EZB-Landesdurchschnitt als Schaetzung eingesetzt und der Eintrag
     mit `folgezins_geschaetzt: true` markiert. Ohne EZB-Wert wird 0
     angenommen - lieber zu vorsichtig als zu optimistisch.
"""

from __future__ import annotations

import re
from typing import Any

from util import LAENDER_PFAD, WITHHOLDING_PFAD, cfg_get, lade_json, log

INLANDSFALL = "DE"  # Sitzland des Anlegers


# ------------------------------------------------------------------ Stammdaten

def lade_stammdaten() -> tuple[dict[str, dict], dict[str, dict]]:
    """withholding.json und laender.json als Dicts nach Land."""
    qst_liste = lade_json(WITHHOLDING_PFAD, default=[]) or []
    laender_liste = lade_json(LAENDER_PFAD, default=[]) or []

    qst = {str(e.get("land", "")).upper(): e for e in qst_liste if e.get("land")}
    laender = {str(e.get("land", "")).upper(): e for e in laender_liste if e.get("land")}
    return qst, laender


# ------------------------------------------------------------------ Bausteine

def brutto_12m(aktionszins: float, aktionsdauer_monate: int | None,
               folgezins: float | None) -> float:
    """Gewichteter Durchschnittszins ueber die naechsten 12 Monate."""
    dauer = max(0, min(int(aktionsdauer_monate or 0), 12))
    folge = float(folgezins) if folgezins is not None else 0.0
    return (float(aktionszins) * dauer + folge * (12 - dauer)) / 12.0


def qst_effektiv_pct(land: str | None, qst_daten: dict[str, dict],
                     erstattung_selbst: bool) -> tuple[float, str]:
    """Effektive Quellensteuer in Prozent + Begruendung fuer die App."""
    code = (land or "").upper()

    if code == INLANDSFALL:
        return 0.0, ("Inlandsfall: keine ausländische Quellensteuer. "
                     "Die deutsche Abgeltungssteuer ist im Score bewusst nicht enthalten.")

    eintrag = qst_daten.get(code)
    if not eintrag:
        return 0.0, "Kein Quellensteuer-Datensatz für dieses Land – 0 % angenommen."

    aufwand = str(eintrag.get("rueckerstattung_aufwand", "")).lower()
    mit_dba = float(eintrag.get("quellensteuer_mit_dba_pct") or 0.0)

    if aufwand in ("keiner", "niedrig") and erstattung_selbst:
        return 0.0, (f"Rückerstattungsaufwand '{aufwand}' und Erstattung selbst erledigt "
                     f"→ 0 % statt {mit_dba:.2f} %.")
    if aufwand in ("keiner", "niedrig"):
        return mit_dba, (f"Rückerstattung wäre '{aufwand}', Einstellung ist aus "
                         f"→ {mit_dba:.2f} % einbehalten.")
    return mit_dba, (f"Rückerstattungsaufwand '{aufwand}' → mit DBA verbleiben "
                     f"{mit_dba:.2f} %.")


_RATING_STUFEN = ("AAA", "AA", "A", "BBB", "BB", "B", "CCC", "CC", "C", "D")


def rating_gruppe(rating: str | None) -> str:
    """'AA+' -> 'AA', 'A-' -> 'A'. Unbekannt -> ''."""
    if not rating:
        return ""
    r = re.sub(r"[^A-Za-z]", "", str(rating)).upper()
    for stufe in _RATING_STUFEN:  # laengste zuerst
        if r == stufe:
            return stufe
    for stufe in _RATING_STUFEN:
        if r.startswith(stufe):
            return stufe
    return ""


def risiko_abschlag_pp(rating: str | None) -> float:
    """Abschlag in Prozentpunkten laut config.json."""
    tabelle = cfg_get("score.risiko_abschlag_pp", {}) or {}
    gruppe = rating_gruppe(rating)
    if gruppe and gruppe in tabelle:
        return float(tabelle[gruppe])
    return float(tabelle.get("_default", 0.60))


# ------------------------------------------------------------------ Hauptlauf

def berechne(angebot: dict[str, Any], qst_daten: dict[str, dict],
             laender_daten: dict[str, dict],
             referenz: dict[str, Any] | None = None) -> dict[str, Any]:
    """Ein Angebot um alle Rechenfelder ergaenzen. Aendert das Dict direkt."""
    land = (angebot.get("einlagensicherung_land") or angebot.get("land") or "").upper() or None
    land_info = laender_daten.get(land or "", {})
    qst_info = qst_daten.get(land or "", {})

    zins = float(angebot.get("zinssatz_pct") or 0.0)
    dauer = int(angebot.get("aktionsdauer_monate") or 0)
    folge = angebot.get("folgezins_pct")

    # Annahme B: fehlender Folgezins bei befristeter Aktion
    geschaetzt = False
    if folge is None:
        if dauer <= 0:
            folge = zins  # kein Aktionszeitraum -> der Zins laeuft weiter
        else:
            mir = ((referenz or {}).get("ezb_mir") or {}).get(land or "", {})
            schaetzung = mir.get("wert_pct")
            folge = float(schaetzung) if schaetzung is not None else 0.0
            geschaetzt = True

    b12 = brutto_12m(zins, dauer, folge)

    qst_mit, grund_mit = qst_effektiv_pct(land, qst_daten, erstattung_selbst=True)
    qst_ohne, grund_ohne = qst_effektiv_pct(land, qst_daten, erstattung_selbst=False)

    netto_mit = b12 * (1.0 - qst_mit / 100.0)
    netto_ohne = b12 * (1.0 - qst_ohne / 100.0)

    rating = land_info.get("staatsrating_sp")
    abschlag = risiko_abschlag_pp(rating)

    abg_pct = float(cfg_get("score.abgeltungssteuer_de_pct", 26.375))

    # EZB-Vergleich
    mir = ((referenz or {}).get("ezb_mir") or {}).get(land or "", {})
    ezb_wert = mir.get("wert_pct")
    diff_ezb = round(zins - float(ezb_wert), 4) if ezb_wert is not None else None

    angebot.update({
        "brutto_12m_pct": round(b12, 4),
        "folgezins_pct": round(float(folge), 4) if folge is not None else None,
        "folgezins_geschaetzt": geschaetzt,

        "qst_effektiv_mit_erstattung_pct": round(qst_mit, 4),
        "qst_effektiv_ohne_erstattung_pct": round(qst_ohne, 4),
        "qst_begruendung_mit_erstattung": grund_mit,
        "qst_begruendung_ohne_erstattung": grund_ohne,
        "qst_standard_pct": qst_info.get("quellensteuer_standard_pct"),
        "qst_mit_dba_pct": qst_info.get("quellensteuer_mit_dba_pct"),
        "rueckerstattung_aufwand": qst_info.get("rueckerstattung_aufwand"),
        "rueckerstattung_moeglich": qst_info.get("rueckerstattung_moeglich"),
        "rueckerstattung_formular": qst_info.get("formular_bezeichnung"),
        "rueckerstattung_quelle": qst_info.get("quelle_url"),

        "netto_12m_mit_erstattung_pct": round(netto_mit, 4),
        "netto_12m_ohne_erstattung_pct": round(netto_ohne, 4),

        "staatsrating_sp": rating,
        "staatsrating_moodys": land_info.get("staatsrating_moodys"),
        "rating_gruppe": rating_gruppe(rating),
        "risiko_abschlag_pp": round(abschlag, 4),

        "score_mit_erstattung": round(netto_mit - abschlag, 4),
        "score_ohne_erstattung": round(netto_ohne - abschlag, 4),

        "einlagensicherung_betrag_eur": land_info.get("einlagensicherung_betrag_eur"),
        "sicherungssystem_name": land_info.get("sicherungssystem_name"),
        "sicherung_quelle": land_info.get("quelle_url"),
        "land_waehrung": land_info.get("waehrung"),

        # Nur Anzeige - absichtlich NICHT im Score.
        "netto_nach_abgeltungssteuer_mit_erstattung_pct": round(netto_mit * (1 - abg_pct / 100.0), 4),
        "netto_nach_abgeltungssteuer_ohne_erstattung_pct": round(netto_ohne * (1 - abg_pct / 100.0), 4),

        "ezb_landesdurchschnitt_pct": ezb_wert,
        "ezb_periode": mir.get("periode"),
        "differenz_zu_ezb_pp": diff_ezb,
    })
    return angebot


def berechne_alle(angebote: list[dict[str, Any]],
                  referenz: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    qst_daten, laender_daten = lade_stammdaten()
    if not qst_daten:
        log().warning("withholding.json leer - Quellensteuer wird ueberall mit 0 %% gerechnet.")
    if not laender_daten:
        log().warning("laender.json leer - Ratings und Einlagensicherung fehlen.")

    for a in angebote:
        berechne(a, qst_daten, laender_daten, referenz)

    angebote.sort(key=lambda a: (-(a.get("score_mit_erstattung") or -99), a.get("bank", "")))
    return angebote
