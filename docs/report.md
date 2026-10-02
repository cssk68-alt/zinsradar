# Lauf-Report 2026-10-02

Erstellt: 2026-10-02T12:00:13+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 21 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 7 |
| Rohtreffer | 306 |
| Angebote nach Dedupe | 208 |
| Angebote im Ergebnis | 208 |
| davon stale | 56 |
| Laufzeit (s) | 123.2 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 208 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 5 |  |
| finanzfluss.de | 2 | css_heuristik | 15 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 49 |  |
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
| spaarrente.nl | 2 | css_heuristik | 49 |  |
| compricer.se | 2 | css_heuristik | 46 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* verworfen (Altwert-Ausreisser): Koniec mit 7.0 % liegt ueber der Grenze 6.38 % (1,5x bester frischer Wert)
* Land-Dopplungen im Altbestand aufgeloest: 3 Eintraege verschmolzen

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (14)

- **Consorsbank** (FR): 3.8 % vs. EZB 0.05 % (+3.75 pp)
- **MyInvestor** (ES): 3.25 % vs. EZB 0.16 % (+3.09 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.51 % (+3.69 pp)
- **Suresse Direkt Bank** (DE): 3.7 % vs. EZB 0.51 % (+3.19 pp)
- **Bigbank** (DE): 4.15 % vs. EZB 0.51 % (+3.64 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (DE): 4.0 % vs. EZB 0.51 % (+3.49 pp)
- **Openbank** (ES): 4.0 % vs. EZB 0.16 % (+3.84 pp)
- **Hamburg Direct Bank** (DE): 3.61 % vs. EZB 0.51 % (+3.1 pp)
- **Besonderheiten** (DE): 4.25 % vs. EZB 0.51 % (+3.74 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.51 % (+3.74 pp)
- **Advanzia** (DE): 3.85 % vs. EZB 0.51 % (+3.34 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.51 % (+3.44 pp)

## Heute nicht gefunden - als stale behalten (57)

- **Koniec** (PL), stale seit 2026-10-01 (1 Tage)
- **Brad Pitt daje** (PL), stale seit 2026-09-22 (10 Tage)
- **Nawet** (PL), stale seit 2026-09-24 (8 Tage)
- **Zamień 0 na** (PL), stale seit 2026-09-24 (8 Tage)
- **Do 300 zł za konto** (PL), stale seit 2026-09-22 (10 Tage)
- **Sprawdzamy kredyty konsolidacyjne** (PL), stale seit 2026-09-26 (6 Tage)
- **BBVA** (DE), stale seit 2026-10-01 (1 Tage)
- **Brocc Finance 0,05** (SE), stale seit 2026-09-30 (2 Tage)
- **SIGNAL IDUNA** (DE), stale seit 2026-09-30 (2 Tage)
- **RiverBank** (LU), stale seit 2026-10-01 (1 Tage)
- **SWK Bank** (DE), stale seit 2026-09-28 (4 Tage)
- **IKB** (DE), stale seit 2026-09-22 (10 Tage)
- **Postbank** (DE), stale seit 2026-09-27 (5 Tage)
- **Ikano Bank 1,15** (SE), stale seit 2026-09-30 (2 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-30 (2 Tage)
- **Nordax Bank 1,80** (SE), stale seit 2026-09-30 (2 Tage)
- **Banco do Brasil** (DE), stale seit 2026-10-01 (1 Tage)
- **Kommunalkredit Invest** (AT), stale seit 2026-09-22 (10 Tage)
- **Multitude Bank 2,55** (MT), stale seit 2026-09-30 (2 Tage)
- **Raisin** (DE), stale seit 2026-09-27 (5 Tage)
- **Aros Kapital 2,00** (SE), stale seit 2026-09-30 (2 Tage)
- **JAK Medlemsbank 1,50** (SE), stale seit 2026-09-30 (2 Tage)
- **Bankaktiebolaget Nordiska 2,10** (SE), stale seit 2026-09-30 (2 Tage)
- **Bluestep Bank 0,45** (SE), stale seit 2026-09-30 (2 Tage)
- **Northmill Bank 1,80** (SE), stale seit 2026-09-30 (2 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-30 (2 Tage)
- **Svea Bank 1,80** (SE), stale seit 2026-09-30 (2 Tage)
- **Fedelta** (SE), stale seit 2026-09-30 (2 Tage)
- **Bank Norwegian 1,75** (SE), stale seit 2026-09-30 (2 Tage)
- **LEP (Livret d’Épargne Populaire)** (FR), stale seit 2026-09-29 (3 Tage)
- **LEP (sous conditions de revenus)** (FR), stale seit 2026-09-29 (3 Tage)
- **wiLLBe** (LI), stale seit 2026-09-29 (3 Tage)
- **0TO9** (SE), stale seit 2026-10-01 (1 Tage)
- **Avida Finans 2,00** (SE), stale seit 2026-09-30 (2 Tage)
- **finvesto** (DE), stale seit 2026-09-28 (4 Tage)
- **Distingo** (DE), stale seit 2026-09-27 (5 Tage)
- **Grenke Bank** (DE), stale seit 2026-09-23 (9 Tage)
- **SimpleSave** (IE), stale seit 2026-10-01 (1 Tage)
- **Yapi Kredi** (DE), stale seit 2026-09-27 (5 Tage)
- **Carrefour Banque** (FR), stale seit 2026-09-29 (3 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-09-22 (10 Tage)
- **FIMBank** (MT), stale seit 2026-09-22 (10 Tage)
- **Santander Consumer Bank** (DE), stale seit 2026-09-27 (5 Tage)
- **Stellantis Direktbank** (DE), stale seit 2026-09-21 (11 Tage)
- **Banca CF+** (IT), stale seit 2026-09-27 (5 Tage)
- **Nexent-Bank** (DE), stale seit 2026-09-27 (5 Tage)
- **Livret Jeune ≥** (FR), stale seit 2026-09-29 (3 Tage)
- **Allgemeine Beamtenbank** (DE), stale seit 2026-09-27 (5 Tage)
- **Targobank** (DE), stale seit 2026-09-27 (5 Tage)
- **MIEDŹ** (PL), stale seit 2026-09-28 (4 Tage)
- **ROPA** (PL), stale seit 2026-09-28 (4 Tage)
- **BITCOIN** (PL), stale seit 2026-09-28 (4 Tage)
- **ZŁOTO** (PL), stale seit 2026-09-27 (5 Tage)
- **EUR/PLN** (PL), stale seit 2026-09-27 (5 Tage)
- **CHF/PLN** (PL), stale seit 2026-09-28 (4 Tage)
- **USD/PLN** (PL), stale seit 2026-09-28 (4 Tage)
- **EUR/USD** (PL), stale seit 2026-09-28 (4 Tage)

## Neu hinzugekommen (4)

- **CreditPlus** (DE): 3.25 %
- **Santander Consumer Bank** (NL): 3.01 %
- **Banca CF+** (NL): 2.35 %
- **FCM Bank** (NL): 2.26 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
