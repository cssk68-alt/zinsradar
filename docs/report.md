# Lauf-Report 2026-09-24

Erstellt: 2026-09-24T11:14:09+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 331 |
| Angebote nach Dedupe | 213 |
| Angebote im Ergebnis | 213 |
| davon stale | 54 |
| Laufzeit (s) | 124.9 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 213 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 8 |  |
| finanzfluss.de | 2 | css_heuristik | 31 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 50 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 7 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: ld+json vorhanden, aber ohne verwertbares Zin |
| bankier.pl | 2 | css_heuristik | 9 |  |
| compricer.se | 2 | css_heuristik | 46 |  |
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
| finanztip.de | 2 | css_heuristik | 9 |  |
| spaarrente.nl | 2 | css_heuristik | 50 |  |
| compricer.se | 2 | css_heuristik | 46 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 5 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **xtb** (DE): 0.9 % -> 3.5 % (+2.6 pp) [Quelle: finanzfluss.de]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (12)

- **BBVA** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)
- **Consorsbank** (FR): 3.6 % vs. EZB 0.04 % (+3.56 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.5 % (+3.7 pp)
- **Suresse Direkt Bank** (DE): 3.7 % vs. EZB 0.5 % (+3.2 pp)
- **Bigbank** (DE): 4.15 % vs. EZB 0.5 % (+3.65 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Hamburg Direct Bank** (DE): 3.61 % vs. EZB 0.5 % (+3.11 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.5 % (+3.75 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.5 % (+3.45 pp)
- **ING** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)
- **Allgemeine Beamtenbank** (DE): 3.55 % vs. EZB 0.5 % (+3.05 pp)

## Heute nicht gefunden - als stale behalten (53)

- **Brad Pitt daje** (PL), stale seit 2026-09-22 (2 Tage)
- **Lokata na** (PL), stale seit 2026-09-12 (12 Tage)
- **Do 300 zł za konto** (PL), stale seit 2026-09-22 (2 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-09-23 (1 Tage)
- **IKB** (DE), stale seit 2026-09-22 (2 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (8 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-09-23 (1 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (7 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-09-23 (1 Tage)
- **SBAB Bank 1,25** (SE), stale seit 2026-09-23 (1 Tage)
- **Kommunalkredit Invest** (AT), stale seit 2026-09-22 (2 Tage)
- **Ferratum Bank** (DE), stale seit 2026-09-14 (10 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-19 (5 Tage)
- **Multitude Bank 2,55** (MT), stale seit 2026-09-23 (1 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-09-23 (1 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-09-23 (1 Tage)
- **JAK Medlemsbank Sparränta 1,50** (SE), stale seit 2026-09-10 (14 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-09-23 (1 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-09-23 (1 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-09-23 (1 Tage)
- **Handelsbanken Sparränta 0,05** (SE), stale seit 2026-09-10 (14 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-19 (5 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-09-23 (1 Tage)
- **Moank Sparränta 2,40** (SE), stale seit 2026-09-10 (14 Tage)
- **Bank Norwegian 1,75** (SE), stale seit 2026-09-23 (1 Tage)
- **SEB Sparränta 1,70** (SE), stale seit 2026-09-10 (14 Tage)
- **wiLLBe** (LI), stale seit 2026-09-21 (3 Tage)
- **Swedbank Sparränta 1,75** (SE), stale seit 2026-09-10 (14 Tage)
- **Nordea Sparränta 1,75** (SE), stale seit 2026-09-10 (14 Tage)
- **Klarna** (SE), stale seit 2026-09-11 (13 Tage)
- **Qred Bank AB** (SE), stale seit 2026-09-23 (1 Tage)
- **0TO9** (SE), stale seit 2026-09-22 (2 Tage)
- **Grenke Bank** (DE), stale seit 2026-09-23 (1 Tage)
- **Collector Bank** (SE), stale seit 2026-09-22 (2 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-09-22 (2 Tage)
- **FIMBank** (MT), stale seit 2026-09-22 (2 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-09-16 (8 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (8 Tage)
- **Stellantis Direktbank** (DE), stale seit 2026-09-21 (3 Tage)
- **Lunar Sparränta** (SE), stale seit 2026-09-10 (14 Tage)
- **Lantmännen Finans Sparränta** (SE), stale seit 2026-09-10 (14 Tage)
- **Ekobanken Sparränta 1,15** (SE), stale seit 2026-09-10 (14 Tage)
- **Nordnet Sparränta** (SE), stale seit 2026-09-10 (14 Tage)
- **Avanza Bank Sparränta** (SE), stale seit 2026-09-10 (14 Tage)
- **USD/PLN** (PL), stale seit 2026-09-23 (1 Tage)
- **ZŁOTO** (PL), stale seit 2026-09-23 (1 Tage)
- **ICA Banken Sparränta** (SE), stale seit 2026-09-10 (14 Tage)
- **EUR/PLN** (PL), stale seit 2026-09-23 (1 Tage)
- **BITCOIN** (PL), stale seit 2026-09-23 (1 Tage)
- **CHF/PLN** (PL), stale seit 2026-09-23 (1 Tage)
- **EUR/USD** (PL), stale seit 2026-09-23 (1 Tage)
- **MIEDŹ** (PL), stale seit 2026-09-23 (1 Tage)
- **ROPA** (PL), stale seit 2026-09-23 (1 Tage)

## Neu hinzugekommen (8)

- **Nawet** (PL): 6.0 %
- **SIGNAL IDUNA** (DE): 3.25 %
- **Klarna** (NL): 3.0 %
- **FCM Bank** (NL): 2.26 %
- **Collector Bank** (DE): 2.2 %
- **Inbank** (NL): 2.2 %
- **FCM Bank** (DE): 3.15 %
- **Allgemeine Beamtenbank** (DE): 3.55 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
