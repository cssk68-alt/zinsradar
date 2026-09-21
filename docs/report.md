# Lauf-Report 2026-09-21

Erstellt: 2026-09-21T12:09:34+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 316 |
| Angebote nach Dedupe | 200 |
| Angebote im Ergebnis | 200 |
| davon stale | 27 |
| Laufzeit (s) | 116.2 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 200 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 8 |  |
| finanzfluss.de | 2 | css_heuristik | 31 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 7 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: ld+json vorhanden, aber ohne verwertbares Zin |
| bankier.pl | 2 | css_heuristik | 11 |  |
| compricer.se | 2 | css_heuristik | 44 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | 2 | css_heuristik | 2 |  |
| openbank.de | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 24 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 12 |  |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 45 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 3 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **xtb** (DE): 0.9 % -> 3.5 % (+2.6 pp) [Quelle: finanzfluss.de]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (11)

- **BBVA** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)
- **Consorsbank** (FR): 3.6 % vs. EZB 0.04 % (+3.56 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.5 % (+3.7 pp)
- **Bigbank** (DE): 4.15 % vs. EZB 0.5 % (+3.65 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Hamburg Direct Bank** (DE): 3.61 % vs. EZB 0.5 % (+3.11 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.5 % (+3.75 pp)
- **Stellantis Direktbank** (DE): 3.62 % vs. EZB 0.5 % (+3.12 pp)
- **Opel Bank** (DE): 3.52 % vs. EZB 0.5 % (+3.02 pp)
- **ING** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)

## Heute nicht gefunden - als stale behalten (26)

- **Lokata na** (PL), stale seit 2026-09-12 (9 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (5 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (4 Tage)
- **Ferratum Bank** (DE), stale seit 2026-09-14 (7 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-19 (2 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-09-08 (13 Tage)
- **JAK Medlemsbank Sparränta 1,50** (SE), stale seit 2026-09-10 (11 Tage)
- **Handelsbanken Sparränta 0,05** (SE), stale seit 2026-09-10 (11 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-19 (2 Tage)
- **Moank Sparränta 2,40** (SE), stale seit 2026-09-10 (11 Tage)
- **SEB Sparränta 1,70** (SE), stale seit 2026-09-10 (11 Tage)
- **Swedbank Sparränta 1,75** (SE), stale seit 2026-09-10 (11 Tage)
- **Nordea Sparränta 1,75** (SE), stale seit 2026-09-10 (11 Tage)
- **Klarna** (SE), stale seit 2026-09-11 (10 Tage)
- **SimpleSave** (IE), stale seit 2026-09-17 (4 Tage)
- **Avida Bank AB** (SE), stale seit 2026-09-09 (12 Tage)
- **0TO9** (SE), stale seit 2026-09-07 (14 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-09-16 (5 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (5 Tage)
- **Banca Progetto** (IT), stale seit 2026-09-16 (5 Tage)
- **Lunar Sparränta** (SE), stale seit 2026-09-10 (11 Tage)
- **Lantmännen Finans Sparränta** (SE), stale seit 2026-09-10 (11 Tage)
- **Ekobanken Sparränta 1,15** (SE), stale seit 2026-09-10 (11 Tage)
- **Nordnet Sparränta** (SE), stale seit 2026-09-10 (11 Tage)
- **Avanza Bank Sparränta** (SE), stale seit 2026-09-10 (11 Tage)
- **ICA Banken Sparränta** (SE), stale seit 2026-09-10 (11 Tage)

## Neu hinzugekommen (6)

- **Ikano Bank 1,15** (SE): 3.15 %
- **Klarna** (NL): 3.0 %
- **Multitude Bank 2,55** (MT): 3.1 %
- **Aros Kapital 2,00** (SE): 2.95 %
- **Banca Progetto** (NL): 2.25 %
- **Inbank** (NL): 2.2 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
