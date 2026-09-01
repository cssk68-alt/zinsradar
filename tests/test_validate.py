"""Tests fuer die Plausibilitaetsregeln gegen Vortag und EZB."""

from datetime import date, timedelta

import pytest

import validate as v


def _angebot(bank="Testbank", zins=3.0, land="DE", **kw):
    a = {
        "bank": bank, "produkt": "Tagesgeld", "land": land,
        "einlagensicherung_land": land, "zinssatz_pct": zins,
        "dedupe_key": f"{bank.lower()}|tagesgeld|{land}",
        "quellen": [{"id": "test.de"}],
    }
    a.update(kw)
    return a


def _stand(angebote, datum=None):
    return {"stand_datum": datum or date.today().isoformat(),
            "angebote": [dict(a, stand=datum or date.today().isoformat()) for a in angebote]}


# ------------------------------------------------------- Regel: 0 Treffer

def test_null_treffer_behaelt_vortag():
    alt = _stand([_angebot(zins=3.0)])
    ergebnis, bericht = v.validiere([], alt, None)
    assert bericht["komplettausfall"] is True
    assert len(ergebnis) == 1
    assert ergebnis[0]["stale"] is True
    assert ergebnis[0]["zinssatz_pct"] == pytest.approx(3.0)


def test_null_treffer_ohne_vortag_bleibt_leer():
    ergebnis, bericht = v.validiere([], None, None)
    assert ergebnis == []
    assert bericht["komplettausfall"] is True


def test_zu_alter_stale_faellt_raus():
    lange_her = (date.today() - timedelta(days=40)).isoformat()
    alt = _stand([_angebot(stale_seit=lange_her)], datum=lange_her)
    ergebnis, bericht = v.validiere([], alt, None)
    assert ergebnis == []
    assert bericht["ausgelaufen_entfernt"]


# ------------------------------------------------------- Regel: Zins > 10 %

def test_zins_ueber_grenze_behaelt_alten_wert():
    alt = _stand([_angebot(zins=3.0)])
    ergebnis, bericht = v.validiere([_angebot(zins=25.0)], alt, None)
    assert ergebnis[0]["zinssatz_pct"] == pytest.approx(3.0)
    assert ergebnis[0]["stale"] is True
    assert bericht["zins_zu_hoch"][0]["wert"] == pytest.approx(25.0)


def test_zins_ueber_grenze_ohne_vortag_wird_verworfen():
    ergebnis, bericht = v.validiere([_angebot(zins=25.0), _angebot(bank="Gut", zins=3.0)], None, None)
    assert [a["bank"] for a in ergebnis] == ["Gut"]
    assert bericht["zins_zu_hoch"][0]["verworfen"] is True


# ------------------------------------------------------- Regel: Sprung > 2 pp

def test_grosser_sprung_behaelt_alten_wert():
    alt = _stand([_angebot(zins=1.0)])
    ergebnis, bericht = v.validiere([_angebot(zins=5.0)], alt, None)
    assert ergebnis[0]["zinssatz_pct"] == pytest.approx(1.0)
    assert ergebnis[0]["stale"] is True
    assert ergebnis[0]["verworfener_neuwert_pct"] == pytest.approx(5.0)
    assert bericht["sprung_zum_vortag"][0]["differenz_pp"] == pytest.approx(4.0)


def test_kleiner_sprung_wird_uebernommen():
    alt = _stand([_angebot(zins=3.0)])
    ergebnis, bericht = v.validiere([_angebot(zins=4.0)], alt, None)
    assert ergebnis[0]["zinssatz_pct"] == pytest.approx(4.0)
    assert ergebnis[0]["stale"] is False
    assert ergebnis[0]["veraenderung_pp"] == pytest.approx(1.0)
    assert not bericht["sprung_zum_vortag"]


def test_sprung_nach_unten_zaehlt_auch():
    alt = _stand([_angebot(zins=5.0)])
    ergebnis, _ = v.validiere([_angebot(zins=1.0)], alt, None)
    assert ergebnis[0]["zinssatz_pct"] == pytest.approx(5.0)


# ------------------------------------------------------- Regel: EZB-Abstand

def test_weit_ueber_ezb_wird_geflaggt():
    neu = _angebot(zins=5.0)
    neu["ezb_landesdurchschnitt_pct"] = 0.5
    neu["ezb_periode"] = "2026-06"
    ergebnis, bericht = v.validiere([neu], None, None)
    assert ergebnis[0]["flag"] == "pruefen"
    assert "EZB" in ergebnis[0]["flag_grund"]
    assert bericht["ezb_abweichung"][0]["differenz_pp"] == pytest.approx(4.5)


def test_nahe_am_ezb_kein_flag():
    neu = _angebot(zins=2.0)
    neu["ezb_landesdurchschnitt_pct"] = 0.5
    ergebnis, bericht = v.validiere([neu], None, None)
    assert "flag" not in ergebnis[0]
    assert not bericht["ezb_abweichung"]


# ------------------------------------------------------- Verschwundene

def test_verschwundenes_angebot_bleibt_stale():
    alt = _stand([_angebot(bank="Weg AG"), _angebot(bank="Bleibt AG")])
    ergebnis, bericht = v.validiere([_angebot(bank="Bleibt AG")], alt, None)
    banken = {a["bank"]: a for a in ergebnis}
    assert banken["Weg AG"]["stale"] is True
    assert banken["Bleibt AG"]["stale"] is False
    assert bericht["verschwunden_stale"][0]["bank"] == "Weg AG"


def test_unplausibler_altbestand_wird_nicht_konserviert():
    """Wenn der Namensfilter nachgeschaerft wurde, darf Muell nicht bleiben."""
    alt = _stand([_angebot(bank="Monate 1")])
    ergebnis, bericht = v.validiere([_angebot(bank="Echte Bank")], alt, None)
    assert [a["bank"] for a in ergebnis] == ["Echte Bank"]
    assert any("nicht plausibel" in str(x) for x in bericht["ausgelaufen_entfernt"])


def test_neue_angebote_werden_gemeldet():
    alt = _stand([_angebot(bank="Alt AG")])
    _, bericht = v.validiere([_angebot(bank="Alt AG"), _angebot(bank="Neu AG")], alt, None)
    assert bericht["neu_hinzugekommen"][0]["bank"] == "Neu AG"


# ------------------------------------------------------- Report

def test_report_wird_geschrieben(tmp_path):
    alt = _stand([_angebot(zins=1.0)])
    _, bericht = v.validiere([_angebot(zins=9.0)], alt, None)
    pfad = tmp_path / "report.md"
    text = v.report_schreiben(pfad, bericht, {
        "stand": "2026-09-01T06:00:00+00:00", "quellen_gesamt": 3, "quellen_erfolg": 2,
        "quellen_robots": 0, "quellen_leer": 1, "rohtreffer": 5, "angebote_dedupe": 1,
        "dauer_s": 12.3, "tier_verteilung": {"2": 1},
        "quellen_detail": [{"id": "a.de", "tier": 2, "methode": "css", "treffer": 1, "fehler": None}],
    })
    assert pfad.exists()
    assert "Sprung zum Vortag" in text
    assert "a.de" in text
