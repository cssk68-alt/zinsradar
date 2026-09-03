# Lauf-Report 2026-09-03

Erstellt: 2026-09-03T16:39:14+00:00

## Zusammenfassung

| Kennzahl | Wert |
| --- | ---: |
| Quellen gesamt | 28 |
| Quellen mit Treffer | 20 |
| Quellen durch robots.txt uebersprungen | 0 |
| Quellen ohne Treffer | 8 |
| Rohtreffer | 309 |
| Angebote nach Dedupe | 171 |
| Angebote im Ergebnis | 171 |
| davon stale | 29 |
| Laufzeit (s) | 139.1 |

### Extraktionsstufen

| Stufe | Angebote |
| --- | ---: |
| Stufe 2 | 171 |

### Welche Quelle lief auf welcher Stufe

| Quelle | Stufe | Methode | Treffer | Hinweis |
| --- | :-: | --- | ---: | --- |
| weltsparen.de | 2 | css_heuristik | 4 |  |
| check24.de | 2 | css_heuristik | 3 |  |
| biallo.de | 2 | css_heuristik | 9 |  |
| finanzfluss.de | 2 | css_heuristik | 32 |  |
| durchblicker.at | 2 | css_heuristik | 2 |  |
| bankenrechner.at | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| raisin.nl | - | - | 0 | S1/json_endpoint: HTTP 404; S1/jsonld: ld+json vorhanden, aber ohne verwertbares Zinsangebot; S2/css_konfiguri |
| moneyvox.fr | 2 | css_heuristik | 20 |  |
| raisin.fr | 2 | css_heuristik | 7 |  |
| confrontaconti.it | - | - | 0 | HTTP 403 |
| tucapital.es | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: ld+json vorhanden, aber ohne verwertbares Zin |
| bankier.pl | 2 | css_heuristik | 9 |  |
| compricer.se | 2 | css_heuristik | 46 |  |
| bankinter.pt | - | - | 0 | HTTP 403 |
| ing.de | 2 | css_heuristik | 2 |  |
| consorsbank.de | 2 | css_heuristik | 1 |  |
| comdirect.de | - | - | 0 | HTTP 404 |
| traderepublic.com | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| santander.de | 2 | css_heuristik | 2 |  |
| openbank.de | - | - | 0 | S1/json_endpoint: kein json_endpoint in sources.yaml; S1/jsonld: kein <script type=application/ld+json> gefund |
| klarna.com | 2 | css_heuristik | 8 |  |
| tagesgeld.info | 2 | css_heuristik | 24 |  |
| tagesgeldvergleich.com | 2 | css_heuristik | 10 |  |
| verivox.de | 2 | css_heuristik | 9 |  |
| finanztip.de | 2 | css_heuristik | 10 |  |
| spaarrente.nl | 2 | css_heuristik | 48 |  |
| compricer.se | 2 | css_heuristik | 46 |  |


## Nachbereinigung des Altbestands

Uebernommene Vortagseintraege durchlaufen dieselben Qualitaetsfilter
wie frische Treffer. Was dabei aufgefallen ist:

* Land-Dopplungen im Altbestand aufgeloest: 9 Eintraege verschmolzen

## Sprung zum Vortag groesser als erlaubt - Vortagswert behalten (1)

- **xtb** (DE): 0.9 % -> 3.0 % (+2.1 pp) [Quelle: finanzfluss.de]

## Weit ueber EZB-Landesdurchschnitt - Flag 'pruefen' (8)

- **Consorsbank** (FR): 3.6 % vs. EZB 0.04 % (+3.56 pp)
- **Chase** (DE): 4.0 % vs. EZB 0.5 % (+3.5 pp)
- **Renault Bank** (DE): 4.1 % vs. EZB 0.5 % (+3.6 pp)
- **Revolut** (DE): 4.25 % vs. EZB 0.5 % (+3.75 pp)
- **Stellantis Direktbank** (DE): 3.62 % vs. EZB 0.5 % (+3.12 pp)
- **Hamburg Direct Bank** (DE): 3.61 % vs. EZB 0.5 % (+3.11 pp)
- **Opel Bank** (DE): 3.52 % vs. EZB 0.5 % (+3.02 pp)
- **ING** (DE): 3.75 % vs. EZB 0.5 % (+3.25 pp)

## Heute nicht gefunden - als stale behalten (28)

- **Oyak Anker Bank** (DE), stale seit 2026-09-02 (1 Tage)
- **Raisin RenteBoost** (DE), stale seit 2026-09-03 (0 Tage)
- **Multitude Bank** (MT), stale seit 2026-09-03 (0 Tage)
- **Raisin StartZins** (DE), stale seit 2026-09-03 (0 Tage)
- **Handelsbanken Sparränta 0,05** (SE), stale seit 2026-09-03 (0 Tage)
- **LEP (Livret d’Épargne Populaire)** (FR), stale seit 2026-09-03 (0 Tage)
- **LEP (sous conditions de revenus)** (FR), stale seit 2026-09-03 (0 Tage)
- **SEB Sparränta 1,70** (SE), stale seit 2026-09-03 (0 Tage)
- **Swedbank Sparränta 1,75** (SE), stale seit 2026-09-03 (0 Tage)
- **Distingo Bank** (FR), stale seit 2026-09-03 (0 Tage)
- **Avarda Bank** (SE), stale seit 2026-09-03 (0 Tage)
- **BW-Bank** (DE), stale seit 2026-09-03 (0 Tage)
- **Nordea Sparränta 1,75** (SE), stale seit 2026-09-03 (0 Tage)
- **Avida Bank AB** (SE), stale seit 2026-09-03 (0 Tage)
- **Instabank ASA** (NO), stale seit 2026-09-03 (0 Tage)
- **Anyfin** (SE), stale seit 2026-09-03 (0 Tage)
- **Heder Bank** (NO), stale seit 2026-09-03 (0 Tage)
- **BluOr Bank AS** (LV), stale seit 2026-09-03 (0 Tage)
- **Inbank** (EE), stale seit 2026-09-03 (0 Tage)
- **Renault Bank** (FR), stale seit 2026-09-03 (0 Tage)
- **Banca Progetto** (IT), stale seit 2026-09-03 (0 Tage)
- **Banca CF+** (IT), stale seit 2026-09-03 (0 Tage)
- **Lunar Sparränta** (SE), stale seit 2026-09-03 (0 Tage)
- **Lantmännen Finans Sparränta** (SE), stale seit 2026-09-03 (0 Tage)
- **Livret Jeune ≥** (FR), stale seit 2026-09-03 (0 Tage)
- **Ekobanken Sparränta 1,15** (SE), stale seit 2026-09-03 (0 Tage)
- **Nordnet Sparränta** (SE), stale seit 2026-09-03 (0 Tage)
- **Avanza Bank Sparränta** (SE), stale seit 2026-09-03 (0 Tage)

## Neu hinzugekommen (9)

- **Renault Bank** (DE): 4.1 %
- **Banca Progetto** (NL): 2.25 %
- **Avarda Bank** (NL): 2.2 %
- **BW-Bank** (NL): 2.2 %
- **Banca CF+** (NL): 2.2 %
- **Distingo Bank** (NL): 2.2 %
- **Inbank** (NL): 2.16 %
- **Instabank** (DE): 2.16 %
- **Renault Bank** (NL): 2.15 %

---

Angaben ohne Gewaehr. Keine Anlageberatung.
