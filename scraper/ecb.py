"""Referenzdaten von der EZB. Offizielle APIs, kein Scraping.

Drei Quellen, alle am 2026-09-01 gegen die echte API geprueft:

  1. MIR-Datensatz (Bank Interest Rates), Serie
         MIR.M.{LAND}.B.L21.A.R.A.2250.EUR.N
     = Zins auf taeglich faellige Einlagen privater Haushalte, monatlich.
     Abruf ueber data-api.ecb.europa.eu. Wichtig: im API-Pfad steht der
     Dataflow ("MIR") getrennt, der Schluessel beginnt danach mit der
     Frequenz - also /service/data/MIR/M.DE.B.L21.A.R.A.2250.EUR.N

  2. EST-Datensatz, Serie EST.B.EU000A2X2A25.WT = €STR-Tagesreihe.
     Dient als Zinsniveau-Trendindikator.

  3. eurofxref-daily.xml fuer die FX-Umrechnung.

Format ist ueberall csvdata - deutlich einfacher zu parsen als SDMX-XML
und stabil.
"""

from __future__ import annotations

import csv
import io
import xml.etree.ElementTree as ET
from typing import Any

from fetch import Fetcher
from util import cfg_get, jetzt_iso, log

BASIS = "https://data-api.ecb.europa.eu/service/data"


def _csv_beobachtungen(text: str) -> list[dict[str, str]]:
    """csvdata-Antwort -> Liste von Zeilen als Dict."""
    try:
        leser = csv.DictReader(io.StringIO(text))
        return [z for z in leser if z.get("TIME_PERIOD")]
    except Exception as e:
        log().warning("EZB-CSV nicht lesbar: %s", e)
        return []


def _serie_holen(fetcher: Fetcher, dataflow: str, schluessel: str,
                 letzte: int = 1) -> list[dict[str, str]]:
    url = f"{BASIS}/{dataflow}/{schluessel}"
    # Die data-api hat keine robots.txt-Beschraenkung fuer /service/, aber
    # wir fragen trotzdem und halten das Rate-Limit ein.
    ant = fetcher.hole(f"{url}?format=csvdata&lastNObservations={letzte}")
    if not ant.ok:
        log().warning("EZB %s/%s nicht abrufbar: %s", dataflow, schluessel, ant.fehler)
        return []
    return _csv_beobachtungen(ant.text)


def _zahl(wert: str | None) -> float | None:
    if wert is None or wert == "":
        return None
    try:
        return float(wert)
    except ValueError:
        return None


# ------------------------------------------------------------------ MIR

def mir_laender(fetcher: Fetcher, laender: list[str] | None = None) -> dict[str, Any]:
    """Tagesgeld-Durchschnitt je Land, aktuellster Monat.

    Holt alle Laender in einem Request (SDMX erlaubt DE+FR+NL im
    Schluessel) und faellt bei Problemen auf Einzelabrufe zurueck.
    """
    laender = laender or list(cfg_get("ezb.mir_laender", ["DE", "FR", "NL", "IT", "ES", "AT", "IE", "PT", "U2"]))
    muster = cfg_get("ezb.mir_serie_muster", "M.{land}.B.L21.A.R.A.2250.EUR.N")

    ergebnis: dict[str, Any] = {}

    sammel = muster.format(land="+".join(laender))
    zeilen = _serie_holen(fetcher, "MIR", sammel, letzte=2)

    if not zeilen:
        log().info("EZB MIR: Sammelabruf leer, versuche Einzelabrufe.")
        for land in laender:
            zeilen.extend(_serie_holen(fetcher, "MIR", muster.format(land=land), letzte=2))

    for zeile in zeilen:
        land = (zeile.get("REF_AREA") or "").strip()
        wert = _zahl(zeile.get("OBS_VALUE"))
        periode = (zeile.get("TIME_PERIOD") or "").strip()
        if not land or wert is None:
            continue
        vorher = ergebnis.get(land)
        if vorher and vorher["periode"] >= periode:
            continue
        ergebnis[land] = {
            "wert_pct": round(wert, 4),
            "periode": periode,
            "serie": f"MIR.{muster.format(land=land)}",
            "titel": (zeile.get("TITLE") or "").strip() or None,
            "status": (zeile.get("OBS_STATUS") or "").strip() or None,
        }

    fehlend = [l for l in laender if l not in ergebnis]
    if fehlend:
        log().warning("EZB MIR: keine Daten fuer %s", ", ".join(fehlend))
    log().info("EZB MIR: %d von %d Laendern geladen", len(ergebnis), len(laender))
    return ergebnis


# ------------------------------------------------------------------ €STR

def estr(fetcher: Fetcher, tage: int | None = None) -> dict[str, Any]:
    """€STR-Tagesreihe + Trend als Zinsniveau-Indikator."""
    tage = int(tage if tage is not None else cfg_get("ezb.estr_tage", 90))
    serie = cfg_get("ezb.estr_serie", "B.EU000A2X2A25.WT")
    zeilen = _serie_holen(fetcher, "EST", serie, letzte=tage)

    punkte = []
    for z in zeilen:
        wert = _zahl(z.get("OBS_VALUE"))
        datum = (z.get("TIME_PERIOD") or "").strip()
        if wert is not None and datum:
            punkte.append({"datum": datum, "wert_pct": round(wert, 4)})
    punkte.sort(key=lambda p: p["datum"])

    if not punkte:
        log().warning("EZB €STR: keine Daten")
        return {"aktuell_pct": None, "datum": None, "reihe": [], "trend": "unbekannt"}

    aktuell = punkte[-1]
    veraenderung_30 = None
    if len(punkte) >= 2:
        # ~30 Bankarbeitstage zurueck, sonst der aelteste vorhandene Punkt
        rueck = punkte[max(0, len(punkte) - 31)]
        veraenderung_30 = round(aktuell["wert_pct"] - rueck["wert_pct"], 4)

    if veraenderung_30 is None:
        trend = "unbekannt"
    elif veraenderung_30 > 0.05:
        trend = "steigend"
    elif veraenderung_30 < -0.05:
        trend = "fallend"
    else:
        trend = "stabil"

    log().info("EZB €STR: %.3f%% am %s (%s)", aktuell["wert_pct"], aktuell["datum"], trend)
    return {
        "aktuell_pct": aktuell["wert_pct"],
        "datum": aktuell["datum"],
        "veraenderung_30t_pp": veraenderung_30,
        "trend": trend,
        "serie": f"EST.{serie}",
        "reihe": punkte[-60:],
    }


# ------------------------------------------------------------------ FX

def fx_kurse(fetcher: Fetcher) -> dict[str, Any]:
    """eurofxref-daily.xml -> {waehrung: kurs}. 1 EUR = kurs * Waehrung."""
    url = cfg_get("ezb.fx_url", "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml")
    ant = fetcher.hole(url)
    if not ant.ok:
        log().warning("EZB FX nicht abrufbar: %s", ant.fehler)
        return {"datum": None, "kurse": {}}

    try:
        wurzel = ET.fromstring(ant.text)
    except ET.ParseError as e:
        log().warning("EZB FX-XML kaputt: %s", e)
        return {"datum": None, "kurse": {}}

    gewuenscht = set(cfg_get("ezb.fx_waehrungen", []) or [])
    kurse: dict[str, float] = {}
    datum = None

    for el in wurzel.iter():
        tag = el.tag.split("}")[-1]
        if tag != "Cube":
            continue
        if "time" in el.attrib:
            datum = el.attrib["time"]
        code = el.attrib.get("currency")
        rate = el.attrib.get("rate")
        if code and rate:
            if gewuenscht and code not in gewuenscht:
                continue
            wert = _zahl(rate)
            if wert:
                kurse[code] = wert

    kurse["EUR"] = 1.0
    log().info("EZB FX: %d Kurse vom %s", len(kurse) - 1, datum)
    return {"datum": datum, "kurse": kurse, "quelle": url}


# ------------------------------------------------------------------ Bundle

def referenzdaten(fetcher: Fetcher) -> dict[str, Any]:
    """Alle drei Referenzquellen einsammeln. Teilausfaelle sind erlaubt."""
    log().info("Referenzdaten von der EZB holen ...")
    fehler: list[str] = []

    try:
        mir = mir_laender(fetcher)
    except Exception as e:  # pragma: no cover - Netzausfall
        mir, _ = {}, fehler.append(f"MIR: {type(e).__name__}: {e}")
    try:
        est = estr(fetcher)
    except Exception as e:  # pragma: no cover
        est, _ = {}, fehler.append(f"€STR: {type(e).__name__}: {e}")
    try:
        fx = fx_kurse(fetcher)
    except Exception as e:  # pragma: no cover
        fx, _ = {"datum": None, "kurse": {}}, fehler.append(f"FX: {type(e).__name__}: {e}")

    if not mir:
        fehler.append("MIR: keine Laenderdaten")
    if not (fx or {}).get("kurse"):
        fehler.append("FX: keine Kurse")

    return {
        "stand": jetzt_iso(),
        "quelle": "European Central Bank Data Portal (data-api.ecb.europa.eu) und eurofxref",
        "lizenz_hinweis": "EZB-Daten sind frei nutzbar mit Quellenangabe.",
        "ezb_mir": mir,
        "estr": est,
        "fx": fx,
        "fehler": fehler,
    }
