# Lauf-Report 2026-09-23

Erstellt: 2026-09-23T10:54:19+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 320 |
| Angebote nach Dedupe | 210 |
| Angebote im Ergebnis | 210 |
| davon stale | 34 |
| Laufzeit (s) | 116.0 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 210 |

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
| bankier.pl | 2 | css_heuristik | 8 |  |
| compricer.se | 2 | css_heuristik | 44 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | 2 | css_heuristik | 2 |  |
| openbank.de | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 23 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 12 |  |
| finanztip.de | 2 | css_heuristik | 9 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 45 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 5 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **xtb** (DE): 0.9 % -> 3.5 % (+2.6 pp) [Quelle: finanzfluss.de]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (11)

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

## Heute nicht gefunden - als stale behalten (33)

- **Brad Pitt daje** (PL), stale seit 2026-09-22 (1 Tage)
- **Lokata na** (PL), stale seit 2026-09-12 (11 Tage)
- **Zamień 0 na** (PL), stale seit 2026-09-22 (1 Tage)
- **Do 300 zł za konto** (PL), stale seit 2026-09-22 (1 Tage)
- **IKB** (DE), stale seit 2026-09-22 (1 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (7 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (6 Tage)
- **Kommunalkredit Invest** (AT), stale seit 2026-09-22 (1 Tage)
- **Ferratum Bank** (DE), stale seit 2026-09-14 (9 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-19 (4 Tage)
- **JAK Medlemsbank Sparränta 1,50** (SE), stale seit 2026-09-10 (13 Tage)
- **Handelsbanken Sparränta 0,05** (SE), stale seit 2026-09-10 (13 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-19 (4 Tage)
- **Moank Sparränta 2,40** (SE), stale seit 2026-09-10 (13 Tage)
- **SEB Sparränta 1,70** (SE), stale seit 2026-09-10 (13 Tage)
- **wiLLBe** (LI), stale seit 2026-09-21 (2 Tage)
- **Swedbank Sparränta 1,75** (SE), stale seit 2026-09-10 (13 Tage)
- **Nordea Sparränta 1,75** (SE), stale seit 2026-09-10 (13 Tage)
- **Klarna** (SE), stale seit 2026-09-11 (12 Tage)
- **0TO9** (SE), stale seit 2026-09-22 (1 Tage)
- **Anyfin** (SE), stale seit 2026-09-22 (1 Tage)
- **Collector Bank** (SE), stale seit 2026-09-22 (1 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-09-22 (1 Tage)
- **FIMBank** (MT), stale seit 2026-09-22 (1 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-09-16 (7 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (7 Tage)
- **Stellantis Direktbank** (DE), stale seit 2026-09-21 (2 Tage)
- **Lunar Sparränta** (SE), stale seit 2026-09-10 (13 Tage)
- **Lantmännen Finans Sparränta** (SE), stale seit 2026-09-10 (13 Tage)
- **Ekobanken Sparränta 1,15** (SE), stale seit 2026-09-10 (13 Tage)
- **Nordnet Sparränta** (SE), stale seit 2026-09-10 (13 Tage)
- **Avanza Bank Sparränta** (SE), stale seit 2026-09-10 (13 Tage)
- **ICA Banken Sparränta** (SE), stale seit 2026-09-10 (13 Tage)

## Neu hinzugekommen (15)

- **Klarna** (NL): 3.0 %
- **Bankaktiebolaget Nordiska 2,10** (SE): 2.9 %
- **finvesto** (DE): 2.35 %
- **FCM Bank** (NL): 2.26 %
- **Collector Bank** (DE): 2.2 %
- **Inbank** (NL): 2.2 %
- **FCM Bank** (DE): 3.15 %
- **USD/PLN** (PL): 0.83 %
- **ZŁOTO** (PL): 0.57 %
- **EUR/PLN** (PL): 0.49 %
- **BITCOIN** (PL): 0.47 %
- **CHF/PLN** (PL): 0.47 %
- **EUR/USD** (PL): 0.34 %
- **MIEDŹ** (PL): 0.3 %
- **ROPA** (PL): 0.09 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
