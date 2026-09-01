"""Gemeinsame Helfer: Pfade, Config, JSON-IO, Logging.

Bewusst klein gehalten. Alles, was mehr als ein Modul braucht, steht hier -
alles andere bleibt in seinem Modul.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------- Pfade

SCRAPER_DIR = Path(__file__).resolve().parent
ROOT = SCRAPER_DIR.parent
DATA_DIR = ROOT / "data"
HISTORY_DIR = DATA_DIR / "history"
DOCS_DIR = ROOT / "docs"
APP_DIR = ROOT / "app"

CONFIG_PFAD = ROOT / "config.json"
SOURCES_PFAD = SCRAPER_DIR / "sources.yaml"
ZINSEN_PFAD = DATA_DIR / "zinsen.json"
REFERENZ_PFAD = DATA_DIR / "referenz.json"
WITHHOLDING_PFAD = DATA_DIR / "withholding.json"
LAENDER_PFAD = DATA_DIR / "laender.json"
OVERRIDES_PFAD = DATA_DIR / "overrides.json"
REPORT_PFAD = DOCS_DIR / "report.md"
QUELLEN_STATUS_PFAD = DOCS_DIR / "quellen_status.md"


# ---------------------------------------------------------------- Zeit

def heute_iso() -> str:
    return date.today().isoformat()


def jetzt_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ---------------------------------------------------------------- JSON

def lade_json(pfad: Path, default: Any = None) -> Any:
    """Laedt JSON. Fehlende oder kaputte Datei -> default, kein Absturz."""
    try:
        with open(pfad, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, OSError) as e:
        logging.getLogger("zinsradar").warning("JSON kaputt: %s (%s)", pfad, e)
        return default


def schreibe_json(pfad: Path, daten: Any, *, indent: int = 2) -> None:
    """Atomar schreiben: erst Tempdatei, dann umbenennen.

    Verhindert halb geschriebene Dateien, wenn der Workflow abbricht -
    die PWA wuerde sonst kaputtes JSON vom raw-Endpoint ziehen.
    """
    pfad.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(pfad.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(daten, f, ensure_ascii=False, indent=indent, sort_keys=False)
            f.write("\n")
        os.replace(tmp, pfad)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


# ---------------------------------------------------------------- Config

_config_cache: dict[str, Any] | None = None


def lade_config(neu: bool = False) -> dict[str, Any]:
    global _config_cache
    if _config_cache is None or neu:
        cfg = lade_json(CONFIG_PFAD, default={})
        if not cfg:
            logging.getLogger("zinsradar").warning(
                "config.json fehlt oder ist leer - benutze eingebaute Defaults."
            )
            cfg = _DEFAULT_CONFIG
        _config_cache = cfg
    return _config_cache


def cfg_get(pfad: str, default: Any = None) -> Any:
    """Punktpfad-Zugriff, z.B. cfg_get('fetch.timeout_s', 30)."""
    knoten: Any = lade_config()
    for teil in pfad.split("."):
        if not isinstance(knoten, dict) or teil not in knoten:
            return default
        knoten = knoten[teil]
    return knoten


_DEFAULT_CONFIG: dict[str, Any] = {
    "score": {
        "risiko_abschlag_pp": {"AAA": 0.0, "AA": 0.05, "A": 0.10, "BBB": 0.25, "_default": 0.60},
        "abgeltungssteuer_de_pct": 26.375,
    },
    "validierung": {
        "max_zins_pct": 10.0,
        "max_abweichung_vortag_pp": 2.0,
        "ezb_abstand_flag_pp": 3.0,
        "min_treffer_gesamt": 1,
        "max_stale_tage": 14,
    },
    "fetch": {
        "min_abstand_pro_domain_s": 2.0,
        "timeout_s": 30.0,
        "max_versuche": 3,
        "backoff_faktor": 2.0,
        "backoff_basis_s": 1.5,
        "robots_respektieren": True,
        "robots_cache_s": 3600,
        "user_agent": "ZinsradarBot/1.0",
        "playwright_timeout_ms": 25000,
        "playwright_warte_auf": "networkidle",
    },
    "extraktion": {
        "llm_aktiv": True,
        "llm_modell": "gemini-2.0-flash",
        "llm_max_zeichen": 8000,
        "llm_timeout_s": 60.0,
        "heuristik_aktiv": True,
        "confidence": {
            "tier1_json_endpoint": 0.95,
            "tier1_jsonld": 0.9,
            "tier2_css_konfiguriert": 0.75,
            "tier2_css_heuristik": 0.5,
            "tier3_llm": 0.4,
        },
        "min_confidence_aufnahme": 0.3,
    },
}


# ---------------------------------------------------------------- Quellen

def lade_quellen() -> list[dict[str, Any]]:
    """Laedt sources.yaml. Akzeptiert reine Liste oder {'quellen': [...]}."""
    import yaml  # lokal, damit util.py ohne PyYAML importierbar bleibt

    with open(SOURCES_PFAD, "r", encoding="utf-8") as f:
        roh = yaml.safe_load(f)

    if isinstance(roh, dict):
        quellen = roh.get("quellen") or []
    elif isinstance(roh, list):
        quellen = roh
    else:
        quellen = []

    for q in quellen:
        q.setdefault("id", quelle_id(q.get("url", "")))
    return [q for q in quellen if q.get("url")]


def quelle_id(url: str) -> str:
    """Stabile Kurz-ID aus der Domain. sources.yaml braucht kein id-Feld."""
    from urllib.parse import urlparse

    host = (urlparse(url).hostname or "unbekannt").lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def domain_von(url: str) -> str:
    from urllib.parse import urlparse

    return (urlparse(url).hostname or "").lower()


# ---------------------------------------------------------------- Logging

def log_einrichten(level: int = logging.INFO, datei: Path | None = None) -> logging.Logger:
    logger = logging.getLogger("zinsradar")
    if logger.handlers:
        return logger
    logger.setLevel(level)

    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(message)s", datefmt="%H:%M:%S")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    if datei is not None:
        datei.parent.mkdir(parents=True, exist_ok=True)
        fh = logging.FileHandler(datei, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def log() -> logging.Logger:
    return logging.getLogger("zinsradar")
