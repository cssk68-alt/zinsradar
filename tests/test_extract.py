"""Tests fuer die drei Extraktionsstufen - mit HTML-Fixtures, ohne Netz."""

import json

import pytest

import extract as e


QUELLE_PORTAL = {
    "id": "test.de", "url": "https://test.de/tagesgeld", "land": "DE",
    "sprache": "de", "typ": "portal", "rendering": "static_html",
    "container_selector": "div.angebot",
    "felder": {
        "bank": ".name",
        "zinssatz": ".zins",
        "mindestanlage": ".min",
    },
}


# ============================================================ Stufe 1: JSON-LD

JSONLD_SEITE = """<!DOCTYPE html><html><head>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FinancialProduct",
  "name": "Tagesgeld Plus",
  "provider": {"@type": "BankOrCreditUnion", "name": "Muster Bank AG"},
  "interestRate": "3.4",
  "areaServed": "DE",
  "feesAndCommissionsSpecification": "keine"
}
</script></head><body><p>Irgendwas</p></body></html>"""


def test_jsonld_wird_gelesen():
    treffer, versuch = e.stufe1_jsonld(JSONLD_SEITE, QUELLE_PORTAL)
    assert len(treffer) == 1
    assert treffer[0]["bank"] == "Muster Bank AG"
    assert treffer[0]["extraction_tier"] == 1
    assert treffer[0]["extraction_method"] == "jsonld"
    assert versuch.treffer == 1


JSONLD_GRAPH = """<html><head><script type="application/ld+json">
{"@context":"https://schema.org","@graph":[
  {"@type":"WebPage","name":"Vergleich"},
  {"@type":"Offer","name":"Sparkonto","seller":{"name":"Graph Bank"},"interestRate":2.9}
]}</script></head><body></body></html>"""


def test_jsonld_findet_in_graph():
    treffer, _ = e.stufe1_jsonld(JSONLD_GRAPH, QUELLE_PORTAL)
    assert treffer[0]["bank"] == "Graph Bank"
    assert treffer[0]["zinssatz_pct"] == pytest.approx(2.9)


def test_jsonld_ohne_zins_wird_verworfen():
    html = """<html><head><script type="application/ld+json">
    {"@type":"Organization","name":"Nur eine Bank"}</script></head><body></body></html>"""
    treffer, versuch = e.stufe1_jsonld(html, QUELLE_PORTAL)
    assert treffer == []
    assert versuch.fehler


def test_jsonld_kaputtes_json_stuerzt_nicht_ab():
    html = '<html><head><script type="application/ld+json">{kaputt,,</script></head><body></body></html>'
    treffer, versuch = e.stufe1_jsonld(html, QUELLE_PORTAL)
    assert treffer == []
    assert versuch.fehler


def test_dezimalbruch_wird_zu_prozent():
    """Manche APIs liefern 0.034 statt 3.4."""
    roh = e._dict_zu_rohtreffer({"name": "X Bank", "interestRate": 0.034})
    assert roh["zinssatz_pct"] == pytest.approx(3.4)


# ============================================================ Stufe 2a: CSS

CSS_SEITE = """<html><body>
<div class="angebot"><span class="name">Alpha Bank</span>
  <span class="zins">3,25 % p.a.</span><span class="min">ab 1.000 EUR</span></div>
<div class="angebot"><span class="name">Beta Bank</span>
  <span class="zins">2,80 %</span><span class="min">0 EUR</span></div>
</body></html>"""


def test_css_selektoren_greifen():
    treffer, versuch = e.stufe2_css(CSS_SEITE, QUELLE_PORTAL)
    assert len(treffer) == 2
    assert treffer[0]["bank"] == "Alpha Bank"
    assert treffer[0]["zinssatz"] == "3,25 % p.a."
    assert treffer[0]["extraction_tier"] == 2
    assert versuch.methode == "css_konfiguriert"


def test_css_ohne_treffer_meldet_fehler():
    quelle = dict(QUELLE_PORTAL, container_selector="div.gibtesnicht")
    treffer, versuch = e.stufe2_css(CSS_SEITE, quelle)
    assert treffer == []
    assert "findet nichts" in versuch.fehler


def test_kaputter_selektor_bricht_nicht_ab():
    """Erfundene Selektoren duerfen die gueltigen nicht mitreissen."""
    quelle = dict(QUELLE_PORTAL, container_selector="div[[kaputt, div.angebot")
    treffer, _ = e.stufe2_css(CSS_SEITE, quelle)
    assert len(treffer) == 2


def test_literal_wird_aufgeloest():
    assert e._literal("literal:'ING Deutschland'") == "ING Deutschland"
    assert e._literal('literal:"Klarna"') == "Klarna"
    assert e._literal("literal:0") == "0"
    assert e._literal(".css-klasse") is None


def test_literal_felder_werden_gesammelt():
    quelle = {"felder": {"bank": "literal:'X Bank'", "zinssatz": ".zins",
                         "einlagensicherung_land": "literal:'FR'"}}
    literale = e._literal_felder(quelle)
    assert literale == {"bank": "X Bank", "einlagensicherung_land": "FR"}


# ============================================================ Stufe 2b: Heuristik

# Struktur wie bei echten Vergleichsportalen: Klassennamen, die keine
# Selektorliste erraten wuerde, plus getrennte Namens- und Zinszeile.
HEURISTIK_SEITE = """<html><body>
<div class="wrap">
  <div class="topOfferResult-item saving"><h3>1 DHB Bank NetSparkonto</h3>
     <ul><li>Basiszins: 1,95% Aktionszins: 3,40% - gilt für die ersten 6 Monate</li></ul></div>
  <div class="topOfferResult-item saving"><h3>2 Chase Tagesgeld</h3>
     <ul><li>Basiszins: 2,00% Aktionszins: 4,00% - gilt für die ersten 4 Monate</li></ul></div>
  <div class="topOfferResult-item saving"><h3>3 Revolut Sparkonto</h3>
     <ul><li>Basiszins: 1,25% Aktionszins: 4,25% - gilt für die ersten 4 Monate</li></ul></div>
</div></body></html>"""


def test_heuristik_findet_ohne_selektoren():
    quelle = dict(QUELLE_PORTAL, container_selector="div.existiert-nicht", felder={})
    treffer, versuch = e.stufe2_heuristik(HEURISTIK_SEITE, quelle)
    banken = sorted(t["bank"] for t in treffer)
    assert len(treffer) == 3
    assert "DHB Bank NetSparkonto" in banken[1]
    assert all(t["extraction_tier"] == 2 for t in treffer)
    assert versuch.methode == "css_heuristik"


def test_heuristik_trennt_aktion_von_basis():
    quelle = dict(QUELLE_PORTAL, container_selector="x", felder={})
    treffer, _ = e.stufe2_heuristik(HEURISTIK_SEITE, quelle)
    dhb = [t for t in treffer if "DHB" in t["bank"]][0]
    assert dhb["zinssatz_pct"] == pytest.approx(3.40)   # Aktionszins
    assert dhb["folgezins_pct"] == pytest.approx(1.95)  # Basiszins


def test_aktion_und_basis_ohne_label_nimmt_reihenfolge():
    aktion, basis = e._aktion_und_basis("3,00 % und 1,50 %", [3.0, 1.5], "de")
    assert (aktion, basis) == (3.0, 1.5)


def test_heuristik_ignoriert_ranglistennummer():
    """"1 DHB Bank" darf nicht als 1,00 % Zins gelesen werden."""
    quelle = dict(QUELLE_PORTAL, container_selector="x", felder={})
    treffer, _ = e.stufe2_heuristik(HEURISTIK_SEITE, quelle)
    assert all(t["zinssatz_pct"] > 1.5 for t in treffer)


def test_heuristik_uebernimmt_literale():
    """Handrecherchierte Festwerte gelten auch, wenn nur die Heuristik greift."""
    quelle = dict(QUELLE_PORTAL, container_selector="x",
                  felder={"einlagensicherung_land": "literal:'FR'"})
    treffer, _ = e.stufe2_heuristik(HEURISTIK_SEITE, quelle)
    assert all(t["einlagensicherung_land"] == "FR" for t in treffer)


def test_heuristik_ignoriert_fremdprozente():
    html = """<html><body>
      <div class="row"><span>Alpha Bank</span><span>3,00 %</span></div>
      <div class="row"><span>Beta Bank</span><span>2,50 %</span></div>
      <div class="werbung"><span>Jetzt 15 % Rabatt sichern</span></div>
    </body></html>"""
    quelle = dict(QUELLE_PORTAL, container_selector="x", felder={})
    treffer, _ = e.stufe2_heuristik(html, quelle)
    assert all(t["zinssatz_pct"] <= 8.0 for t in treffer)


BANK_SEITE = """<html><body>
  <h1>Tagesgeld</h1>
  <section class="hero"><p>Jetzt <strong>3,75 %</strong> p.a. für 6 Monate sichern</p></section>
</body></html>"""


def test_einzelseite_einer_bank():
    quelle = {"id": "bank.de", "url": "https://bank.de", "land": "DE", "sprache": "de",
              "typ": "bank", "container_selector": "div.gibtesnicht",
              "felder": {"bank": "literal:'Muster Bank'", "einlagensicherung_land": "literal:'DE'"}}
    treffer, versuch = e.stufe2_heuristik(BANK_SEITE, quelle)
    assert len(treffer) == 1
    assert treffer[0]["bank"] == "Muster Bank"
    assert treffer[0]["zinssatz_pct"] == pytest.approx(3.75)
    assert treffer[0]["einlagensicherung_land"] == "DE"


# ============================================================ Labels/Namen

@pytest.mark.parametrize("text,ist_label", [
    ("Basiszins:", True), ("Anbieter", True), ("AAA", True), ("BBB+", True),
    ("Video-Ident", True), ("Jetzt Festzins sichern", True), ("Deutschland", True),
    ("DHB Bank", False), ("Chase", False), ("1822direkt", False),
])
def test_label_erkennung(text, ist_label):
    assert e._ist_label(text) is ist_label


def test_namens_kandidat_schneidet_praefixe():
    assert e._namens_kandidat("Anbieter und Produkt 1 DHB Bank") == "DHB Bank"
    assert e._namens_kandidat("3 Revolut Tagesgeld") == "Revolut Tagesgeld"
    assert e._namens_kandidat("Produktdetails Basiszins") == ""


# ============================================================ Stufe 3: LLM

def test_textreduktion_entfernt_skripte_und_nav():
    html = """<html><body>
      <nav>Startseite Kontakt Impressum</nav>
      <script>var x = 'unsichtbar';</script>
      <style>.a{color:red}</style>
      <div class="cookie-banner">Wir nutzen Cookies</div>
      <main><p>Tagesgeld 3,5 % bei der Musterbank</p></main>
      <footer>AGB</footer></body></html>"""
    text = e.html_zu_fliesstext(html)
    assert "Musterbank" in text
    assert "unsichtbar" not in text
    assert "Impressum" not in text
    assert "Cookies" not in text


def test_textreduktion_kappt_laenge():
    html = "<html><body><p>" + ("Zins " * 5000) + "</p></body></html>"
    assert len(e.html_zu_fliesstext(html, max_zeichen=800)) <= 800


def test_llm_ohne_key_ueberspringt(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    treffer, versuch = e.stufe3_llm("<html><body>" + "Tagesgeld 3 % " * 20 + "</body></html>",
                                    QUELLE_PORTAL)
    assert treffer == []
    assert "GEMINI_API_KEY" in versuch.fehler
    assert versuch.stufe == 3


def test_llm_schema_ist_gueltiges_json():
    assert json.dumps(e.LLM_SCHEMA)
    assert e.LLM_SCHEMA["properties"]["angebote"]["items"]["required"] == ["bank", "zinssatz"]


# ============================================================ Reihenfolge

class _FetcherStub:
    """Tut so, als gaebe es kein Netz - der json_endpoint schlaegt fehl."""

    def hole_json(self, url, robots=True):
        from fetch import Antwort
        return Antwort(url=url, fehler="Testmodus"), None


def test_stufenreihenfolge_erste_erfolgreiche_gewinnt():
    """JSON-LD schlaegt die CSS-Selektoren, auch wenn beide vorhanden sind."""
    html = JSONLD_SEITE.replace("</body>",
                                '<div class="angebot"><span class="name">CSS Bank</span>'
                                '<span class="zins">9,9 %</span></div></body>')
    erg = e.extrahiere(QUELLE_PORTAL, _FetcherStub(), html=html)
    assert erg.tier == 1
    assert erg.treffer[0]["bank"] == "Muster Bank AG"


def test_faellt_auf_heuristik_zurueck():
    quelle = dict(QUELLE_PORTAL, container_selector="div.gibtesnicht", felder={})
    erg = e.extrahiere(quelle, _FetcherStub(), html=HEURISTIK_SEITE)
    assert erg.tier == 2
    assert erg.methode == "css_heuristik"
    assert len(erg.treffer) == 3


def test_protokolliert_alle_versuche():
    quelle = dict(QUELLE_PORTAL, container_selector="div.nix", felder={})
    erg = e.extrahiere(quelle, _FetcherStub(), html="<html><body>leer</body></html>")
    stufen = [(v.stufe, v.methode) for v in erg.versuche]
    assert (1, "json_endpoint") in stufen
    assert (1, "jsonld") in stufen
    assert (2, "css_konfiguriert") in stufen
    assert (2, "css_heuristik") in stufen
    assert (3, "llm_gemini") in stufen
    assert erg.treffer == []
