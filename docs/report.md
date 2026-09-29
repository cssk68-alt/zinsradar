# Lauf-Report 2026-09-29

Erstellt: 2026-09-29T12:15:41+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 316 |
| Angebote nach Dedupe | 206 |
| Angebote im Ergebnis | 206 |
| davon stale | 53 |
| Laufzeit (s) | 114.2 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 206 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 7 |  |
| finanzfluss.de | 2 | css_heuristik | 17 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 8 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: ld+json vorhanden, aber ohne verwertbares Zin |
| bankier.pl | 2 | css_heuristik | 8 |  |
| compricer.se | 2 | css_heuristik | 47 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | - | - | 0 | HTTP 404 |
| openbank.de | 2 | css_heuristik | 2 |  |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 24 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 12 |  |
| finanztip.de | 2 | css_heuristik | 9 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 47 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 6 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (12)

- **BBVA** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)
- **Consorsbank** (FR): 3.8 % vs. EZB 0.04 % (+3.76 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.5 % (+3.7 pp)
- **Suresse Direkt Bank** (DE): 3.7 % vs. EZB 0.5 % (+3.2 pp)
- **Bigbank** (DE): 4.15 % vs. EZB 0.5 % (+3.65 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Hamburg Direct Bank** (DE): 3.61 % vs. EZB 0.5 % (+3.11 pp)
- **Besonderheiten** (DE): 4.25 % vs. EZB 0.5 % (+3.75 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.5 % (+3.75 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.5 % (+3.45 pp)

## Heute nicht gefunden - als stale behalten (53)

- **Brad Pitt daje** (PL), stale seit 2026-09-22 (7 Tage)
- **Nawet** (PL), stale seit 2026-09-24 (5 Tage)
- **Zamień 0 na** (PL), stale seit 2026-09-24 (5 Tage)
- **Do 300 zł za konto** (PL), stale seit 2026-09-22 (7 Tage)
- **Sprawdzamy kredyty konsolidacyjne** (PL), stale seit 2026-09-26 (3 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-09-25 (4 Tage)
- **SWK Bank** (DE), stale seit 2026-09-28 (1 Tage)
- **IKB** (DE), stale seit 2026-09-22 (7 Tage)
- **Postbank** (DE), stale seit 2026-09-27 (2 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (13 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-09-25 (4 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (12 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-09-25 (4 Tage)
- **SBAB Bank 1,25** (SE), stale seit 2026-09-25 (4 Tage)
- **Kommunalkredit Invest** (AT), stale seit 2026-09-22 (7 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-19 (10 Tage)
- **Multitude Bank 2,55** (MT), stale seit 2026-09-25 (4 Tage)
- **Raisin** (DE), stale seit 2026-09-27 (2 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-09-25 (4 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-09-25 (4 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-09-25 (4 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-09-25 (4 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-09-25 (4 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-19 (10 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-09-25 (4 Tage)
- **Bank Norwegian 1,75** (SE), stale seit 2026-09-25 (4 Tage)
- **finvesto** (DE), stale seit 2026-09-28 (1 Tage)
- **Distingo** (DE), stale seit 2026-09-27 (2 Tage)
- **Grenke Bank** (DE), stale seit 2026-09-23 (6 Tage)
- **BW-Bank** (DE), stale seit 2026-09-24 (5 Tage)
- **Collector Bank** (SE), stale seit 2026-09-22 (7 Tage)
- **Yapi Kredi** (DE), stale seit 2026-09-27 (2 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-09-22 (7 Tage)
- **FIMBank** (MT), stale seit 2026-09-22 (7 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (13 Tage)
- **Santander Consumer Bank** (DE), stale seit 2026-09-27 (2 Tage)
- **Stellantis Direktbank** (DE), stale seit 2026-09-21 (8 Tage)
- **Banca CF+** (IT), stale seit 2026-09-27 (2 Tage)
- **Klarna Bank AB** (SE), stale seit 2026-09-27 (2 Tage)
- **Advanzia** (DE), stale seit 2026-09-27 (2 Tage)
- **Nexent-Bank** (DE), stale seit 2026-09-27 (2 Tage)
- **Allgemeine Beamtenbank** (DE), stale seit 2026-09-27 (2 Tage)
- **Targobank** (DE), stale seit 2026-09-27 (2 Tage)
- **Izola Bank** (FR), stale seit 2026-09-27 (2 Tage)
- **MIEDŹ** (PL), stale seit 2026-09-28 (1 Tage)
- **ROPA** (PL), stale seit 2026-09-28 (1 Tage)
- **BITCOIN** (PL), stale seit 2026-09-28 (1 Tage)
- **Alisa Bank Plc** (FI), stale seit 2026-09-27 (2 Tage)
- **ZŁOTO** (PL), stale seit 2026-09-27 (2 Tage)
- **EUR/PLN** (PL), stale seit 2026-09-27 (2 Tage)
- **CHF/PLN** (PL), stale seit 2026-09-28 (1 Tage)
- **USD/PLN** (PL), stale seit 2026-09-28 (1 Tage)
- **EUR/USD** (PL), stale seit 2026-09-28 (1 Tage)

## Zu lange stale - entfernt (1)

- **Ferratum Bank**

## Neu hinzugekommen (8)

- **Koniec** (PL): 7.0 %
- **Santander Consumer Bank** (NL): 3.01 %
- **Banca CF+** (NL): 2.35 %
- **FCM Bank** (NL): 2.26 %
- **BW-Bank** (NL): 2.2 %
- **Collector Bank** (DE): 2.2 %
- **Inbank** (NL): 2.15 %
- **xtb** (DE): 3.5 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
