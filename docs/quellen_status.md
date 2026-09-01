# Quellen-Status

Erzeugt: 2026-09-01T20:35:58+00:00 | HTML-Parser: lexbor

Erzeugt von `python scraper/bootstrap.py`. Dieser Bericht sagt, welche
Angaben aus `sources.yaml` der Realitaet standhalten. Die Selektoren dort
stammen aus einer LLM-Recherche und sind ungeprueft - hier steht das Ergebnis
der Pruefung.

| Bewertung | Anzahl | Bedeutung |
| --- | ---: | --- |
| gut | 0 | Stufe 1 oder konfigurierte Selektoren greifen |
| notduerftig | 13 | Nur Heuristik oder LLM liefert etwas |
| kaputt | 6 | Keine Stufe liefert Daten |
| gesperrt | 3 | robots.txt verbietet den Abruf |

## Uebersicht

| Quelle | Land | HTTP | robots | Container | Felder OK | Heuristik | Greift |
| --- | :-: | :-: | :-: | ---: | :-: | ---: | --- |
| weltsparen.de | DE | 200 | ja | 0 | 0/8 | 4 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| check24.de | DE | 200 | ja | 0 | 0/8 | 3 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| biallo.de | DE | 200 | ja | 0 | 0/8 | 8 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| finanzfluss.de | DE | 200 | ja | 0 | 0/8 | 53 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| durchblicker.at | AT | 200 | ja | 0 | 0/8 | 2 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| bankenrechner.at | AT | 200 | ja | 0 | 0/8 | 0 | KEINE Stufe greift |
| sparente.nl | NL | - | NEIN | - | 0/0 | - | Quelle wird im Lauf uebersprungen |
| raisin.nl | NL | 200 | ja | 0 | 0/8 | 10 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| moneyvox.fr | FR | 200 | ja | 0 | 0/8 | 20 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| raisin.fr | FR | 200 | ja | 0 | 0/8 | 7 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| confrontaconti.it | IT | 403 | ja | - | 0/0 | - | URL pruefen / ersetzen |
| tucapital.es | ES | 200 | ja | 0 | 0/8 | 0 | KEINE Stufe greift |
| bankier.pl | PL | 200 | ja | 0 | 0/8 | 8 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| compracer.se | SE | - | NEIN | - | 0/0 | - | Quelle wird im Lauf uebersprungen |
| bankinter.pt | PT | 403 | ja | - | 0/0 | - | URL pruefen / ersetzen |
| ing.de | DE | 200 | ja | 0 | 3/8 | 2 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| consorsbank.de | DE | 200 | ja | 0 | 3/8 | 1 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| comdirect.de | DE | 404 | ja | - | 0/0 | - | URL pruefen / ersetzen |
| trade-republic.com | DE | - | NEIN | - | 0/0 | - | Quelle wird im Lauf uebersprungen |
| santander.de | DE | 200 | ja | 0 | 3/8 | 2 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |
| openbank.de | ES | 200 | ja | 0 | 4/8 | 0 | KEINE Stufe greift |
| klarna.com | SE | 200 | ja | 0 | 4/8 | 8 | Stufe 2b (Heuristik, ohne YAML-Selektoren) |

## URLs mit Problem (404 / 403 / nicht erreichbar)

- `sparente.nl` -> https://www.sparente.nl/sparen/vrij-opneembaar : **HTTP None**
- `confrontaconti.it` -> https://www.confrontaconti.it/conti-deposito/ : **Seite nicht abrufbar: HTTP 403**
- `compracer.se` -> https://www.compracer.se/spara/sparkonto/ : **HTTP None**
- `bankinter.pt` -> https://www.bankinter.pt/poupanca/contas-remuneradas : **Seite nicht abrufbar: HTTP 403**
- `comdirect.de` -> https://www.comdirect.de/konto/tagesgeldkonto.html : **Seite nicht abrufbar: HTTP 404**
- `trade-republic.com` -> https://trade-republic.com/de-de/zinsen : **HTTP None**

## container_selector ohne Treffer

- `weltsparen.de`: `div.product-card-container, div[data-testid='product-card']`
- `check24.de`: `tr.c24-comparison-row, div.c24-product-row`
- `biallo.de`: `table.b-table--comparison tbody tr`
- `finanzfluss.de`: `div.table-row, div.product-card`
- `durchblicker.at`: `div.result-card, tr.result-row`
- `bankenrechner.at`: `table#sparzinsen-tabelle tbody tr`
- `raisin.nl`: `div.product-card`
- `moneyvox.fr`: `div.tableau-offres table tbody tr`
- `raisin.fr`: `div.product-item`
- `tucapital.es`: `table.tablacomparativa tbody tr`
- `bankier.pl`: `table.boxTable tbody tr`
- `ing.de`: `section.product-hero, div.ib-content-box`
- `consorsbank.de`: `div.stage-content, div.price-box`
- `santander.de`: `div.product-detail-stage`
- `openbank.de`: `div.hero-banner, div.product-card`
- `klarna.com`: `div[data-testid='savings-rate-card']`

## Details je Quelle

### weltsparen.de  (notduerftig)

- URL: https://www.weltsparen.de/tagesgeld/
- Land/Typ/Rendering: DE / plattform / js_required (gerendert)
- robots.txt live: **erlaubt** (keine robots.txt (HTTP 404))
- YAML behauptet robots: `ja`
- HTTP: 200 , 674575 Zeichen, 4.3s
- json_endpoint: 0 Treffer - HTTP 404
- JSON-LD: 0 Treffer (3 ld+json-Block(s), 1 Kandidat(en))
- container_selector `div.product-card-container, div[data-testid='product-card']`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 4 Angebote ueber Struktur 'tr.? (Tiefe 19, 4x)'
    - Monate 1–3 - 0.5 %
    - Monate 4–6 - 0.5 %
    - Monate 7–9 - 0.5 %
    - Monate 10–12 - 0.5 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `.bank-name, [data-testid='bank-name']` | 0 Treffer |  |
| zinssatz | `.interest-rate, [data-testid='interest-rate']` | 0 Treffer |  |
| zinstyp | `.rate-type` | 0 Treffer |  |
| aktionsdauer_monate | `.bonus-duration` | 0 Treffer |  |
| folgezins | `.standard-rate` | 0 Treffer |  |
| mindestanlage | `.min-deposit` | 0 Treffer |  |
| hoechstanlage | `.max-deposit` | 0 Treffer |  |
| einlagensicherung_land | `.deposit-protection-country` | 0 Treffer |  |

**Probleme:**

- json_endpoint unbrauchbar: HTTP 404
- container_selector trifft nichts: div.product-card-container, div[data-testid='product-card']
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Dynamisches SPA-Rendering via Next.js; API-Endpoints nutzen Cloudflare-Bot-Protection.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### check24.de  (notduerftig)

- URL: https://www.check24.de/tagesgeld/
- Land/Typ/Rendering: DE / portal / js_required (gerendert)
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `teilweise`
- HTTP: 200 , 622315 Zeichen, 3.2s
- json_endpoint: 0 Treffer - robots.txt: robots.txt verbietet diesen Pfad
- JSON-LD: 0 Treffer (7 ld+json-Block(s), 1 Kandidat(en))
- container_selector `tr.c24-comparison-row, div.c24-product-row`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 3 Angebote ueber Struktur 'div.accordionList.jsWidget (Tiefe 8, 4x)'
    - 24.08.2026: Zinserhöhung IGG Bank Tagesgeld: jetzt - 2.28 %
    - 22.06.2026: Zinserhöhung BBBank Tagesgeld: jetzt - 3.03 %
    - 29.05.2026: Zinserhöhung TF Bank Tagesgeld: jetzt - 3.3 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `.c24-bank-name` | 0 Treffer |  |
| zinssatz | `.c24-interest-value` | 0 Treffer |  |
| zinstyp | `.c24-rate-type` | 0 Treffer |  |
| aktionsdauer_monate | `.c24-promo-months` | 0 Treffer |  |
| folgezins | `.c24-follow-rate` | 0 Treffer |  |
| mindestanlage | `.c24-min-amount` | 0 Treffer |  |
| hoechstanlage | `.c24-max-amount` | 0 Treffer |  |
| einlagensicherung_land | `.c24-country-flag` | 0 Treffer |  |

**Probleme:**

- json_endpoint unbrauchbar: robots.txt: robots.txt verbietet diesen Pfad
- container_selector trifft nichts: tr.c24-comparison-row, div.c24-product-row
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Strenge Akamai/DataDome Captchas; Selektoren aendern sich bei A/B-Tests haeufig.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### biallo.de  (notduerftig)

- URL: https://www.biallo.de/tagesgeld/
- Land/Typ/Rendering: DE / portal / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 149534 Zeichen, 2.0s
- JSON-LD: 0 Treffer (2 ld+json-Block(s), 0 Kandidat(en))
- container_selector `table.b-table--comparison tbody tr`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 8 Angebote ueber Struktur 'div auf Tiefe 10 (9x)'
    - DHB Bank DHB NetSp@rkonto - 3.4 %
    - S&P Länderrating AAA Niederlande - 3.4 %
    - Chase Tagesgeld - 4.0 %
    - S&P Länderrating AAA Deutschland - 4.0 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `td.b-table__cell--bank span.b-bank-name` | 0 Treffer |  |
| zinssatz | `td.b-table__cell--interest span.b-rate` | 0 Treffer |  |
| zinstyp | `td.b-table__cell--details .b-badge` | 0 Treffer |  |
| aktionsdauer_monate | `td.b-table__cell--details .b-promo-duration` | 0 Treffer |  |
| folgezins | `td.b-table__cell--details .b-base-rate` | 0 Treffer |  |
| mindestanlage | `td.b-table__cell--min` | 0 Treffer |  |
| hoechstanlage | `td.b-table__cell--max` | 0 Treffer |  |
| einlagensicherung_land | `td.b-table__cell--country img` | 0 Treffer |  |

**Probleme:**

- container_selector trifft nichts: table.b-table--comparison tbody tr
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Mischung aus redaktionellen Empfehlungen und Werbelinks; Tabellenstruktur variiert mobilspezifisch.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### finanzfluss.de  (notduerftig)

- URL: https://www.finanzfluss.de/vergleich/tagesgeld/
- Land/Typ/Rendering: DE / portal / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 5683102 Zeichen, 2.0s
- JSON-LD: 0 Treffer (1 ld+json-Block(s), 0 Kandidat(en))
- container_selector `div.table-row, div.product-card`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 53 Angebote ueber Struktur 'div auf Tiefe 15 (54x)'
    - Revolut - 4.25 %
    - Chase - 4.0 %
    - Chase - 2.0 %
    - Ikano Bank - 3.91 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `.provider-name` | 0 Treffer |  |
| zinssatz | `.interest-rate-value` | 0 Treffer |  |
| zinstyp | `.rate-badge` | 0 Treffer |  |
| aktionsdauer_monate | `.guarantee-period` | 0 Treffer |  |
| folgezins | `.sub-rate-info` | 0 Treffer |  |
| mindestanlage | `.min-investment` | 0 Treffer |  |
| hoechstanlage | `.max-investment` | 0 Treffer |  |
| einlagensicherung_land | `.country-info` | 0 Treffer |  |

**Probleme:**

- container_selector trifft nichts: div.table-row, div.product-card
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Static HTML wird via SSG erzeugt; Zinssaetze enthalten oft Zusatztext wie 'p.a.' im selben Tag.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### durchblicker.at  (notduerftig)

- URL: https://durchblicker.at/sparzinsen
- Land/Typ/Rendering: AT / portal / js_required (gerendert)
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 416745 Zeichen, 3.7s
- json_endpoint: 0 Treffer - HTTP 404
- JSON-LD: 0 Treffer (4 ld+json-Block(s), 0 Kandidat(en))
- container_selector `div.result-card, tr.result-row`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 2 Angebote ueber Struktur 'div auf Tiefe 8 (2x)'
    - sparzinsen 12. August 2026 - 3.0 %
    - Bundesschatz 2026: Zinsen, Steuern & Festgeld-Vergleich - 3.1 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `.bank-title` | 0 Treffer |  |
| zinssatz | `.rate-percentage` | 0 Treffer |  |
| zinstyp | `.rate-type-description` | 0 Treffer |  |
| aktionsdauer_monate | `.bonus-period-info` | 0 Treffer |  |
| folgezins | `.sub-rate` | 0 Treffer |  |
| mindestanlage | `.min-amount-info` | 0 Treffer |  |
| hoechstanlage | `.max-amount-info` | 0 Treffer |  |
| einlagensicherung_land | `.guarantee-country` | 0 Treffer |  |

**Probleme:**

- json_endpoint unbrauchbar: HTTP 404
- container_selector trifft nichts: div.result-card, tr.result-row
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Erfordert Initialisierung von Session-Cookies via POST-Request vor Abruf.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### bankenrechner.at  (kaputt)

- URL: https://www.bankenrechner.at/sparzinsen
- Land/Typ/Rendering: AT / portal / static_html
- robots.txt live: **erlaubt** (keine robots.txt (HTTP 404))
- YAML behauptet robots: `ja`
- HTTP: 200 , 15682 Zeichen, 1.9s
- JSON-LD: 0 Treffer (kein <script type=application/ld+json> gefunden)
- container_selector `table#sparzinsen-tabelle tbody tr`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 0 Angebote - keine wiederkehrende Struktur mit Zins gefunden
- Fliesstext fuer LLM: 1233 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `td.bank-name` | 0 Treffer |  |
| zinssatz | `td.zins-wert` | 0 Treffer |  |
| zinstyp | `td.zins-art` | 0 Treffer |  |
| aktionsdauer_monate | `td.aktions-dauer` | 0 Treffer |  |
| folgezins | `td.folge-zins` | 0 Treffer |  |
| mindestanlage | `td.mindest-betrag` | 0 Treffer |  |
| hoechstanlage | `td.hoechst-betrag` | 0 Treffer |  |
| einlagensicherung_land | `td.sicherung-land` | 0 Treffer |  |

**Probleme:**

- container_selector trifft nichts: table#sparzinsen-tabelle tbody tr
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Offizielles Portal der Arbeiterkammer; sehr stabiles HTML, aber unregelmaessige Update-Zyklen.

**Greift:** KEINE Stufe greift

---

### sparente.nl  (gesperrt)

- URL: https://www.sparente.nl/sparen/vrij-opneembaar
- Land/Typ/Rendering: NL / portal / static_html
- robots.txt live: **VERBOTEN** (robots.txt nicht erreichbar: ConnectError)
- YAML behauptet robots: `ja`
- HTTP: None , 0 Zeichen, 0s
- Fliesstext fuer LLM: 0 Zeichen

**Probleme:**

- robots.txt verbietet den Abruf (robots.txt nicht erreichbar: ConnectError)

> Notiz aus sources.yaml: GEPRUEFT 01.09.2026: Domain nicht erreichbar (DNS/Verbindung) - vermutlich eingestellt. Niederlaendische Begrifflichkeiten ('Vrij opneembaar'); Punkttrennung bei Dezimalzahlen beachten.

**Greift:** Quelle wird im Lauf uebersprungen

---

### raisin.nl  (notduerftig)

- URL: https://www.raisin.nl/spaarrekening/
- Land/Typ/Rendering: NL / plattform / js_required (gerendert)
- robots.txt live: **erlaubt** (keine robots.txt (HTTP 404))
- YAML behauptet robots: `ja`
- HTTP: 200 , 498878 Zeichen, 6.1s
- json_endpoint: 0 Treffer - HTTP 404
- JSON-LD: 0 Treffer (2 ld+json-Block(s), 1 Kandidat(en))
- container_selector `div.product-card`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 10 Angebote ueber Struktur 'div.styles-module_innerContainer__rTA-g (Tiefe 16, 10x)'
    - Raisin RenteBoost - 3.05 %
    - Avarda Bank - 2.2 %
    - BW-Bank - 2.2 %
    - EuroExtra - 2.2 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `.bank-name` | 0 Treffer |  |
| zinssatz | `.interest-rate` | 0 Treffer |  |
| zinstyp | `.rate-type` | 0 Treffer |  |
| aktionsdauer_monate | `.action-months` | 0 Treffer |  |
| folgezins | `.follow-rate` | 0 Treffer |  |
| mindestanlage | `.min-deposit` | 0 Treffer |  |
| hoechstanlage | `.max-deposit` | 0 Treffer |  |
| einlagensicherung_land | `.deposit-protection` | 0 Treffer |  |

**Probleme:**

- json_endpoint unbrauchbar: HTTP 404
- container_selector trifft nichts: div.product-card
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Produktangebot weicht von der deutschen Raisin/WeltSparen-Plattform ab.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### moneyvox.fr  (notduerftig)

- URL: https://www.moneyvox.fr/livret/comparatif/
- Land/Typ/Rendering: FR / portal / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 151416 Zeichen, 2.1s
- JSON-LD: 0 Treffer (1 ld+json-Block(s), 1 Kandidat(en))
- container_selector `div.tableau-offres table tbody tr`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 20 Angebote ueber Struktur 'tr.? (Tiefe 11, 20x)'
    - Livret A - 1.7 %
    - LDDS - 1.7 %
    - Livret Jeune minimum - 1.7 %
    - LEP - 2.5 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `td.col-banque img.logo` | 0 Treffer |  |
| zinssatz | `td.col-taux span.taux-actuel` | 0 Treffer |  |
| zinstyp | `td.col-taux span.badge-promo` | 0 Treffer |  |
| aktionsdauer_monate | `td.col-conditions .duree-promo` | 0 Treffer |  |
| folgezins | `td.col-conditions .taux-de-base` | 0 Treffer |  |
| mindestanlage | `td.col-montant .min` | 0 Treffer |  |
| hoechstanlage | `td.col-montant .max` | 0 Treffer |  |
| einlagensicherung_land | `td.col-garantie` | 0 Treffer |  |

**Probleme:**

- container_selector trifft nichts: div.tableau-offres table tbody tr
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Strikte Unterscheidung zwischen 'Livret A / LDD' (reguliert) und 'Livrets bancaires' (frei).

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### raisin.fr  (notduerftig)

- URL: https://www.raisin.fr/livret-epargne/
- Land/Typ/Rendering: FR / plattform / js_required (gerendert)
- robots.txt live: **erlaubt** (keine robots.txt (HTTP 404))
- YAML behauptet robots: `ja`
- HTTP: 200 , 528171 Zeichen, 5.3s
- json_endpoint: 0 Treffer - HTTP 404
- JSON-LD: 0 Treffer (4 ld+json-Block(s), 1 Kandidat(en))
- container_selector `div.product-item`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 7 Angebote ueber Struktur 'div.styles-module_innerContainer__rTA-g (Tiefe 16, 7x)'
    - Lea Bank AB - 2.19 %
    - EuroExtra - 2.02 %
    - Morrow Bank AB - 2.02 %
    - Klarna Bank AB - 1.81 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `.bank-name` | 0 Treffer |  |
| zinssatz | `.rate-value` | 0 Treffer |  |
| zinstyp | `.rate-label` | 0 Treffer |  |
| aktionsdauer_monate | `.bonus-duration` | 0 Treffer |  |
| folgezins | `.standard-rate` | 0 Treffer |  |
| mindestanlage | `.min-amount` | 0 Treffer |  |
| hoechstanlage | `.max-amount` | 0 Treffer |  |
| einlagensicherung_land | `.guarantee-country` | 0 Treffer |  |

**Probleme:**

- json_endpoint unbrauchbar: HTTP 404
- container_selector trifft nichts: div.product-item
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Fokus in Frankreich primaer auf Festgeld (Comptes a terme), Tagesgeld (Comptes epargne) seltener.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### confrontaconti.it  (kaputt)

- URL: https://www.confrontaconti.it/conti-deposito/
- Land/Typ/Rendering: IT / portal / js_required (gerendert)
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 403 , 1497 Zeichen, 3.8s
- Fliesstext fuer LLM: 0 Zeichen

**Probleme:**

- Seite nicht abrufbar: HTTP 403

> Notiz aus sources.yaml: GEPRUEFT 01.09.2026: HTTP 403. Italienische Angabe unterscheidet strikt zwischen Tasso Lordo (Brutto) und Tasso Netto (Netto nach 26% QSt).

**Greift:** URL pruefen / ersetzen

---

### tucapital.es  (kaputt)

- URL: https://www.tucapital.es/cuentas/mejores-cuentas-remuneradas/
- Land/Typ/Rendering: ES / portal / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 57683 Zeichen, 1.9s
- JSON-LD: 0 Treffer (1 ld+json-Block(s), 0 Kandidat(en))
- container_selector `table.tablacomparativa tbody tr`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 0 Angebote - keine wiederkehrende Struktur mit Zins gefunden
- Fliesstext fuer LLM: 1807 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `td.col_banco` | 0 Treffer |  |
| zinssatz | `td.col_interes` | 0 Treffer |  |
| zinstyp | `td.col_tipo` | 0 Treffer |  |
| aktionsdauer_monate | `td.col_promocion` | 0 Treffer |  |
| folgezins | `td.col_interes_base` | 0 Treffer |  |
| mindestanlage | `td.col_minimo` | 0 Treffer |  |
| hoechstanlage | `td.col_maximo` | 0 Treffer |  |
| einlagensicherung_land | `td.col_fgd` | 0 Treffer |  |

**Probleme:**

- container_selector trifft nichts: table.tablacomparativa tbody tr
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Sehr einfache HTML-Struktur, jedoch oft unregelmaessige Formatierung von Prozentzahlen.

**Greift:** KEINE Stufe greift

---

### bankier.pl  (notduerftig)

- URL: https://www.bankier.pl/gospodarka/wskazniki-finansowe/lokaty-i-konta-oszczednosciowe
- Land/Typ/Rendering: PL / portal / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 516353 Zeichen, 2.0s
- JSON-LD: 0 Treffer (kein <script type=application/ld+json> gefunden)
- container_selector `table.boxTable tbody tr`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 8 Angebote ueber Struktur 'li auf Tiefe 10 (8x)'
    - Wykres notowania wig20 - 0.47 %
    - Wykres notowania wig - 0.53 %
    - Wykres notowania mwig40 - 0.71 %
    - Wykres notowania swig80 - 0.39 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `td.colBank` | 0 Treffer |  |
| zinssatz | `td.colOprocentowanie` | 0 Treffer |  |
| zinstyp | `td.colTyp` | 0 Treffer |  |
| aktionsdauer_monate | `td.colOkres` | 0 Treffer |  |
| folgezins | `td.colOprocentowanieBaza` | 0 Treffer |  |
| mindestanlage | `td.colKwotaMin` | 0 Treffer |  |
| hoechstanlage | `td.colKwotaMax` | 0 Treffer |  |
| einlagensicherung_land | `td.colGwarancja` | 0 Treffer |  |

**Probleme:**

- container_selector trifft nichts: table.boxTable tbody tr
- Feldselektoren ohne Treffer: bank, zinssatz, zinstyp, aktionsdauer_monate, folgezins, mindestanlage, hoechstanlage, einlagensicherung_land

> Notiz aus sources.yaml: Zinsen in PLN (Zloty); Umrechnung und Waehrungsrisiko beachten. QSt ('Belka-Steuer') 19%.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### compracer.se  (gesperrt)

- URL: https://www.compracer.se/spara/sparkonto/
- Land/Typ/Rendering: SE / portal / js_required
- robots.txt live: **VERBOTEN** (robots.txt nicht erreichbar: ConnectError)
- YAML behauptet robots: `ja`
- HTTP: None , 0 Zeichen, 0s
- Fliesstext fuer LLM: 0 Zeichen

**Probleme:**

- robots.txt verbietet den Abruf (robots.txt nicht erreichbar: ConnectError)

> Notiz aus sources.yaml: GEPRUEFT 01.09.2026: Domain nicht erreichbar. Unterscheidung zwischen Konten mit staatlicher Einlagensicherung (Insaettningsgarantin) und ungesicherten Hochzinskonten.

**Greift:** Quelle wird im Lauf uebersprungen

---

### bankinter.pt  (kaputt)

- URL: https://www.bankinter.pt/poupanca/contas-remuneradas
- Land/Typ/Rendering: PT / bank / static_html
- robots.txt live: **erlaubt** (keine robots.txt (HTTP 403))
- YAML behauptet robots: `ja`
- HTTP: 403 , 5748 Zeichen, 2.0s
- Fliesstext fuer LLM: 0 Zeichen

**Probleme:**

- Seite nicht abrufbar: HTTP 403

> Notiz aus sources.yaml: GEPRUEFT 01.09.2026: HTTP 403 auf der Produktseite. Verwendung der Begriffe TANB (Taxa Anual Nominal Bruta) und TANL (Netto). URL im Anhang enthielt ein kyrillisch/akzentuiertes 'poupanca' - hier ASCII-normalisiert, bootstrap.py prueft die Erreichbarkeit.

**Greift:** URL pruefen / ersetzen

---

### ing.de  (notduerftig)

- URL: https://www.ing.de/sparen-anlegen/sparen/tagesgeld/
- Land/Typ/Rendering: DE / bank / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 82518 Zeichen, 2.0s
- JSON-LD: 0 Treffer (2 ld+json-Block(s), 0 Kandidat(en))
- container_selector `section.product-hero, div.ib-content-box`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 2 Angebote ueber Struktur 'div.ingde-font-300.intro__checkmarks-list-right (Tiefe 12, 2x)'
    - ING Deutschland - 3.2 %
    - ING Deutschland - 3.75 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `literal:'ING Deutschland'` | literal | ING Deutschland |
| zinssatz | `.ib-headline--hero span.highlight, .interest-rate` | 0 Treffer |  |
| zinstyp | `.interest-label` | 0 Treffer |  |
| aktionsdauer_monate | `.promo-duration` | 0 Treffer |  |
| folgezins | `.base-rate` | 0 Treffer |  |
| mindestanlage | `literal:'0 EUR'` | literal | 0 EUR |
| hoechstanlage | `.max-amount-info` | 0 Treffer |  |
| einlagensicherung_land | `literal:'DE'` | literal | DE |

**Probleme:**

- container_selector trifft nichts: section.product-hero, div.ib-content-box
- Feldselektoren ohne Treffer: zinssatz, zinstyp, aktionsdauer_monate, folgezins, hoechstanlage

> Notiz aus sources.yaml: Zinssatz steht oft mitten im Fliesstext oder grossem Hero-Header; Parsing via RegEx noetig.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### consorsbank.de  (notduerftig)

- URL: https://www.consorsbank.de/ev/Sparen-Anlegen/Sparen/Tagesgeld
- Land/Typ/Rendering: DE / bank / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 41566 Zeichen, 2.0s
- JSON-LD: 0 Treffer (kein <script type=application/ld+json> gefunden)
- container_selector `div.stage-content, div.price-box`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 1 Angebote ueber Struktur 'div auf Tiefe 4 (2x)'
    - Consorsbank - 3.6 %
- Fliesstext fuer LLM: 8000 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `literal:'Consorsbank'` | literal | Consorsbank |
| zinssatz | `span.price-tag, div.rate-display` | 0 Treffer |  |
| zinstyp | `span.rate-type` | 0 Treffer |  |
| aktionsdauer_monate | `span.duration` | 0 Treffer |  |
| folgezins | `span.standard-rate` | 0 Treffer |  |
| mindestanlage | `literal:'0 EUR'` | literal | 0 EUR |
| hoechstanlage | `span.max-deposit` | 0 Treffer |  |
| einlagensicherung_land | `literal:'FR'` | literal | FR |

**Probleme:**

- container_selector trifft nichts: div.stage-content, div.price-box
- Feldselektoren ohne Treffer: zinssatz, zinstyp, aktionsdauer_monate, folgezins, hoechstanlage

> Notiz aus sources.yaml: Consorsbank gehoert zur BNP Paribas; Einlagensicherung ist nominell Frankreich (FGDR). ANNAHME AUS DER RECHERCHE - ungeprueft, siehe README.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### comdirect.de  (kaputt)

- URL: https://www.comdirect.de/konto/tagesgeldkonto.html
- Land/Typ/Rendering: DE / bank / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 404 , 1229735 Zeichen, 2.1s
- Fliesstext fuer LLM: 0 Zeichen

**Probleme:**

- Seite nicht abrufbar: HTTP 404

> Notiz aus sources.yaml: GEPRUEFT 01.09.2026: HTTP 401, Bot-Schutz blockt. Aktionszinssaetze gelten oft nur fuer Neukunden oder bei gleichzeitigem Depotuebertrag.

**Greift:** URL pruefen / ersetzen

---

### trade-republic.com  (gesperrt)

- URL: https://trade-republic.com/de-de/zinsen
- Land/Typ/Rendering: DE / bank / js_required
- robots.txt live: **VERBOTEN** (robots.txt nicht erreichbar: ConnectError)
- YAML behauptet robots: `ja`
- HTTP: None , 0 Zeichen, 0s
- Fliesstext fuer LLM: 0 Zeichen

**Probleme:**

- robots.txt verbietet den Abruf (robots.txt nicht erreichbar: ConnectError)

> Notiz aus sources.yaml: GEPRUEFT 01.09.2026: Verbindung wird serverseitig abgewiesen, robots.txt nicht abrufbar -> Quelle wird uebersprungen. Guthaben wird auf Treuhand-Sammelkonten bei Partnerbanken (z.B. Citi, Solaris, Deutsche Bank, HSBC) verwahrt. Einlagensicherungsland damit nicht eindeutig.

**Greift:** Quelle wird im Lauf uebersprungen

---

### santander.de  (notduerftig)

- URL: https://www.santander.de/privatkunden/sparen-anlegen/tagesgeld/
- Land/Typ/Rendering: DE / bank / static_html
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 187424 Zeichen, 1.8s
- JSON-LD: 0 Treffer (1 ld+json-Block(s), 0 Kandidat(en))
- container_selector `div.product-detail-stage`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 2 Angebote ueber Struktur 'tr.? (Tiefe 12, 2x)'
    - Santander Consumer Bank - 0.3 %
    - Santander Consumer Bank - 2.75 %
- Fliesstext fuer LLM: 4826 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `literal:'Santander Consumer Bank'` | literal | Santander Consumer Bank |
| zinssatz | `.interest-rate-big` | 0 Treffer |  |
| zinstyp | `.rate-type` | 0 Treffer |  |
| aktionsdauer_monate | `.promo-time` | 0 Treffer |  |
| folgezins | `.base-rate` | 0 Treffer |  |
| mindestanlage | `literal:'0 EUR'` | literal | 0 EUR |
| hoechstanlage | `.max-amount` | 0 Treffer |  |
| einlagensicherung_land | `literal:'DE'` | literal | DE |

**Probleme:**

- container_selector trifft nichts: div.product-detail-stage
- Feldselektoren ohne Treffer: zinssatz, zinstyp, aktionsdauer_monate, folgezins, hoechstanlage

> Notiz aus sources.yaml: Deutsche Tochtergesellschaft der spanischen Banco Santander, unterliegt aber der deutschen Einlagensicherung.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---

### openbank.de  (kaputt)

- URL: https://www.openbank.de/tagesgeldkonto
- Land/Typ/Rendering: ES / bank / js_required (gerendert)
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 103152 Zeichen, 6.6s
- JSON-LD: 0 Treffer (kein <script type=application/ld+json> gefunden)
- container_selector `div.hero-banner, div.product-card`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 0 Angebote - keine wiederkehrende Struktur mit Zins gefunden
- Fliesstext fuer LLM: 2997 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `literal:'Openbank'` | literal | Openbank |
| zinssatz | `.interest-rate-highlight` | 0 Treffer |  |
| zinstyp | `.condition-text` | 0 Treffer |  |
| aktionsdauer_monate | `.bonus-period` | 0 Treffer |  |
| folgezins | `.standard-rate` | 0 Treffer |  |
| mindestanlage | `literal:'0 EUR'` | literal | 0 EUR |
| hoechstanlage | `literal:'unbegrenzt'` | literal | unbegrenzt |
| einlagensicherung_land | `literal:'ES'` | literal | ES |

**Probleme:**

- container_selector trifft nichts: div.hero-banner, div.product-card
- Feldselektoren ohne Treffer: zinssatz, zinstyp, aktionsdauer_monate, folgezins

> Notiz aus sources.yaml: Spanische Direktbank (FGD Spanien); laut Recherche 0% Quellensteuer mit Ansaessigkeitsmeldung - ungeprueft.

**Greift:** KEINE Stufe greift

---

### klarna.com  (notduerftig)

- URL: https://www.klarna.com/de/festgeld/
- Land/Typ/Rendering: SE / bank / js_required
- robots.txt live: **erlaubt** (robots.txt gelesen)
- YAML behauptet robots: `ja`
- HTTP: 200 , 728933 Zeichen, 4.1s
- json_endpoint: 0 Treffer - HTTP 404
- JSON-LD: 0 Treffer (1 ld+json-Block(s), 0 Kandidat(en))
- container_selector `div[data-testid='savings-rate-card']`: **0 Knoten**
- Stufe 2 (konfiguriert): 0 Angebote - container_selector findet nichts
- Stufe 2b (Heuristik): 8 Angebote ueber Struktur 'div.pr-m2m2w9.richtext.richtext--left (Tiefe 18, 8x)'
    - Klarna Bank AB - 1.84 %
    - Klarna Bank AB - 2.89 %
    - Klarna Bank AB - 2.46 %
    - Klarna Bank AB - 3.0 %
- Fliesstext fuer LLM: 4408 Zeichen

| Feld | Selektor | Status | Beispielwert |
| --- | --- | :-: | --- |
| bank | `literal:'Klarna Bank AB'` | literal | Klarna Bank AB |
| zinssatz | `[data-testid='flexible-rate-value']` | 0 Treffer |  |
| zinstyp | `literal:'variabel'` | literal | variabel |
| aktionsdauer_monate | `literal:'0'` | literal | 0 |
| folgezins | `[data-testid='flexible-rate-value']` | 0 Treffer |  |
| mindestanlage | `.min-savings-amount` | 0 Treffer |  |
| hoechstanlage | `.max-savings-amount` | 0 Treffer |  |
| einlagensicherung_land | `literal:'SE'` | literal | SE |

**Probleme:**

- json_endpoint unbrauchbar: HTTP 404
- container_selector trifft nichts: div[data-testid='savings-rate-card']
- Feldselektoren ohne Treffer: zinssatz, folgezins, mindestanlage, hoechstanlage

> Notiz aus sources.yaml: Schwedische Einlagensicherung (Riksgaelden); Konten laut Recherche in EUR gefuehrt, SE erhebt 0% QSt fuer Gebietsfremde.

**Greift:** Stufe 2b (Heuristik, ohne YAML-Selektoren)

---
