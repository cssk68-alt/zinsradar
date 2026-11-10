# Lauf-Report 2026-11-10

Erstellt: 2026-11-10T14:30:52+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 310 |
| Angebote nach Dedupe | 190 |
| Angebote im Ergebnis | 190 |
| davon stale | 32 |
| Laufzeit (s) | 249.6 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 190 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 12 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 8 |  |
| finanzfluss.de | 2 | css_heuristik | 15 |  |
| durchblicker.at | - | - | 0 | HTTP 403 |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 8 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | 2 | css_heuristik | 2 |  |
| bankier.pl | 2 | css_heuristik | 10 |  |
| compricer.se | 2 | css_heuristik | 47 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | - | - | 0 | HTTP 404 |
| openbank.de | 2 | css_heuristik | 2 |  |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 25 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 15 |  |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 47 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 4 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (24)

- **HVB** (DE): 3.76 % vs. EZB 0.52 % (+3.24 pp)
- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **ING Deutschland** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Volkswagen Bank** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Cronbank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **SWK Bank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **pbb direkt** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
- **Raisin RenteBoost** (NL): 3.3 % vs. EZB 0.15 % (+3.15 pp)
- **Crédit Agricole** (DE): 4.1 % vs. EZB 0.52 % (+3.58 pp)
- **CA Savings (Crédit Agricole)** (FR): 4.1 % vs. EZB 0.05 % (+4.05 pp)
- **Distingo** (DE): 3.95 % vs. EZB 0.52 % (+3.43 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Bigbank** (DE): 3.9 % vs. EZB 0.52 % (+3.38 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Hamburg Direct Bank** (DE): 3.81 % vs. EZB 0.52 % (+3.29 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.52 % (+3.73 pp)
- **Advanzia** (DE): 4.1 % vs. EZB 0.52 % (+3.58 pp)
- **Ikano Bank** (DE): 3.91 % vs. EZB 0.52 % (+3.39 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.52 % (+3.43 pp)
- **ING** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **XTB** (DE): 4.5 % vs. EZB 0.52 % (+3.98 pp)

## Heute nicht gefunden - als stale behalten (32)

- **Saldo Bank** (SE), stale seit 2026-11-09 (1 Tage)
- **SIGNAL IDUNA** (DE), stale seit 2026-10-27 (14 Tage)
- **Multitude Bank** (SE), stale seit 2026-11-04 (6 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-10-31 (10 Tage)
- **Ikano Bank** (SE), stale seit 2026-11-08 (2 Tage)
- **Multitude Bank** (MT), stale seit 2026-11-04 (6 Tage)
- **Qred** (SE), stale seit 2026-11-08 (2 Tage)
- **Ferratum Bank** (DE), stale seit 2026-11-09 (1 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-10-31 (10 Tage)
- **Northmill Bank** (SE), stale seit 2026-11-07 (3 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-10-31 (10 Tage)
- **Suresse Direkt Bank** (DE), stale seit 2026-11-08 (2 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-10-31 (10 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-10-31 (10 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-10-29 (12 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-10-31 (10 Tage)
- **Serafim Finans 2,50** (SE), stale seit 2026-11-08 (2 Tage)
- **Resurs Bank 2,35** (SE), stale seit 2026-10-31 (10 Tage)
- **Instabank ASA** (NO), stale seit 2026-11-08 (2 Tage)
- **0TO9** (SE), stale seit 2026-11-04 (6 Tage)
- **Carrefour Banque** (NL), stale seit 2026-11-08 (2 Tage)
- **Sambla** (SE), stale seit 2026-10-31 (10 Tage)
- **Banca CF+** (IT), stale seit 2026-11-05 (5 Tage)
- **DKB** (DE), stale seit 2026-11-04 (6 Tage)
- **ZŁOTO** (PL), stale seit 2026-11-06 (4 Tage)
- **EUR/USD** (PL), stale seit 2026-11-06 (4 Tage)
- **USD/PLN** (PL), stale seit 2026-11-06 (4 Tage)
- **MIEDŹ** (PL), stale seit 2026-11-06 (4 Tage)
- **ROPA** (PL), stale seit 2026-11-06 (4 Tage)
- **CHF/PLN** (PL), stale seit 2026-11-04 (6 Tage)
- **BITCOIN** (PL), stale seit 2026-11-06 (4 Tage)
- **EUR/PLN** (PL), stale seit 2026-11-06 (4 Tage)

## Neu hinzugekommen (5)

- **Saldo Bank 2,80** (SE): 3.45 %
- **Banca CF+** (NL): 2.5 %
- **Instabank** (DE): 2.45 %
- **Northmill Bank** (DE): 2.3 %
- **Ikano Bank** (DE): 3.91 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
