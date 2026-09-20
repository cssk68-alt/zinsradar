# Lauf-Report 2026-09-20

Erstellt: 2026-09-20T10:45:50+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 329 |
| Angebote nach Dedupe | 197 |
| Angebote im Ergebnis | 197 |
| davon stale | 35 |
| Laufzeit (s) | 123.9 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 197 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 9 |  |
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
| compricer.se | 2 | css_heuristik | 45 |  |
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

## Heute nicht gefunden - als stale behalten (34)

- **Lokata na** (PL), stale seit 2026-09-12 (8 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-09-19 (1 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (4 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (3 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-09-19 (1 Tage)
- **SBAB Bank 1,25** (SE), stale seit 2026-09-19 (1 Tage)
- **Ferratum Bank** (DE), stale seit 2026-09-14 (6 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-19 (1 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-09-08 (12 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-09-19 (1 Tage)
- **JAK Medlemsbank Sparränta 1,50** (SE), stale seit 2026-09-10 (10 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-09-19 (1 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-09-19 (1 Tage)
- **Handelsbanken Sparränta 0,05** (SE), stale seit 2026-09-10 (10 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-19 (1 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-09-19 (1 Tage)
- **Moank Sparränta 2,40** (SE), stale seit 2026-09-10 (10 Tage)
- **Bank Norwegian 1,75** (SE), stale seit 2026-09-19 (1 Tage)
- **SEB Sparränta 1,70** (SE), stale seit 2026-09-10 (10 Tage)
- **Swedbank Sparränta 1,75** (SE), stale seit 2026-09-10 (10 Tage)
- **Nordea Sparränta 1,75** (SE), stale seit 2026-09-10 (10 Tage)
- **Klarna** (SE), stale seit 2026-09-11 (9 Tage)
- **SimpleSave** (IE), stale seit 2026-09-17 (3 Tage)
- **Avida Bank AB** (SE), stale seit 2026-09-09 (11 Tage)
- **0TO9** (SE), stale seit 2026-09-07 (13 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-09-16 (4 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (4 Tage)
- **Banca Progetto** (IT), stale seit 2026-09-16 (4 Tage)
- **Lunar Sparränta** (SE), stale seit 2026-09-10 (10 Tage)
- **Lantmännen Finans Sparränta** (SE), stale seit 2026-09-10 (10 Tage)
- **Ekobanken Sparränta 1,15** (SE), stale seit 2026-09-10 (10 Tage)
- **Nordnet Sparränta** (SE), stale seit 2026-09-10 (10 Tage)
- **Avanza Bank Sparränta** (SE), stale seit 2026-09-10 (10 Tage)
- **ICA Banken Sparränta** (SE), stale seit 2026-09-10 (10 Tage)

## Neu hinzugekommen (3)

- **Klarna** (NL): 3.0 %
- **Banca Progetto** (NL): 2.25 %
- **Inbank** (NL): 2.2 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
