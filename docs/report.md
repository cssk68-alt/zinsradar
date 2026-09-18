# Lauf-Report 2026-09-18

Erstellt: 2026-09-18T10:41:56+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 316 |
| Angebote nach Dedupe | 195 |
| Angebote im Ergebnis | 195 |
| davon stale | 25 |
| Laufzeit (s) | 119.0 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 195 |

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
| bankier.pl | 2 | css_heuristik | 12 |  |
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

## Heute nicht gefunden - als stale behalten (24)

- **Lokata na** (PL), stale seit 2026-09-12 (6 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (2 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (1 Tage)
- **Ferratum Bank** (DE), stale seit 2026-09-14 (4 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-09-08 (10 Tage)
- **JAK Medlemsbank Sparränta 1,50** (SE), stale seit 2026-09-10 (8 Tage)
- **Handelsbanken Sparränta 0,05** (SE), stale seit 2026-09-10 (8 Tage)
- **Moank Sparränta 2,40** (SE), stale seit 2026-09-10 (8 Tage)
- **SEB Sparränta 1,70** (SE), stale seit 2026-09-10 (8 Tage)
- **Swedbank Sparränta 1,75** (SE), stale seit 2026-09-10 (8 Tage)
- **Nordea Sparränta 1,75** (SE), stale seit 2026-09-10 (8 Tage)
- **Klarna** (SE), stale seit 2026-09-11 (7 Tage)
- **SimpleSave** (IE), stale seit 2026-09-17 (1 Tage)
- **Avida Bank AB** (SE), stale seit 2026-09-09 (9 Tage)
- **0TO9** (SE), stale seit 2026-09-07 (11 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-09-16 (2 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (2 Tage)
- **Banca Progetto** (IT), stale seit 2026-09-16 (2 Tage)
- **Lunar Sparränta** (SE), stale seit 2026-09-10 (8 Tage)
- **Lantmännen Finans Sparränta** (SE), stale seit 2026-09-10 (8 Tage)
- **Ekobanken Sparränta 1,15** (SE), stale seit 2026-09-10 (8 Tage)
- **Nordnet Sparränta** (SE), stale seit 2026-09-10 (8 Tage)
- **Avanza Bank Sparränta** (SE), stale seit 2026-09-10 (8 Tage)
- **ICA Banken Sparränta** (SE), stale seit 2026-09-10 (8 Tage)

## Zu lange stale - entfernt (3)

- **LEP (Livret d’Épargne Populaire)**
- **LEP (sous conditions de revenus)**
- **Livret Jeune ≥**

## Neu hinzugekommen (7)

- **Banco do Brasil** (DE): 3.04 %
- **Svea Bank 1,80** (SE): 2.8 %
- **Banca Progetto** (NL): 2.25 %
- **IKB Deutsche Industriebank** (DE): 2.25 %
- **Qred Bank AB** (SE): 2.25 %
- **Klarna** (DE): 3.0 %
- **Inbank** (NL): 2.2 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
