# Zinsradar

Europaweiter Tagesgeld-Zins-Aggregator mit Android-App.

Kein Server, keine laufenden Kosten: GitHub Actions sammelt einmal täglich die
Zinsen und schreibt sie als `data/zinsen.json` ins Repo. Die PWA lädt genau
diese Datei über `raw.githubusercontent.com` und hält sie offline vor.
Capacitor verpackt die PWA zu einer APK zum Sideloaden.

Verglichen wird nicht der plakative Werbezins, sondern was nach zwölf Monaten,
nach Quellensteuer und nach einem Risikoabschlag für das Sitzland übrig bleibt.

> **Keine Anlageberatung. Alle Angaben ohne Gewähr.**
> Zinssätze ändern sich laufend – vor Abschluss immer beim Anbieter prüfen.

---

## Inhalt

- [Wie es funktioniert](#wie-es-funktioniert)
- [Schnellstart](#schnellstart)
- [Die dreistufige Extraktion](#die-dreistufige-extraktion)
- [Referenzdaten der EZB](#referenzdaten-der-ezb)
- [Die Berechnung](#die-berechnung)
- [Die App](#die-app)
- [APK bauen](#apk-bauen)
- [GitHub Actions einrichten](#github-actions-einrichten)
- [Manuelle Korrekturen](#manuelle-korrekturen)
- [Annahmen](#annahmen)
- [Bekannte Grenzen](#bekannte-grenzen)
- [Projektstruktur](#projektstruktur)

---

## Wie es funktioniert

```
                    GitHub Actions (täglich 06:00 UTC)
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
   scraper/fetch.py         scraper/ecb.py          data/overrides.json
   robots.txt, 1 Req/2s     MIR · €STR · FX         manuelle Korrekturen
        │                        │                        │
   scraper/extract.py            │                        │
   Stufe 1 → 2 → 3               │                        │
        │                        │                        │
        └──── normalize.py ──── score.py ──── validate.py ─┘
                                 │
                        data/zinsen.json  (committet ins Repo)
                                 │
                    raw.githubusercontent.com
                                 │
                 ┌───────────────┴───────────────┐
              PWA (/app)                  APK (/android)
           Browser, offline           Capacitor + WebView
```

Es gibt bewusst keinen Server und keine Datenbank. Der einzige Zustand ist
`data/zinsen.json` samt Historie in `data/history/`.

---

## Schnellstart

Voraussetzungen: Python 3.12 oder neuer. Für JS-Seiten zusätzlich Playwright,
für die APK JDK 21 und das Android SDK.

```bash
git clone <dein-repo> zinsradar && cd zinsradar
python -m venv .venv
```

Windows: `.venv\Scripts\activate` · Linux/macOS: `source .venv/bin/activate`

```bash
pip install -r requirements.txt -r requirements-render.txt -r requirements-dev.txt
playwright install chromium
```

Erst prüfen, welche Quellen überhaupt taugen:

```bash
python scraper/bootstrap.py
```

Das schreibt `docs/quellen_status.md`: welche URLs 404/403 liefern, welche
Selektoren null Treffer bringen und welche Stufe je Quelle greifen würde.
**Dieser Schritt ist der wichtigste beim Aufsetzen**, siehe
[Annahmen](#annahmen).

Dann der eigentliche Lauf:

```bash
python scraper/run.py
```

Ergebnis: `data/zinsen.json`, `data/referenz.json`, `data/history/<datum>.json`
und `docs/report.md`.

Nützliche Schalter:

```bash
python scraper/run.py --nur biallo --nur ing.de   # nur einzelne Quellen
python scraper/run.py --dry-run                   # nichts schreiben
python scraper/run.py --kein-llm                  # Stufe 3 überspringen
python scraper/run.py --keine-referenz            # EZB-Abruf überspringen
python scraper/run.py --keys                      # Schlüssel für overrides.json
```

Tests:

```bash
python -m pytest
```

App lokal ansehen:

```bash
python -m http.server 8731 --directory app
```

Dann `http://localhost:8731` öffnen. Solange die Datenquelle noch nicht auf
dein Repo zeigt, nutzt die App die mitgelieferte Kopie unter `app/data/`
(wird von `tools/sync_web.py` oder vom Android-Build angelegt).

---

## Die dreistufige Extraktion

Pro Quelle wird der Reihe nach probiert; die erste erfolgreiche Stufe gewinnt.
Jeder Treffer bekommt `extraction_tier` (1–3) und `confidence`; im Log und in
`docs/report.md` steht, welche Quelle auf welcher Stufe lief.

### Stufe 1 — strukturierte Daten (bevorzugt, weil redesignfest)

1. **`json_endpoint`** aus `sources.yaml`, falls vorhanden.
2. **JSON-LD** aus `<script type="application/ld+json">`: schema.org
   `Offer`, `FinancialProduct`, `BankAccount`, `InvestmentOrDeposit`.
   `@graph`, `itemListElement` und verschachtelte `offers` werden mit
   durchsucht.

Feldnamen werden über eine mehrsprachige Synonymtabelle gemappt
(`interestRate`, `tasso`, `taux`, `oprocentowanie` …). Werte unter 0,25
werden als Dezimalbruch erkannt und mit 100 multipliziert (0.034 → 3,4 %).

Der Anbieter wird gezielt aus `provider`/`seller`/`brand`/`issuer` gelesen,
**nicht** aus dem generischen `name` — das ist in schema.org der Produktname.

### Stufe 2 — CSS-Selektoren

**2a** benutzt `container_selector` und `felder` aus `sources.yaml`.
Kommagetrennte Alternativen werden einzeln probiert, damit ein kaputter
Teilselektor die gültigen nicht mitreißt. `literal:'…'` setzt einen Festwert
statt eines Selektors.

**2b** ist eine generische Struktur-Heuristik ohne jede Konfiguration. Sie
existiert, weil die Selektoren aus einer LLM-Recherche stammen und ungeprüft
sind — die Pipeline darf nicht an ihnen hängen.

Statt Klassennamen zu raten, gruppiert 2b Elemente nach *Signatur*
(Tag + Klassen + Baumtiefe) und sucht die Struktur, die sich wiederholt und
jedes Mal eine Prozentangabe enthält. Bewertet wird nach der Zahl
**unterschiedlicher** Banknamen, damit Layout-Dopplungen nicht gewinnen.

Dazu vier Schutzmechanismen, die sich in der Praxis als nötig erwiesen haben:

| Problem | Lösung |
| --- | --- |
| „1 DHB Bank" wird als 1,00 % gelesen | im strengen Modus nur echte Prozentangaben (`%`, „Prozent", „p.a.") |
| „15 % Rabatt" landet als Sparzins in der Liste | eigenes Zinsfenster 0,05–8,0 % nur für die Heuristik |
| Spaltenüberschriften als Bankname („Basiszins:", „AAA", „Video-Ident") | Label-Filter plus Präfix-Abschneiden |
| Namenszeile und Zinszeile stehen in getrennten `<tr>` | Namenssuche geht bei Bedarf zum vorherigen Geschwisterknoten |

Beschriftete Werte werden auseinandergehalten: aus
„Basiszins: 1,95 % Aktionszins: 3,40 % – erste 6 Monate" wird
Aktionszins 3,40 %, Folgezins 1,95 %, Dauer 6 Monate.

### Stufe 3 — LLM-Fallback

Das HTML wird auf Fließtext reduziert (Skripte, Navigation, Cookie-Banner
raus; max. 8000 Zeichen) und mit festem JSON-Schema an **Gemini 2.0 Flash**
geschickt: „extrahiere alle Sparzins-Angebote".

Der Key kommt aus dem Secret `GEMINI_API_KEY`. **Fehlt er, wird die Stufe
übersprungen, nicht abgebrochen.** Treffer bekommen `extraction_tier: 3` und
werden in der App als „automatisch erkannt" markiert.

---

## Referenzdaten der EZB

Offizielle APIs, kein Scraping. Alle Endpunkte wurden am 01.09.2026 gegen die
echte API geprüft:

| Was | Serie / URL |
| --- | --- |
| Tagesgeld-Durchschnitt je Land | `data-api.ecb.europa.eu/service/data/MIR/M.{LAND}.B.L21.A.R.A.2250.EUR.N` |
| €STR-Tagesreihe | `data-api.ecb.europa.eu/service/data/EST/B.EU000A2X2A25.WT` |
| Wechselkurse | `ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml` |

Länder: DE FR NL IT ES AT IE PT und U2 (Euroraum). Abruf als `csvdata`, alle
Länder in einem Request (`M.DE+FR+NL...`), mit Rückfall auf Einzelabrufe.

Achtung bei der Serien-ID: Im API-Pfad steht der Dataflow (`MIR`) getrennt,
der Schlüssel beginnt danach mit der Frequenz — also
`/service/data/MIR/M.DE.B.L21...`, nicht `/service/data/MIR.M.DE...`.

Ergebnis in `data/referenz.json`, ein kompakter Auszug zusätzlich in
`data/zinsen.json`, damit die App nur eine Datei laden muss.

---

## Die Berechnung

```
brutto_12m = (aktionszins * min(aktionsdauer, 12)
              + folgezins * max(0, 12 - aktionsdauer)) / 12

netto_12m  = brutto_12m * (1 - qst_effektiv)

qst_effektiv = 0, wenn rueckerstattung_aufwand ∈ {keiner, niedrig}
                  UND Einstellung „Rückerstattung selbst machen" = an,
               sonst quellensteuer_mit_dba_pct

score = netto_12m - risiko_abschlag[staatsrating_sp]
```

Risikoabschlag in Prozentpunkten (`config.json`, Gruppe ohne +/−):

| Rating | AAA | AA | A | BBB | darunter |
| --- | --- | --- | --- | --- | --- |
| Abschlag | 0,00 | 0,05 | 0,10 | 0,25 | 0,60 |

Die **deutsche Abgeltungssteuer** (25 % + Soli = 26,375 %) ist bewusst *nicht*
im Score: sie trifft alle Anbieter gleich und würde die Reihenfolge nicht
ändern. Sie lässt sich in den Einstellungen als reine Anzeige zuschalten.

Weil die Einstellung „Rückerstattung selbst machen" in der App sitzt und nicht
im Scraper, werden **beide Varianten vorberechnet** und mitgeliefert
(`netto_12m_mit_erstattung_pct` / `..._ohne_erstattung_pct`, analog beim
Score). Die App schaltet nur zwischen zwei fertigen Zahlen um.

### Validierung

`validate.py` prüft jeden Lauf gegen den Vortag:

| Regel | Folge |
| --- | --- |
| 0 Treffer insgesamt | kompletter Vortagsstand bleibt, alles `stale` |
| Zins > 10 % | alter Wert bleibt, `stale`; ohne Vortagswert verworfen |
| Abweichung > 2 pp zum Vortag | alter Wert bleibt, `stale` |
| Zins > 3 pp über EZB-Landesschnitt | Flag `prüfen` (Wert bleibt sichtbar) |

Alles landet in `docs/report.md`. Schwellen stehen in `config.json`.

---

## Die App

Vanilla HTML/CSS/JS in `/app`, kein Build-Step, kein Framework, keine externen
Ressourcen (damit sie offline vollständig funktioniert).

1. **Vollständige Liste** aller gefundenen Anbieter, sortierbar nach Score
   (Standard), Netto, Brutto, Name, Land. Es wird nichts weggefiltert.
2. **Zweite Zeile je Eintrag** mit „netto X,XX % über 12 Monate nach
   Quellensteuer"; Tippen öffnet die vollständige Rechnung mit allen
   Zwischenschritten und den Formeln.
3. **Badges**: Einlagensicherung und Länderrating, farbcodiert
   (AAA/AA grün, A/BBB gelb, darunter rot).
4. **Referenzleiste** oben: EZB-Marktdurchschnitt des gefilterten Landes
   (sonst Euroraum) und €STR mit 30-Tage-Trend.
5. **Filter**: Land, Zinstyp, Anlagebetrag (prüft Mindest- und Höchstanlage),
   Anbietertyp, nur EUR, nur Watchlist, stale ausblenden.
6. **Watchlist** mit lokaler Benachrichtigung, wenn ein beobachteter Zins über
   dem eingestellten Schwellwert liegt (Capacitor LocalNotifications in der
   APK, Web-Notification im Browser, sonst In-App-Hinweis).
7. **Offline**: Service Worker, „Stand:"-Datum, veraltete Einträge ausgegraut,
   Tier-3-Werte als „automatisch erkannt" markiert.
8. **Pull-to-Refresh**, Dark Mode (System/hell/dunkel), deutsche Oberfläche.

### Datenquelle eintragen

**Das ist der einzige Pflicht-Handgriff.** In `app/config.js`:

```js
datenUrl: "https://raw.githubusercontent.com/DEIN-NUTZERNAME/zinsradar/main/data/zinsen.json",
```

Alternativ zur Laufzeit in den Einstellungen der App — der Wert dort gewinnt
gegen die Datei.

---

## APK bauen

Das Android-Projekt kommt **ohne Node und npm** aus: Capacitor wird als
Maven-Artefakt (`com.capacitorjs:core`) geladen, nicht aus `node_modules`.
`npx cap sync` ersetzt der Gradle-Task `syncWeb`, der `/app` nach
`assets/public` kopiert und die aktuellen Zinsdaten als Offline-Startbestand
dazulegt.

Voraussetzungen: JDK 21, Android SDK mit Platform 35.

```bash
cd android
```

`local.properties` anlegen (Pfad anpassen, Forward-Slashes benutzen):

```properties
sdk.dir=C\:/Android/sdk
```

Dann:

```bash
./gradlew assembleDebug
```

Ergebnis: `android/app/build/outputs/apk/debug/app-debug.apk` — direkt aufs
Handy kopieren und installieren („Installation aus unbekannten Quellen"
erlauben). Läuft ab Android 7 (API 24), Ziel ist API 35.

### Signiertes Release

Keystore erzeugen (einmalig, gut aufheben — ohne ihn sind keine Updates der
App möglich):

```bash
keytool -genkeypair -v -keystore zinsradar.jks -keyalg RSA -keysize 2048 -validity 10000 -alias zinsradar
```

Dann bauen:

```bash
ZR_KEYSTORE_PATH=../zinsradar.jks ZR_KEYSTORE_PASSWORD=… ZR_KEY_ALIAS=zinsradar ZR_KEY_PASSWORD=… ./gradlew assembleRelease
```

Ohne Keystore fällt der Release-Build auf den Debug-Key zurück; die APK ist
dann installierbar, aber nicht mit dem eigenen Schlüssel signiert.

### Icons neu erzeugen

```bash
python tools/icons.py
```

Rastert `app/icons/icon.svg` ohne Bildbibliothek (reines `zlib`) zu allen
PWA- und Launcher-Größen.

---

## GitHub Actions einrichten

### `scrape.yml` — täglich 06:00 UTC

Läuft den Scraper, committet `data/*.json` und `docs/report.md` zurück ins
Repo, schreibt eine Zusammenfassung in die Job-Summary. Manuell startbar mit
Auswahl einzelner Quellen.

Damit der Bot pushen darf: **Settings → Actions → General → Workflow
permissions → „Read and write permissions"**.

### `build-apk.yml` — bei Tag `v*`

Baut die APK, hängt sie an ein GitHub Release und lädt sie als Artefakt hoch.

```bash
git tag v1.0.0 && git push origin v1.0.0
```

### Secrets

| Secret | Pflicht | Wofür |
| --- | --- | --- |
| `GEMINI_API_KEY` | nein | Stufe 3. Fehlt er, wird die Stufe stillschweigend übersprungen. |
| `KEYSTORE_BASE64` | nein | Keystore als Base64: `base64 -w0 zinsradar.jks` |
| `KEYSTORE_PASSWORD` | nein | Keystore-Passwort |
| `KEY_ALIAS` | nein | Alias im Keystore |
| `KEY_PASSWORD` | nein | Passwort des Schlüssels |

Ohne Keystore-Secrets baut der Workflow eine mit dem Debug-Key signierte APK
und warnt im Log.

---

## Manuelle Korrekturen

`data/overrides.json` gewinnt **immer** gegen Scraper-Werte und wird nie
automatisch überschrieben. Schlüssel abfragen:

```bash
python scraper/run.py --keys
```

```json
{
  "eintraege": {
    "beispielbank ag|tagesgeld|de": {
      "zinssatz_pct": 3.25,
      "aktionsdauer_monate": 6,
      "folgezins_pct": 1.5,
      "quelle_manuell": "https://www.beispielbank.de/tagesgeld",
      "geprueft_am": "2026-09-01",
      "notiz": "Website zeigt veralteten Wert."
    }
  }
}
```

Ein Schlüssel, der auf kein gefundenes Angebot passt, wird als eigener
Eintrag aufgenommen — so lässt sich eine Bank pflegen, die kein Scraper
findet. Solche Einträge tragen in der App das Badge „manuell geprüft".

---

## Annahmen

Getroffen ohne Rückfrage, wie beauftragt. Der Reihe nach, wichtigste zuerst.

### 1. Die Selektoren in `sources.yaml` sind Hinweise, keine Wahrheit

Sie stammen aus einer LLM-Recherche und sind ungeprüft. Die Architektur ist so
gebaut, dass sie ohne sie funktioniert: Stufe 1 braucht sie gar nicht,
Stufe 2b ersetzt sie durch Struktur-Erkennung, Stufe 3 durch ein Sprachmodell.

Der erste echte Lauf hat das bestätigt: **kein einziger `container_selector`
traf**, sechs URLs antworteten mit 404, zwei mit 403, mehrere
`json_endpoint` existieren gar nicht. Trotzdem lieferten 9 Quellen Daten —
komplett über Stufe 2b.

Danach wurden vier URLs korrigiert (getestet am 01.09.2026):

| Quelle | vorher (404) | jetzt |
| --- | --- | --- |
| ing.de | `/sparen/tagesgeld/` | `/sparen-anlegen/sparen/tagesgeld/` |
| klarna.com | `/de/festgeld-tagesgeld/` | `/de/festgeld/` |
| raisin.nl | `/sparen/vrij-opneembaar-sparen/` | `/spaarrekening/` |
| raisin.fr | `/comptes-a-terme/` | `/livret-epargne/` |

Damit liefern **13 von 22 Quellen rund 72 Angebote aus 7 Ländern**. Der Rest
scheitert an Bot-Schutz (403/401), toten Domains oder robots.txt.
`docs/quellen_status.md` listet jede Quelle einzeln mit Begründung auf.

Die YAML-Selektoren bleiben trotzdem drin: sie kosten nichts, und wo sie
stimmen, liefern sie bessere Daten als die Heuristik. Die `literal:`-Werte
darin sind handrecherchierte Fakten (Consorsbank → Einlagensicherung FR) und
werden auch dann angewandt, wenn nur die Heuristik greift.

### 2. Auch `withholding.json` und `laender.json` sind ungeprüft

Sie stammen aus derselben Recherche und werden unverändert übernommen, weil
sie als Vorgabe geliefert wurden. Stichproben wirken plausibel, mindestens ein
Eintrag ist aber zweifelhaft: Für HR steht die „Hrvatska agencija za osiguranje
radnih tražbina" als Einlagensicherung – das ist die Agentur für
Arbeitnehmerforderungen, nicht die Einlagensicherung.

**Alle Steuer- und Sicherungsangaben vor einer echten Anlage selbst prüfen.**
Die `quelle_url` je Eintrag führt zur zuständigen Behörde.

### 3. Deutschland wird als Inlandsfall behandelt

`withholding.json` führt für DE 25 % mit `rueckerstattung_moeglich: false`.
Das sind die deutsche Abgeltungssteuer, keine ausländische Quellensteuer.
Da die Vorgabe ausdrücklich sagt, die Abgeltungssteuer gehöre nicht in den
Score, ist `qst_effektiv` für DE immer 0 — sonst würden deutsche Banken doppelt
bestraft. Die 26,375 % erscheinen nur im Anzeige-Toggle.

### 4. Fehlender Folgezins wird geschätzt

Ist eine Aktion befristet und der Folgezins unbekannt, wird der
EZB-Landesdurchschnitt eingesetzt und der Eintrag mit
`folgezins_geschaetzt: true` markiert. Gibt es keinen EZB-Wert, wird 0
angenommen — lieber zu vorsichtig als zu optimistisch. Ohne Aktionszeitraum
läuft der Zins einfach weiter.

### 5. Das Sicherungsland kann eine Annahme sein

Steht im Angebot kein Land, wird das Land der Quelle übernommen. Bei einer
Bankseite ist das richtig, bei einem Vergleichsportal oft falsch — BBVA steht
auf einer deutschen Seite, sichert aber in Spanien. Die Herkunft der Angabe
wird als `land_quelle` mitgeführt (`erkannt` / `bankseite` /
`quellenland_angenommen`) und in der App als „Land angenommen" gekennzeichnet;
im Detail steht ein ausdrücklicher Warnhinweis. Quellensteuer und Rating
hängen daran, deshalb ist das die wichtigste Stelle für `overrides.json`.

Findet dieselbe Bank sich einmal mit belegtem und einmal mit angenommenem Land,
gewinnt die belegte Angabe und die Einträge werden verschmolzen.

### 6. Zinssätze werden nicht in Euro umgerechnet

Ein Zins in PLN bleibt ein PLN-Zins — eine Umrechnung wäre sinnlos.
Umgerechnet werden nur Beträge (Mindest-/Höchstanlage, Einlagensicherung).
Angebote in Fremdwährung tragen `waehrungsrisiko: true` und ein Badge.
Das Währungsrisiko geht **nicht** in den Score ein.

### 7. Verschwundene Angebote bleiben zunächst stehen

Ein Eintrag, den ein Lauf nicht mehr findet, verschwindet nicht sofort,
sondern bleibt bis zu 14 Tage als `stale` (`max_stale_tage` in `config.json`).
Sonst würde ein einzelner Netzwerkfehler die halbe Liste leeren. Einträge,
deren Bankname die inzwischen verschärfte Plausibilitätsprüfung nicht mehr
besteht, werden dagegen sofort entfernt.

### 8. Die 3-pp-EZB-Regel flaggt derzeit fast alle deutschen Angebote

Die MIR-Serie misst den Durchschnitt **aller** täglich fälligen Einlagen
privater Haushalte, inklusive unverzinster Girokonten — für DE aktuell rund
0,5 %. Aktionszinsen von 3–4 % liegen damit strukturell mehr als 3 pp darüber.
Die Regel ist wie beauftragt umgesetzt; die Schwelle steht als
`validierung.ezb_abstand_flag_pp` in `config.json` und lässt sich anheben.

### 9. Weitere kleinere Festlegungen

- **Projektname** „Zinsradar", App-ID `de.zinsradar.app`.
- **`robots.txt` wird live geprüft.** Das Feld `robots_txt_erlaubt` in
  `sources.yaml` ist nur ein Hinweis und entscheidet nichts. Bei HTTP 5xx auf
  `/robots.txt` wird die Domain vorsichtshalber gemieden (RFC 9309), bei 404
  gilt alles als erlaubt. Ein `Crawl-delay` größer als 2 s wird eingehalten.
- **User-Agent im konventionellen Crawler-Format:**
  `Mozilla/5.0 (compatible; ZinsradarBot/1.0; +https://…)`. Der Bot nennt
  sich klar beim Namen — mehrere Banken weisen einen UA ohne das
  `Mozilla`-Präfix aber schon auf Verbindungsebene ab. Playwright behält
  seinen echten Chromium-UA; ein gerenderter Browser *ist* ein Browser.
  An der strikten Befolgung von robots.txt ändert das nichts, und Captchas
  werden nicht umgangen.
- **Zusätzliche Dateien**, die die Aufgabe nicht nennt: `scraper/util.py`
  (Pfade, Config, atomares JSON-Schreiben), `scraper/run.py` (Orchestrator,
  ohne ihn hätte der Workflow nichts aufzurufen), `tools/icons.py`,
  `tests/`, `config.json` im Repo-Root.
- **`config.json` liegt im Root**, nicht in `/data`. Die für die Anzeige
  nötigen Teile (Risikotabelle, Formeln) werden in `data/zinsen.json`
  gespiegelt, damit die App die Rechnung erklären kann, ohne eine zweite
  Datei zu laden.
- **`minSdk 24`** statt 33. Die Vorgabe nennt Android 13+, aber ein
  niedrigeres Minimum kostet nichts und macht die APK breiter nutzbar.
- **Ein Angebot pro Bank und Produkt und Land.** Produktzusätze werden für den
  Vergleichsschlüssel entfernt, damit „Revolut" und
  „Revolut Tagesgeld(Standard)" nicht zweimal erscheinen.
- **Die Bankinter-URL** enthielt im Anhang ein akzentuiertes `poupança`;
  sie wurde ASCII-normalisiert. Nicht-ASCII in URLs wird generell
  prozent-kodiert.

---

## Bekannte Grenzen

- **Bot-Schutz.** Cloudflare, DataDome und Akamai blocken einen Teil der
  Quellen zuverlässig. Playwright hilft beim Rendern, nicht gegen Captchas.
  Captchas werden nicht umgangen.
- **Stufe 2b ist eine Heuristik.** Sie hat Confidence 0,5 und kann
  Randspalten falsch zuordnen. Sie ist das Sicherheitsnetz, nicht der
  Idealfall. Wer bessere Daten will, korrigiert die Selektoren in
  `sources.yaml` anhand von `docs/quellen_status.md`.
- **Ohne `GEMINI_API_KEY` fehlt Stufe 3** und damit die Quellen, an denen
  Stufe 1 und 2 scheitern.
- **Aktionsbedingungen** (Neukundenstatus, Depotübertrag, Gehaltseingang)
  werden nicht ausgewertet. Sie stehen oft nur im Kleingedruckten.
- **Trade Republic und ähnliche Treuhandmodelle** haben kein eindeutiges
  Sicherungsland — das Guthaben liegt bei wechselnden Partnerbanken.
- **Die Historie in `data/history/`** wächst um eine Datei pro Tag. Nach ein
  paar Jahren lohnt sich Aufräumen.

---

## Projektstruktur

```
zinsradar/
├── scraper/
│   ├── sources.yaml       Quellen (Selektoren = ungeprüfte Hinweise)
│   ├── fetch.py           robots.txt, Rate-Limit, Retry, Playwright
│   ├── extract.py         die drei Stufen
│   ├── ecb.py             MIR, €STR, FX
│   ├── normalize.py       Parsing, Dedupe, Merge, FX
│   ├── validate.py        Plausibilität, stale-Logik, report.md
│   ├── score.py           brutto/netto/Score
│   ├── bootstrap.py       Quellen-Diagnose → quellen_status.md
│   ├── run.py             Orchestrator
│   └── util.py            Pfade, Config, atomares JSON
├── data/
│   ├── zinsen.json        Ergebnis (die App lädt nur diese Datei)
│   ├── referenz.json      EZB-Rohdaten
│   ├── history/           ein Stand je Tag
│   ├── withholding.json   Quellensteuer je Land
│   ├── laender.json       Einlagensicherung, Ratings, Währung
│   └── overrides.json     manuelle Korrekturen (gewinnen immer)
├── app/                   PWA: index.html, app.css, app.js, sw.js, config.js
├── android/               Capacitor-Projekt (Gradle, kein npm)
├── tools/icons.py         Icon-Generator
├── tests/                 pytest
├── docs/                  report.md, quellen_status.md
├── config.json            Schwellen, Risikotabelle, Fetch-Verhalten
└── .github/workflows/     scrape.yml, build-apk.yml
```

---

## Lizenz und Daten

Der Code steht unter der MIT-Lizenz (`LICENSE`).

Die EZB-Daten sind frei nutzbar mit Quellenangabe. Die Angebotsdaten stammen
von den je Eintrag genannten Websites; die App zeigt zu jedem Eintrag die
Quelle mit Link. Dieses Projekt ist ein privates Vergleichswerkzeug und keine
kommerzielle Weiterverbreitung fremder Datenbanken.

**Keine Anlageberatung. Alle Angaben ohne Gewähr.**
