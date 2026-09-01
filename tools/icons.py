"""Erzeugt die PNG-Icons aus app/icons/icon.svg - ohne Bildbibliothek.

Warum selbst rastern: Das Repo soll ohne ImageMagick, Inkscape oder Pillow
auskommen. Ein kleiner Rasterizer mit 3x-Supersampling reicht fuer ein
Launcher-Icon voellig aus und macht die Icons reproduzierbar.

    python tools/icons.py

Schreibt:
    app/icons/icon-192.png
    app/icons/icon-512.png
    android/app/src/main/res/mipmap-*/ic_launcher*.png
"""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_ICONS = ROOT / "app" / "icons"
ANDROID_RES = ROOT / "android" / "app" / "src" / "main" / "res"

SS = 3  # Supersampling-Faktor


# ------------------------------------------------------------------ Zeichnen

def _misch(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _in_rundrect(x, y, w, h, r):
    if x < r and y < r:
        return (x - r) ** 2 + (y - r) ** 2 <= r * r
    if x > w - r and y < r:
        return (x - (w - r)) ** 2 + (y - r) ** 2 <= r * r
    if x < r and y > h - r:
        return (x - r) ** 2 + (y - (h - r)) ** 2 <= r * r
    if x > w - r and y > h - r:
        return (x - (w - r)) ** 2 + (y - (h - r)) ** 2 <= r * r
    return True


def _dist_strecke(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    laenge = dx * dx + dy * dy
    if laenge == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / laenge))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


# Geometrie in 512er-Koordinaten, identisch zu icon.svg
KURVE = [(92, 356), (168, 322), (236, 268), (318, 196), (420, 132)]
RINGE = [(66, 10), (120, 10), (174, 10)]
BG_OBEN = (15, 111, 214)
BG_UNTEN = (11, 63, 125)
WEISS = (255, 255, 255)
GRUEN = (126, 226, 184)


def pixel(fx: float, fy: float, maskiert: bool) -> tuple[int, int, int, int]:
    """Farbe eines Punktes in 512er-Koordinaten. maskiert = ohne Eckenradius."""
    if not maskiert and not _in_rundrect(fx, fy, 512, 512, 112):
        return (0, 0, 0, 0)

    farbe = _misch(BG_OBEN, BG_UNTEN, (fx + fy) / 1024.0)

    # Radar-Ringe
    for radius, breite in RINGE:
        d = abs(math.hypot(fx - 256, fy - 272) - radius)
        if d <= breite / 2:
            farbe = _misch(farbe, WEISS, 0.26)

    # Zinskurve
    for i in range(len(KURVE) - 1):
        x1, y1 = KURVE[i]
        x2, y2 = KURVE[i + 1]
        if _dist_strecke(fx, fy, x1, y1, x2, y2) <= 13:
            farbe = WEISS
            break

    # Endpunkt
    if math.hypot(fx - 420, fy - 132) <= 30:
        farbe = GRUEN

    # Prozentzeichen: zwei Ringe und ein Schrägstrich
    for cx, cy in ((222, 404), (290, 452)):
        d = math.hypot(fx - cx, fy - cy)
        if 14 <= d <= 24:
            farbe = WEISS
    if _dist_strecke(fx, fy, 296, 396, 216, 460) <= 9:
        farbe = WEISS

    return (farbe[0], farbe[1], farbe[2], 255)


def rastern(groesse: int, maskiert: bool = False) -> bytes:
    """RGBA-Bytes mit Supersampling."""
    zeilen = bytearray()
    schritt = 512.0 / groesse
    ss_versatz = [(i + 0.5) / SS for i in range(SS)]

    for y in range(groesse):
        zeilen.append(0)  # Filter-Byte
        for x in range(groesse):
            r = g = b = a = 0
            for sy in ss_versatz:
                for sx in ss_versatz:
                    pr, pg, pb, pa = pixel((x + sx) * schritt, (y + sy) * schritt, maskiert)
                    r += pr * pa; g += pg * pa; b += pb * pa; a += pa
            n = SS * SS
            if a == 0:
                zeilen.extend((0, 0, 0, 0))
            else:
                zeilen.extend((r // a, g // a, b // a, a // n))
    return bytes(zeilen)


def png_schreiben(pfad: Path, groesse: int, maskiert: bool = False) -> None:
    roh = rastern(groesse, maskiert)

    def chunk(typ: bytes, daten: bytes) -> bytes:
        return (struct.pack(">I", len(daten)) + typ + daten
                + struct.pack(">I", zlib.crc32(typ + daten) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", groesse, groesse, 8, 6, 0, 0, 0)
    daten = (b"\x89PNG\r\n\x1a\n"
             + chunk(b"IHDR", ihdr)
             + chunk(b"IDAT", zlib.compress(roh, 9))
             + chunk(b"IEND", b""))
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_bytes(daten)
    print(f"  {pfad.relative_to(ROOT)}  ({groesse}x{groesse}, {len(daten)} Bytes)")


MIPMAPS = {
    "mipmap-mdpi": 48, "mipmap-hdpi": 72, "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144, "mipmap-xxxhdpi": 192,
}


def main() -> None:
    print("PWA-Icons:")
    png_schreiben(APP_ICONS / "icon-192.png", 192)
    png_schreiben(APP_ICONS / "icon-512.png", 512)

    print("Android-Launcher:")
    for ordner, groesse in MIPMAPS.items():
        png_schreiben(ANDROID_RES / ordner / "ic_launcher.png", groesse)
        png_schreiben(ANDROID_RES / ordner / "ic_launcher_round.png", groesse)
        # Vordergrund fuer adaptive Icons: 108dp Flaeche, Motiv im inneren Drittel
        png_schreiben(ANDROID_RES / ordner / "ic_launcher_foreground.png",
                      int(groesse * 108 / 48), maskiert=True)
    print("fertig.")


if __name__ == "__main__":
    main()
