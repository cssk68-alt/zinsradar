# Lauf-Report 2026-11-24

Erstellt: 2026-11-24T17:04:06+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 21 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 7 |
| Rohtreffer | 312 |
| Angebote nach Dedupe | 201 |
| Angebote im Ergebnis | 201 |
| davon stale | 37 |
| Laufzeit (s) | 138.4 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 201 |

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
| confrontaconti.it | - | - | 0 | HTTP 404 |
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

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (2)

- **MIEDŹ** (PL): 3.25 % -> 5.67 % (+2.42 pp) [Quelle: bankier.pl]
- **ROPA** (PL): 2.96 % -> 0.88 % (-2.08 pp) [Quelle: bankier.pl]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (26)

- **HVB** (DE): 3.76 % vs. EZB 0.52 % (+3.24 pp)
- **comdirect** (DE): 3.76 % vs. EZB 0.52 % (+3.24 pp)
- **Comdirect-Bank** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **ING Deutschland** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **GEFA Bank** (DE): 3.6 % vs. EZB 0.52 % (+3.08 pp)
- **SIGNAL IDUNA** (DE): 3.6 % vs. EZB 0.52 % (+3.08 pp)
- **SWK Bank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
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

## Heute nicht gefunden - als stale behalten (36)

- **VeloBank daje** (PL), stale seit 2026-11-20 (4 Tage)
- **Cronbank** (DE), stale seit 2026-11-20 (4 Tage)
- **KT Bank** (DE), stale seit 2026-11-20 (4 Tage)
- **IKB** (DE), stale seit 2026-11-10 (14 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-11-10 (14 Tage)
- **Qred** (SE), stale seit 2026-11-23 (1 Tage)
- **Brocc Finance** (SE), stale seit 2026-11-15 (9 Tage)
- **Ikano Bank** (SE), stale seit 2026-11-17 (7 Tage)
- **Raisin** (NL), stale seit 2026-11-21 (3 Tage)
- **SBAB Bank 1,25** (SE), stale seit 2026-11-10 (14 Tage)
- **Bankaktiebolaget Nordiska** (SE), stale seit 2026-11-10 (14 Tage)
- **Northmill Bank 2,00** (SE), stale seit 2026-11-12 (12 Tage)
- **JAK Medlemsbank** (SE), stale seit 2026-11-15 (9 Tage)
- **Svea Bank 2,00** (SE), stale seit 2026-11-19 (5 Tage)
- **Brixo** (SE), stale seit 2026-11-20 (4 Tage)
- **Aros Kapital** (SE), stale seit 2026-11-17 (7 Tage)
- **Bluestep Bank** (SE), stale seit 2026-11-11 (13 Tage)
- **PSD Bank RheinNeckarSaar** (DE), stale seit 2026-11-17 (7 Tage)
- **Plus** (SE), stale seit 2026-11-10 (14 Tage)
- **Serafim Finans 2,50** (SE), stale seit 2026-11-22 (2 Tage)
- **Resurs Bank 2,35** (SE), stale seit 2026-11-22 (2 Tage)
- **NIBC Weltsparwochen** (DE), stale seit 2026-11-18 (6 Tage)
- **Instabank ASA** (NO), stale seit 2026-11-22 (2 Tage)
- **Raisin Bank** (DE), stale seit 2026-11-18 (6 Tage)
- **0TO9** (SE), stale seit 2026-11-17 (7 Tage)
- **Wormser** (FR), stale seit 2026-11-18 (6 Tage)
- **FIMBank** (MT), stale seit 2026-11-22 (2 Tage)
- **Nordax Bank** (SE), stale seit 2026-11-16 (8 Tage)
- **Renault Bank direkt** (DE), stale seit 2026-11-23 (1 Tage)
- **Bank Norwegian** (SE), stale seit 2026-11-11 (13 Tage)
- **Qliro** (SE), stale seit 2026-11-12 (12 Tage)
- **LEP (Livret d’Épargne Populaire)** (FR), stale seit 2026-11-23 (1 Tage)
- **LEP (sous conditions de revenus)** (FR), stale seit 2026-11-23 (1 Tage)
- **Sambla** (SE), stale seit 2026-11-19 (5 Tage)
- **Livret Jeune ≥** (FR), stale seit 2026-11-23 (1 Tage)
- **XTB** (DE), stale seit 2026-11-16 (8 Tage)

## Zu lange stale - entfernt (1)

- **Ferratum Bank**

## Neu hinzugekommen (5)

- **comdirect** (DE): 3.76 %
- **Instabank** (DE): 2.6 %
- **ViViBanca** (IT): 2.75 %
- **Nordax Bank** (NL): 2.48 %
- **Ikano Bank** (DE): 3.91 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
