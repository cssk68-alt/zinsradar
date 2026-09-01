"""Kopiert die aktuellen Daten nach app/data/ - fuer lokale Vorschau.

Der Android-Build macht dasselbe von sich aus (Gradle-Task `syncWeb`).
Dieses Skript ist nur fuer die Vorschau im Browser:

    python tools/sync_web.py
    python -m http.server 8731 --directory app

app/data/ steht in .gitignore - die Daten leben in /data.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUELLE = ROOT / "data"
ZIEL = ROOT / "app" / "data"

DATEIEN = ("zinsen.json", "referenz.json", "laender.json", "withholding.json")


def main() -> int:
    ZIEL.mkdir(parents=True, exist_ok=True)
    kopiert = 0
    for name in DATEIEN:
        quelle = QUELLE / name
        if not quelle.exists():
            print(f"  fehlt: {name}")
            continue
        shutil.copy2(quelle, ZIEL / name)
        print(f"  {name}  ({quelle.stat().st_size} Bytes)")
        kopiert += 1

    if not (ZIEL / "zinsen.json").exists():
        print("\nzinsen.json fehlt. Erst 'python scraper/run.py' laufen lassen.")
        return 1

    print(f"\n{kopiert} Datei(en) nach app/data/ kopiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
