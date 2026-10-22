# Lauf-Report 2026-10-22

Erstellt: 2026-10-22T11:17:06+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 18 |
| Quellen durch robots.txt uebersprungen | 1 |
| Quellen ohne Treffer | 9 |
| Rohtreffer | 288 |
| Angebote nach Dedupe | 192 |
| Angebote im Ergebnis | 192 |
| davon stale | 51 |
| Laufzeit (s) | 135.7 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 192 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 6 |  |
| finanzfluss.de | 2 | css_heuristik | 14 |  |
| durchblicker.at | - | - | 0 | HTTP 403 |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 8 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | robots.txt nicht erreichbar: ConnectTimeout |
| bankier.pl | 2 | css_heuristik | 8 |  |
| compricer.se | 2 | css_heuristik | 46 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | - | - | 0 | HTTP 404 |
| openbank.de | 2 | css_heuristik | 2 |  |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 23 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | - | - | 0 | HTTP 403 |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| compricer.se | 2 | css_heuristik | 46 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 10 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **BITCOIN** (PL): 0.68 % -> 3.38 % (+2.7 pp) [Quelle: bankier.pl]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (17)

- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **Volkswagen Bank** (DE): 3.75 % vs. EZB 0.51 % (+3.24 pp)
- **Hamburg Direct Bank** (DE): 3.62 % vs. EZB 0.51 % (+3.11 pp)
- **Ferratum Bank** (DE): 3.8 % vs. EZB 0.51 % (+3.29 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.51 % (+3.69 pp)
- **bunq Free** (NL): 3.15 % vs. EZB 0.14 % (+3.01 pp)
- **Crédit Agricole** (DE): 4.1 % vs. EZB 0.51 % (+3.59 pp)
- **Suresse Direkt Bank** (DE): 3.8 % vs. EZB 0.51 % (+3.29 pp)
- **Distingo** (DE): 3.95 % vs. EZB 0.51 % (+3.44 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Bigbank** (DE): 3.9 % vs. EZB 0.51 % (+3.39 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Advanzia** (DE): 4.1 % vs. EZB 0.51 % (+3.59 pp)
- **Ikano Bank** (DE): 3.91 % vs. EZB 0.51 % (+3.4 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.51 % (+3.44 pp)

## Heute nicht gefunden - als stale behalten (51)

- **Lokata na** (PL), stale seit 2026-10-18 (4 Tage)
- **MyInvestor** (ES), stale seit 2026-10-21 (1 Tage)
- **Brocc Finance** (SE), stale seit 2026-10-09 (13 Tage)
- **Ikano Bank** (SE), stale seit 2026-10-20 (2 Tage)
- **pbb direkt** (DE), stale seit 2026-10-14 (8 Tage)
- **SBAB Bank** (SE), stale seit 2026-10-08 (14 Tage)
- **Danske Bank** (SE), stale seit 2026-10-08 (14 Tage)
- **Multitude Bank 2,50** (SE), stale seit 2026-10-17 (5 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-10-14 (8 Tage)
- **Bankaktiebolaget Nordiska** (SE), stale seit 2026-10-21 (1 Tage)
- **Northmill Bank** (SE), stale seit 2026-10-09 (13 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-10-18 (4 Tage)
- **Multitude Bank 2,50** (MT), stale seit 2026-10-17 (5 Tage)
- **Handelsbanken** (SE), stale seit 2026-10-08 (14 Tage)
- **Commerzbank** (DE), stale seit 2026-10-16 (6 Tage)
- **Plus** (SE), stale seit 2026-10-08 (14 Tage)
- **Raisin StartZins** (DE), stale seit 2026-10-19 (3 Tage)
- **Trade Republic** (NL), stale seit 2026-10-08 (14 Tage)
- **Aros Kapital** (SE), stale seit 2026-10-17 (5 Tage)
- **Coeli** (SE), stale seit 2026-10-13 (9 Tage)
- **JAK Medlemsbank** (SE), stale seit 2026-10-15 (7 Tage)
- **Bluestep Bank** (SE), stale seit 2026-10-11 (11 Tage)
- **Ferratum (Multitude Bank)** (MT), stale seit 2026-10-21 (1 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-10-11 (11 Tage)
- **Serafim Finans** (SE), stale seit 2026-10-13 (9 Tage)
- **Bigbank** (EE), stale seit 2026-10-15 (7 Tage)
- **CA Savings (Crédit Agricole)** (FR), stale seit 2026-10-21 (1 Tage)
- **Ascory Bank** (DE), stale seit 2026-10-21 (1 Tage)
- **Swedbank** (SE), stale seit 2026-10-08 (14 Tage)
- **Renault Bank** (FR), stale seit 2026-10-15 (7 Tage)
- **Nordea** (SE), stale seit 2026-10-08 (14 Tage)
- **SEB** (SE), stale seit 2026-10-08 (14 Tage)
- **Scalable Capital Bank** (DE), stale seit 2026-10-11 (11 Tage)
- **Avida Finans** (SE), stale seit 2026-10-20 (2 Tage)
- **Qliro** (SE), stale seit 2026-10-13 (9 Tage)
- **qred** (SE), stale seit 2026-10-21 (1 Tage)
- **0TO9** (SE), stale seit 2026-10-21 (1 Tage)
- **SimpleSave** (NL), stale seit 2026-10-21 (1 Tage)
- **Yapi Kredi Bank Deutschland** (DE), stale seit 2026-10-14 (8 Tage)
- **YapiKredi Deutschland** (DE), stale seit 2026-10-21 (1 Tage)
- **Carrefour Banque** (FR), stale seit 2026-10-18 (4 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-10-21 (1 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-10-08 (14 Tage)
- **Collector Bank** (NL), stale seit 2026-10-20 (2 Tage)
- **Besonderheiten** (DE), stale seit 2026-10-14 (8 Tage)
- **Revolut** (DE), stale seit 2026-10-21 (1 Tage)
- **Cosmos Direkt** (DE), stale seit 2026-10-11 (11 Tage)
- **Advanzia Bank** (LU), stale seit 2026-10-21 (1 Tage)
- **DKB** (DE), stale seit 2026-10-21 (1 Tage)
- **Ekobanken** (SE), stale seit 2026-10-08 (14 Tage)
- **XTB** (DE), stale seit 2026-10-21 (1 Tage)

## Zu lange stale - entfernt (2)

- **Openbank Girokonto +**
- **CreditPlus**

## Neu hinzugekommen (11)

- **Bankaktiebolaget Nordiska 2,10** (SE): 3.15 %
- **Bigbank** (NL): 3.0 %
- **Bigbank** (DE): 3.9 %
- **Advanzia Bank** (DE): 2.71 %
- **Renault Bank direkt** (DE): 2.51 %
- **FCM Bank** (NL): 2.43 %
- **SimpleSave** (IE): 2.46 %
- **Carrefour Banque** (NL): 2.35 %
- **Renault Bank** (NL): 2.3 %
- **Ikano Bank** (DE): 3.91 %
- **Revolut** (NL): 1.25 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
