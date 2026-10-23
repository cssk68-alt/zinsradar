# Lauf-Report 2026-10-23

Erstellt: 2026-10-23T11:08:37+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 19 |
| Quellen durch robots.txt uebersprungen | 1 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 308 |
| Angebote nach Dedupe | 186 |
| Angebote im Ergebnis | 186 |
| davon stale | 32 |
| Laufzeit (s) | 138.9 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 186 |

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
| verivox.de | 2 | css_heuristik | 22 |  |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| compricer.se | 2 | css_heuristik | 46 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 9 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (21)

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
- **CA Savings (Crédit Agricole)** (FR): 4.1 % vs. EZB 0.05 % (+4.05 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.51 % (+3.74 pp)
- **Advanzia** (DE): 4.1 % vs. EZB 0.51 % (+3.59 pp)
- **Ikano Bank** (DE): 3.91 % vs. EZB 0.51 % (+3.4 pp)
- **DKB** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.51 % (+3.44 pp)
- **XTB** (DE): 4.5 % vs. EZB 0.51 % (+3.99 pp)

## Heute nicht gefunden - als stale behalten (32)

- **Lokata na** (PL), stale seit 2026-10-18 (5 Tage)
- **MyInvestor** (ES), stale seit 2026-10-21 (2 Tage)
- **Brocc Finance** (SE), stale seit 2026-10-09 (14 Tage)
- **Ikano Bank** (SE), stale seit 2026-10-20 (3 Tage)
- **pbb direkt** (DE), stale seit 2026-10-14 (9 Tage)
- **Multitude Bank** (SE), stale seit 2026-10-22 (1 Tage)
- **Multitude Bank 2,50** (SE), stale seit 2026-10-17 (6 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-10-14 (9 Tage)
- **Bankaktiebolaget Nordiska** (SE), stale seit 2026-10-21 (2 Tage)
- **Northmill Bank** (SE), stale seit 2026-10-09 (14 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-10-18 (5 Tage)
- **Multitude Bank** (MT), stale seit 2026-10-22 (1 Tage)
- **Multitude Bank 2,50** (MT), stale seit 2026-10-17 (6 Tage)
- **Commerzbank** (DE), stale seit 2026-10-16 (7 Tage)
- **Raisin StartZins** (DE), stale seit 2026-10-19 (4 Tage)
- **Aros Kapital** (SE), stale seit 2026-10-17 (6 Tage)
- **Coeli** (SE), stale seit 2026-10-13 (10 Tage)
- **JAK Medlemsbank** (SE), stale seit 2026-10-15 (8 Tage)
- **Bluestep Bank** (SE), stale seit 2026-10-11 (12 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-10-11 (12 Tage)
- **Serafim Finans** (SE), stale seit 2026-10-13 (10 Tage)
- **Bigbank** (EE), stale seit 2026-10-15 (8 Tage)
- **Renault Bank** (FR), stale seit 2026-10-15 (8 Tage)
- **Scalable Capital Bank** (DE), stale seit 2026-10-11 (12 Tage)
- **Avida Finans** (SE), stale seit 2026-10-20 (3 Tage)
- **Qliro** (SE), stale seit 2026-10-13 (10 Tage)
- **Yapi Kredi Deutschland** (DE), stale seit 2026-10-22 (1 Tage)
- **Carrefour Banque** (FR), stale seit 2026-10-18 (5 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-10-21 (2 Tage)
- **Collector Bank** (NL), stale seit 2026-10-20 (3 Tage)
- **Besonderheiten** (DE), stale seit 2026-10-14 (9 Tage)
- **Cosmos Direkt** (DE), stale seit 2026-10-11 (12 Tage)

## Zu lange stale - entfernt (10)

- **SBAB Bank**
- **Danske Bank**
- **Handelsbanken**
- **Plus**
- **Trade Republic**
- **Swedbank**
- **Nordea**
- **SEB**
- **BluOr Bank AS**
- **Ekobanken**

## Neu hinzugekommen (13)

- **Multitude Bank 2,60** (SE): 3.4 %
- **Multitude Bank 2,60** (MT): 3.4 %
- **Bigbank** (NL): 3.0 %
- **Bigbank** (DE): 3.9 %
- **Renault Bank direkt** (DE): 2.51 %
- **FCM Bank** (NL): 2.43 %
- **Resursbank** (DE): 2.41 %
- **Renault Bank** (NL): 2.4 %
- **Avida Finans** (DE): 2.37 %
- **Collector Bank** (DE): 2.37 %
- **Carrefour Banque** (NL): 2.35 %
- **Northmill Bank** (DE): 2.3 %
- **Ikano Bank** (DE): 3.91 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
