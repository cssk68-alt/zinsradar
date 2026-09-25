# Lauf-Report 2026-09-25

Erstellt: 2026-09-25T11:19:36+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 1 |
| Quellen ohne Treffer | 7 |
| Rohtreffer | 319 |
| Angebote nach Dedupe | 202 |
| Angebote im Ergebnis | 202 |
| davon stale | 31 |
| Laufzeit (s) | 142.2 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 202 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 11 |  |
| check24.de | 2 | css_heuristik | 4 |  |
| biallo.de | 2 | css_heuristik | 7 |  |
| finanzfluss.de | 2 | css_heuristik | 31 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 50 |  |
| raisin.nl | 2 | css_heuristik | 10 |  |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 7 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | robots.txt nicht erreichbar: ConnectTimeout |
| bankier.pl | 2 | css_heuristik | 10 |  |
| compricer.se | 2 | css_heuristik | 46 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | 2 | css_heuristik | 2 |  |
| openbank.de | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| klarna.com | - | - | 0 | S1/json_endpoint: HTTP 202; S1/jsonld: kein <script type=application/ld+json> gefunden; S2/css_konfiguriert: c |
| tagesgeld.info | 2 | css_heuristik | 24 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 12 |  |
| finanztip.de | 2 | css_heuristik | 9 |  |
| spaarrente.nl | 2 | css_heuristik | 50 |  |
| compricer.se | 2 | css_heuristik | 47 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 7 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **xtb** (DE): 0.9 % -> 3.5 % (+2.6 pp) [Quelle: finanzfluss.de]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (12)

- **BBVA** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)
- **Consorsbank** (FR): 3.6 % vs. EZB 0.04 % (+3.56 pp)
- **Trading** (DE): 4.2 % vs. EZB 0.5 % (+3.7 pp)
- **Suresse Direkt Bank** (DE): 3.7 % vs. EZB 0.5 % (+3.2 pp)
- **Bigbank** (DE): 4.15 % vs. EZB 0.5 % (+3.65 pp)
- **Leaseplan Bank** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Hamburg Direct Bank** (DE): 3.61 % vs. EZB 0.5 % (+3.11 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.5 % (+3.75 pp)
- **Opel Bank** (DE): 3.95 % vs. EZB 0.5 % (+3.45 pp)
- **ING** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)
- **Allgemeine Beamtenbank** (DE): 3.55 % vs. EZB 0.5 % (+3.05 pp)

## Heute nicht gefunden - als stale behalten (30)

- **Brad Pitt daje** (PL), stale seit 2026-09-22 (3 Tage)
- **Lokata na** (PL), stale seit 2026-09-12 (13 Tage)
- **Nawet** (PL), stale seit 2026-09-24 (1 Tage)
- **Zamień 0 na** (PL), stale seit 2026-09-24 (1 Tage)
- **Do 300 zł za konto** (PL), stale seit 2026-09-22 (3 Tage)
- **IKB** (DE), stale seit 2026-09-22 (3 Tage)
- **Aareal Bank** (DE), stale seit 2026-09-16 (9 Tage)
- **Saldo Bank 2,80** (SE), stale seit 2026-09-17 (8 Tage)
- **Kommunalkredit Invest** (AT), stale seit 2026-09-22 (3 Tage)
- **Ferratum Bank** (DE), stale seit 2026-09-14 (11 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-19 (6 Tage)
- **Serafim Finans 2,35** (SE), stale seit 2026-09-19 (6 Tage)
- **Klarna** (SE), stale seit 2026-09-11 (14 Tage)
- **Instabank ASA** (NO), stale seit 2026-09-24 (1 Tage)
- **0TO9** (SE), stale seit 2026-09-22 (3 Tage)
- **Grenke Bank** (DE), stale seit 2026-09-23 (2 Tage)
- **BW-Bank** (DE), stale seit 2026-09-24 (1 Tage)
- **Collector Bank** (SE), stale seit 2026-09-22 (3 Tage)
- **FCM Bank Ltd.** (MT), stale seit 2026-09-22 (3 Tage)
- **FIMBank** (MT), stale seit 2026-09-22 (3 Tage)
- **Inbank** (EE), stale seit 2026-09-16 (9 Tage)
- **Stellantis Direktbank** (DE), stale seit 2026-09-21 (4 Tage)
- **USD/PLN** (PL), stale seit 2026-09-23 (2 Tage)
- **ZŁOTO** (PL), stale seit 2026-09-23 (2 Tage)
- **EUR/PLN** (PL), stale seit 2026-09-23 (2 Tage)
- **BITCOIN** (PL), stale seit 2026-09-23 (2 Tage)
- **CHF/PLN** (PL), stale seit 2026-09-23 (2 Tage)
- **EUR/USD** (PL), stale seit 2026-09-23 (2 Tage)
- **MIEDŹ** (PL), stale seit 2026-09-23 (2 Tage)
- **ROPA** (PL), stale seit 2026-09-23 (2 Tage)

## Zu lange stale - entfernt (12)

- **JAK Medlemsbank Sparränta 1,50**
- **Handelsbanken Sparränta 0,05**
- **Moank Sparränta 2,40**
- **SEB Sparränta 1,70**
- **Swedbank Sparränta 1,75**
- **Nordea Sparränta 1,75**
- **Lunar Sparränta**
- **Lantmännen Finans Sparränta**
- **Ekobanken Sparränta 1,15**
- **Nordnet Sparränta**
- **Avanza Bank Sparränta**
- **ICA Banken Sparränta**

## Neu hinzugekommen (8)

- **Klarna** (NL): 3.0 %
- **Sambla** (SE): 2.35 %
- **Instabank** (DE): 2.27 %
- **FCM Bank** (NL): 2.26 %
- **BW-Bank** (NL): 2.2 %
- **Collector Bank** (DE): 2.2 %
- **Inbank** (NL): 2.2 %
- **FCM Bank** (DE): 3.15 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
