"""Tests fuer die Berechnung: brutto_12m, Quellensteuer, Risiko, Score."""

import pytest

import score as s


# ------------------------------------------------------------------ brutto_12m

def test_brutto_ohne_aktion():
    assert s.brutto_12m(3.0, 0, 3.0) == pytest.approx(3.0)


def test_brutto_mit_aktion():
    # 4 % für 6 Monate, danach 1 %  ->  (4*6 + 1*6)/12 = 2.5
    assert s.brutto_12m(4.0, 6, 1.0) == pytest.approx(2.5)


def test_brutto_aktion_laenger_als_ein_jahr_wird_gekappt():
    assert s.brutto_12m(4.0, 24, 1.0) == pytest.approx(4.0)


def test_brutto_ohne_folgezins_ist_konservativ():
    # Kein Folgezins bekannt -> 0 für die Restmonate
    assert s.brutto_12m(4.0, 6, None) == pytest.approx(2.0)


# ------------------------------------------------------------------ Rating

@pytest.mark.parametrize("rating,gruppe", [
    ("AAA", "AAA"), ("AA+", "AA"), ("AA", "AA"), ("AA-", "AA"),
    ("A+", "A"), ("A", "A"), ("A-", "A"),
    ("BBB+", "BBB"), ("BBB-", "BBB"), ("BB", "BB"), ("D", "D"),
    (None, ""), ("", ""),
])
def test_rating_gruppe(rating, gruppe):
    assert s.rating_gruppe(rating) == gruppe


@pytest.mark.parametrize("rating,abschlag", [
    ("AAA", 0.0), ("AA+", 0.05), ("A-", 0.10), ("BBB", 0.25),
    ("BB", 0.60), ("CCC", 0.60), (None, 0.60),
])
def test_risiko_abschlag(rating, abschlag):
    assert s.risiko_abschlag_pp(rating) == pytest.approx(abschlag)


# ------------------------------------------------------------------ Quellensteuer

QST = {
    "AT": {"land": "AT", "quellensteuer_standard_pct": 27.5, "quellensteuer_mit_dba_pct": 0.0,
           "rueckerstattung_aufwand": "niedrig"},
    "IT": {"land": "IT", "quellensteuer_standard_pct": 26.0, "quellensteuer_mit_dba_pct": 0.0,
           "rueckerstattung_aufwand": "hoch"},
    "PT": {"land": "PT", "quellensteuer_standard_pct": 28.0, "quellensteuer_mit_dba_pct": 10.0,
           "rueckerstattung_aufwand": "mittel"},
    "DE": {"land": "DE", "quellensteuer_standard_pct": 25.0, "quellensteuer_mit_dba_pct": 25.0,
           "rueckerstattung_aufwand": "keiner"},
}


def test_qst_niedriger_aufwand_mit_setting_null():
    wert, _ = s.qst_effektiv_pct("AT", QST, erstattung_selbst=True)
    assert wert == pytest.approx(0.0)


def test_qst_niedriger_aufwand_ohne_setting_dba_satz():
    wert, _ = s.qst_effektiv_pct("AT", QST, erstattung_selbst=False)
    assert wert == pytest.approx(0.0)   # AT hat mit DBA ohnehin 0 %


def test_qst_hoher_aufwand_ignoriert_setting():
    mit, _ = s.qst_effektiv_pct("PT", QST, erstattung_selbst=True)
    ohne, _ = s.qst_effektiv_pct("PT", QST, erstattung_selbst=False)
    assert mit == pytest.approx(10.0)
    assert ohne == pytest.approx(10.0)


def test_inlandsfall_de_ohne_quellensteuer():
    """Die 25 % für DE sind die Abgeltungssteuer - die gehoert nicht in den Score."""
    mit, grund = s.qst_effektiv_pct("DE", QST, erstattung_selbst=True)
    ohne, _ = s.qst_effektiv_pct("DE", QST, erstattung_selbst=False)
    assert mit == pytest.approx(0.0)
    assert ohne == pytest.approx(0.0)
    assert "Abgeltungssteuer" in grund


def test_unbekanntes_land_ohne_abzug():
    wert, _ = s.qst_effektiv_pct("XX", QST, erstattung_selbst=True)
    assert wert == pytest.approx(0.0)


# ------------------------------------------------------------------ Gesamt

LAENDER = {
    "IT": {"land": "IT", "staatsrating_sp": "BBB", "einlagensicherung_betrag_eur": 100000,
           "waehrung": "EUR", "sicherungssystem_name": "FITD"},
    "DE": {"land": "DE", "staatsrating_sp": "AAA", "einlagensicherung_betrag_eur": 100000,
           "waehrung": "EUR", "sicherungssystem_name": "EdB"},
}


def _angebot(**kw):
    basis = {"bank": "Testbank", "produkt": "Tagesgeld", "einlagensicherung_land": "IT",
             "land": "IT", "zinssatz_pct": 4.0, "aktionsdauer_monate": 0,
             "folgezins_pct": 4.0, "waehrung": "EUR"}
    basis.update(kw)
    return basis


def test_berechne_kompletter_pfad():
    a = s.berechne(_angebot(), QST, LAENDER, None)
    assert a["brutto_12m_pct"] == pytest.approx(4.0)
    # IT: Aufwand "hoch" -> Setting wirkt nicht, mit DBA 0 %
    assert a["qst_effektiv_mit_erstattung_pct"] == pytest.approx(0.0)
    assert a["netto_12m_mit_erstattung_pct"] == pytest.approx(4.0)
    # BBB -> 0.25 pp Abschlag
    assert a["score_mit_erstattung"] == pytest.approx(3.75)
    assert a["risiko_abschlag_pp"] == pytest.approx(0.25)


def test_berechne_aktion_und_score():
    a = s.berechne(_angebot(zinssatz_pct=5.0, aktionsdauer_monate=6, folgezins_pct=1.0),
                   QST, LAENDER, None)
    assert a["brutto_12m_pct"] == pytest.approx(3.0)
    assert a["score_mit_erstattung"] == pytest.approx(3.0 - 0.25)


def test_beide_varianten_werden_geliefert():
    a = s.berechne(_angebot(einlagensicherung_land="PT", land="PT"), QST,
                   {"PT": {"staatsrating_sp": "A-"}}, None)
    assert a["qst_effektiv_mit_erstattung_pct"] == pytest.approx(10.0)
    assert a["netto_12m_mit_erstattung_pct"] == pytest.approx(4.0 * 0.9)
    assert "netto_12m_ohne_erstattung_pct" in a
    assert a["score_mit_erstattung"] == pytest.approx(4.0 * 0.9 - 0.10)


def test_abgeltungssteuer_nur_anzeige():
    """Sie darf im Score nicht auftauchen, nur im Anzeigefeld."""
    a = s.berechne(_angebot(einlagensicherung_land="DE", land="DE"), QST, LAENDER, None)
    assert a["score_mit_erstattung"] == pytest.approx(4.0)   # AAA -> 0 Abschlag
    assert a["netto_nach_abgeltungssteuer_mit_erstattung_pct"] < a["netto_12m_mit_erstattung_pct"]


def test_fehlender_folgezins_wird_aus_ezb_geschaetzt():
    referenz = {"ezb_mir": {"IT": {"wert_pct": 0.8, "periode": "2026-06"}}}
    a = s.berechne(_angebot(aktionsdauer_monate=6, folgezins_pct=None), QST, LAENDER, referenz)
    assert a["folgezins_geschaetzt"] is True
    assert a["folgezins_pct"] == pytest.approx(0.8)
    assert a["brutto_12m_pct"] == pytest.approx((4.0 * 6 + 0.8 * 6) / 12)


def test_ezb_abstand_wird_berechnet():
    referenz = {"ezb_mir": {"IT": {"wert_pct": 0.5, "periode": "2026-06"}}}
    a = s.berechne(_angebot(), QST, LAENDER, referenz)
    assert a["differenz_zu_ezb_pp"] == pytest.approx(3.5)
    assert a["ezb_periode"] == "2026-06"


def test_sortierung_nach_score():
    angebote = [_angebot(bank="A", zinssatz_pct=2.0, folgezins_pct=2.0),
                _angebot(bank="B", zinssatz_pct=5.0, folgezins_pct=5.0)]
    ergebnis = s.berechne_alle(angebote, None)
    assert ergebnis[0]["bank"] == "B"
