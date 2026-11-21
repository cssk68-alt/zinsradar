# Lauf-Report 2026-11-21

Erstellt: 2026-11-21T14:19:49+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 21 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 7 |
| Rohtreffer | 304 |
| Angebote nach Dedupe | 191 |
| Angebote im Ergebnis | 191 |
| davon stale | 33 |
| Laufzeit (s) | 122.0 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 191 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 7 |  |
| finanzfluss.de | 2 | css_heuristik | 15 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 13 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | 2 | css_heuristik | 2 |  |
| bankier.pl | 2 | css_heuristik | 8 |  |
| compricer.se | 2 | css_heuristik | 47 |  |
| bankinter.pt | - | - | 0 | HTTP 404 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | - | - | 0 | HTTP 404 |
| openbank.de | 2 | css_heuristik | 2 |  |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 24 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 16 |  |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 47 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 4 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (25)

- **HVB** (DE): 3.76 % vs. EZB 0.52 % (+3.24 pp)
- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **ING Deutschland** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **GEFA Bank** (DE): 3.6 % vs. EZB 0.52 % (+3.08 pp)
- **SIGNAL IDUNA** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **SWK Bank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
- **Raisin** (NL): 3.3 % vs. EZB 0.15 % (+3.15 pp)
- **Raisin RenteBoost** (NL): 3.3 % vs. EZB 0.15 % (+3.15 pp)
- **Joe Broker (Targobank)** (DE): 4.2 % vs. EZB 0.52 % (+3.68 pp)
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
- **XTB Broker** (DE): 4.5 % vs. EZB 0.52 % (+3.98 pp)

## Heute nicht gefunden - als stale behalten (33)

- **VeloBank daje** (PL), stale seit 2026-11-20 (1 Tage)
- **Cronbank** (DE), stale seit 2026-11-20 (1 Tage)
- **KT Bank** (DE), stale seit 2026-11-20 (1 Tage)
- **IKB** (DE), stale seit 2026-11-10 (11 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-11-10 (11 Tage)
- **Brocc Finance** (SE), stale seit 2026-11-15 (6 Tage)
- **Ikano Bank** (SE), stale seit 2026-11-17 (4 Tage)
- **SBAB Bank 1,25** (SE), stale seit 2026-11-10 (11 Tage)
- **Ferratum Bank** (DE), stale seit 2026-11-09 (12 Tage)
- **Bankaktiebolaget Nordiska** (SE), stale seit 2026-11-10 (11 Tage)
- **Northmill Bank** (SE), stale seit 2026-11-07 (14 Tage)
- **Northmill Bank 2,00** (SE), stale seit 2026-11-12 (9 Tage)
- **JAK Medlemsbank** (SE), stale seit 2026-11-15 (6 Tage)
- **Svea Bank 2,00** (SE), stale seit 2026-11-19 (2 Tage)
- **Suresse Direkt Bank** (DE), stale seit 2026-11-08 (13 Tage)
- **Brixo** (SE), stale seit 2026-11-20 (1 Tage)
- **Aros Kapital** (SE), stale seit 2026-11-17 (4 Tage)
- **Bluestep Bank** (SE), stale seit 2026-11-11 (10 Tage)
- **PSD Bank RheinNeckarSaar** (DE), stale seit 2026-11-17 (4 Tage)
- **Plus** (SE), stale seit 2026-11-10 (11 Tage)
- **Serafim Finans** (SE), stale seit 2026-11-17 (4 Tage)
- **NIBC Weltsparwochen** (DE), stale seit 2026-11-18 (3 Tage)
- **Skandia** (SE), stale seit 2026-11-20 (1 Tage)
- **Raisin Bank** (DE), stale seit 2026-11-18 (3 Tage)
- **0TO9** (SE), stale seit 2026-11-17 (4 Tage)
- **Wormser** (FR), stale seit 2026-11-18 (3 Tage)
- **Nordax Bank** (SE), stale seit 2026-11-16 (5 Tage)
- **Bank Norwegian** (SE), stale seit 2026-11-11 (10 Tage)
- **Qliro** (SE), stale seit 2026-11-12 (9 Tage)
- **Carrefour Banque** (NL), stale seit 2026-11-08 (13 Tage)
- **Sambla** (SE), stale seit 2026-11-19 (2 Tage)
- **Banca Progetto** (IT), stale seit 2026-11-18 (3 Tage)
- **XTB** (DE), stale seit 2026-11-16 (5 Tage)

## Zu lange stale - entfernt (7)

- **ZŁOTO**
- **EUR/USD**
- **USD/PLN**
- **MIEDŹ**
- **ROPA**
- **BITCOIN**
- **EUR/PLN**

## Neu hinzugekommen (5)

- **Kommunalkredit Invest** (AT): 3.4 %
- **Banca Progetto** (NL): 2.55 %
- **Nordax Bank** (DE): 2.51 %
- **Nordax Bank** (NL): 2.45 %
- **Ikano Bank** (DE): 3.91 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
