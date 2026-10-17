# Lauf-Report 2026-10-17

Erstellt: 2026-10-17T10:15:21+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 304 |
| Angebote nach Dedupe | 190 |
| Angebote im Ergebnis | 190 |
| davon stale | 50 |
| Laufzeit (s) | 115.5 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 190 |

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
| verivox.de | 2 | css_heuristik | 23 |  |
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

## Heute nicht gefunden - als stale behalten (50)

- **Openbank Girokonto +** (DE), stale seit 2026-10-07 (10 Tage)
- **Brocc Finance** (SE), stale seit 2026-10-09 (8 Tage)
- **Ikano Bank** (SE), stale seit 2026-10-14 (3 Tage)
- **pbb direkt** (DE), stale seit 2026-10-14 (3 Tage)
- **SBAB Bank** (SE), stale seit 2026-10-08 (9 Tage)
- **CreditPlus** (DE), stale seit 2026-10-07 (10 Tage)
- **Danske Bank** (SE), stale seit 2026-10-08 (9 Tage)
- **Multitude Bank** (SE), stale seit 2026-10-16 (1 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-10-14 (3 Tage)
- **Volkswagen Bank Sparbrief** (DE), stale seit 2026-10-14 (3 Tage)
- **Northmill Bank** (SE), stale seit 2026-10-09 (8 Tage)
- **Saldo Bank** (SE), stale seit 2026-10-10 (7 Tage)
- **Multitude Bank** (MT), stale seit 2026-10-16 (1 Tage)
- **Handelsbanken** (SE), stale seit 2026-10-08 (9 Tage)
- **Raisin RenteBoost** (DE), stale seit 2026-10-05 (12 Tage)
- **Commerzbank** (DE), stale seit 2026-10-16 (1 Tage)
- **Plus** (SE), stale seit 2026-10-08 (9 Tage)
- **Trade Republic** (NL), stale seit 2026-10-08 (9 Tage)
- **Suresse Direkt Bank** (DE), stale seit 2026-10-14 (3 Tage)
- **Coeli** (SE), stale seit 2026-10-13 (4 Tage)
- **JAK Medlemsbank** (SE), stale seit 2026-10-15 (2 Tage)
- **Bluestep Bank** (SE), stale seit 2026-10-11 (6 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-10-11 (6 Tage)
- **Serafim Finans** (SE), stale seit 2026-10-13 (4 Tage)
- **Bigbank** (EE), stale seit 2026-10-15 (2 Tage)
- **Swedbank** (SE), stale seit 2026-10-08 (9 Tage)
- **Renault Bank** (FR), stale seit 2026-10-15 (2 Tage)
- **Nordea** (SE), stale seit 2026-10-08 (9 Tage)
- **SEB** (SE), stale seit 2026-10-08 (9 Tage)
- **Scalable Capital Bank** (DE), stale seit 2026-10-11 (6 Tage)
- **Qliro** (SE), stale seit 2026-10-13 (4 Tage)
- **Yapi Kredi Bank Deutschland** (DE), stale seit 2026-10-14 (3 Tage)
- **Avida Bank AB** (SE), stale seit 2026-10-05 (12 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-10-08 (9 Tage)
- **BW-Bank** (DE), stale seit 2026-10-05 (12 Tage)
- **Avarda Bank** (SE), stale seit 2026-10-05 (12 Tage)
- **Besonderheiten** (DE), stale seit 2026-10-14 (3 Tage)
- **Collector Bank** (SE), stale seit 2026-10-05 (12 Tage)
- **IKB Deutsche Industriebank** (DE), stale seit 2026-10-05 (12 Tage)
- **Cosmos Direkt** (DE), stale seit 2026-10-11 (6 Tage)
- **Banca Progetto** (IT), stale seit 2026-10-07 (10 Tage)
- **ZŁOTO** (PL), stale seit 2026-10-15 (2 Tage)
- **ROPA** (PL), stale seit 2026-10-15 (2 Tage)
- **Ekobanken** (SE), stale seit 2026-10-08 (9 Tage)
- **BITCOIN** (PL), stale seit 2026-10-15 (2 Tage)
- **MIEDŹ** (PL), stale seit 2026-10-15 (2 Tage)
- **USD/PLN** (PL), stale seit 2026-10-15 (2 Tage)
- **EUR/USD** (PL), stale seit 2026-10-15 (2 Tage)
- **CHF/PLN** (PL), stale seit 2026-10-14 (3 Tage)
- **EUR/PLN** (PL), stale seit 2026-10-15 (2 Tage)

## Neu hinzugekommen (13)

- **Multitude Bank 2,50** (SE): 3.2 %
- **Multitude Bank 2,50** (MT): 3.2 %
- **Raisin RenteBoost** (NL): 3.05 %
- **Bigbank** (NL): 3.0 %
- **Bigbank** (DE): 3.9 %
- **Renault Bank direkt** (DE): 2.51 %
- **Banca Progetto** (NL): 2.4 %
- **Avarda Bank** (NL): 2.33 %
- **Collector Bank** (NL): 2.3 %
- **IKB Deutsche Industriebank** (NL): 2.3 %
- **Renault Bank** (NL): 2.3 %
- **BW-Bank** (NL): 2.26 %
- **Ikano Bank** (DE): 3.91 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
