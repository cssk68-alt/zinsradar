"""Dreistufige Extraktion. Erste erfolgreiche Stufe gewinnt.

  Stufe 1  json_endpoint aus sources.yaml ODER JSON-LD aus
           <script type="application/ld+json"> (schema.org Offer /
           FinancialProduct). Bevorzugt, weil redesignfest.
  Stufe 2  CSS-Selektoren aus sources.yaml.
           2a = die konfigurierten Selektoren,
           2b = generische Struktur-Heuristik, wenn 2a nichts findet.
           2b existiert, weil die Selektoren aus der Recherche stammen
           und ungeprueft sind - die Pipeline darf nicht an ihnen haengen.
  Stufe 3  LLM-Fallback: HTML auf Fliesstext reduzieren, an Gemini 2.0
           Flash mit festem JSON-Schema. Ohne GEMINI_API_KEY wird die
           Stufe uebersprungen, nicht abgebrochen.

Jeder Rohtreffer traegt `extraction_tier` (1|2|3) und `confidence`.
Das Parsen der Werte passiert erst in normalize.py - hier wird nur
eingesammelt.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

import httpx

from fetch import Antwort, Fetcher
from normalize import ZINS_MAX, aufraeumen, entschaerfe, finde_prozente
from util import cfg_get, log

# ------------------------------------------------------------------ HTML-Parser

try:  # Lexbor kann mehr CSS als die Modest-Engine
    from selectolax.lexbor import LexborHTMLParser as _Parser
    _PARSER_NAME = "lexbor"
except ImportError:  # pragma: no cover - abhaengig vom selectolax-Build
    from selectolax.parser import HTMLParser as _Parser
    _PARSER_NAME = "modest"

# Tags, die fuer die Textreduktion (Stufe 3) und die Heuristik (2b) stoeren.
MUELL_TAGS = (
    "script", "style", "noscript", "svg", "iframe", "template",
    "nav", "header", "footer", "form", "aside", "button", "select",
)

FELDER = (
    "bank", "zinssatz", "zinstyp", "aktionsdauer_monate", "folgezins",
    "mindestanlage", "hoechstanlage", "einlagensicherung_land",
)

# Engeres Zinsfenster nur fuer die Heuristik (Stufe 2b). Ohne das liest sie
# ein "15 % Rabatt" oder "0 % Dispo" irgendwo auf der Seite als Sparzins.
# Konfigurierte Selektoren und LLM duerfen weiterhin bis ZINS_MAX liefern.
def _heuristik_fenster() -> tuple[float, float]:
    return (
        float(cfg_get("extraktion.heuristik_zins_min_pct", 0.05)),
        float(cfg_get("extraktion.heuristik_zins_max_pct", 8.0)),
    )


@dataclass
class StufenVersuch:
    stufe: int
    methode: str
    treffer: int = 0
    fehler: str | None = None
    detail: str = ""


@dataclass
class Ergebnis:
    """Was eine Quelle geliefert hat - inklusive Protokoll aller Stufen."""

    quelle_id: str
    url: str
    tier: int | None = None
    methode: str = ""
    treffer: list[dict[str, Any]] = field(default_factory=list)
    versuche: list[StufenVersuch] = field(default_factory=list)
    fehler: str | None = None
    gesperrt: bool = False
    http_status: int | None = None

    @property
    def erfolg(self) -> bool:
        return bool(self.treffer)


# ------------------------------------------------------------------ Hilfen

def _conf(schluessel: str, default: float) -> float:
    return float(cfg_get(f"extraktion.confidence.{schluessel}", default))


def _parse(html: str):
    try:
        return _Parser(html)
    except Exception as e:
        log().debug("HTML nicht parsebar: %s", e)
        return None


def _knoten_text(node) -> str:
    try:
        return aufraeumen(node.text(deep=True, separator=" ", strip=True))
    except Exception:
        return ""


def _css(baum, selektor: str) -> list:
    """CSS-Suche, die bei ungueltigen Selektoren nicht abstuerzt.

    Kommagetrennte Alternativen werden einzeln probiert und
    zusammengefuehrt - so bringt ein kaputter Teilselektor die
    gueltigen nicht mit zu Fall.
    """
    if not selektor:
        return []
    gefunden: list = []
    gesehen: set[int] = set()
    for teil in [s.strip() for s in selektor.split(",") if s.strip()]:
        try:
            for n in baum.css(teil):
                if id(n) not in gesehen:
                    gesehen.add(id(n))
                    gefunden.append(n)
        except Exception:
            continue
    return gefunden


def _literal(wert: Any) -> str | None:
    """literal:'ING Deutschland' -> ING Deutschland"""
    if not isinstance(wert, str):
        return None
    m = re.match(r"""^literal:\s*(['"])(.*)\1\s*$""", wert.strip(), re.DOTALL)
    if m:
        return m.group(2)
    if wert.strip().startswith("literal:"):
        return wert.strip()[len("literal:"):].strip().strip("'\"")
    return None


def _literal_felder(quelle: dict[str, Any]) -> dict[str, str]:
    """Alle als literal:'...' hinterlegten Festwerte einer Quelle."""
    ergebnis: dict[str, str] = {}
    for feld, sel in (quelle.get("felder") or {}).items():
        wert = _literal(sel)
        if wert:
            ergebnis[feld] = wert
    return ergebnis


def _feldwert_aus_knoten(node) -> str:
    """Text eines Knotens - bei img/meta die Attribute."""
    if node is None:
        return ""
    tag = getattr(node, "tag", "")
    attrs = {}
    try:
        attrs = dict(node.attributes or {})
    except Exception:
        attrs = {}
    if tag == "img":
        return aufraeumen(attrs.get("alt") or attrs.get("title") or attrs.get("src") or "")
    if tag == "meta":
        return aufraeumen(attrs.get("content") or "")
    text = _knoten_text(node)
    if not text:
        for a in ("data-value", "content", "title", "aria-label", "alt"):
            if attrs.get(a):
                return aufraeumen(attrs[a])
    return text


# ================================================================== STUFE 1

# Schluesselnamen, die in APIs/JSON-LD fuer die jeweiligen Felder auftauchen.
_KEY_MAP: dict[str, tuple[str, ...]] = {
    "bank": ("bank", "bankname", "provider", "providername", "institution", "issuer",
             "partnerbank", "name", "brand", "seller", "nomebanca", "banque", "banco", "entidad"),
    "zinssatz": ("interestrate", "interest", "rate", "zins", "zinssatz", "nominalrate",
                 "annualpercentagerate", "apr", "aer", "tasso", "tassolordo", "taux",
                 "oprocentowanie", "ranta", "tanb", "grossrate", "raterate", "yield",
                 "effectiverate", "actionrate", "promorate", "bonusrate"),
    "folgezins": ("baserate", "standardrate", "followrate", "folgezins", "basiszins",
                  "tassobase", "tauxdebase", "subrate", "afterrate", "regularrate"),
    "aktionsdauer_monate": ("duration", "months", "promoduration", "bonusduration",
                            "aktionsdauer", "durata", "duree", "periodmonths", "term"),
    "mindestanlage": ("minamount", "mindeposit", "minimum", "mindestanlage", "minimo",
                      "minimuminvestment", "minbalance", "importominimo"),
    "hoechstanlage": ("maxamount", "maxdeposit", "maximum", "hoechstanlage", "massimo",
                      "maximuminvestment", "maxbalance", "importomassimo"),
    "einlagensicherung_land": ("country", "land", "depositprotectioncountry", "guaranteecountry",
                               "countrycode", "paese", "pays", "protectioncountry",
                               "depositprotection", "areaserved"),
    "zinstyp": ("ratetype", "zinstyp", "type", "tipotasso", "typerate", "category"),
    "produkt": ("product", "productname", "produkt", "accounttype", "prodotto"),
    "waehrung": ("currency", "waehrung", "currencycode", "valuta", "pricecurrency"),
}

_KEY_LOOKUP: dict[str, str] = {
    kandidat: feld for feld, kandidaten in _KEY_MAP.items() for kandidat in kandidaten
}


def _key_norm(k: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(k).lower())


def _flach(obj: Any, prefix: str = "", tiefe: int = 0) -> dict[str, Any]:
    """Verschachteltes Dict auf einfache Schluessel-Wert-Paare abflachen."""
    flach: dict[str, Any] = {}
    if tiefe > 4 or not isinstance(obj, dict):
        return flach
    for k, v in obj.items():
        name = f"{prefix}{k}"
        if isinstance(v, (str, int, float, bool)) or v is None:
            flach[name] = v
        elif isinstance(v, dict):
            # schema.org-Muster: {"name": ...} oder {"value": ...}
            if set(map(_key_norm, v)) & {"name", "value", "@value"}:
                for innen in ("name", "value", "@value"):
                    if innen in v and isinstance(v[innen], (str, int, float)):
                        flach[name] = v[innen]
                        break
            flach.update(_flach(v, f"{name}.", tiefe + 1))
        elif isinstance(v, list) and v and isinstance(v[0], (str, int, float)):
            flach[name] = v[0]
    return flach


# Schluessel, die eindeutig das Institut benennen. Das generische "name"
# gehoert NICHT dazu: in schema.org ist `name` der Produktname und der
# Anbieter steckt in `provider`/`seller`/`brand`.
_BANK_SPEZIFISCH = (
    "bank", "bankname", "provider", "providername", "institution", "issuer",
    "partnerbank", "seller", "brand", "nomebanca", "banque", "banco", "entidad",
)


def _bank_aus_json(flach: dict[str, Any]) -> tuple[str | None, bool]:
    """Institutsnamen aus flachen JSON-Schluesseln ziehen.

    Rueckgabe: (Name, aus_generischem_name). Das zweite Flag sagt, ob der
    Name nur aus einem blanken `name` stammt - dann ist er wahrscheinlich
    der Produkt- und nicht der Bankname.
    """
    eintraege = [(s, _key_norm(s.split(".")[-1]), _key_norm(s.split(".")[0]), w)
                 for s, w in flach.items() if isinstance(w, str) and w.strip()]

    # 1) Blattschluessel ist selbst eindeutig ("bankName", "provider")
    for kandidat in _BANK_SPEZIFISCH:
        for _, blatt, _, wert in eintraege:
            if blatt == kandidat:
                return wert, False
    # 2) Verschachtelt: provider.name, seller.name, brand.name
    for kandidat in _BANK_SPEZIFISCH:
        for _, blatt, praefix, wert in eintraege:
            if praefix == kandidat and blatt in ("name", "value", "legalname"):
                return wert, False
    # 3) Letzte Wahl: ein blankes "name"
    for _, blatt, _, wert in eintraege:
        if blatt == "name":
            return wert, True
    return None, False


def _dict_zu_rohtreffer(obj: dict[str, Any]) -> dict[str, Any] | None:
    """Ein JSON-Objekt auf die Rohtreffer-Felder abbilden."""
    flach = _flach(obj)
    roh: dict[str, Any] = {}
    for schluessel, wert in flach.items():
        if wert is None or wert == "":
            continue
        blatt = _key_norm(schluessel.split(".")[-1])
        feld = _KEY_LOOKUP.get(blatt)
        if feld and feld != "bank" and feld not in roh:
            roh[feld] = wert

    bank, aus_generisch = _bank_aus_json(flach)
    if bank:
        roh["bank"] = bank
        # Der Anbieter stand in provider/seller - dann ist das blanke
        # `name` der Produktname.
        if not aus_generisch and not roh.get("produkt"):
            for schluessel, wert in flach.items():
                if _key_norm(schluessel) == "name" and isinstance(wert, str) and wert.strip():
                    roh["produkt"] = wert
                    break
    # Ohne Zins ist der Treffer wertlos.
    if "zinssatz" not in roh:
        return None
    if isinstance(roh.get("zinssatz"), (int, float)):
        wert = float(roh["zinssatz"])
        # Manche APIs liefern 0.035 statt 3.5
        if 0 < wert < 0.25:
            wert *= 100
        if not (0 <= wert <= ZINS_MAX):
            return None
        roh["zinssatz_pct"] = round(wert, 4)
    if isinstance(roh.get("folgezins"), (int, float)):
        f = float(roh["folgezins"])
        if 0 < f < 0.25:
            f *= 100
        if 0 <= f <= ZINS_MAX:
            roh["folgezins_pct"] = round(f, 4)
    if isinstance(roh.get("aktionsdauer_monate"), (int, float)):
        roh["aktionsdauer_monate"] = int(roh["aktionsdauer_monate"])
    if not roh.get("bank"):
        return None
    return roh


def _sammle_objekte(daten: Any, tiefe: int = 0) -> list[dict[str, Any]]:
    """Rekursiv alle Dicts einsammeln, die nach Produkt aussehen."""
    gefunden: list[dict[str, Any]] = []
    if tiefe > 6:
        return gefunden
    if isinstance(daten, list):
        for e in daten:
            gefunden.extend(_sammle_objekte(e, tiefe + 1))
    elif isinstance(daten, dict):
        roh = _dict_zu_rohtreffer(daten)
        if roh:
            gefunden.append(roh)
        else:
            for v in daten.values():
                if isinstance(v, (list, dict)):
                    gefunden.extend(_sammle_objekte(v, tiefe + 1))
    return gefunden


def stufe1_json_endpoint(quelle: dict[str, Any], fetcher: Fetcher) -> tuple[list[dict], StufenVersuch]:
    endpoint = quelle.get("json_endpoint")
    versuch = StufenVersuch(1, "json_endpoint")
    if not endpoint:
        versuch.fehler = "kein json_endpoint in sources.yaml"
        return [], versuch

    ant, daten = fetcher.hole_json(endpoint)
    if ant.gesperrt:
        versuch.fehler = f"robots.txt: {ant.fehler}"
        return [], versuch
    if daten is None:
        versuch.fehler = ant.fehler or f"HTTP {ant.status}"
        return [], versuch

    treffer = _sammle_objekte(daten)
    for t in treffer:
        t["extraction_tier"] = 1
        t["extraction_method"] = "json_endpoint"
        t["confidence"] = _conf("tier1_json_endpoint", 0.95)
    versuch.treffer = len(treffer)
    versuch.detail = endpoint
    if not treffer:
        versuch.fehler = "Endpoint antwortete, aber keine Produkte erkennbar"
    return treffer, versuch


_JSONLD_TYPEN = {
    "offer", "aggregateoffer", "financialproduct", "bankaccount", "depositaccount",
    "investmentordeposit", "savingsaccount", "product", "loanorcredit",
}


def _jsonld_bloecke(baum) -> list[Any]:
    bloecke: list[Any] = []
    for node in _css(baum, 'script[type="application/ld+json"]'):
        roh = None
        try:
            roh = node.text(deep=True, strip=False)
        except Exception:
            continue
        if not roh or not roh.strip():
            continue
        text = roh.strip()
        try:
            bloecke.append(json.loads(text))
        except ValueError:
            # Manche Seiten haengen mehrere Objekte oder Kommentare hinein.
            geputzt = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
            try:
                bloecke.append(json.loads(geputzt))
            except ValueError:
                continue
    return bloecke


def _jsonld_kandidaten(knoten: Any, tiefe: int = 0) -> list[dict[str, Any]]:
    """Objekte mit passendem @type einsammeln (inkl. @graph, itemListElement)."""
    gefunden: list[dict[str, Any]] = []
    if tiefe > 6:
        return gefunden
    if isinstance(knoten, list):
        for e in knoten:
            gefunden.extend(_jsonld_kandidaten(e, tiefe + 1))
        return gefunden
    if not isinstance(knoten, dict):
        return gefunden

    typen = knoten.get("@type") or knoten.get("type") or ""
    typ_liste = [typen] if isinstance(typen, str) else list(typen or [])
    if any(_key_norm(t) in _JSONLD_TYPEN for t in typ_liste):
        gefunden.append(knoten)

    for schluessel in ("@graph", "itemListElement", "offers", "makesOffer", "hasOfferCatalog",
                       "itemOffered", "mainEntity", "about", "item"):
        if schluessel in knoten:
            gefunden.extend(_jsonld_kandidaten(knoten[schluessel], tiefe + 1))
    return gefunden


def stufe1_jsonld(html: str, quelle: dict[str, Any]) -> tuple[list[dict], StufenVersuch]:
    versuch = StufenVersuch(1, "jsonld")
    baum = _parse(html)
    if baum is None:
        versuch.fehler = "HTML nicht parsebar"
        return [], versuch

    bloecke = _jsonld_bloecke(baum)
    if not bloecke:
        versuch.fehler = "kein <script type=application/ld+json> gefunden"
        return [], versuch

    kandidaten: list[dict[str, Any]] = []
    for b in bloecke:
        kandidaten.extend(_jsonld_kandidaten(b))

    treffer: list[dict[str, Any]] = []
    for k in kandidaten:
        roh = _dict_zu_rohtreffer(k)
        if roh is None:
            continue
        roh["extraction_tier"] = 1
        roh["extraction_method"] = "jsonld"
        roh["confidence"] = _conf("tier1_jsonld", 0.9)
        treffer.append(roh)

    versuch.treffer = len(treffer)
    versuch.detail = f"{len(bloecke)} ld+json-Block(s), {len(kandidaten)} Kandidat(en)"
    if not treffer:
        versuch.fehler = "ld+json vorhanden, aber ohne verwertbares Zinsangebot"
    return treffer, versuch


# ================================================================== STUFE 2

def stufe2_css(html: str, quelle: dict[str, Any]) -> tuple[list[dict], StufenVersuch]:
    """Die konfigurierten Selektoren - Hinweise aus der Recherche."""
    versuch = StufenVersuch(2, "css_konfiguriert")
    baum = _parse(html)
    if baum is None:
        versuch.fehler = "HTML nicht parsebar"
        return [], versuch

    felder: dict[str, str] = dict(quelle.get("felder") or {})
    container_sel = quelle.get("container_selector") or ""

    container = _css(baum, container_sel)
    versuch.detail = f"container '{container_sel}' -> {len(container)} Knoten"

    if not container:
        # Kein Container. Nur bei einer Bank-Einzelseite ist es sinnvoll,
        # die Feldselektoren global zu suchen - dort gibt es genau ein
        # Angebot. Auf einem Vergleichsportal wuerde das aus einer Liste
        # von 20 Angeboten faelschlich ein einziges machen.
        einzel = (_einzeltreffer_aus_selektoren(baum, felder, quelle)
                  if (quelle.get("typ") or "").lower() == "bank" else None)
        if einzel:
            versuch.treffer = 1
            versuch.detail += " | Einzelseiten-Modus ueber Feldselektoren"
            return [einzel], versuch
        versuch.fehler = "container_selector findet nichts"
        return [], versuch

    treffer: list[dict[str, Any]] = []
    for knoten in container:
        roh: dict[str, Any] = {}
        for feld in FELDER:
            sel = felder.get(feld)
            if not sel:
                continue
            lit = _literal(sel)
            if lit is not None:
                roh[feld] = lit
                continue
            gefunden = _css(knoten, sel)
            if gefunden:
                roh[feld] = _feldwert_aus_knoten(gefunden[0])
        if not roh.get("zinssatz"):
            continue
        if not roh.get("bank"):
            # Manche Tabellen haben den Namen nur im Zeilentext.
            roh["bank"] = _bank_aus_knoten(knoten)
        if not roh.get("bank"):
            continue
        roh["extraction_tier"] = 2
        roh["extraction_method"] = "css_konfiguriert"
        roh["confidence"] = _conf("tier2_css_konfiguriert", 0.75)
        treffer.append(roh)

    versuch.treffer = len(treffer)
    if not treffer:
        versuch.fehler = f"{len(container)} Container, aber keiner mit Bank+Zins"
    return treffer, versuch


def _einzeltreffer_aus_selektoren(baum, felder: dict[str, str],
                                  quelle: dict[str, Any]) -> dict[str, Any] | None:
    """Fuer Bank-Einzelseiten: Felder global suchen statt im Container."""
    roh: dict[str, Any] = {}
    for feld in FELDER:
        sel = felder.get(feld)
        if not sel:
            continue
        lit = _literal(sel)
        if lit is not None:
            roh[feld] = lit
            continue
        gefunden = _css(baum, sel)
        if gefunden:
            roh[feld] = _feldwert_aus_knoten(gefunden[0])
    if not roh.get("bank") or not roh.get("zinssatz"):
        return None
    if not finde_prozente(roh.get("zinssatz"), quelle.get("sprache", "de")):
        return None
    roh["extraction_tier"] = 2
    roh["extraction_method"] = "css_konfiguriert_einzelseite"
    roh["confidence"] = _conf("tier2_css_konfiguriert", 0.75)
    return roh


# Feldbezeichner, die wie ein Bankname aussehen, aber keiner sind.
_LABEL_WOERTER = re.compile(
    r"^(?:basis|aktions|neukunden|bestands|garantie|effektiv|nominal|soll|haben)?"
    r"\s*(?:zins(?:satz|en)?|rate|tasso|taux|rente|oprocentowanie|interesse|"
    r"anbieter|provider|bank|produkt|konto|angebot|konditionen|details?|"
    r"laufzeit|einlage|betrag|mindest\w*|hoechst\w*|max\w*|min\w*|"
    r"sicherung|garantie|land|waehrung|platz|rang|note|bewertung|"
    r"mehr\s+\w+|zum\s+\w+|jetzt\s+\w+|vergleich|test\w*)\s*:?\s*$",
    re.IGNORECASE,
)


# Ratings ("AAA", "BBB+", "Aa3"), Legitimationsverfahren und Werbe-Buttons
# stehen in Vergleichstabellen direkt neben dem Zins und werden sonst als
# Bankname gelesen.
_KEIN_NAME = re.compile(
    r"^(?:a{1,3}[+-]?|b{1,3}[+-]?|c{1,3}[+-]?|d|aa[123]|baa?[123]|"
    r"[a-c]{1,3}[+-]?\s*/\s*[a-c]{1,3}[+-]?)$"
    r"|^\w*[-\s]?ident\b"
    r"|\b(?:sichern|entdecken|vergleichen|eroeffnen|beantragen|ansehen|"
    r"berechnen|weiter|hier)\b",
    re.IGNORECASE,
)


def _ist_label(text: str) -> bool:
    """True, wenn der Text eine Spaltenueberschrift statt eines Namens ist."""
    t = entschaerfe(text)
    if not t or len(t) < 2:
        return True
    if _LABEL_WOERTER.match(t):
        return True
    if _KEIN_NAME.search(t):
        return True
    # Ein reiner Laendername ist die Sicherungsland-Spalte, keine Bank.
    from normalize import _LAND_WOERTER
    for woerter in _LAND_WOERTER.values():
        if t in woerter:
            return True
    # Fragmente wie "Bis 300 EUR &" oder "ab 1.000"
    if re.match(r"^(?:bis|ab|bei|fuer|max|min|von|unter|ueber|mind)\b", t):
        return True
    # Reine Zahlen, Prozente, Waehrungen
    return bool(re.fullmatch(r"[\d\s.,%€£+-]*", t))


# Spaltenueberschriften, die Tabellen den Zellen voranstellen
# ("Anbieter und Produkt 1 DHB Bank ..."). Werden vom Namen abgeschnitten.
_LABEL_PRAEFIX = re.compile(
    r"^(?:anbieter(?:\s+und\s+produkt)?|produkt\s*details?|produkt|details?|"
    r"bank\s*name|institut|konditionen|zinssatz|zinsen|rang|platz|nr\.?|"
    r"testsieger|empfehlung|unser\s+tipp|top\s*angebot)\b[:\s-]*",
    re.IGNORECASE,
)

# Woerter, die als Bankname auftauchen koennen, aber keiner sind.
_NAME_BLACKLIST = {
    "ios", "android", "web", "app", "apps", "desktop", "mobile", "browser",
    "online", "filiale", "neu", "aktion", "tipp", "top", "mehr", "alle",
    "ja", "nein", "keine", "kein", "info", "faq", "cookie", "cookies",
    "newsletter", "werbung", "anzeige", "sponsored", "eur", "euro",
}


def _namens_kandidat(wert: str) -> str:
    """Text zu einem moeglichen Banknamen trimmen. Leer = untauglich."""
    wert = re.sub(r"\d+[.,]?\d*\s*%.*$", "", wert or "")
    for _ in range(3):  # mehrere gestapelte Praefixe abtragen
        gekuerzt = _LABEL_PRAEFIX.sub("", wert).lstrip()
        gekuerzt = re.sub(r"^\s*\d{1,2}[.)]?\s+", "", gekuerzt)
        if gekuerzt == wert:
            break
        wert = gekuerzt
    wert = re.sub(r"^\s*\d{1,2}[.)]?\s+", "", wert)  # fuehrende Ranglistennummer
    wert = wert.strip(" -–—|,;: ")
    if not (3 <= len(wert) <= 60):
        return ""
    if _ist_label(wert):
        return ""
    if entschaerfe(wert) in _NAME_BLACKLIST:
        return ""
    if not re.search(r"[A-Za-zÀ-ÿ]{2}", wert):
        return ""
    return wert


def _bank_aus_knoten(knoten, *, nachbarn: bool = True) -> str:
    """Banknamen aus einem Container raten: Bild-alt, Link-Text, erster Text.

    Findet sich im Knoten selbst nichts (typisch fuer eine zweite
    Tabellenzeile, die nur "Basiszins: 1,95 %" enthaelt), wird beim
    vorherigen Geschwisterknoten nachgesehen.
    """
    for sel in ("img[alt]", "a[title]", "a", "th", "h1", "h2", "h3", "h4", "strong", "b"):
        for n in _css(knoten, sel):
            kandidat = _namens_kandidat(_feldwert_aus_knoten(n))
            if kandidat:
                return kandidat

    text = _knoten_text(knoten)
    for teil in re.split(r"\s{2,}|\||·", text or "")[:3]:
        kandidat = _namens_kandidat(teil)
        if kandidat:
            return kandidat

    if nachbarn:
        vorher = getattr(knoten, "prev", None)
        schritte = 0
        while vorher is not None and schritte < 4:
            schritte += 1
            if getattr(vorher, "tag", None) not in (None, "-text"):
                kandidat = _bank_aus_knoten(vorher, nachbarn=False)
                if kandidat:
                    return kandidat
            vorher = getattr(vorher, "prev", None)
    return ""


# ---- 2b: generische Heuristik, unabhaengig von den YAML-Selektoren ----

# Beschriftungen, die einen Prozentwert als Aktions- bzw. Basiszins ausweisen.
_AKTION_LABEL = re.compile(
    r"(aktions?zins|aktionszinssatz|bonus\w*|neukunden\w*|willkommens\w*|promo\w*|"
    r"startzins|tasso\s+promo|taux\s+promo|premie)\D{0,30}?"
    r"(\d{1,2}(?:[.,]\d{1,3})?)\s*%",
    re.IGNORECASE,
)
_BASIS_LABEL = re.compile(
    r"(basis\w*|grundzins|folgezins|standard\w*|regel\w*|danach|anschliessend|"
    r"anschließend|ab\s+dem\s+\d+|tasso\s+base|taux\s+de\s+base|base\s*rate)\D{0,30}?"
    r"(\d{1,2}(?:[.,]\d{1,3})?)\s*%",
    re.IGNORECASE,
)


def _aktion_und_basis(text: str, prozente: list[float],
                      sprache: str) -> tuple[float, float | None]:
    """Aus einem Zeilentext Aktions- und Folgezins auseinanderhalten.

    "Basiszins: 1,95% Aktionszins: 3,40% - erste 6 Monate"
    -> (3.40, 1.95). Ohne Beschriftungen gilt die Lesereihenfolge.
    """
    from normalize import _deutungen  # lokal, vermeidet Import-Zyklus beim Laden

    def _wert(m) -> float | None:
        if not m:
            return None
        kandidaten = _deutungen(m.group(2), sprache)
        for k in kandidaten:
            if 0 <= k <= ZINS_MAX:
                return round(k, 4)
        return None

    aktion = _wert(_AKTION_LABEL.search(text))
    basis = _wert(_BASIS_LABEL.search(text))

    if aktion is not None and basis is not None:
        return aktion, basis
    if aktion is not None:
        return aktion, None
    if basis is not None:
        # Nur ein Basiszins beschriftet: der andere Wert ist die Aktion.
        rest = [p for p in prozente if abs(p - basis) > 1e-9]
        return (rest[0], basis) if rest else (basis, basis)

    return prozente[0], (prozente[1] if len(prozente) > 1 else None)


# Tags, in denen ein einzelnes Angebot stecken kann.
_LISTEN_TAGS = ("div", "li", "tr", "article", "section")


def _tiefe(node) -> int:
    t = 0
    p = getattr(node, "parent", None)
    while p is not None and t < 40:
        t += 1
        p = getattr(p, "parent", None)
    return t


def _klassen(node) -> tuple[str, ...]:
    try:
        roh = (node.attributes or {}).get("class") or ""
    except Exception:
        roh = ""
    return tuple(sorted(roh.split()))


def _struktur_gruppen(baum, sprache: str) -> list[tuple[str, list]]:
    """Wiederkehrende Container mit Prozentangabe finden - ohne Selektor-Raten.

    Statt auf Klassennamen wie `.product-card` zu hoffen (die aus der
    Recherche stammen und oft falsch sind), werden Geschwister mit
    gleicher Signatur (Tag + Klassen + Baumtiefe) gruppiert. Wiederholt
    sich eine Struktur mehrfach und enthaelt jedes Mal einen Prozentwert,
    ist das mit hoher Wahrscheinlichkeit die Angebotsliste.
    """
    h_min, h_max = _heuristik_fenster()
    nach_signatur: dict[tuple, list] = {}
    nach_tag_tiefe: dict[tuple, list] = {}

    geprueft = 0
    for tag in _LISTEN_TAGS:
        for node in _css(baum, tag):
            geprueft += 1
            if geprueft > 12000:  # Reissleine fuer Riesenseiten
                break
            try:
                roh_html = node.html or ""
            except Exception:
                continue
            if len(roh_html) > 20000:
                continue
            text = _knoten_text(node)
            if not (10 <= len(text) <= 600):
                continue
            if "%" not in text and "prozent" not in text.lower():
                continue
            if not finde_prozente(text, sprache, streng=True, min_pct=h_min, max_pct=h_max):
                continue
            tiefe = _tiefe(node)
            nach_signatur.setdefault((tag, _klassen(node), tiefe), []).append(node)
            nach_tag_tiefe.setdefault((tag, tiefe), []).append(node)

    gruppen: list[tuple[str, list]] = []
    for (tag, klassen, tiefe), knoten in nach_signatur.items():
        if len(knoten) >= 2:
            name = f"{tag}.{'.'.join(klassen) or '?'} (Tiefe {tiefe}, {len(knoten)}x)"
            gruppen.append((name, knoten))
    for (tag, tiefe), knoten in nach_tag_tiefe.items():
        if len(knoten) >= 2:
            gruppen.append((f"{tag} auf Tiefe {tiefe} ({len(knoten)}x)", knoten))

    # Kleine, praezise Gruppen zuerst bewerten.
    gruppen.sort(key=lambda g: len(g[1]))
    return gruppen[:40]


def stufe2_heuristik(html: str, quelle: dict[str, Any]) -> tuple[list[dict], StufenVersuch]:
    """Findet Angebote ohne jede Selektor-Konfiguration.

    Sucht wiederkehrende Container, die genau eine plausible Prozentzahl
    und einen Namenskandidaten enthalten. Das ist der Grund, warum die
    Architektur ohne die recherchierten Selektoren funktioniert.
    """
    versuch = StufenVersuch(2, "css_heuristik")
    if not cfg_get("extraktion.heuristik_aktiv", True):
        versuch.fehler = "per Config deaktiviert"
        return [], versuch

    baum = _parse(html)
    if baum is None:
        versuch.fehler = "HTML nicht parsebar"
        return [], versuch

    for tag in MUELL_TAGS:
        for n in _css(baum, tag):
            try:
                n.decompose()
            except Exception:
                pass

    sprache = quelle.get("sprache", "de")
    # Die literal:-Werte aus sources.yaml sind handrecherchierte Fakten
    # (z.B. Consorsbank -> Einlagensicherung FR). Sie gelten auch dann,
    # wenn die CSS-Selektoren daneben nichts taugen.
    literale = _literal_felder(quelle)
    literal_bank = literale.get("bank")
    h_min, h_max = _heuristik_fenster()

    bester: list[dict[str, Any]] = []
    beste_quelle = ""
    beste_guete = (0, 0.0)

    for name, knoten in _struktur_gruppen(baum, sprache):
        if len(knoten) > 400:
            continue
        kandidaten: list[dict[str, Any]] = []
        for n in knoten:
            text = _knoten_text(n)
            # streng: nur echte Prozentangaben, keine blanken Zahlen -
            # sonst wird die Ranglistennummer "1" zu 1,00 % Zins.
            prozente = finde_prozente(text, sprache, streng=True, min_pct=h_min, max_pct=h_max)
            if not prozente:
                continue
            bank = literal_bank or _bank_aus_knoten(n)
            if not bank or len(bank) < 2:
                continue
            aktion, basis = _aktion_und_basis(text, prozente, sprache)
            treffer_roh = {
                "bank": bank,
                "zinssatz": f"{aktion}%",
                "zinssatz_pct": aktion,
                "folgezins_pct": basis,
                "zinstyp": text,
                "aktionsdauer_monate": text,
                "mindestanlage": text,
                "einlagensicherung_land": text,
                "_kontext": text[:300],
            }
            # Festwerte aus sources.yaml gewinnen gegen den geratenen Text -
            # ausser beim Zins selbst, der immer von der Seite kommt.
            for feld, wert in literale.items():
                if feld != "zinssatz":
                    treffer_roh[feld] = wert
            kandidaten.append(treffer_roh)

        if not kandidaten:
            continue
        # Guete: erstens Anzahl unterschiedlicher Banknamen (eine Struktur mit
        # 40 Layout-Dopplungen derselben Bank ist schlechter als eine mit 8
        # echten), zweitens - bei Gleichstand - die feinere Granularitaet.
        namen = {entschaerfe(k["bank"])[:40] for k in kandidaten}
        mittel_laenge = sum(len(k["_kontext"]) for k in kandidaten) / len(kandidaten)
        guete = (len(namen), -mittel_laenge)
        if guete > beste_guete:
            beste_guete = guete
            bester = kandidaten
            beste_quelle = name

    if not bester:
        # Einzelseite: eine Bank, Zins irgendwo im Fliesstext.
        einzel = _heuristik_einzelseite(baum, quelle)
        if einzel:
            versuch.treffer = 1
            versuch.detail = "Einzelseiten-Heuristik (Hero-/Fliesstext)"
            return [einzel], versuch
        versuch.fehler = "keine wiederkehrende Struktur mit Zins gefunden"
        return [], versuch

    # Gleiche Bank + gleicher Zins mehrfach = meist Layout-Dopplung.
    gesehen: set[tuple[str, float]] = set()
    treffer: list[dict[str, Any]] = []
    for k in bester:
        schluessel = (entschaerfe(k["bank"])[:40], k["zinssatz_pct"])
        if schluessel in gesehen:
            continue
        gesehen.add(schluessel)
        k["extraction_tier"] = 2
        k["extraction_method"] = "css_heuristik"
        k["confidence"] = _conf("tier2_css_heuristik", 0.5)
        treffer.append(k)

    versuch.treffer = len(treffer)
    versuch.detail = f"Struktur '{beste_quelle}'"
    return treffer, versuch


def _heuristik_einzelseite(baum, quelle: dict[str, Any]) -> dict[str, Any] | None:
    """Eine Bankseite = ein Angebot. Zins aus Ueberschrift oder Fliesstext."""
    if quelle.get("typ") != "bank":
        return None
    sprache = quelle.get("sprache", "de")
    literale = _literal_felder(quelle)
    literal_bank = literale.get("bank")
    h_min, h_max = _heuristik_fenster()

    bank = literal_bank
    if not bank:
        for sel in ("h1", "meta[property='og:site_name']", "title"):
            n = _css(baum, sel)
            if n:
                bank = _feldwert_aus_knoten(n[0])[:60]
                if bank:
                    break
    if not bank:
        return None

    # Ueberschriften zuerst - dort steht der Werbezins.
    for sel in ("h1", "h2", "[class*=hero]", "[class*=stage]", "[class*=rate]",
                "[class*=zins]", "[class*=price]"):
        for n in _css(baum, sel)[:12]:
            text = _knoten_text(n)
            prozente = finde_prozente(text, sprache, streng=True, min_pct=h_min, max_pct=h_max)
            if prozente:
                return _einzel_roh(bank, prozente, text, sprache, literale)

    ganz = _knoten_text(baum.body) if getattr(baum, "body", None) else ""
    prozente = finde_prozente(ganz[:4000], sprache, streng=True, min_pct=h_min, max_pct=h_max)
    if prozente:
        return _einzel_roh(bank, prozente, ganz[:400], sprache, literale)
    return None


def _einzel_roh(bank: str, prozente: list[float], kontext: str,
                sprache: str = "de",
                literale: dict[str, str] | None = None) -> dict[str, Any]:
    aktion, basis = _aktion_und_basis(kontext, prozente, sprache)
    roh = {
        "bank": bank,
        "zinssatz": f"{aktion}%",
        "zinssatz_pct": aktion,
        "folgezins_pct": basis,
        "zinstyp": kontext,
        "aktionsdauer_monate": kontext,
        "mindestanlage": kontext,
        "einlagensicherung_land": kontext,
        "_kontext": kontext[:300],
        "extraction_tier": 2,
        "extraction_method": "css_heuristik_einzelseite",
        "confidence": _conf("tier2_css_heuristik", 0.5) * 0.9,
    }
    # Handrecherchierte Festwerte aus sources.yaml gewinnen gegen den
    # aus dem Fliesstext geratenen Kontext.
    for feld, wert in (literale or {}).items():
        if feld != "zinssatz":       # der Zins kommt immer aus der Seite
            roh[feld] = wert
    return roh


# ================================================================== STUFE 3

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{modell}:generateContent"

LLM_PROMPT = """Du bekommst den Fliesstext einer Webseite ueber Sparzinsen \
(Tagesgeld / Sparkonto / Festgeld) aus dem Land {land}, Sprache {sprache}.

Extrahiere ALLE Sparzins-Angebote, die im Text stehen.

Regeln:
- Nur was wirklich dasteht. Nichts schaetzen, nichts ergaenzen.
- Zinssaetze als Zahl mit Punkt als Dezimaltrennzeichen, ohne Prozentzeichen.
- Ist kein Zinssatz genannt, gib das Angebot nicht aus.
- aktionsdauer_monate nur, wenn eine befristete Aktion genannt ist, sonst 0.
- folgezins ist der Zins NACH der Aktion. Unbekannt -> leer lassen.
- einlagensicherung_land als ISO-2-Code (DE, FR, NL, ...), wenn erkennbar.
- Gibt es keine Angebote, gib eine leere Liste zurueck.

Text:
---
{text}
---
"""

LLM_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "angebote": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "bank": {"type": "STRING"},
                    "produkt": {"type": "STRING"},
                    "zinssatz": {"type": "STRING"},
                    "zinstyp": {"type": "STRING"},
                    "aktionsdauer_monate": {"type": "STRING"},
                    "folgezins": {"type": "STRING"},
                    "mindestanlage": {"type": "STRING"},
                    "hoechstanlage": {"type": "STRING"},
                    "einlagensicherung_land": {"type": "STRING"},
                    "waehrung": {"type": "STRING"},
                },
                "required": ["bank", "zinssatz"],
            },
        }
    },
    "required": ["angebote"],
}


def html_zu_fliesstext(html: str, max_zeichen: int | None = None) -> str:
    """HTML auf lesbaren Text reduzieren: Skripte, Navigation, Styles raus."""
    if max_zeichen is None:
        max_zeichen = int(cfg_get("extraktion.llm_max_zeichen", 8000))
    baum = _parse(html)
    if baum is None:
        text = re.sub(r"<[^>]+>", " ", html)
        return aufraeumen(text)[:max_zeichen]

    for tag in MUELL_TAGS:
        for n in _css(baum, tag):
            try:
                n.decompose()
            except Exception:
                pass
    # Cookie-Banner und Werbeblöcke wegwerfen
    for sel in ("[class*=cookie]", "[id*=cookie]", "[class*=consent]",
                "[class*=banner]", "[class*=newsletter]", "[class*=breadcrumb]"):
        for n in _css(baum, sel):
            try:
                n.decompose()
            except Exception:
                pass

    wurzel = getattr(baum, "body", None) or baum
    text = _knoten_text(wurzel)
    text = re.sub(r"(\s*\|\s*){2,}", " | ", text)
    return text[:max_zeichen]


def stufe3_llm(html: str, quelle: dict[str, Any]) -> tuple[list[dict], StufenVersuch]:
    versuch = StufenVersuch(3, "llm_gemini")

    if not cfg_get("extraktion.llm_aktiv", True):
        versuch.fehler = "LLM-Stufe per Config deaktiviert"
        return [], versuch

    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        versuch.fehler = "GEMINI_API_KEY nicht gesetzt - Stufe uebersprungen"
        return [], versuch

    text = html_zu_fliesstext(html)
    if len(text) < 80:
        versuch.fehler = "zu wenig Text nach der Reduktion"
        return [], versuch

    modell = cfg_get("extraktion.llm_modell", "gemini-2.0-flash")
    prompt = LLM_PROMPT.format(
        land=quelle.get("land", "?"),
        sprache=quelle.get("sprache", "?"),
        text=text,
    )
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.0,
            "responseMimeType": "application/json",
            "responseSchema": LLM_SCHEMA,
        },
    }

    try:
        r = httpx.post(
            GEMINI_URL.format(modell=modell),
            params={"key": key},
            json=payload,
            timeout=float(cfg_get("extraktion.llm_timeout_s", 60.0)),
        )
    except httpx.HTTPError as e:
        versuch.fehler = f"Gemini nicht erreichbar: {type(e).__name__}"
        return [], versuch

    if r.status_code != 200:
        versuch.fehler = f"Gemini HTTP {r.status_code}: {r.text[:200]}"
        return [], versuch

    try:
        antwort = r.json()
        roh_text = antwort["candidates"][0]["content"]["parts"][0]["text"]
        daten = json.loads(roh_text)
    except (ValueError, KeyError, IndexError, TypeError) as e:
        versuch.fehler = f"Gemini-Antwort unlesbar: {type(e).__name__}"
        return [], versuch

    angebote = daten.get("angebote") if isinstance(daten, dict) else None
    if not isinstance(angebote, list):
        versuch.fehler = "Gemini lieferte kein 'angebote'-Array"
        return [], versuch

    treffer: list[dict[str, Any]] = []
    for a in angebote:
        if not isinstance(a, dict) or not a.get("bank") or not a.get("zinssatz"):
            continue
        roh = {k: v for k, v in a.items() if v not in (None, "")}
        roh["extraction_tier"] = 3
        roh["extraction_method"] = "llm_gemini"
        roh["confidence"] = _conf("tier3_llm", 0.4)
        treffer.append(roh)

    versuch.treffer = len(treffer)
    versuch.detail = f"{modell}, {len(text)} Zeichen Prompt-Text"
    if not treffer:
        versuch.fehler = "LLM fand keine Angebote"
    return treffer, versuch


# ================================================================== Steuerung

def html_holen(quelle: dict[str, Any], fetcher: Fetcher) -> Antwort:
    """Seite holen - gerendert nur bei rendering: js_required."""
    url = quelle["url"]
    if (quelle.get("rendering") or "").strip() == "js_required":
        return fetcher.hole_gerendert(url)
    return fetcher.hole(url)


def extrahiere(quelle: dict[str, Any], fetcher: Fetcher, *,
               html: str | None = None) -> Ergebnis:
    """Die drei Stufen der Reihe nach. Erste erfolgreiche gewinnt.

    `html` kann vorgegeben werden (Tests, bootstrap.py), dann wird die
    Seite nicht erneut geholt. Der json_endpoint wird trotzdem probiert.
    """
    erg = Ergebnis(quelle_id=quelle.get("id", ""), url=quelle.get("url", ""))

    # --- Stufe 1a: JSON-Endpoint (braucht kein HTML) ---
    treffer, versuch = stufe1_json_endpoint(quelle, fetcher)
    erg.versuche.append(versuch)
    if treffer:
        erg.treffer, erg.tier, erg.methode = treffer, 1, "json_endpoint"
        log().info("  Quelle %-24s Stufe 1 (json_endpoint): %d Treffer", erg.quelle_id, len(treffer))
        return erg

    # --- Seite besorgen ---
    if html is None:
        ant = html_holen(quelle, fetcher)
        erg.http_status = ant.status
        erg.gesperrt = ant.gesperrt
        if ant.gesperrt:
            erg.fehler = ant.fehler
            log().info("  Quelle %-24s uebersprungen (robots.txt)", erg.quelle_id)
            return erg
        if not ant.ok:
            erg.fehler = ant.fehler or f"HTTP {ant.status}"
            erg.versuche.append(StufenVersuch(0, "fetch", 0, erg.fehler))
            log().warning("  Quelle %-24s nicht abrufbar: %s", erg.quelle_id, erg.fehler)
            return erg
        html = ant.text

    # --- Stufe 1b: JSON-LD ---
    treffer, versuch = stufe1_jsonld(html, quelle)
    erg.versuche.append(versuch)
    if treffer:
        erg.treffer, erg.tier, erg.methode = treffer, 1, "jsonld"
        log().info("  Quelle %-24s Stufe 1 (JSON-LD): %d Treffer", erg.quelle_id, len(treffer))
        return erg

    # --- Stufe 2a: konfigurierte Selektoren ---
    treffer, versuch = stufe2_css(html, quelle)
    erg.versuche.append(versuch)
    if treffer:
        erg.treffer, erg.tier, erg.methode = treffer, 2, versuch.methode
        log().info("  Quelle %-24s Stufe 2 (Selektoren): %d Treffer", erg.quelle_id, len(treffer))
        return erg

    # --- Stufe 2b: generische Heuristik ---
    treffer, versuch = stufe2_heuristik(html, quelle)
    erg.versuche.append(versuch)
    if treffer:
        erg.treffer, erg.tier, erg.methode = treffer, 2, "css_heuristik"
        log().info("  Quelle %-24s Stufe 2 (Heuristik): %d Treffer", erg.quelle_id, len(treffer))
        return erg

    # --- Stufe 3: LLM ---
    treffer, versuch = stufe3_llm(html, quelle)
    erg.versuche.append(versuch)
    if treffer:
        erg.treffer, erg.tier, erg.methode = treffer, 3, "llm_gemini"
        log().info("  Quelle %-24s Stufe 3 (LLM): %d Treffer", erg.quelle_id, len(treffer))
        return erg

    erg.fehler = "; ".join(f"S{v.stufe}/{v.methode}: {v.fehler}" for v in erg.versuche if v.fehler)
    log().warning("  Quelle %-24s KEIN Treffer (%s)", erg.quelle_id, erg.fehler[:160])
    return erg


def parser_name() -> str:
    return _PARSER_NAME
