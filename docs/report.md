# Lauf-Report 2026-10-10

Erstellt: 2026-10-10T12:01:24+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 293 |
| Angebote nach Dedupe | 203 |
| Angebote im Ergebnis | 203 |
| davon stale | 65 |
| Laufzeit (s) | 121.7 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 203 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 6 |  |
| finanzfluss.de | 2 | css_heuristik | 15 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 7 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | HTTP 403 |
| bankier.pl | 2 | css_heuristik | 8 |  |
| compricer.se | 2 | css_heuristik | 45 |  |
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
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| compricer.se | 2 | css_heuristik | 45 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 10 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (16)

- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **Hamburg Direct Bank** (DE): 3.62 % vs. EZB 0.51 % (+3.11 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.51 % (+3.69 pp)
- **Crédit Agricole** (DE): 4.1 % vs. EZB 0.51 % (+3.59 pp)
- **Suresse Direkt Bank** (DE): 3.7 % vs. EZB 0.51 % (+3.19 pp)
- **Bigbank** (DE): 4.15 % vs. EZB 0.51 % (+3.64 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Renault Bank** (FR): 4.1 % vs. EZB 0.05 % (+4.05 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Volkswagen Bank** (DE): 3.75 % vs. EZB 0.51 % (+3.24 pp)
- **Besonderheiten** (DE): 4.25 % vs. EZB 0.51 % (+3.74 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.51 % (+3.74 pp)
- **Advanzia** (DE): 3.85 % vs. EZB 0.51 % (+3.34 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.51 % (+3.44 pp)

## Heute nicht gefunden - als stale behalten (65)

- **Sprawdzamy kredyty konsolidacyjne** (PL), stale seit 2026-09-26 (14 Tage)
- **Openbank Girokonto +** (DE), stale seit 2026-10-07 (3 Tage)
- **BBVA** (DE), stale seit 2026-10-01 (9 Tage)
- **MyInvestor** (ES), stale seit 2026-10-09 (1 Tage)
- **Brocc Finance** (SE), stale seit 2026-10-09 (1 Tage)
- **SBAB Bank** (SE), stale seit 2026-10-08 (2 Tage)
- **CreditPlus** (DE), stale seit 2026-10-07 (3 Tage)
- **SIGNAL IDUNA** (DE), stale seit 2026-09-30 (10 Tage)
- **Danske Bank** (SE), stale seit 2026-10-08 (2 Tage)
- **Postbank** (DE), stale seit 2026-09-27 (13 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-09-30 (10 Tage)
- **Northmill Bank** (SE), stale seit 2026-10-09 (1 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-30 (10 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-09-30 (10 Tage)
- **Banco do Brasil** (DE), stale seit 2026-10-01 (9 Tage)
- **Handelsbanken** (SE), stale seit 2026-10-08 (2 Tage)
- **Moank** (SE), stale seit 2026-10-08 (2 Tage)
- **Raisin RenteBoost** (DE), stale seit 2026-10-05 (5 Tage)
- **Multitude Bank 2,55** (MT), stale seit 2026-09-30 (10 Tage)
- **Plus** (SE), stale seit 2026-10-08 (2 Tage)
- **Raisin** (DE), stale seit 2026-09-27 (13 Tage)
- **Trade Republic** (NL), stale seit 2026-10-08 (2 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-09-30 (10 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-09-30 (10 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-09-30 (10 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-09-30 (10 Tage)
- **Serafim Finans** (SE), stale seit 2026-10-08 (2 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-09-30 (10 Tage)
- **Fedelta** (SE), stale seit 2026-09-30 (10 Tage)
- **Swedbank** (SE), stale seit 2026-10-08 (2 Tage)
- **Nordea** (SE), stale seit 2026-10-08 (2 Tage)
- **SEB** (SE), stale seit 2026-10-08 (2 Tage)
- **Skandia** (SE), stale seit 2026-10-08 (2 Tage)
- **Bank Norwegian 1,75** (SE), stale seit 2026-09-30 (10 Tage)
- **LEP (Livret d’Épargne Populaire)** (FR), stale seit 2026-09-29 (11 Tage)
- **LEP (sous conditions de revenus)** (FR), stale seit 2026-09-29 (11 Tage)
- **wiLLBe** (LI), stale seit 2026-09-29 (11 Tage)
- **Avida Bank AB** (SE), stale seit 2026-10-05 (5 Tage)
- **Avida Finans 2,00** (SE), stale seit 2026-09-30 (10 Tage)
- **finvesto** (DE), stale seit 2026-09-28 (12 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-10-08 (2 Tage)
- **Distingo** (DE), stale seit 2026-09-27 (13 Tage)
- **BW-Bank** (DE), stale seit 2026-10-05 (5 Tage)
- **Avarda Bank** (SE), stale seit 2026-10-05 (5 Tage)
- **Collector Bank** (SE), stale seit 2026-10-05 (5 Tage)
- **IKB Deutsche Industriebank** (DE), stale seit 2026-10-05 (5 Tage)
- **SimpleSave** (IE), stale seit 2026-10-01 (9 Tage)
- **Yapi Kredi** (DE), stale seit 2026-09-27 (13 Tage)
- **Banca Progetto** (IT), stale seit 2026-10-07 (3 Tage)
- **Santander Consumer Bank** (DE), stale seit 2026-09-27 (13 Tage)
- **Banca CF+** (IT), stale seit 2026-09-27 (13 Tage)
- **Nexent-Bank** (DE), stale seit 2026-09-27 (13 Tage)
- **Livret Jeune ≥** (FR), stale seit 2026-09-29 (11 Tage)
- **xtb** (DE), stale seit 2026-10-04 (6 Tage)
- **Allgemeine Beamtenbank** (DE), stale seit 2026-09-27 (13 Tage)
- **Targobank** (DE), stale seit 2026-09-27 (13 Tage)
- **Ekobanken** (SE), stale seit 2026-10-08 (2 Tage)
- **MIEDŹ** (PL), stale seit 2026-09-28 (12 Tage)
- **ROPA** (PL), stale seit 2026-09-28 (12 Tage)
- **BITCOIN** (PL), stale seit 2026-09-28 (12 Tage)
- **ZŁOTO** (PL), stale seit 2026-09-27 (13 Tage)
- **EUR/PLN** (PL), stale seit 2026-09-27 (13 Tage)
- **CHF/PLN** (PL), stale seit 2026-09-28 (12 Tage)
- **USD/PLN** (PL), stale seit 2026-09-28 (12 Tage)
- **EUR/USD** (PL), stale seit 2026-09-28 (12 Tage)

## Neu hinzugekommen (10)

- **Raisin RenteBoost** (NL): 3.05 %
- **Santander Consumer Bank** (NL): 3.01 %
- **Banca Progetto** (NL): 2.4 %
- **Banca CF+** (NL): 2.35 %
- **Avarda Bank** (NL): 2.3 %
- **Collector Bank** (NL): 2.3 %
- **IKB Deutsche Industriebank** (NL): 2.3 %
- **BW-Bank** (NL): 2.26 %
- **Collector Bank** (DE): 2.2 %
- **Northmill Bank** (DE): 2.07 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
