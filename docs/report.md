# Lauf-Report 2026-10-19

Erstellt: 2026-10-19T12:19:15+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 308 |
| Angebote nach Dedupe | 192 |
| Angebote im Ergebnis | 192 |
| davon stale | 43 |
| Laufzeit (s) | 125.2 |

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
| raisin.fr | 2 | css_heuristik | 7 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | 2 | css_heuristik | 2 |  |
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

* Land-Dopplungen im Altbestand aufgeloest: 11 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (21)

- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **Volkswagen Bank** (DE): 3.75 % vs. EZB 0.51 % (+3.24 pp)
- **Hamburg Direct Bank** (DE): 3.62 % vs. EZB 0.51 % (+3.11 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
- **Ferratum Bank** (DE): 3.8 % vs. EZB 0.51 % (+3.29 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.51 % (+3.69 pp)
- **bunq Free** (NL): 3.15 % vs. EZB 0.14 % (+3.01 pp)
- **Crédit Agricole** (DE): 4.1 % vs. EZB 0.51 % (+3.59 pp)
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

## Heute nicht gefunden - als stale behalten (43)

- **Lokata na** (PL), stale seit 2026-10-18 (1 Tage)
- **Openbank Girokonto +** (DE), stale seit 2026-10-07 (12 Tage)
- **Brocc Finance** (SE), stale seit 2026-10-09 (10 Tage)
- **Ikano Bank** (SE), stale seit 2026-10-14 (5 Tage)
- **pbb direkt** (DE), stale seit 2026-10-14 (5 Tage)
- **SBAB Bank** (SE), stale seit 2026-10-08 (11 Tage)
- **CreditPlus** (DE), stale seit 2026-10-07 (12 Tage)
- **Danske Bank** (SE), stale seit 2026-10-08 (11 Tage)
- **Multitude Bank 2,50** (SE), stale seit 2026-10-17 (2 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-10-14 (5 Tage)
- **Northmill Bank** (SE), stale seit 2026-10-09 (10 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-10-18 (1 Tage)
- **Multitude Bank 2,50** (MT), stale seit 2026-10-17 (2 Tage)
- **Handelsbanken** (SE), stale seit 2026-10-08 (11 Tage)
- **Raisin RenteBoost** (DE), stale seit 2026-10-05 (14 Tage)
- **Commerzbank** (DE), stale seit 2026-10-16 (3 Tage)
- **Plus** (SE), stale seit 2026-10-08 (11 Tage)
- **Trade Republic** (NL), stale seit 2026-10-08 (11 Tage)
- **Suresse Direkt Bank** (DE), stale seit 2026-10-14 (5 Tage)
- **Aros Kapital** (SE), stale seit 2026-10-17 (2 Tage)
- **Coeli** (SE), stale seit 2026-10-13 (6 Tage)
- **JAK Medlemsbank** (SE), stale seit 2026-10-15 (4 Tage)
- **Bluestep Bank** (SE), stale seit 2026-10-11 (8 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-10-11 (8 Tage)
- **Serafim Finans** (SE), stale seit 2026-10-13 (6 Tage)
- **Bigbank** (EE), stale seit 2026-10-15 (4 Tage)
- **Swedbank** (SE), stale seit 2026-10-08 (11 Tage)
- **Renault Bank** (FR), stale seit 2026-10-15 (4 Tage)
- **Nordea** (SE), stale seit 2026-10-08 (11 Tage)
- **SEB** (SE), stale seit 2026-10-08 (11 Tage)
- **Scalable Capital Bank** (DE), stale seit 2026-10-11 (8 Tage)
- **Qliro** (SE), stale seit 2026-10-13 (6 Tage)
- **Yapi Kredi Bank Deutschland** (DE), stale seit 2026-10-14 (5 Tage)
- **Avida Bank AB** (SE), stale seit 2026-10-05 (14 Tage)
- **Carrefour Banque** (FR), stale seit 2026-10-18 (1 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-10-08 (11 Tage)
- **BW-Bank** (DE), stale seit 2026-10-05 (14 Tage)
- **Avarda Bank** (SE), stale seit 2026-10-05 (14 Tage)
- **Besonderheiten** (DE), stale seit 2026-10-14 (5 Tage)
- **Collector Bank** (SE), stale seit 2026-10-05 (14 Tage)
- **IKB Deutsche Industriebank** (DE), stale seit 2026-10-05 (14 Tage)
- **Cosmos Direkt** (DE), stale seit 2026-10-11 (8 Tage)
- **Ekobanken** (SE), stale seit 2026-10-08 (11 Tage)

## Neu hinzugekommen (12)

- **Raisin RenteBoost** (NL): 3.05 %
- **Bigbank** (NL): 3.0 %
- **Bigbank** (DE): 3.9 %
- **Renault Bank direkt** (DE): 2.51 %
- **Carrefour Banque** (NL): 2.35 %
- **Avarda Bank** (NL): 2.33 %
- **Collector Bank** (NL): 2.3 %
- **IKB Deutsche Industriebank** (NL): 2.3 %
- **Renault Bank** (NL): 2.3 %
- **BW-Bank** (NL): 2.26 %
- **ViViBanca** (IT): 2.45 %
- **Ikano Bank** (DE): 3.91 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
