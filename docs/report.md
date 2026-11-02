# Lauf-Report 2026-11-02

Erstellt: 2026-11-02T14:55:06+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 19 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 9 |
| Rohtreffer | 320 |
| Angebote nach Dedupe | 188 |
| Angebote im Ergebnis | 188 |
| davon stale | 27 |
| Laufzeit (s) | 122.2 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 188 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 12 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 7 |  |
| finanzfluss.de | 2 | css_heuristik | 14 |  |
| durchblicker.at | - | - | 0 | HTTP 403 |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 8 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | HTTP 403 |
| bankier.pl | 2 | css_heuristik | 7 |  |
| compricer.se | 2 | css_heuristik | 46 |  |
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
| verivox.de | 2 | css_heuristik | 22 |  |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 46 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 2 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **ROPA** (PL): 0.91 % -> 6.27 % (+5.36 pp) [Quelle: bankier.pl]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (24)

- **Hamburg Direct Bank** (DE): 3.82 % vs. EZB 0.52 % (+3.3 pp)
- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **ING Deutschland** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Volkswagen Bank** (DE): 3.75 % vs. EZB 0.52 % (+3.23 pp)
- **Cronbank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **SWK Bank** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **pbb direkt** (DE): 3.55 % vs. EZB 0.52 % (+3.03 pp)
- **Raisin RenteBoost** (NL): 3.3 % vs. EZB 0.15 % (+3.15 pp)
- **Ferratum Bank** (DE): 3.8 % vs. EZB 0.52 % (+3.28 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.52 % (+3.68 pp)
- **Crédit Agricole** (DE): 4.1 % vs. EZB 0.52 % (+3.58 pp)
- **Suresse Direkt Bank** (DE): 3.8 % vs. EZB 0.52 % (+3.28 pp)
- **Distingo** (DE): 3.95 % vs. EZB 0.52 % (+3.43 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Bigbank** (DE): 3.9 % vs. EZB 0.52 % (+3.38 pp)
- **CA Savings (Crédit Agricole)** (FR): 4.1 % vs. EZB 0.05 % (+4.05 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.52 % (+3.73 pp)
- **Advanzia** (DE): 4.1 % vs. EZB 0.52 % (+3.58 pp)
- **DKB** (DE): 4.0 % vs. EZB 0.52 % (+3.48 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.52 % (+3.43 pp)
- **XTB** (DE): 4.5 % vs. EZB 0.52 % (+3.98 pp)

## Heute nicht gefunden - als stale behalten (26)

- **SIGNAL IDUNA** (DE), stale seit 2026-10-27 (6 Tage)
- **Multitude Bank 2,60** (SE), stale seit 2026-10-31 (2 Tage)
- **MyInvestor** (ES), stale seit 2026-11-01 (1 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-10-31 (2 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-10-25 (8 Tage)
- **Ikano Bank 1,40** (SE), stale seit 2026-10-31 (2 Tage)
- **Kommunalkredit Invest** (AT), stale seit 2026-10-23 (10 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-10-31 (2 Tage)
- **Multitude Bank 2,60** (MT), stale seit 2026-10-31 (2 Tage)
- **RiverBank** (LU), stale seit 2026-10-28 (5 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-10-31 (2 Tage)
- **Northmill Bank 2,00** (SE), stale seit 2026-10-31 (2 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-10-31 (2 Tage)
- **Raisin StartZins** (DE), stale seit 2026-10-19 (14 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-10-31 (2 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-10-31 (2 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-10-29 (4 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-10-31 (2 Tage)
- **Resurs Bank 2,35** (SE), stale seit 2026-10-31 (2 Tage)
- **Avida Finans** (SE), stale seit 2026-10-20 (13 Tage)
- **Qred Bank AB** (SE), stale seit 2026-10-28 (5 Tage)
- **Yapi Kredi Deutschland** (DE), stale seit 2026-10-22 (11 Tage)
- **Sambla** (SE), stale seit 2026-10-31 (2 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-10-21 (12 Tage)
- **ViViBanca** (IT), stale seit 2026-10-25 (8 Tage)
- **EUR/PLN** (PL), stale seit 2026-10-29 (4 Tage)

## Zu lange stale - entfernt (3)

- **Lokata na**
- **Saldo Bank 2,80**
- **Carrefour Banque**

## Neu hinzugekommen (3)

- **FCM Bank** (NL): 2.43 %
- **Avida Finans** (DE): 2.37 %
- **Carrefour Banque** (NL): 2.35 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
