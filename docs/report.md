# Lauf-Report 2026-11-07

Erstellt: 2026-11-07T12:34:22+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 19 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 9 |
| Rohtreffer | 296 |
| Angebote nach Dedupe | 190 |
| Angebote im Ergebnis | 190 |
| davon stale | 39 |
| Laufzeit (s) | 138.0 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 190 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 12 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 7 |  |
| finanzfluss.de | 2 | css_heuristik | 15 |  |
| durchblicker.at | - | - | 0 | HTTP 403 |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 8 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | 2 | css_heuristik | 2 |  |
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
| tagesgeld.info | 2 | css_heuristik | 25 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | - | - | 0 | HTTP 403 |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 47 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 4 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (22)

- **Hamburg Direct Bank** (DE): 3.82 % vs. EZB 0.52 % (+3.3 pp)
- **HVB** (DE): 3.76 % vs. EZB 0.52 % (+3.24 pp)
- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **ING Deutschland** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Volkswagen Bank** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Cronbank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **SWK Bank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **pbb direkt** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
- **Raisin RenteBoost** (NL): 3.3 % vs. EZB 0.15 % (+3.15 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.52 % (+3.68 pp)
- **Crédit Agricole** (DE): 4.1 % vs. EZB 0.52 % (+3.58 pp)
- **Suresse Direkt Bank** (DE): 3.8 % vs. EZB 0.52 % (+3.28 pp)
- **Distingo** (DE): 3.95 % vs. EZB 0.52 % (+3.43 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Bigbank** (DE): 3.9 % vs. EZB 0.52 % (+3.38 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Advanzia** (DE): 4.1 % vs. EZB 0.52 % (+3.58 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.52 % (+3.43 pp)
- **ING** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)

## Heute nicht gefunden - als stale behalten (39)

- **SIGNAL IDUNA** (DE), stale seit 2026-10-27 (11 Tage)
- **Multitude Bank** (SE), stale seit 2026-11-04 (3 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-10-31 (7 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-10-25 (13 Tage)
- **Ikano Bank 1,40** (SE), stale seit 2026-10-31 (7 Tage)
- **Multitude Bank** (MT), stale seit 2026-11-04 (3 Tage)
- **Ferratum Bank** (DE), stale seit 2026-11-02 (5 Tage)
- **RiverBank** (LU), stale seit 2026-10-28 (10 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-10-31 (7 Tage)
- **Northmill Bank 2,00** (SE), stale seit 2026-10-31 (7 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-10-31 (7 Tage)
- **CA Savings (Crédit Agricole)** (FR), stale seit 2026-11-06 (1 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-10-31 (7 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-10-31 (7 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-10-29 (9 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-10-31 (7 Tage)
- **Ferratum (Multitude Bank)** (MT), stale seit 2026-11-06 (1 Tage)
- **Serafim Finans** (SE), stale seit 2026-11-02 (5 Tage)
- **Resurs Bank 2,35** (SE), stale seit 2026-10-31 (7 Tage)
- **Ascory Bank** (DE), stale seit 2026-11-06 (1 Tage)
- **Skandia** (SE), stale seit 2026-11-06 (1 Tage)
- **Nordax Bank** (SE), stale seit 2026-11-06 (1 Tage)
- **0TO9** (SE), stale seit 2026-11-04 (3 Tage)
- **YapiKredi Deutschland** (DE), stale seit 2026-11-06 (1 Tage)
- **Sambla** (SE), stale seit 2026-10-31 (7 Tage)
- **Banca CF+** (IT), stale seit 2026-11-05 (2 Tage)
- **Revolut** (DE), stale seit 2026-11-06 (1 Tage)
- **ViViBanca** (IT), stale seit 2026-10-25 (13 Tage)
- **Advanzia Bank** (LU), stale seit 2026-11-06 (1 Tage)
- **DKB** (DE), stale seit 2026-11-04 (3 Tage)
- **ZŁOTO** (PL), stale seit 2026-11-06 (1 Tage)
- **XTB** (DE), stale seit 2026-11-06 (1 Tage)
- **EUR/USD** (PL), stale seit 2026-11-06 (1 Tage)
- **USD/PLN** (PL), stale seit 2026-11-06 (1 Tage)
- **MIEDŹ** (PL), stale seit 2026-11-06 (1 Tage)
- **ROPA** (PL), stale seit 2026-11-06 (1 Tage)
- **CHF/PLN** (PL), stale seit 2026-11-04 (3 Tage)
- **BITCOIN** (PL), stale seit 2026-11-06 (1 Tage)
- **EUR/PLN** (PL), stale seit 2026-11-06 (1 Tage)

## Zu lange stale - entfernt (1)

- **Kommunalkredit Invest**

## Neu hinzugekommen (6)

- **KT Bank** (DE): 3.5 %
- **Fedelta** (SE): 3.05 %
- **Advanzia Bank** (DE): 2.71 %
- **Banca CF+** (NL): 2.5 %
- **Nordax Bank** (NL): 2.45 %
- **Revolut** (NL): 1.25 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
