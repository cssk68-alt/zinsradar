# Lauf-Report 2026-10-11

Erstellt: 2026-10-11T12:13:45+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 21 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 7 |
| Rohtreffer | 296 |
| Angebote nach Dedupe | 202 |
| Angebote im Ergebnis | 202 |
| davon stale | 62 |
| Laufzeit (s) | 115.7 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 202 |

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
| tucapital.es | 2 | css_heuristik | 2 |  |
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

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (17)

- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **Hamburg Direct Bank** (DE): 3.62 % vs. EZB 0.51 % (+3.11 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
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

## Heute nicht gefunden - als stale behalten (62)

- **Openbank Girokonto +** (DE), stale seit 2026-10-07 (4 Tage)
- **BBVA** (DE), stale seit 2026-10-01 (10 Tage)
- **Brocc Finance** (SE), stale seit 2026-10-09 (2 Tage)
- **SBAB Bank** (SE), stale seit 2026-10-08 (3 Tage)
- **CreditPlus** (DE), stale seit 2026-10-07 (4 Tage)
- **SIGNAL IDUNA** (DE), stale seit 2026-09-30 (11 Tage)
- **Danske Bank** (SE), stale seit 2026-10-08 (3 Tage)
- **Postbank** (DE), stale seit 2026-09-27 (14 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-09-30 (11 Tage)
- **Northmill Bank** (SE), stale seit 2026-10-09 (2 Tage)
- **Saldo Bank** (SE), stale seit 2026-10-10 (1 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-09-30 (11 Tage)
- **Banco do Brasil** (DE), stale seit 2026-10-01 (10 Tage)
- **Handelsbanken** (SE), stale seit 2026-10-08 (3 Tage)
- **Moank** (SE), stale seit 2026-10-08 (3 Tage)
- **Raisin RenteBoost** (DE), stale seit 2026-10-05 (6 Tage)
- **Multitude Bank 2,55** (MT), stale seit 2026-09-30 (11 Tage)
- **Plus** (SE), stale seit 2026-10-08 (3 Tage)
- **Raisin** (DE), stale seit 2026-09-27 (14 Tage)
- **Trade Republic** (NL), stale seit 2026-10-08 (3 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-09-30 (11 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-09-30 (11 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-09-30 (11 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-09-30 (11 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-10-10 (1 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-09-30 (11 Tage)
- **Fedelta** (SE), stale seit 2026-09-30 (11 Tage)
- **Swedbank** (SE), stale seit 2026-10-08 (3 Tage)
- **Nordea** (SE), stale seit 2026-10-08 (3 Tage)
- **SEB** (SE), stale seit 2026-10-08 (3 Tage)
- **Bank Norwegian 1,75** (SE), stale seit 2026-09-30 (11 Tage)
- **LEP (Livret d’Épargne Populaire)** (FR), stale seit 2026-09-29 (12 Tage)
- **LEP (sous conditions de revenus)** (FR), stale seit 2026-09-29 (12 Tage)
- **wiLLBe** (LI), stale seit 2026-09-29 (12 Tage)
- **Avida Bank AB** (SE), stale seit 2026-10-05 (6 Tage)
- **Avida Finans 2,00** (SE), stale seit 2026-09-30 (11 Tage)
- **finvesto** (DE), stale seit 2026-09-28 (13 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-10-08 (3 Tage)
- **Distingo** (DE), stale seit 2026-09-27 (14 Tage)
- **BW-Bank** (DE), stale seit 2026-10-05 (6 Tage)
- **Avarda Bank** (SE), stale seit 2026-10-05 (6 Tage)
- **Collector Bank** (SE), stale seit 2026-10-05 (6 Tage)
- **IKB Deutsche Industriebank** (DE), stale seit 2026-10-05 (6 Tage)
- **SimpleSave** (IE), stale seit 2026-10-01 (10 Tage)
- **Yapi Kredi** (DE), stale seit 2026-09-27 (14 Tage)
- **Banca Progetto** (IT), stale seit 2026-10-07 (4 Tage)
- **Santander Consumer Bank** (DE), stale seit 2026-09-27 (14 Tage)
- **Banca CF+** (IT), stale seit 2026-09-27 (14 Tage)
- **Nexent-Bank** (DE), stale seit 2026-09-27 (14 Tage)
- **Livret Jeune ≥** (FR), stale seit 2026-09-29 (12 Tage)
- **xtb** (DE), stale seit 2026-10-04 (7 Tage)
- **Allgemeine Beamtenbank** (DE), stale seit 2026-09-27 (14 Tage)
- **Targobank** (DE), stale seit 2026-09-27 (14 Tage)
- **Ekobanken** (SE), stale seit 2026-10-08 (3 Tage)
- **MIEDŹ** (PL), stale seit 2026-09-28 (13 Tage)
- **ROPA** (PL), stale seit 2026-09-28 (13 Tage)
- **BITCOIN** (PL), stale seit 2026-09-28 (13 Tage)
- **ZŁOTO** (PL), stale seit 2026-09-27 (14 Tage)
- **EUR/PLN** (PL), stale seit 2026-09-27 (14 Tage)
- **CHF/PLN** (PL), stale seit 2026-09-28 (13 Tage)
- **USD/PLN** (PL), stale seit 2026-09-28 (13 Tage)
- **EUR/USD** (PL), stale seit 2026-09-28 (13 Tage)

## Zu lange stale - entfernt (1)

- **Sprawdzamy kredyty konsolidacyjne**

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
