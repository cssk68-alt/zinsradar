"""Tests fuer Zahlen-Parsing, Dedupe und Merge."""

import pytest

import normalize as n


# ------------------------------------------------------------------ Zinsen

@pytest.mark.parametrize("text,sprache,erwartet", [
    ("3,50 % p.a.", "de", 3.5),
    ("3.50%", "de", 3.5),
    ("3,5%", "de", 3.5),
    ("0,75 Prozent", "de", 0.75),
    ("Tasso lordo 3,00%", "it", 3.0),
    ("taux 2,60 %", "fr", 2.6),
    ("2.75% AER", "nl", 2.75),
    ("oprocentowanie 5,50%", "pl", 5.5),
    ("4,25 % p. a.", "de", 4.25),
])
def test_zins_parsen(text, sprache, erwartet):
    assert n.parse_zins(text, sprache) == pytest.approx(erwartet)


def test_mehrere_prozente_in_lesereihenfolge():
    text = "bis zu 4,00 % für 6 Monate, danach 1,25 %"
    assert n.finde_prozente(text, "de") == [4.0, 1.25]


def test_streng_ignoriert_blanke_zahlen():
    """Ranglistennummern duerfen nicht als Zins durchgehen."""
    assert n.finde_prozente("1 DHB Bank NetSparkonto", "de", streng=True) == []
    assert n.finde_prozente("1 DHB Bank NetSparkonto", "de", streng=False) == [1.0]


def test_fenster_begrenzt_ausreisser():
    assert n.finde_prozente("15 % Rabatt", "de", streng=True, max_pct=8.0) == []
    assert n.finde_prozente("3,5 %", "de", streng=True, max_pct=8.0) == [3.5]


def test_zins_ueber_grenze_wird_nicht_gelesen():
    assert n.parse_zins("120 %", "de") is None


# ------------------------------------------------------------------ Betraege

@pytest.mark.parametrize("text,sprache,betrag,waehrung", [
    ("ab 1.000 EUR", "de", 1000.0, "EUR"),
    ("min. 1,000.00 SEK", "sv", 1000.0, "SEK"),
    ("50 000 zl", "pl", 50000.0, "PLN"),
    ("0 EUR", "de", 0.0, "EUR"),
    ("unbegrenzt", "de", None, "EUR"),
    ("keine Mindestanlage", "de", None, "EUR"),
    ("2.500.000 Kc", "cz", 2500000.0, "CZK"),
])
def test_betrag_parsen(text, sprache, betrag, waehrung):
    wert, w = n.parse_betrag(text, sprache)
    assert w == waehrung
    if betrag is None:
        assert wert is None
    else:
        assert wert == pytest.approx(betrag)


def test_tausender_vs_dezimal():
    """Mehrdeutige Zahlen: Sprache bestimmt die Reihenfolge der Lesarten,
    der Wertebereich entscheidet dann, welche genommen wird."""
    # Deutsch: "1.000" ist zuerst tausend, "1,0" waere die Dezimallesart.
    assert n._deutungen("1.000", "de") == [1000.0, 1.0]
    assert n._deutungen("1.000", "nl") == [1.0, 1000.0]
    # Als Betrag gilt die sprachliche Lesart ...
    assert n.parse_betrag("1.000 EUR", "de")[0] == pytest.approx(1000.0)
    # ... als Zins die Lesart, die in den Zinsbereich passt.
    assert n.finde_prozente("1.000 %", "de") == [1.0]
    # Eindeutige Formate bleiben eindeutig.
    assert n.parse_betrag("1,234.56 EUR", "nl")[0] == pytest.approx(1234.56)
    assert n.parse_betrag("1.234,56 EUR", "de")[0] == pytest.approx(1234.56)


# ------------------------------------------------------------------ Sonstiges

@pytest.mark.parametrize("text,erwartet", [
    ("6 Monate", 6), ("12 mesi", 12), ("1 Jahr", 12), ("24 maanden", 24),
    ("3 mois", 3), ("0", 0), ("kein Aktionszeitraum", None),
])
def test_monate(text, erwartet):
    assert n.parse_monate(text) == erwartet


@pytest.mark.parametrize("text,erwartet", [
    ("Deutschland", "DE"), ("/flags/nl.svg", "NL"), ("ES", "ES"),
    ("Sverige", "SE"), ("Italia", "IT"), ("irgendwas", None),
])
def test_land(text, erwartet):
    assert n.parse_land(text) == erwartet


def test_zinstyp():
    assert n.parse_zinstyp("Aktionszins für Neukunden") == "aktion"
    assert n.parse_zinstyp("variabel, täglich verfügbar") == "variabel"
    assert n.parse_zinstyp("", aktionsdauer=6) == "aktion"
    assert n.parse_zinstyp("", aktionsdauer=0) == "variabel"


def test_fx():
    assert n.fx_umrechnen(50000, "PLN", {"PLN": 4.0}) == pytest.approx(12500.0)
    assert n.fx_umrechnen(100, "EUR", {}) == pytest.approx(100.0)
    assert n.fx_umrechnen(100, "XYZ", {"PLN": 4.0}) is None
    assert n.fx_umrechnen(None, "PLN", {"PLN": 4.0}) is None


# ------------------------------------------------------------------ Namen

@pytest.mark.parametrize("name,ok", [
    ("DHB Bank", True), ("ING Deutschland AG", True), ("1822direkt", True),
    ("Monate 1", False),
    ("Zinsgutschrift / Jahr 12 Kontotyp", False),
    ("S&P Länderrating AAA Deutschland", False),
    ("Bis 300€ &", False),
    ("Pieniądze na dowolny cel. Co wybierasz?", False),
    ("", False), ("AB", False),
])
def test_bank_plausibel(name, ok):
    assert n.bank_plausibel(name) is ok


def test_dedupe_key_ignoriert_produktzusatz():
    a = n.dedupe_key("Revolut Tagesgeld(Standard)", "Tagesgeld", "DE")
    b = n.dedupe_key("Revolut", "Tagesgeld", "DE")
    assert a == b


def test_dedupe_key_trennt_laender():
    assert n.dedupe_key("X Bank", "Tagesgeld", "DE") != n.dedupe_key("X Bank", "Tagesgeld", "FR")


def test_rechtsform_stoert_dedupe_nicht():
    assert n.bank_schluessel("Klarna Bank AB") == n.bank_schluessel("Klarna Bank")


# ------------------------------------------------------------------ Normalisieren

QUELLE = {"id": "test.de", "url": "https://test.de", "land": "DE",
          "sprache": "de", "typ": "portal"}


def _roh(**kw):
    basis = {"bank": "Testbank", "zinssatz": "3,00 %", "extraction_tier": 2,
             "extraction_method": "test", "confidence": 0.7}
    basis.update(kw)
    return basis


def test_normalisieren_grundfall():
    a = n.normalisiere(_roh(), QUELLE, {})
    assert a["bank"] == "Testbank"
    assert a["zinssatz_pct"] == pytest.approx(3.0)
    assert a["zinstyp"] == "variabel"
    assert a["aktionsdauer_monate"] == 0
    assert a["folgezins_pct"] == pytest.approx(3.0)   # variabel -> laeuft weiter
    assert a["land_quelle"] == "quellenland_angenommen"


def test_normalisieren_verwirft_ohne_zins():
    assert n.normalisiere(_roh(zinssatz="keine Angabe"), QUELLE, {}) is None


def test_normalisieren_verwirft_unplausiblen_namen():
    assert n.normalisiere(_roh(bank="Monate 1"), QUELLE, {}) is None


def test_scheinaktion_wird_zu_variabel():
    """'2,95 % für 48 Monate, danach 2,95 %' ist keine Aktion."""
    a = n.normalisiere(_roh(zinssatz="2,95 %", zinssatz_pct=2.95, folgezins_pct=2.95,
                            zinstyp="Aktion", aktionsdauer_monate="48 Monate"), QUELLE, {})
    assert a["zinstyp"] == "variabel"
    assert a["aktionsdauer_monate"] == 0


def test_echte_aktion_bleibt_aktion():
    a = n.normalisiere(_roh(zinssatz="4,00 %", zinssatz_pct=4.0, folgezins_pct=1.5,
                            zinstyp="Aktionszins", aktionsdauer_monate="6 Monate"), QUELLE, {})
    assert a["zinstyp"] == "aktion"
    assert a["aktionsdauer_monate"] == 6
    assert a["folgezins_pct"] == pytest.approx(1.5)


@pytest.mark.parametrize("name", [
    "Planbare Geldanlage", "Kapitalanlage sichern", "Sparplan Basis",
])
def test_werbeslogans_sind_keine_banken(name):
    assert n.bank_plausibel(name) is False


def test_bankseite_markiert_land_anders():
    q = dict(QUELLE, typ="bank")
    a = n.normalisiere(_roh(), q, {})
    assert a["land_quelle"] == "bankseite"


def test_erkanntes_land_gewinnt():
    a = n.normalisiere(_roh(einlagensicherung_land="Spanien"), QUELLE, {})
    assert a["einlagensicherung_land"] == "ES"
    assert a["land_quelle"] == "erkannt"


# ------------------------------------------------------------------ Merge

def test_merge_fuehrt_gleiche_bank_zusammen():
    q2 = dict(QUELLE, id="andere.de")
    a1 = n.normalisiere(_roh(), QUELLE, {})
    a2 = n.normalisiere(_roh(mindestanlage="1.000 EUR"), q2, {})
    zusammen = n.merge([a1, a2])
    assert len(zusammen) == 1
    assert zusammen[0]["quellen_anzahl"] == 2
    assert zusammen[0]["mindestanlage"] == pytest.approx(1000.0)


def test_merge_bevorzugt_niedrigeren_tier():
    a1 = n.normalisiere(_roh(zinssatz="3,00 %", extraction_tier=2, confidence=0.5), QUELLE, {})
    a2 = n.normalisiere(_roh(zinssatz="3,20 %", extraction_tier=1, confidence=0.95),
                        dict(QUELLE, id="api.de"), {})
    zusammen = n.merge([a1, a2])
    assert len(zusammen) == 1
    assert zusammen[0]["zinssatz_pct"] == pytest.approx(3.2)
    assert zusammen[0]["extraction_tier"] == 1


def test_merge_meldet_abweichung():
    a1 = n.normalisiere(_roh(zinssatz="3,00 %"), QUELLE, {})
    a2 = n.normalisiere(_roh(zinssatz="3,50 %"), dict(QUELLE, id="andere.de"), {})
    zusammen = n.merge([a1, a2])
    assert zusammen[0]["quellen_abweichung"][0]["differenz_pp"] == pytest.approx(0.5)


def test_land_dopplung_wird_aufgeloest():
    """Portal rät DE, Bankseite belegt FR -> ein Eintrag mit FR."""
    portal = n.normalisiere(_roh(), QUELLE, {})
    bank = n.normalisiere(_roh(einlagensicherung_land="Frankreich"),
                          dict(QUELLE, id="bank.de", typ="bank"), {})
    zusammen = n.merge([portal, bank])
    assert len(zusammen) == 1
    assert zusammen[0]["einlagensicherung_land"] == "FR"
    assert zusammen[0]["quellen_anzahl"] == 2


def test_zwei_belegte_laender_bleiben_getrennt():
    """Eine Bank kann echte Angebote in zwei Laendern haben."""
    a = n.normalisiere(_roh(einlagensicherung_land="Frankreich"),
                       dict(QUELLE, id="a.de", typ="bank"), {})
    b = n.normalisiere(_roh(einlagensicherung_land="Spanien"),
                       dict(QUELLE, id="b.de", typ="bank"), {})
    assert len(n.merge([a, b])) == 2


def test_merge_verliert_keine_angebote():
    """Regressionstest: die Land-Nachbereinigung darf nichts verschlucken."""
    eingaben = []
    for i in range(12):
        eingaben.append(n.normalisiere(
            _roh(bank=f"Bank {i} AG", zinssatz=f"{2 + i * 0.1:.2f} %".replace(".", ",")),
            QUELLE, {}))
    assert len(n.merge(eingaben)) == 12


# ------------------------------------------------------------------ Overrides

def test_override_gewinnt():
    a = n.normalisiere(_roh(), QUELLE, {})
    ov = {"eintraege": {a["override_key"]: {"zinssatz_pct": 9.99, "notiz": "geprüft"}}}
    ergebnis, protokoll = n.overrides_anwenden([a], ov)
    assert ergebnis[0]["zinssatz_pct"] == pytest.approx(9.99)
    assert ergebnis[0]["override"] is True
    assert protokoll


def test_override_ohne_treffer_wird_eigener_eintrag():
    ov = {"eintraege": {"neue bank|tagesgeld|at": {"zinssatz_pct": 3.1}}}
    ergebnis, _ = n.overrides_anwenden([], ov)
    assert len(ergebnis) == 1
    assert ergebnis[0]["einlagensicherung_land"] == "AT"
    assert ergebnis[0]["extraction_tier"] == 0
