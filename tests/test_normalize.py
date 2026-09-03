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


# ------------------------------------------------- Datenqualitaet (v1.1)

@pytest.mark.parametrize("muell", [
    "Wykres notowania dax",
    "Wykres notowania wig20",
    "Derzeit",
    "22.06.2026: Zinserhöhung BBBank Tagesgeld: jetzt",
    "Kursverlauf Nasdaq",
])
def test_bank_plausibel_wirft_chartkacheln_raus(muell):
    """Portalseiten stellen Kursmodule neben die Zinstabelle."""
    assert n.bank_plausibel(muell) is False


@pytest.mark.parametrize("echt", [
    "Trade Republic", "BW-Bank", "Banca Progetto", "Livret A",
    "ING", "DHB Bank", "Oyak Anker Bank",
])
def test_bank_plausibel_laesst_echte_namen_durch(echt):
    assert n.bank_plausibel(echt) is True


@pytest.mark.parametrize("roh,erwartet", [
    ("Revolut Tagesgeld(Standard)", "Revolut"),
    ("Chase Tagesgeld", "Chase"),
    ("DHB Bank DHB NetSp@rkonto", "DHB Bank"),
    ("Livret A", "Livret A"),                 # darf nicht verschwinden
    ("Tagesgeld", "Tagesgeld"),               # nichts uebrig -> unveraendert
    ("Trade Republic", "Trade Republic"),
])
def test_anzeigename_ohne_produktzusatz(roh, erwartet):
    assert n.bank_normalisieren(roh) == erwartet


@pytest.mark.parametrize("betrag,ok", [
    (None, False), (0, True), (0.0, True),
    (4.25, False),     # das war der Zinssatz
    (12.0, False), (99.99, False),
    (100, True), (500.0, True), (100000, True),
    (-5, False),
])
def test_betrag_plausibel(betrag, ok):
    assert n.betrag_plausibel(betrag) is ok


def test_betrag_gleich_zins_wird_verworfen():
    assert n.betrag_plausibel(2500.0, 2500.0) is False
    assert n.betrag_plausibel(2500.0, 3.5) is True


def test_mindestanlage_uebernimmt_keinen_zinssatz():
    """Regression: 'Mindestanlage 4,25 €' war in Wahrheit der Zins."""
    a = n.normalisiere(_roh(zinssatz="4,25 %", mindestanlage="4,25"), QUELLE, {})
    assert a["mindestanlage"] is None
    assert a["mindestanlage_eur"] is None


def test_mindestanlage_bleibt_wenn_plausibel():
    a = n.normalisiere(_roh(mindestanlage="5.000 €"), QUELLE, {})
    assert a["mindestanlage"] == pytest.approx(5000.0)


def test_hoechstanlage_kleiner_als_mindestanlage_faellt_raus():
    a = n.normalisiere(_roh(mindestanlage="100.000 €", hoechstanlage="500 €"), QUELLE, {})
    assert a["mindestanlage"] is None
    assert a["hoechstanlage"] is None


def test_altbestand_saeubern_raeumt_vortagsmuell_auf():
    """Uebernommene stale-Eintraege muessen dieselben Filter passieren."""
    angebote = [
        {"bank": "Wykres notowania dax", "zinssatz_pct": 0.45},
        {"bank": "Chase Tagesgeld", "zinssatz_pct": 4.0,
         "mindestanlage": 4.0, "mindestanlage_eur": 4.0},
        {"bank": "Trade Republic", "zinssatz_pct": 2.25,
         "mindestanlage": 1000.0, "mindestanlage_eur": 1000.0},
    ]
    behalten, protokoll = n.altbestand_saeubern(angebote)

    assert [a["bank"] for a in behalten] == ["Chase", "Trade Republic"]
    assert behalten[0]["mindestanlage"] is None
    assert behalten[0]["mindestanlage_eur"] is None
    assert behalten[1]["mindestanlage"] == pytest.approx(1000.0)
    assert len(protokoll) == 3       # verworfen, gekuerzt, Betrag entfernt


def test_altbestand_dedupe_nach_namenskuerzung():
    """Nach dem Kuerzen darf dieselbe Bank nicht zweimal dastehen."""
    angebote = [
        {"bank": "DHB Bank", "produkt": "Tagesgeld", "einlagensicherung_land": "DE",
         "zinssatz_pct": 3.4, "stale": False, "quellen_anzahl": 1},
        {"bank": "DHB Bank DHB NetSp@rkonto", "produkt": "Tagesgeld",
         "einlagensicherung_land": "DE", "zinssatz_pct": 3.4,
         "stale": True, "quellen_anzahl": 1},
    ]
    behalten, protokoll = n.altbestand_saeubern(angebote)
    assert len(behalten) == 1
    assert behalten[0]["stale"] is False
    assert any("Dopplung" in z for z in protokoll)


def test_altbestand_haelt_gleiche_bank_in_zwei_laendern_auseinander():
    """Renault Bank DE und FR sind zwei Angebote, keine Dopplung."""
    angebote = [
        {"bank": "Renault Bank", "produkt": "Tagesgeld",
         "einlagensicherung_land": "DE", "zinssatz_pct": 3.5},
        {"bank": "Renault Bank", "produkt": "Tagesgeld",
         "einlagensicherung_land": "FR", "zinssatz_pct": 2.15},
    ]
    behalten, _ = n.altbestand_saeubern(angebote)
    assert len(behalten) == 2


@pytest.mark.parametrize("schlagzeile", [
    "Sikorski: Nasz sojusznik został zaatakowany",
    "Bundesschatz 2026: Zinsen, Steuern &",
    "Tagesgeldvergleich: die besten Anbieter",
])
def test_bank_plausibel_wirft_schlagzeilen_raus(schlagzeile):
    """Nachrichtenkacheln stehen auf Portalen neben der Zinstabelle."""
    assert n.bank_plausibel(schlagzeile) is False


# ------------------------------------ Aktionszins und Neukunden (v1.1)

# Genau der Textblock, an dem der Chase-Fehler hing: 4 % gelten nur vier
# Monate, danach 2 %. Vorher stand die 4 % als Dauerzins in der Liste.
CHASE_BLOCK = (
    "Zinsgutschrift / Jahr 12 Kontotyp Tagesgeldkonto Basiszins Ab 0€: 2% "
    "Aktionszins Ab 0€: 4% Dauer Aktionszins 4 Kundenkreis Neukunden "
    "Besonderheiten 4 % p. a. für die ersten 4 Monate bis 500.000 €; "
    "danach sowie darüber variabel, aktuell 2 % p. a."
)


def test_aktionsdauer_aus_chase_block():
    assert n.aktionsdauer_aus_text(CHASE_BLOCK) == 4


def test_aktionsdauer_faellt_nicht_auf_zinsgutschrift_herein():
    """'Zinsgutschrift / Jahr 12' ist keine Aktionsdauer."""
    assert n.aktionsdauer_aus_text("Zinsgutschrift / Jahr 12 Laufzeit 12 Monate") is None


@pytest.mark.parametrize("text,erwartet", [
    ("3,5 % für die ersten 6 Monate", 6),
    ("12 Monate lang garantiert", 12),
    ("Aktionsdauer: 9", 9),
    ("garantiert für 4 Monate", 4),
    ("kein Hinweis auf eine Dauer", None),
])
def test_aktionsdauer_muster(text, erwartet):
    assert n.aktionsdauer_aus_text(text) == erwartet


@pytest.mark.parametrize("text,erwartet", [
    (CHASE_BLOCK, True),
    ("Nur für Neukunden", True),
    ("Kundenkreis: Neukunden", True),
    ("Willkommenszins für 6 Monate", True),
    ("offre pour nouveaux clients", True),
    ("2,0 % auch für Bestandskunden", False),
    ("Neu- und Bestandskunden erhalten 2 %", False),
    ("Tagesgeld ohne Mindestanlage", False),
])
def test_neukunden_erkannt(text, erwartet):
    assert n.neukunden_erkannt(text) is erwartet


def test_chase_wird_zur_aktion():
    """Ende-zu-Ende: aus dem Block muss ein befristetes Angebot werden."""
    a = n.normalisiere(_roh(bank="Chase", zinssatz="4,0 %", folgezins_pct=2.0,
                            zinstyp=CHASE_BLOCK, aktionsdauer_monate=CHASE_BLOCK),
                       QUELLE, {})
    assert a["zinssatz_pct"] == pytest.approx(4.0)
    assert a["zinstyp"] == "aktion"
    assert a["aktionsdauer_monate"] == 4
    assert a["folgezins_pct"] == pytest.approx(2.0)
    assert a["nur_neukunden"] is True


def test_folgezins_ueber_aktionszins_ist_lesefehler():
    """Eine Aktion lockt mit mehr, nicht mit weniger."""
    a = n.normalisiere(_roh(zinssatz="3,20 %", folgezins_pct=3.75,
                            zinstyp="Aktionszins", aktionsdauer_monate="4 Monate"),
                       QUELLE, {})
    assert a["zinstyp"] == "variabel"
    assert a["aktionsdauer_monate"] == 0


def test_merge_uebernimmt_aktion_aus_zweitem_block():
    """Die Werbekachel darf den Datenblock nicht überstimmen."""
    kachel = n.normalisiere(_roh(bank="Chase", zinssatz="4,00 %"), QUELLE, {})
    block = n.normalisiere(_roh(bank="Chase", zinssatz="4,00 %", folgezins_pct=2.0,
                                zinstyp=CHASE_BLOCK, aktionsdauer_monate=CHASE_BLOCK),
                           QUELLE, {})
    assert kachel["zinstyp"] == "variabel"          # allein weiß sie nichts
    zusammen = n.merge([kachel, block])
    assert len(zusammen) == 1
    assert zusammen[0]["zinstyp"] == "aktion"
    assert zusammen[0]["aktionsdauer_monate"] == 4
    assert zusammen[0]["folgezins_pct"] == pytest.approx(2.0)
    assert zusammen[0]["nur_neukunden"] is True


def test_merge_meldet_folgezins_nicht_als_widerspruch():
    """4 % Aktion und 2 % Basis sind kein Quellenkonflikt."""
    haupt = n.normalisiere(_roh(bank="Chase", zinssatz="4,00 %", folgezins_pct=2.0,
                                zinstyp=CHASE_BLOCK, aktionsdauer_monate=CHASE_BLOCK),
                           QUELLE, {})
    andere = n.normalisiere(_roh(bank="Chase", zinssatz="2,00 %"),
                            {**QUELLE, "id": "zweite.de"}, {})
    zusammen = n.merge([haupt, andere])
    assert "quellen_abweichung" not in zusammen[0]


@pytest.mark.parametrize("roh,erwartet", [
    ("Ayvens Bank³", "Ayvens Bank"),
    ("Cosmos Direkt 8", "Cosmos Direkt"),
    ("Yapi Kredi Bank Deutschland 42", "Yapi Kredi Bank Deutschland"),
    ("Scalable Capital Bank²", "Scalable Capital Bank"),
    ("1822direkt", "1822direkt"),      # Ziffern im Wort bleiben
    ("N26", "N26"),
    ("Trade Republic", "Trade Republic"),
])
def test_fussnoten_am_banknamen(roh, erwartet):
    """Sonst zählt dieselbe Bank auf zwei Portalen als zwei Banken."""
    assert n.bank_normalisieren(roh) == erwartet


@pytest.mark.parametrize("roh,erwartet", [
    ("Nordax Bank (via Raisin)", "Nordax Bank"),
    ("Avida Finans über Raisin 4", "Avida Finans"),
    ("Klarna (via Raisin)", "Klarna"),
    ("Ferratum (Multitude Bank)", "Ferratum (Multitude Bank)"),  # keine Plattform
    ("Trade Republic", "Trade Republic"),
])
def test_plattform_zusatz_am_banknamen(roh, erwartet):
    """Sonst steht dieselbe Bank zweimal: direkt und über die Plattform."""
    assert n.bank_normalisieren(roh) == erwartet


def test_plattform_zusatz_vereint_dedupe_key():
    assert n.dedupe_key("Nordax Bank", "Tagesgeld", "SE") == \
           n.dedupe_key("Nordax Bank (via Raisin)", "Tagesgeld", "SE")


# ---------------------------------- Fußnotenziffer als Zins (v1.1)

@pytest.mark.parametrize("name,zins,ist_fussnote", [
    ("Cosmos Direkt 8", 8.0, True),
    ("Lea Bank über Raisin 6", 6.0, True),
    ("Cosmos Direkt 8", 2.2, False),      # richtiger Zins, Fußnote egal
    ("Trade Republic", 3.0, False),
    ("1822direkt", 3.5, False),
    ("N26", 26.0, False),                 # Ziffern im Wort, kein Leerzeichen
])
def test_fussnote_ist_zins(name, zins, ist_fussnote):
    assert n.fussnote_ist_zins(name, zins) is ist_fussnote


def test_treffer_mit_fussnoten_zins_wird_verworfen():
    """'Cosmos Direkt 8' mit 8,00 % ist Spalte 2 der Tabelle, kein Angebot."""
    assert n.normalisiere(_roh(bank="Cosmos Direkt 8", zinssatz="8,00 %"), QUELLE, {}) is None
    # Derselbe Name mit echtem Zins bleibt drin.
    a = n.normalisiere(_roh(bank="Cosmos Direkt 8", zinssatz="2,20 %"), QUELLE, {})
    assert a is not None and a["bank"] == "Cosmos Direkt"


@pytest.mark.parametrize("label", [
    "Rente en inleg Actierente", "Variabele rente", "Sparkonto", "Oprocentowanie",
])
def test_fremdsprachige_spaltenlabels_sind_keine_banken(label):
    assert n.bank_plausibel(label) is False


def test_altwert_ausreisser_fliegt_raus():
    """Ein Lesefehler von gestern darf nicht tagelang oben stehen."""
    angebote = [
        {"bank": "Revolut", "zinssatz_pct": 4.25, "stale": False},
        {"bank": "Chase", "zinssatz_pct": 4.0, "stale": False},
        {"bank": "Cosmos Direkt", "zinssatz_pct": 8.0, "stale": True},   # 1,9x
        {"bank": "Lea Bank", "zinssatz_pct": 6.0, "stale": True},        # 1,4x -> bleibt
    ]
    behalten, protokoll = n.altbestand_saeubern(angebote)
    namen = [a["bank"] for a in behalten]
    assert "Cosmos Direkt" not in namen
    assert "Lea Bank" in namen
    assert any("Ausreisser" in z for z in protokoll)


def test_ohne_frische_werte_wird_nichts_verworfen():
    """Fällt der ganze Lauf aus, bleibt der Altbestand vollständig."""
    angebote = [{"bank": "Chase", "zinssatz_pct": 9.0, "stale": True}]
    behalten, _ = n.altbestand_saeubern(angebote)
    assert len(behalten) == 1


def test_wortwiederholung_mit_praefix():
    """'1822 Direkt 1822direkt' – das zweite Vorkommen klebt zusammen."""
    assert n.bank_normalisieren("1822 Direkt 1822direkt") == "1822 Direkt"


# ------------------------------------- Aktion in sich stimmig (v1.1)

def test_aktion_konsistent_folgezins_hoeher():
    """Santander: 0,30 % 'Aktion' mit 3,01 % danach – das ist keine Aktion."""
    a = {"zinssatz_pct": 0.30, "folgezins_pct": 3.01, "zinstyp": "aktion",
         "aktionsdauer_monate": 4}
    n.aktion_konsistent(a)
    assert a["zinstyp"] == "variabel"
    assert a["aktionsdauer_monate"] == 0
    assert a["folgezins_pct"] == pytest.approx(0.30)


def test_aktion_konsistent_gleicher_folgezins():
    a = {"zinssatz_pct": 3.0, "folgezins_pct": 3.0, "zinstyp": "aktion",
         "aktionsdauer_monate": 6}
    n.aktion_konsistent(a)
    assert a["zinstyp"] == "variabel" and a["aktionsdauer_monate"] == 0


def test_aktion_konsistent_ohne_dauer():
    a = {"zinssatz_pct": 4.0, "folgezins_pct": 2.0, "zinstyp": "aktion",
         "aktionsdauer_monate": 0}
    n.aktion_konsistent(a)
    assert a["zinstyp"] == "variabel" and a["folgezins_pct"] == pytest.approx(4.0)


def test_aktion_konsistent_laesst_echte_aktion_stehen():
    a = {"zinssatz_pct": 4.0, "folgezins_pct": 2.0, "zinstyp": "aktion",
         "aktionsdauer_monate": 4}
    n.aktion_konsistent(a)
    assert a["zinstyp"] == "aktion"
    assert a["aktionsdauer_monate"] == 4
    assert a["folgezins_pct"] == pytest.approx(2.0)


def test_dauer_ohne_aktion_wird_geloescht():
    a = {"zinssatz_pct": 2.0, "folgezins_pct": 2.0, "zinstyp": "variabel",
         "aktionsdauer_monate": 6}
    n.aktion_konsistent(a)
    assert a["aktionsdauer_monate"] == 0


# ---------------------------- Produktkategorien und Produktnamen (v1.1)

@pytest.mark.parametrize("kategorie", [
    "Livret bancaire (non réglementé)",
    "Compte à terme",
    "Conto deposito",
    "Spaarrekening",
    "Livret",
])
def test_produktkategorie_ist_keine_bank(kategorie):
    """Rubriküberschriften standen mit 5,00 % ganz oben in der Liste."""
    assert n.bank_plausibel(kategorie) is False


@pytest.mark.parametrize("roh,erwartet", [
    ("DHB Bank NetSp@rkonto", "DHB Bank"),
    ("Ikano Bank Fleks Horten", "Ikano Bank"),
    ("Renault Bank direkt", "Renault Bank direkt"),   # ein Folgewort: bleibt
    ("Lea Bank AB", "Lea Bank AB"),
    ("Yapi Kredi Bank Deutschland", "Yapi Kredi Bank Deutschland"),
    # Diese dürfen NICHT gekürzt werden:
    ("Bank of Scotland", "Bank of Scotland"),
    ("Banca Progetto", "Banca Progetto"),
    ("Bank Norwegian", "Bank Norwegian"),
    ("Sparda-Bank München", "Sparda-Bank München"),
    ("Hamburg Direct Bank", "Hamburg Direct Bank"),
    ("Suresse Direkt Bank", "Suresse Direkt Bank"),
    ("Deutsche Skatbank", "Deutsche Skatbank"),
    ("Livret A", "Livret A"),
])
def test_produktname_hinter_bank_wird_abgeschnitten(roh, erwartet):
    assert n.bank_normalisieren(roh) == erwartet


def test_produktname_vereint_dedupe_key():
    assert n.dedupe_key("DHB Bank", "Tagesgeld", "DE") == \
           n.dedupe_key("DHB Bank NetSp@rkonto", "Tagesgeld", "DE")


# --------------------------- Dieselbe Bank in zwei Ländern (v1.1)

def _land_roh(bank, land, zins, land_quelle, stale=False, quellen=1):
    return {"bank": bank, "produkt": "Tagesgeld", "einlagensicherung_land": land,
            "land": land, "zinssatz_pct": zins, "land_quelle": land_quelle,
            "stale": stale, "quellen": [{"id": f"q{i}"} for i in range(quellen)],
            "quellen_anzahl": quellen}


def test_gleicher_zins_zwei_laender_wird_verschmolzen():
    """Nordax: Schweden (belegt) und Niederlande (geraten), beide 2,19 %."""
    behalten, _ = n.altbestand_saeubern([
        _land_roh("Nordax Bank", "SE", 2.19, "erkannt", quellen=3),
        _land_roh("Nordax Bank", "NL", 2.19, "quellenland_angenommen", stale=True),
    ])
    assert len(behalten) == 1
    assert behalten[0]["einlagensicherung_land"] == "SE"


def test_verschiedene_zinsen_bleiben_zwei_angebote():
    """ING Deutschland 3,75 % und ING Niederlande 1,25 % sind zwei Angebote."""
    behalten, _ = n.altbestand_saeubern([
        _land_roh("ING", "DE", 3.75, "quellenland_angenommen"),
        _land_roh("ING", "NL", 1.25, "quellenland_angenommen"),
    ])
    assert len(behalten) == 2


def test_beide_geraten_gleicher_zins_frischer_gewinnt():
    behalten, _ = n.altbestand_saeubern([
        _land_roh("Klarna", "NL", 3.0, "quellenland_angenommen", stale=True),
        _land_roh("Klarna", "DE", 3.0, "quellenland_angenommen", stale=False, quellen=2),
    ])
    assert len(behalten) == 1
    assert behalten[0]["einlagensicherung_land"] == "DE"
