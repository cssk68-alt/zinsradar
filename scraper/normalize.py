"""Rohtreffer -> saubere Angebote.

Aufgaben:
  * Zahlen-Parsing quer durch europaeische Schreibweisen
    ("3,50 % p.a.", "3.50%", "1.000,00 EUR", "1,000.00 EUR")
  * Zinstyp, Laufzeit, Land, Waehrung erkennen
  * Dedupe ueber (bank, produkt, land)
  * Multi-Quellen-Merge: mehrere Quellen zur selben Bank werden zu einem
    Eintrag verschmolzen, die vertrauenswuerdigste Quelle gewinnt pro Feld
  * FX: Betraege in EUR umrechnen. Der ZINSSATZ wird NICHT umgerechnet -
    ein Zins in PLN bleibt ein PLN-Zins, dafuer gibt es das Flag
    `waehrungsrisiko`.

Die Funktionen hier sind bewusst rein (keine Netzzugriffe), damit sie
testbar bleiben.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any, Iterable

from util import cfg_get, log

# ------------------------------------------------------------------ Konstanten

# Sprachen, in denen der Punkt ueblicherweise das Dezimaltrennzeichen ist.
PUNKT_SPRACHEN = {"en", "nl", "sv", "no", "da", "is"}

ZINS_MIN = 0.0
ZINS_MAX = 15.0

# Wortstaemme fuer Laufzeit-Angaben in den Sprachen der Quellenliste.
_MONAT_WOERTER = (
    r"monat(?:e|en)?|month(?:s)?|mois|mes(?:i|es)?|maand(?:en)?|"
    r"mies(?:i[aą]c(?:e|y)?)?|m[aå]nad(?:er)?|m[eê]s(?:es)?|luna|luni"
)
_JAHR_WOERTER = r"jahr(?:e|en)?|year(?:s)?|an(?:s|ni|no|os|o)?|jaar|rok|[aå]r"

# Waehrungszeichen und -codes, die in Betraegen auftauchen koennen.
# Reihenfolge zaehlt: spezifische Codes vor generischen Symbolen wie "kr".
# entschaerfe() hat Akzente schon entfernt, daher stehen hier ASCII-Formen
# (zloty statt złoty, kc statt kč) neben den Originalzeichen.
_WAEHRUNG_MUSTER = {
    "PLN": r"\bpln\b|z[lł]ot|\bz[lł]\b|zł",
    "CZK": r"\bczk\b|\bkc\b|kč",
    "HUF": r"\bhuf\b|\bft\b|forint",
    "NOK": r"\bnok\b",
    "DKK": r"\bdkk\b",
    "CHF": r"\bchf\b|franken",
    "GBP": r"£|\bgbp\b|pfund",
    "RON": r"\bron\b|\blei\b",
    "BGN": r"\bbgn\b|\blv\b|\blew\b",
    "ISK": r"\bisk\b",
    "SEK": r"\bsek\b|\bkr\b|krona|kronor",
    "EUR": r"€|\beur\b|euro",
}

# Landeserkennung aus Freitext / img-alt / Dateinamen.
_LAND_WOERTER: dict[str, tuple[str, ...]] = {
    "DE": ("deutschland", "germany", "allemagne", "germania", "alemania", "duitsland", "tyskland"),
    "AT": ("oesterreich", "osterreich", "austria", "autriche", "oostenrijk"),
    "NL": ("niederlande", "netherlands", "nederland", "pays-bas", "paesi bassi", "holland"),
    "FR": ("frankreich", "france", "francia", "frankrijk", "francja"),
    "IT": ("italien", "italy", "italia", "italie", "italie", "wlochy"),
    "ES": ("spanien", "spain", "espana", "espagne", "spagna", "spanje", "hiszpania"),
    "PT": ("portugal", "portogallo", "portugalia"),
    "IE": ("irland", "ireland", "irlande", "irlanda", "ierland"),
    "SE": ("schweden", "sweden", "sverige", "suede", "svezia", "zweden", "szwecja"),
    "NO": ("norwegen", "norway", "norge", "norvege", "noorwegen"),
    "DK": ("daenemark", "danemark", "denmark", "danmark", "dania"),
    "FI": ("finnland", "finland", "finlande", "suomi"),
    "PL": ("polen", "poland", "polska", "pologne", "polonia"),
    "CZ": ("tschechien", "czech", "cesko", "tchequie"),
    "BE": ("belgien", "belgium", "belgique", "belgie", "belgia"),
    "LU": ("luxemburg", "luxembourg", "lussemburgo"),
    "LV": ("lettland", "latvia", "latvija"),
    "LT": ("litauen", "lithuania", "lietuva"),
    "EE": ("estland", "estonia", "eesti"),
    "MT": ("malta",),
    "CY": ("zypern", "cyprus", "kypros"),
    "SI": ("slowenien", "slovenia", "slovenija"),
    "SK": ("slowakei", "slovakia", "slovensko"),
    "HR": ("kroatien", "croatia", "hrvatska", "croazia"),
    "HU": ("ungarn", "hungary", "magyar"),
    "RO": ("rumaenien", "romania", "romania"),
    "BG": ("bulgarien", "bulgaria", "balgarija"),
    "GR": ("griechenland", "greece", "grecia", "hellas"),
    "CH": ("schweiz", "switzerland", "suisse", "svizzera"),
    "LI": ("liechtenstein",),
    "IS": ("island", "iceland", "islande"),
    "UK": ("grossbritannien", "united kingdom", "vereinigtes koenigreich", "england", "britain"),
}

ALLE_LAENDER = set(_LAND_WOERTER)


# ------------------------------------------------------------------ Textbasis

def entschaerfe(text: str | None) -> str:
    """Kleinschreibung, Akzente weg, Whitespace normalisiert."""
    if not text:
        return ""
    t = unicodedata.normalize("NFKD", str(text))
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("ß", "ss")
    return re.sub(r"\s+", " ", t).strip().lower()


def aufraeumen(text: str | None) -> str:
    """Nur Whitespace normalisieren, Original-Schreibweise behalten."""
    if not text:
        return ""
    return re.sub(r"\s+", " ", str(text).replace("\xa0", " ")).strip()


# ------------------------------------------------------------------ Zahlen

def _deutungen(roh: str, sprache: str = "de") -> list[float]:
    """Alle plausiblen Lesarten einer Zahl mit . und , zurueckgeben.

    "3,5"     -> [3.5]                      (Komma als Dezimal)
    "1.000"   -> [1000.0, 1.0]              (Tausender oder Dezimal)
    "1.234,56"-> [1234.56]                  (eindeutig)
    "1,234.56"-> [1234.56]                  (eindeutig)
    """
    roh = roh.strip()
    if not roh:
        return []
    hat_komma = "," in roh
    hat_punkt = "." in roh

    if hat_komma and hat_punkt:
        # Das zuletzt auftretende Zeichen ist das Dezimaltrennzeichen.
        if roh.rfind(",") > roh.rfind("."):
            wert = roh.replace(".", "").replace(",", ".")
        else:
            wert = roh.replace(",", "")
        try:
            return [float(wert)]
        except ValueError:
            return []

    trenner = "," if hat_komma else ("." if hat_punkt else "")
    if not trenner:
        try:
            return [float(roh)]
        except ValueError:
            return []

    teile = roh.split(trenner)
    nachkomma = len(teile[-1])
    kandidaten: list[float] = []

    # Lesart A: Trennzeichen ist Dezimalpunkt
    try:
        kandidaten.append(float(roh.replace(trenner, ".")))
    except ValueError:
        pass
    # Lesart B: Trennzeichen ist Tausendertrenner (nur bei exakt 3 Stellen sinnvoll)
    if nachkomma == 3 and len(teile) >= 2:
        try:
            kandidaten.append(float(roh.replace(trenner, "")))
        except ValueError:
            pass

    # Sprachpraeferenz nach vorne sortieren.
    dezimal_erwartet = (trenner == ".") == (sprache in PUNKT_SPRACHEN)
    if not dezimal_erwartet and len(kandidaten) > 1:
        kandidaten.reverse()
    return kandidaten


def finde_prozente(text: str | None, sprache: str = "de", *, streng: bool = False,
                   min_pct: float | None = None, max_pct: float | None = None) -> list[float]:
    """Alle Prozentwerte aus einem Text, in Lesereihenfolge.

    Erkennt "3,5 %", "3.5%", "3,50 Prozent", "3,5 p.a." und - nur wenn
    `streng` aus ist - auch blanke Zahlen im plausiblen Zinsbereich.

    `streng=True` benutzt die Heuristik in extract.py. Ohne das liest sie
    Ranglistennummern ("1 DHB Bank ...") als 1,00 % Zins.

    `min_pct`/`max_pct` engen das Fenster ein. Die Heuristik nutzt das,
    damit ein "15 % Rabatt" irgendwo auf der Seite nicht als Sparzins
    durchgeht.
    """
    if not text:
        return []
    unten = ZINS_MIN if min_pct is None else float(min_pct)
    oben = ZINS_MAX if max_pct is None else float(max_pct)
    t = aufraeumen(text).replace("−", "-").replace(" ", " ")

    treffer: list[float] = []
    gesehen: set[tuple[int, int]] = set()

    # 1) Zahl direkt vor einem Prozentzeichen / Prozentwort / p.a.
    muster = re.compile(
        r"(\d{1,3}(?:[.,]\d{1,3})?)\s*(?:%|prozent|percent|per\s*cent|pct|p\.?\s*a\.?|"
        r"tan[bl]?|taeg|taux|tasso|rente|zins)",
        re.IGNORECASE,
    )
    for m in muster.finditer(t):
        gesehen.add(m.span(1))
        for wert in _deutungen(m.group(1), sprache):
            if unten <= wert <= oben:
                treffer.append(round(wert, 4))
                break

    # 2) Fallback: blanke Zahlen im Zinsbereich, falls oben nichts kam.
    #    Bis zu drei Nachkommastellen, damit auch "2,188" (EZB-Notation) greift.
    if not treffer and not streng:
        for m in re.finditer(r"(?<![\d.,])(\d{1,2}(?:[.,]\d{1,3})?)(?![\d.,])", t):
            if m.span(1) in gesehen:
                continue
            for wert in _deutungen(m.group(1), sprache):
                if max(unten, 0.01) <= wert <= oben:
                    treffer.append(round(wert, 4))
                    break
    return treffer


def parse_zins(text: str | None, sprache: str = "de") -> float | None:
    """Erster plausibler Prozentwert aus dem Text."""
    werte = finde_prozente(text, sprache)
    return werte[0] if werte else None


def erkenne_waehrung(text: str | None, default: str = "EUR") -> str:
    t = entschaerfe(text)
    if not t:
        return default
    for code, muster in _WAEHRUNG_MUSTER.items():
        if re.search(muster, t, re.IGNORECASE):
            return code
    return default


def parse_betrag(text: str | None, sprache: str = "de") -> tuple[float | None, str]:
    """Geldbetrag + erkannte Waehrung.

    "ab 1.000 EUR" -> (1000.0, 'EUR');  "unbegrenzt" -> (None, 'EUR')
    "0 EUR"        -> (0.0, 'EUR')
    """
    if not text:
        return None, "EUR"
    t = aufraeumen(text)
    tl = entschaerfe(t)
    waehrung = erkenne_waehrung(t)

    if re.search(r"unbegrenzt|unlimited|illimit|keine|ohne\s+(?:mindest|limit)|no\s+limit|senza\s+limit", tl):
        return None, waehrung
    if re.search(r"^\s*(?:0|kein[e]?)\b", tl):
        # "0 EUR" / "keine Mindestanlage"
        if not re.search(r"[1-9]", tl):
            return 0.0, waehrung

    m = re.search(r"(\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d{1,2})?|\d+(?:[.,]\d{1,2})?)", t)
    if not m:
        return None, waehrung

    roh = m.group(1).replace(" ", "").replace(" ", "")
    kandidaten = _deutungen(roh, sprache)
    if not kandidaten:
        return None, waehrung

    wert = kandidaten[0]
    # "Mio"/"Tsd" hochskalieren
    rest = tl[m.end(1):][:12]
    if re.search(r"^\s*(?:mio|mill|m\b)", rest):
        wert *= 1_000_000
    elif re.search(r"^\s*(?:tsd|tausend|k\b)", rest):
        wert *= 1_000
    return round(wert, 2), waehrung


def parse_monate(text: str | None) -> int | None:
    """Laufzeit einer Aktion in Monaten. Jahre werden umgerechnet."""
    if text is None:
        return None
    t = entschaerfe(text)
    if not t:
        return None

    m = re.search(rf"(\d{{1,3}})\s*(?:{_MONAT_WOERTER})", t)
    if m:
        return _monate_grenze(int(m.group(1)))
    m = re.search(rf"(\d{{1,2}})\s*(?:{_JAHR_WOERTER})", t)
    if m:
        return _monate_grenze(int(m.group(1)) * 12)
    m = re.search(r"(\d{1,3})\s*m\b", t)
    if m:
        return _monate_grenze(int(m.group(1)))
    # Blanke Zahl (z.B. literal:'0' oder eine reine Monatsspalte)
    if re.fullmatch(r"\d{1,3}", t):
        return _monate_grenze(int(t))
    return None


def _monate_grenze(n: int) -> int | None:
    return n if 0 <= n <= 360 else None


def parse_zinstyp(text: str | None, *, aktionsdauer: int | None = None) -> str:
    """variabel | aktion | fest. Fallback leitet aus der Aktionsdauer ab."""
    t = entschaerfe(text)
    if t:
        if re.search(r"aktion|promo|bonus|neukunde|willkommen|welcome|introduct|"
                     r"garantiert|garanti|zeitlich|befristet|start|tijdelijk|kampanj", t):
            return "aktion"
        if re.search(r"variabel|variable|variabile|veranderlijk|zmienn|rorlig|flexib|"
                     r"taeglich|jederzeit|dagelijks", t):
            return "variabel"
        if re.search(r"\bfest\b|fixed|fisso|vast|sta[lł]|bunden|fixe", t):
            return "fest"
    if aktionsdauer:
        return "aktion" if aktionsdauer > 0 else "variabel"
    return "variabel"


def parse_land(text: str | None, default: str | None = None) -> str | None:
    """ISO-2-Land aus Freitext, img-alt oder Flaggen-Dateinamen."""
    if not text:
        return default
    t = entschaerfe(text)

    for code, woerter in _LAND_WOERTER.items():
        for w in woerter:
            if w and w in t:
                return code

    # Flaggen-Dateinamen: .../flags/de.svg, flag-icon-nl, "DE"
    m = re.search(r"(?:flag[s]?[-_/]|[-_/])([a-z]{2})(?:\.(?:svg|png|jpe?g|webp|gif))?\b", t)
    if m and m.group(1).upper() in ALLE_LAENDER:
        return m.group(1).upper()
    m = re.fullmatch(r"\s*([a-z]{2})\s*", t)
    if m and m.group(1).upper() in ALLE_LAENDER:
        return m.group(1).upper()
    return default


# ------------------------------------------------------------------ Bank/Key

_BANK_MUELL = re.compile(
    r"\b(?:zum\s+angebot|jetzt\s+\w+|mehr\s+infos?|details?|logo|werbung|anzeige|"
    r"sponsored|testsieger|empfehlung)\b",
    re.IGNORECASE,
)
_RECHTSFORM = re.compile(
    r"\b(?:ag|se|nv|n\.v\.|bv|b\.v\.|sa|s\.a\.|spa|s\.p\.a\.|plc|ltd|gmbh|"
    r"kgaa|ab|asa|oyj|a/s|as|sarl|sas|d\.d\.|zrt|nyrt)\b\.?",
    re.IGNORECASE,
)


def bank_normalisieren(name: str | None) -> str:
    """Anzeigename der Bank saeubern (Rechtsform bleibt erhalten)."""
    n = aufraeumen(name)
    if not n:
        return ""
    n = _BANK_MUELL.sub("", n)
    n = re.sub(r"\s*[|·•>–—]\s*.*$", "", n)  # alles nach Trennern weg
    n = re.sub(r"\s{2,}", " ", n).strip(" -–—|,;:")
    return n[:80]


# Produktbezeichnungen, die am Banknamen kleben ("Revolut Tagesgeld(Standard)").
# Nur fuer den Vergleichsschluessel entfernt - der Anzeigename bleibt ganz.
_PRODUKT_WOERTER = re.compile(
    r"\b(?:tagesgeld(?:konto)?|festgeld(?:konto)?|sparkonto|sparbuch|extra[- ]?konto|"
    r"flexgeld|zinskonto|geldmarktkonto|savings?(?:\s*account)?|deposit(?:\s*account)?|"
    r"conto\s*deposito|compte|livret|cuenta|rekening|konto|account|"
    r"standard|basis|classic|plus|premium|direkt|online|flex|neukunde[nr]?)\b",
    re.IGNORECASE,
)


def bank_schluessel(name: str | None) -> str:
    """Vergleichsform fuer den Dedupe: ohne Rechtsform, ohne Produktzusatz.

    "Revolut" und "Revolut Tagesgeld(Standard)" muessen denselben
    Schluessel ergeben, sonst steht dieselbe Bank zweimal in der Liste.
    """
    n = entschaerfe(bank_normalisieren(name))
    n = _RECHTSFORM.sub(" ", n)
    n = _PRODUKT_WOERTER.sub(" ", n)
    n = re.sub(r"\b(?:banca|banco|banque|banken|banc)\b", "bank", n)
    n = re.sub(r"[^a-z0-9 ]+", " ", n)
    n = re.sub(r"\s+", " ", n).strip()
    # Nach dem Entfernen darf nicht nur "bank" uebrig bleiben.
    return n if n and n != "bank" else entschaerfe(bank_normalisieren(name))


# Letzte Instanz vor der Aufnahme: taugt der Name ueberhaupt als Bank?
# Zentral hier statt verstreut in der Heuristik, damit jede Stufe - auch
# das LLM - denselben Mindeststandard passieren muss.
_NAME_VERDAECHTIG = re.compile(
    r"laenderrating|landerrating|rating|einlagensicherung|sicherungssystem|"
    r"quellensteuer|abgeltung|sparerpauschbetrag|rechenbeispiel|zinsertrag|"
    r"zinsgutschrift|gutschrift|kontotyp|kontofuehrung|laufzeit|"
    r"geldanlage|kapitalanlage|sparplan|anlageziel|"
    r"\bmonat(?:e|en)?\b|\bjahr(?:e|en)?\b|\bmesi\b|\bmois\b|\bmaanden\b|"
    r"^(?:bis|ab|bei|fuer|max|min|von|unter|ueber|mind)\b|"
    r"cookie|newsletter|datenschutz|impressum|werbung",
    re.IGNORECASE,
)


def bank_plausibel(name: str | None) -> bool:
    """True, wenn der Name als Institutsname durchgehen kann.

    Letzte Instanz vor der Aufnahme. Faengt ab, was Heuristik und LLM aus
    Tabellenzellen und Werbetexten mitschleppen ("Monate 1",
    "Zinsgutschrift / Jahr 12 Kontotyp", ganze Werbesaetze).
    """
    n = bank_normalisieren(name)
    if not n or not (3 <= len(n) <= 60):
        return False
    t = entschaerfe(n)
    if _NAME_VERDAECHTIG.search(t):
        return False
    if not re.match(r"^[a-z0-9]", t):      # muss mit Buchstabe/Ziffer beginnen
        return False
    if re.search(r"[%€£]|\bp\.?\s*a\.?\b", t):
        return False
    # Ganze Saetze sind Werbetexte, keine Namen.
    if re.search(r"[?!]|\.\s+\w", t):
        return False
    woerter = [w for w in t.split() if w]
    if not (1 <= len(woerter) <= 5):
        return False
    # Ein Name besteht ueberwiegend aus Wörtern, nicht aus Zahlen.
    zahlwoerter = sum(1 for w in woerter if re.fullmatch(r"[\d.,/-]+", w))
    if zahlwoerter * 2 >= len(woerter):
        return False
    return any(len(w) >= 3 for w in woerter)


def dedupe_key(bank: str | None, produkt: str | None, land: str | None) -> str:
    """Der Schluessel aus der Aufgabenstellung: (bank, produkt, land)."""
    return "|".join([
        bank_schluessel(bank),
        entschaerfe(produkt) or "tagesgeld",
        (land or "??").upper(),
    ])


def override_key(bank: str | None, produkt: str | None, land: str | None) -> str:
    """Menschenlesbarer Schluessel fuer data/overrides.json."""
    return "|".join([
        entschaerfe(bank_normalisieren(bank)),
        entschaerfe(produkt) or "tagesgeld",
        (land or "??").lower(),
    ])


# ------------------------------------------------------------------ FX

def fx_umrechnen(betrag: float | None, waehrung: str, fx: dict[str, float] | None) -> float | None:
    """Betrag in EUR. fx-Tabelle ist EZB-Form: 1 EUR = kurs * Fremdwaehrung."""
    if betrag is None:
        return None
    w = (waehrung or "EUR").upper()
    if w == "EUR":
        return round(betrag, 2)
    kurs = (fx or {}).get(w)
    if not kurs:
        return None
    try:
        return round(betrag / float(kurs), 2)
    except (ZeroDivisionError, ValueError, TypeError):
        return None


# ------------------------------------------------------------------ Normalisieren

def normalisiere(roh: dict[str, Any], quelle: dict[str, Any],
                 fx: dict[str, float] | None = None) -> dict[str, Any] | None:
    """Ein Rohtreffer aus extract.py -> ein Angebot. None = unbrauchbar."""
    sprache = quelle.get("sprache", "de")
    quell_land = (quelle.get("land") or "").upper() or None

    bank = bank_normalisieren(roh.get("bank"))
    if not bank_plausibel(bank):
        return None

    zins = roh.get("zinssatz_pct")
    if zins is None:
        zins = parse_zins(roh.get("zinssatz"), sprache)
    if zins is None:
        return None
    zins = float(zins)
    zmin = float(cfg_get("normalisierung.plausibler_zins_min_pct", 0.0))
    zmax = float(cfg_get("normalisierung.plausibler_zins_max_pct", 15.0))
    if not (zmin <= zins <= zmax):
        return None

    dauer = roh.get("aktionsdauer_monate")
    if not isinstance(dauer, int):
        dauer = parse_monate(roh.get("aktionsdauer_monate"))

    folge = roh.get("folgezins_pct")
    if folge is None:
        folge = parse_zins(roh.get("folgezins"), sprache)

    zinstyp = roh.get("zinstyp_norm") or parse_zinstyp(roh.get("zinstyp"), aktionsdauer=dauer)

    # Aktionslogik konsistent machen:
    #  - ohne Dauer keine Aktion
    #  - gleicher Folgezins heisst, dass sich nach Ablauf nichts aendert;
    #    "4,25 % für 48 Monate, danach 4,25 %" ist keine Aktion, sondern ein
    #    falsch gelesener Text (oft ein Festgeld-Block auf derselben Seite)
    #  - ohne Folgezins laeuft der Aktionszins ins Leere -> selber Zins
    if zinstyp == "aktion" and not dauer:
        zinstyp = "variabel"
    if (zinstyp == "aktion" and folge is not None
            and abs(float(folge) - zins) < 1e-9):
        zinstyp = "variabel"
        dauer = 0
    if zinstyp != "aktion":
        dauer = 0
    if folge is None:
        folge = zins if zinstyp != "aktion" else None

    min_betrag, min_waehrung = parse_betrag(roh.get("mindestanlage"), sprache)
    max_betrag, max_waehrung = parse_betrag(roh.get("hoechstanlage"), sprache)
    if isinstance(roh.get("mindestanlage_wert"), (int, float)):
        min_betrag = float(roh["mindestanlage_wert"])
    if isinstance(roh.get("hoechstanlage_wert"), (int, float)):
        max_betrag = float(roh["hoechstanlage_wert"])

    # Land der Einlagensicherung. Wurde es nicht im Treffer gefunden, wird
    # das Land der Quelle angenommen - bei einer Bankseite ist das richtig,
    # bei einem Vergleichsportal oft falsch (BBVA steht auf einer deutschen
    # Seite, sichert aber in Spanien). Deshalb wird die Herkunft der Angabe
    # mitgefuehrt und in der App als "angenommen" gekennzeichnet.
    es_land = parse_land(roh.get("einlagensicherung_land"), default=None)
    if es_land:
        land_quelle = "erkannt"
    else:
        es_land = quell_land
        typ = (quelle.get("typ") or "").lower()
        land_quelle = "bankseite" if typ == "bank" else "quellenland_angenommen"
    waehrung = (roh.get("waehrung") or "").upper() or _waehrung_fuer_land(es_land, min_waehrung, max_waehrung)

    produkt = aufraeumen(roh.get("produkt")) or cfg_get("normalisierung.produkt_default", "Tagesgeld")

    angebot = {
        "bank": bank,
        "produkt": produkt,
        "land": es_land,
        "quell_land": quell_land,
        "zinssatz_pct": round(zins, 4),
        "zinstyp": zinstyp,
        "aktionsdauer_monate": int(dauer or 0),
        "folgezins_pct": round(float(folge), 4) if folge is not None else None,
        "mindestanlage": min_betrag,
        "mindestanlage_eur": fx_umrechnen(min_betrag, min_waehrung, fx),
        "hoechstanlage": max_betrag,
        "hoechstanlage_eur": fx_umrechnen(max_betrag, max_waehrung, fx),
        "waehrung": waehrung,
        "waehrungsrisiko": waehrung != "EUR",
        "einlagensicherung_land": es_land,
        "land_quelle": land_quelle,
        "quellen": [{
            "id": quelle.get("id"),
            "url": quelle.get("url"),
            "typ": quelle.get("typ"),
            "extraction_tier": roh.get("extraction_tier"),
            "extraction_method": roh.get("extraction_method"),
            "confidence": roh.get("confidence"),
        }],
        "extraction_tier": roh.get("extraction_tier"),
        "extraction_method": roh.get("extraction_method"),
        "confidence": float(roh.get("confidence") or 0.0),
        "dedupe_key": "",
        "override_key": "",
    }
    angebot["dedupe_key"] = dedupe_key(bank, produkt, es_land)
    angebot["override_key"] = override_key(bank, produkt, es_land)
    return angebot


def _waehrung_fuer_land(land: str | None, *hinweise: str) -> str:
    """Waehrung raten: erst Betragshinweise, dann Land, sonst EUR."""
    for h in hinweise:
        if h and h != "EUR":
            return h
    nicht_euro = {
        "PL": "PLN", "SE": "SEK", "CZ": "CZK", "HU": "HUF", "NO": "NOK",
        "DK": "DKK", "CH": "CHF", "UK": "GBP", "RO": "RON", "BG": "BGN", "IS": "ISK",
    }
    return nicht_euro.get((land or "").upper(), "EUR")


# ------------------------------------------------------------------ Merge

# Wer gewinnt, wenn zwei Quellen dasselbe Angebot melden.
_QUELLTYP_GEWICHT = {"bank": 1.0, "plattform": 0.85, "portal": 0.7}


def _quellen_dedupe(quellen: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dieselbe Quelle nicht mehrfach listen.

    Eine Seite kann denselben Anbieter in mehreren Bloecken nennen; im
    Detailfenster soll die Quelle trotzdem nur einmal stehen.
    """
    gesehen: set[tuple] = set()
    ergebnis: list[dict[str, Any]] = []
    for q in quellen or []:
        schluessel = (q.get("id"), q.get("url"), q.get("extraction_method"))
        if schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        ergebnis.append(q)
    return ergebnis


def _rang(angebot: dict[str, Any]) -> tuple:
    """Sortierschluessel: niedriger Tier gewinnt, dann Confidence, dann Quelltyp."""
    tier = angebot.get("extraction_tier") or 9
    conf = angebot.get("confidence") or 0.0
    typ = (angebot.get("quellen") or [{}])[0].get("typ", "")
    return (tier, -conf, -_QUELLTYP_GEWICHT.get(typ, 0.5))


def merge(angebote: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dedupe ueber (bank, produkt, land) + Multi-Quellen-Merge.

    Der beste Treffer bildet die Basis. Aus den schwaecheren werden nur
    Felder uebernommen, die in der Basis fehlen - und die Quellenliste
    wird gesammelt, damit die App jede Zahl belegen kann.
    """
    gruppen: dict[str, list[dict[str, Any]]] = {}
    for a in angebote:
        if not a:
            continue
        gruppen.setdefault(a["dedupe_key"], []).append(a)

    ergebnis: list[dict[str, Any]] = []
    for key, gruppe in gruppen.items():
        gruppe.sort(key=_rang)
        basis = dict(gruppe[0])
        basis["quellen"] = list(basis.get("quellen") or [])

        fuellbar = (
            "folgezins_pct", "mindestanlage", "mindestanlage_eur",
            "hoechstanlage", "hoechstanlage_eur", "einlagensicherung_land", "land",
        )
        abweichungen: list[dict[str, Any]] = []

        for weiterer in gruppe[1:]:
            for feld in fuellbar:
                if basis.get(feld) in (None, "") and weiterer.get(feld) not in (None, ""):
                    basis[feld] = weiterer[feld]
            # Ein sicher erkanntes Land schlaegt ein bloss angenommenes -
            # auch wenn die andere Quelle sonst schwaecher ist.
            rang_land = {"erkannt": 2, "bankseite": 1, "quellenland_angenommen": 0}
            if (rang_land.get(weiterer.get("land_quelle"), 0)
                    > rang_land.get(basis.get("land_quelle"), 0)):
                basis["einlagensicherung_land"] = weiterer.get("einlagensicherung_land")
                basis["land"] = weiterer.get("land")
                basis["land_quelle"] = weiterer.get("land_quelle")
            if weiterer.get("zinssatz_pct") is not None and basis.get("zinssatz_pct") is not None:
                diff = abs(float(weiterer["zinssatz_pct"]) - float(basis["zinssatz_pct"]))
                if diff >= 0.05:
                    abweichungen.append({
                        "quelle": (weiterer.get("quellen") or [{}])[0].get("id"),
                        "zinssatz_pct": weiterer["zinssatz_pct"],
                        "differenz_pp": round(diff, 3),
                    })
            basis["quellen"].extend(weiterer.get("quellen") or [])

        if abweichungen:
            basis["quellen_abweichung"] = abweichungen
            log().info(
                "Zins-Abweichung zwischen Quellen fuer %s: %s",
                basis["bank"],
                ", ".join(f"{a['quelle']}={a['zinssatz_pct']}%" for a in abweichungen),
            )

        basis["quellen"] = _quellen_dedupe(basis["quellen"])
        basis["quellen_anzahl"] = len(basis["quellen"])
        # Nach dem Merge kann sich das Land geaendert haben -> Key nachziehen.
        basis["dedupe_key"] = key
        ergebnis.append(basis)

    ergebnis = _laender_dopplungen_aufloesen(ergebnis)
    ergebnis.sort(key=lambda a: (-(a.get("zinssatz_pct") or 0), a.get("bank", "")))
    return ergebnis


_LAND_RANG = {"erkannt": 2, "bankseite": 2, "quellenland_angenommen": 0}


def _laender_dopplungen_aufloesen(angebote: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Dieselbe Bank unter zwei Laendern zusammenfuehren.

    Der Dedupe-Schluessel enthaelt das Land. Steht eine Bank auf ihrer
    eigenen Seite mit belegtem Sicherungsland (Consorsbank -> FR) und auf
    einem deutschen Vergleichsportal mit bloss angenommenem Land (DE),
    entstehen zwei Eintraege fuer dasselbe Produkt. Hier gewinnt die
    belegte Angabe, die angenommene wird eingeschmolzen.
    """
    nach_bank: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for a in angebote:
        schluessel = (bank_schluessel(a.get("bank")), entschaerfe(a.get("produkt")) or "tagesgeld")
        nach_bank.setdefault(schluessel, []).append(a)

    ergebnis: list[dict[str, Any]] = []
    for gruppe in nach_bank.values():
        if len(gruppe) == 1:
            ergebnis.append(gruppe[0])
            continue

        beste = max(gruppe, key=lambda a: _LAND_RANG.get(a.get("land_quelle"), 0))
        bester_rang = _LAND_RANG.get(beste.get("land_quelle"), 0)
        zusammenlegbar = [a for a in gruppe
                          if a is not beste and _LAND_RANG.get(a.get("land_quelle"), 0) < bester_rang]

        if not zusammenlegbar:
            ergebnis.extend(gruppe)      # echte Mehrfachangebote, z.B. zwei Laender
            continue

        for a in zusammenlegbar:
            beste["quellen"] = list(beste.get("quellen") or []) + list(a.get("quellen") or [])
            for feld in ("folgezins_pct", "mindestanlage", "mindestanlage_eur",
                         "hoechstanlage", "hoechstanlage_eur"):
                if beste.get(feld) in (None, "") and a.get(feld) not in (None, ""):
                    beste[feld] = a[feld]
        beste["quellen"] = _quellen_dedupe(beste.get("quellen") or [])
        beste["quellen_anzahl"] = len(beste["quellen"])
        beste["dedupe_key"] = dedupe_key(beste.get("bank"), beste.get("produkt"),
                                         beste.get("einlagensicherung_land"))
        beste["override_key"] = override_key(beste.get("bank"), beste.get("produkt"),
                                             beste.get("einlagensicherung_land"))
        log().info("Land-Dopplung aufgeloest: %s -> %s (%d Eintraege verschmolzen)",
                   beste.get("bank"), beste.get("einlagensicherung_land"), len(zusammenlegbar))
        ergebnis.append(beste)
        ergebnis.extend(a for a in gruppe if a is not beste and a not in zusammenlegbar)

    return ergebnis


# ------------------------------------------------------------------ Overrides

def overrides_anwenden(angebote: list[dict[str, Any]],
                       overrides: dict[str, Any] | None) -> tuple[list[dict[str, Any]], list[str]]:
    """Manuelle Korrekturen einspielen. Sie gewinnen immer.

    Nicht zugeordnete Override-Schluessel werden als eigene Eintraege
    aufgenommen, damit eine manuell gepflegte Bank auch dann erscheint,
    wenn kein Scraper sie findet.
    """
    eintraege = ((overrides or {}).get("eintraege") or {})
    if not eintraege:
        return angebote, []

    benutzt: set[str] = set()
    protokoll: list[str] = []

    for a in angebote:
        ov = eintraege.get(a["override_key"])
        if not isinstance(ov, dict):
            continue
        benutzt.add(a["override_key"])
        geaendert = []
        for feld, wert in ov.items():
            if feld.startswith("_") or feld in ("notiz", "geprueft_am", "quelle_manuell"):
                continue
            if a.get(feld) != wert:
                geaendert.append(f"{feld}: {a.get(feld)} -> {wert}")
            a[feld] = wert
        a["override"] = True
        a["override_notiz"] = ov.get("notiz")
        a["override_geprueft_am"] = ov.get("geprueft_am")
        if ov.get("quelle_manuell"):
            a["quellen"] = list(a.get("quellen") or []) + [{
                "id": "manuell", "url": ov["quelle_manuell"], "typ": "manuell",
                "extraction_tier": 0, "extraction_method": "override", "confidence": 1.0,
            }]
        a["confidence"] = 1.0
        if geaendert:
            protokoll.append(f"{a['bank']} ({a['override_key']}): " + "; ".join(geaendert))

    for key, ov in eintraege.items():
        if key in benutzt or not isinstance(ov, dict) or key.startswith("_"):
            continue
        teile = key.split("|")
        if len(teile) != 3:
            continue
        bank, produkt, land = teile[0].strip(), teile[1].strip(), teile[2].strip().upper()
        if ov.get("zinssatz_pct") is None:
            protokoll.append(f"Override '{key}' passt auf kein Angebot und hat keinen Zins - ignoriert.")
            continue
        neu = {
            "bank": bank.title(), "produkt": produkt.title() or "Tagesgeld", "land": land,
            "quell_land": land, "zinstyp": "variabel", "aktionsdauer_monate": 0,
            "folgezins_pct": None, "mindestanlage": None, "mindestanlage_eur": None,
            "hoechstanlage": None, "hoechstanlage_eur": None,
            "waehrung": _waehrung_fuer_land(land), "einlagensicherung_land": land,
            "quellen": [{"id": "manuell", "url": ov.get("quelle_manuell"), "typ": "manuell",
                         "extraction_tier": 0, "extraction_method": "override", "confidence": 1.0}],
            "extraction_tier": 0, "extraction_method": "override", "confidence": 1.0,
            "override": True, "override_notiz": ov.get("notiz"),
            "override_geprueft_am": ov.get("geprueft_am"),
        }
        for feld, wert in ov.items():
            if not feld.startswith("_") and feld not in ("notiz", "geprueft_am", "quelle_manuell"):
                neu[feld] = wert
        neu["waehrungsrisiko"] = neu["waehrung"] != "EUR"
        neu["dedupe_key"] = dedupe_key(bank, produkt, land)
        neu["override_key"] = key
        neu["quellen_anzahl"] = 1
        angebote.append(neu)
        protokoll.append(f"Override '{key}' als eigener Eintrag aufgenommen.")

    return angebote, protokoll
