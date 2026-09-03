/* Zinsradar – Vanilla JS, kein Framework, kein Build-Step.
 *
 * Datenfluss:
 *   GitHub Actions -> data/zinsen.json -> raw.githubusercontent -> hier.
 *   Kein Server, keine API. Geladene Daten landen im localStorage und im
 *   Service-Worker-Cache, damit die App offline weiterläuft.
 *
 * Leitgedanke der Oberfläche:
 *   Zuerst die Zahl, mit der die Bank selbst wirbt. Danach – kleiner –
 *   was davon in Euro übrig bleibt. Prozentwerte allein sagen niemandem
 *   etwas; "425 € im Jahr" schon.
 *
 * Alle Sheets teilen sich EIN Element (#sheet). Ein einziger Öffnen- und
 * Schließen-Weg heißt: ein einziger Ort, an dem etwas klemmen kann.
 */
(function () {
  "use strict";

  var CFG = window.ZINSRADAR_CONFIG || {};

  var SPEICHER = {
    daten: "zr_daten",
    einst: "zr_einstellungen",
    watch: "zr_watchlist",
    theme: "zr_theme",
    gemeldet: "zr_gemeldet",
    betrag: "zr_betrag",
    erledigt: "zr_erledigt",
  };

  var SEITE = 40;
  var BETRAG_STANDARD = 10000;
  var BETRAG_VORSCHLAEGE = [1000, 5000, 10000, 25000, 50000, 100000];

  var zustand = {
    daten: null,
    sortierung: "score",
    suche: "",
    filter: {
      land: "", typ: "", quelltyp: "", rating: "", minZins: "",
      aktion: "", neukunden: "",
      nurEur: false, nurWatch: false, ohneStale: false, passtZuBetrag: false,
      vollGesichert: false,
    },
    einstellungen: {
      erstattung: true,
      abgeltung: false,
      schwelle: 3.5,
      benachrichtigung: false,
      quelle: "",
    },
    betrag: BETRAG_STANDARD,
    watchlist: [],
    // Neukunden-Angebote kann man nur einmal mitnehmen. Wer eins schon
    // genutzt hat, hakt es ab: raus aus der Liste, rein in die
    // Einstellungen - rückgängig machen geht dort jederzeit.
    erledigt: [],
    laedt: false,
    sichtbar: [],
    // Mit 190 Angeboten dauert ein voller Neuaufbau der Liste ~250 ms -
    // das merkt man beim Tippen in der Suche. Deshalb erst ein Schwung,
    // den Rest auf Knopfdruck.
    limit: SEITE,
  };

  /* ================================================================ Hilfen */

  function $(id) { return document.getElementById(id); }

  var nfZins = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var nfFein = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 3 });
  var nfEuro = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });
  var nfEuroGenau = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  function istZahl(wert) {
    return wert !== null && wert !== undefined && wert !== "" && !isNaN(wert);
  }

  function pct(wert, formatierer) {
    if (!istZahl(wert)) return "–";
    return (formatierer || nfZins).format(wert) + " %";
  }

  /* Steuersätze sind meist glatt: "15 %" liest sich besser als "15,00 %".
     Beim Zinssatz bleiben die zwei Stellen, so wirbt die Bank ja auch. */
  var nfSchlank = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 2 });

  function pctSchlank(wert) {
    if (!istZahl(wert)) return "–";
    return nfSchlank.format(wert) + " %";
  }

  function euro(wert) {
    if (!istZahl(wert)) return "–";
    return nfEuro.format(wert) + " €";
  }

  function euroGenau(wert) {
    if (!istZahl(wert)) return "–";
    return nfEuroGenau.format(wert) + " €";
  }

  /* Zinsen in Euro auf den eingestellten Betrag. */
  function inEuro(prozent) {
    if (!istZahl(prozent)) return null;
    return zustand.betrag * prozent / 100;
  }

  function datumKurz(iso) {
    if (!iso) return "–";
    var d = new Date(iso);
    if (isNaN(d.getTime())) return String(iso).slice(0, 10);
    return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
  }

  function tageSeit(iso) {
    if (!iso) return null;
    var d = new Date(iso);
    if (isNaN(d.getTime())) return null;
    return Math.floor((Date.now() - d.getTime()) / 86400000);
  }

  /* Bewusst NICHT `escape` genannt: das gibt es global schon. */
  function esc(text) {
    return String(text === null || text === undefined ? "" : text)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  /* Zahl aus einem Eingabefeld, in deutscher Schreibweise gedacht.
     `type="number"` liefert bei einem Komma einen LEEREN Wert, und
     Number("1.000") wäre 1 – ein Anlagebetrag von einem Euro. Deshalb
     stehen die Felder auf type="text" und werden hier selbst gelesen.

       "1.000"    -> 1000     (Tausenderpunkt)
       "12,5"     -> 12.5     (Dezimalkomma)
       "1.234,56" -> 1234.56
       "1,234.56" -> 1234.56  (englische Schreibweise)
       "10 000 €" -> 10000
  */
  function zahlAusEingabe(roh) {
    var t = String(roh === null || roh === undefined ? "" : roh)
      .replace(/[\s\u00a0€%]/g, "");
    if (!t) return NaN;
    if (!/^[+-]?[\d.,]+$/.test(t)) return NaN;

    var hatKomma = t.indexOf(",") !== -1;
    var hatPunkt = t.indexOf(".") !== -1;

    if (hatKomma && hatPunkt) {
      // Das zuletzt stehende Zeichen trennt die Nachkommastellen.
      t = t.lastIndexOf(",") > t.lastIndexOf(".")
        ? t.replace(/\./g, "").replace(",", ".")
        : t.replace(/,/g, "");
    } else if (hatKomma) {
      t = t.replace(/,/g, ".");
    } else if (hatPunkt) {
      // Ein Punkt vor genau drei Ziffern ist ein Tausenderpunkt.
      if (/^[+-]?\d{1,3}(\.\d{3})+$/.test(t)) t = t.replace(/\./g, "");
    }
    // Nach dem Aufraeumen darf hoechstens noch ein Punkt uebrig sein,
    // sonst war die Eingabe keine Zahl ("1.2.3").
    if ((t.match(/\./g) || []).length > 1) return NaN;
    var wert = parseFloat(t);
    return isFinite(wert) && /^[+-]?\d*\.?\d*$/.test(t) ? wert : NaN;
  }

  /* Nur http(s) in ein href lassen. esc() verhindert zwar den Ausbruch aus
     dem Attribut, nicht aber ein "javascript:"-Ziel. Die Daten stammen aus
     fremden Webseiten – da gilt: Schema prüfen, nicht hoffen. */
  function sicherLink(url) {
    var t = String(url || "").trim();
    if (!/^https?:\/\//i.test(t)) return "";
    return t;
  }

  function ikon(name, klasse) {
    return '<svg class="ikon-svg' + (klasse ? " " + klasse : "") + '" aria-hidden="true">' +
      '<use href="#i-' + name + '"></use></svg>';
  }

  /* Liest einen gespeicherten Wert und prüft den Typ.
     Ohne die Prüfung legt ein einziger krummer Eintrag die App still
     lahm: zr_erledigt = "5" ergibt beim Start
     "zustand.erledigt.indexOf is not a function", die Liste bleibt leer,
     und der Zustand überlebt jeden Neustart. */
  function lies(schluessel, standard, art) {
    var wert;
    try {
      var roh = localStorage.getItem(schluessel);
      wert = roh ? JSON.parse(roh) : standard;
    } catch (e) { return standard; }

    if (art === "liste" && !Array.isArray(wert)) return standard;
    if (art === "objekt" && (wert === null || typeof wert !== "object" || Array.isArray(wert))) {
      return standard;
    }
    if (art === "zahl") {
      var zahl = Number(wert);
      return isFinite(zahl) && zahl > 0 ? zahl : standard;
    }
    if (art === "text" && typeof wert !== "string") return standard;
    return wert === undefined ? standard : wert;
  }

  function schreib(schluessel, wert) {
    try { localStorage.setItem(schluessel, JSON.stringify(wert)); } catch (e) { /* voll oder privat */ }
  }

  var toastTimer = null;
  function toast(text, dauer) {
    var el = $("toast");
    el.textContent = text;
    el.hidden = false;
    // Animation neu starten, sonst bleibt sie beim zweiten Toast aus.
    el.style.animation = "none";
    void el.offsetWidth;
    el.style.animation = "";
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.hidden = true; }, dauer || 2600);
  }

  /* Suchtext vergleichbar machen: Kleinschreibung, Umlaute aufgelöst.
     Damit findet "muenchen" auch "München" und "oster" auch "Österreich". */
  function suchform(text) {
    var t = String(text || "").toLowerCase();
    t = t.replace(/ä/g, "ae").replace(/ö/g, "oe").replace(/ü/g, "ue").replace(/ß/g, "ss");
    if (t.normalize) t = t.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    return t.replace(/[^a-z0-9]+/g, " ").trim();
  }

  /* Ländernamen ausgeschrieben – Kürzel wie "LV" sagen niemandem etwas. */
  var LAENDER = {
    DE: "Deutschland", AT: "Österreich", NL: "Niederlande", FR: "Frankreich",
    IT: "Italien", ES: "Spanien", PT: "Portugal", IE: "Irland", SE: "Schweden",
    NO: "Norwegen", DK: "Dänemark", FI: "Finnland", PL: "Polen", CZ: "Tschechien",
    BE: "Belgien", LU: "Luxemburg", LV: "Lettland", LT: "Litauen", EE: "Estland",
    MT: "Malta", CY: "Zypern", SI: "Slowenien", SK: "Slowakei", HR: "Kroatien",
    HU: "Ungarn", RO: "Rumänien", BG: "Bulgarien", GR: "Griechenland",
    CH: "Schweiz", LI: "Liechtenstein", IS: "Island", UK: "Großbritannien",
    U2: "Euroraum",
  };

  function landName(code) {
    if (!code) return "unbekannt";
    return LAENDER[String(code).toUpperCase()] || String(code).toUpperCase();
  }

  /* ============================================================ Daten laden */

  function datenUrl() {
    return (zustand.einstellungen.quelle || CFG.datenUrl || "").trim();
  }

  function holeMitTimeout(url, ms) {
    if (typeof AbortController === "undefined") return fetch(url, { cache: "no-store" });
    var ctrl = new AbortController();
    var t = setTimeout(function () { ctrl.abort(); }, ms || CFG.timeoutMs || 12000);
    return fetch(url, { cache: "no-store", signal: ctrl.signal })
      .then(function (r) { clearTimeout(t); return r; })
      .catch(function (e) { clearTimeout(t); throw e; });
  }

  function pruefeStruktur(daten) {
    return daten && typeof daten === "object" && Array.isArray(daten.angebote);
  }

  function laden(erzwingen) {
    if (zustand.laedt) return Promise.resolve();
    zustand.laedt = true;
    $("btnAktualisieren").classList.add("dreht");

    var url = datenUrl();
    var kette = url
      ? holeMitTimeout(url).then(function (r) {
          if (!r.ok) throw new Error("HTTP " + r.status);
          return r.json();
        })
      : Promise.reject(new Error("Keine Daten-Adresse eingestellt"));

    return kette
      .then(function (daten) {
        if (!pruefeStruktur(daten)) throw new Error("Unerwartetes Datenformat");
        schreib(SPEICHER.daten, { geholt: new Date().toISOString(), daten: daten });
        uebernehmen(daten, "netz");
        if (erzwingen) toast(daten.angebote.length + " Angebote aktualisiert");
        pruefeSchwelle(daten);
      })
      .catch(function (fehler) {
        var zwischen = lies(SPEICHER.daten, null, "objekt");
        if (zwischen && pruefeStruktur(zwischen.daten)) {
          uebernehmen(zwischen.daten, "cache", fehler.message, zwischen.geholt);
          if (erzwingen) toast("Kein Netz – gespeicherter Stand");
          return;
        }
        return holeMitTimeout(CFG.lokalerFallback || "data/zinsen.json", 6000)
          .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
          .then(function (daten) {
            if (!pruefeStruktur(daten)) throw new Error("Mitgelieferte Daten unbrauchbar");
            uebernehmen(daten, "mitgeliefert", fehler.message);
          })
          .catch(function () { zeigeFehler(fehler.message); });
      })
      .then(function () {
        zustand.laedt = false;
        $("btnAktualisieren").classList.remove("dreht");
      });
  }

  function uebernehmen(daten, quelle, fehlertext, geholtAm) {
    zustand.daten = daten;
    $("ladeanzeige").hidden = true;

    var hinweis = $("hinweis");
    if (quelle === "netz" || quelle === "start") {
      // "start" ist der gespeicherte Stand, den die App beim Öffnen sofort
      // zeigt, während der Abruf noch läuft. Dabei von "kein Netz" zu
      // sprechen wäre eine Behauptung ins Blaue – der Versuch hat noch
      // gar nicht stattgefunden.
      hinweis.hidden = true;
    } else {
      hinweis.hidden = false;
      hinweis.className = "hinweis";
      hinweis.textContent = quelle === "cache"
        ? (navigator.onLine === false
            ? "Gerade kein Netz. Du siehst den gespeicherten Stand vom " + datumKurz(geholtAm) + "."
            : "Die Daten ließen sich nicht abrufen (" + (fehlertext || "unbekannt") +
              "). Angezeigt wird der gespeicherte Stand vom " + datumKurz(geholtAm) + ".")
        : "Es werden die mitgelieferten Daten angezeigt. Die Daten-Adresse steht in den Einstellungen.";
    }
    rendern();
  }

  function zeigeFehler(text) {
    $("ladeanzeige").hidden = true;
    var hinweis = $("hinweis");
    hinweis.hidden = false;
    hinweis.className = "hinweis fehler";
    hinweis.textContent = "Die Daten konnten nicht geladen werden (" + text +
      "). Prüf die Daten-Adresse in den Einstellungen.";
  }

  /* ============================================== Felder je nach Einstellung */

  function nettoFeld() {
    if (zustand.einstellungen.abgeltung) {
      return zustand.einstellungen.erstattung
        ? "netto_nach_abgeltungssteuer_mit_erstattung_pct"
        : "netto_nach_abgeltungssteuer_ohne_erstattung_pct";
    }
    return zustand.einstellungen.erstattung
      ? "netto_12m_mit_erstattung_pct"
      : "netto_12m_ohne_erstattung_pct";
  }

  function scoreFeld() {
    return zustand.einstellungen.erstattung ? "score_mit_erstattung" : "score_ohne_erstattung";
  }

  function nettoWert(a) { return a[nettoFeld()]; }

  /* "nach Steuern bleiben 425 €" ist irrefuehrend, wenn gar keine Steuer
     abgezogen wurde - bei deutschen Banken ist brutto gleich netto, weil
     die Abgeltungssteuer bewusst draussen bleibt. Dann lieber sagen,
     warum nichts abgeht. */
  function nettoSatz(a) {
    var netto = inEuro(nettoWert(a));
    var qst = qstWert(a);
    if (istZahl(qst) && qst > 0) {
      return "nach Quellensteuer bleiben " + euro(netto);
    }
    if (zustand.einstellungen.abgeltung) {
      return "nach Steuern bleiben " + euro(netto);
    }
    return "ohne Abzug – hier fällt keine ausländische Steuer an";
  }

  function qstWert(a) {
    return zustand.einstellungen.erstattung
      ? a.qst_effektiv_mit_erstattung_pct
      : a.qst_effektiv_ohne_erstattung_pct;
  }

  function grenzenVon(a) {
    var min = istZahl(a.mindestanlage_eur) ? a.mindestanlage_eur : a.mindestanlage;
    var max = istZahl(a.hoechstanlage_eur) ? a.hoechstanlage_eur : a.hoechstanlage;
    return { min: istZahl(min) ? min : null, max: istZahl(max) ? max : null };
  }

  function passtZumBetrag(a) {
    var g = grenzenVon(a);
    if (g.min !== null && zustand.betrag < g.min) return false;
    if (g.max !== null && zustand.betrag > g.max) return false;
    return true;
  }

  /* ================================================== Filtern und Sortieren */

  /* Alles, worin gesucht werden soll, in einem Text. Wird je Angebot
     einmal gebaut und am Objekt gemerkt – bei 200 Angeboten und jedem
     Tastendruck lohnt sich das. */
  function suchtext(a) {
    if (a._suchtext) return a._suchtext;
    var teile = [
      a.bank, a.produkt, landName(a.einlagensicherung_land),
      a.einlagensicherung_land, a.waehrung, a.sicherungssystem_name,
      a.staatsrating_sp,
      a.zinstyp === "aktion" ? "aktion aktionszins befristet" : "",
      a.zinstyp === "fest" ? "festzins fest" : "",
      a.zinstyp === "variabel" ? "variabel" : "",
      a.nur_neukunden ? "neukunden neukundenangebot" : "bestandskunden",
      a.waehrungsrisiko ? "fremdwaehrung waehrungsrisiko" : "euro",
      a.stale ? "veraltet alt" : "",
    ];
    (a.quellen || []).forEach(function (q) { teile.push(q.id, q.typ); });
    a._suchtext = suchform(teile.join(" "));
    return a._suchtext;
  }

  /* Mehrere Wörter heißt UND: "chase neukunden" findet nur, was beides hat. */
  function passtZurSuche(a, worte) {
    var heu = suchtext(a);
    for (var i = 0; i < worte.length; i++) {
      if (heu.indexOf(worte[i]) === -1) return false;
    }
    return true;
  }

  function gefiltert() {
    var f = zustand.filter;
    var worte = suchform(zustand.suche).split(" ").filter(Boolean);
    var minZins = zahlAusEingabe(f.minZins);
    var ratingRang = { AAA: 4, AA: 4, A: 3, BBB: 2 };
    var minRang = f.rating ? (ratingRang[f.rating] || 0) : 0;

    return (zustand.daten.angebote || []).filter(function (a) {
      // Abgehakte Angebote sind aus der Hauptliste raus; sie stehen
      // stattdessen in den Einstellungen unter "Schon genutzt".
      if (zustand.erledigt.indexOf(a.dedupe_key) !== -1) return false;

      if (worte.length && !passtZurSuche(a, worte)) return false;
      if (f.land && (a.einlagensicherung_land || a.land) !== f.land) return false;
      if (f.typ && a.zinstyp !== f.typ) return false;
      if (f.aktion === "nur" && a.zinstyp !== "aktion") return false;
      if (f.aktion === "ohne" && a.zinstyp === "aktion") return false;
      if (f.neukunden === "nur" && !a.nur_neukunden) return false;
      if (f.neukunden === "ohne" && a.nur_neukunden) return false;
      if (f.nurEur && a.waehrung && a.waehrung !== "EUR") return false;
      if (f.ohneStale && a.stale) return false;
      if (f.nurWatch && zustand.watchlist.indexOf(a.dedupe_key) === -1) return false;
      if (f.passtZuBetrag && !passtZumBetrag(a)) return false;
      if (!isNaN(minZins) && (!istZahl(a.zinssatz_pct) || a.zinssatz_pct < minZins)) return false;
      if (minRang) {
        var rang = ratingRang[a.rating_gruppe] || 0;
        if (rang < minRang) return false;
      }
      if (f.vollGesichert) {
        var deckung = a.einlagensicherung_betrag_eur;
        if (!istZahl(deckung) || deckung < zustand.betrag) return false;
      }
      if (f.quelltyp) {
        var typen = (a.quellen || []).map(function (q) { return q.typ; });
        if (typen.indexOf(f.quelltyp) === -1) return false;
      }
      return true;
    });
  }

  function sortiert(liste) {
    var s = zustand.sortierung;
    var zahl = function (wert) { return istZahl(wert) ? wert : -999; };

    return liste.slice().sort(function (a, b) {
      switch (s) {
        // "Höchster Zins" meint das, womit die Bank wirbt.
        case "werbezins": return zahl(b.zinssatz_pct) - zahl(a.zinssatz_pct);
        // "Erstes Jahr" rechnet befristete Aktionen ehrlich herunter.
        case "brutto":    return zahl(b.brutto_12m_pct) - zahl(a.brutto_12m_pct);
        case "netto":  return zahl(nettoWert(b)) - zahl(nettoWert(a));
        case "bank":   return (a.bank || "").localeCompare(b.bank || "", "de");
        case "land":
          var la = landName(a.einlagensicherung_land), lb = landName(b.einlagensicherung_land);
          if (la !== lb) return la.localeCompare(lb, "de");
          return zahl(b[scoreFeld()]) - zahl(a[scoreFeld()]);
        default:       return zahl(b[scoreFeld()]) - zahl(a[scoreFeld()]);
      }
    });
  }

  var FILTER_TEXT = ["land", "typ", "quelltyp", "rating", "minZins", "aktion", "neukunden"];
  var FILTER_SCHALTER = ["nurEur", "nurWatch", "ohneStale", "passtZuBetrag", "vollGesichert"];

  function filterAnzahl() {
    var f = zustand.filter, n = 0;
    FILTER_TEXT.forEach(function (k) { if (f[k]) n++; });
    FILTER_SCHALTER.forEach(function (k) { if (f[k]) n++; });
    return n;
  }

  /* ================================================================ Rendern */

  var RATING_KLASSE = { AAA: "gut", AA: "gut", A: "gut", BBB: "mittel" };

  function ratingKlasse(gruppe) {
    return RATING_KLASSE[gruppe] || (gruppe ? "schwach" : "");
  }

  function ratingWort(gruppe) {
    if (gruppe === "AAA" || gruppe === "AA") return "sehr sicher";
    if (gruppe === "A") return "sicher";
    if (gruppe === "BBB") return "solide";
    if (!gruppe) return "unbekannt";
    return "erhöhtes Risiko";
  }

  function karteHtml(a, index) {
    var beobachtet = zustand.watchlist.indexOf(a.dedupe_key) !== -1;
    var klassen = ["karte"];
    if (a.stale) klassen.push("stale");
    if (beobachtet) klassen.push("watch");

    var land = a.einlagensicherung_land || a.land;
    var zinsenBrutto = inEuro(a.brutto_12m_pct);

    /* Zeile 1: Wer, und was wirbt die Bank */
    var kopf =
      '<div class="karte-kopf">' +
        '<div class="karte-titel">' +
          '<span class="bank">' + esc(a.bank) + "</span>" +
          '<span class="bank-sub">' + esc(a.produkt || "Tagesgeld") + " · " +
            esc(landName(land)) + "</span>" +
        "</div>" +
        '<div class="karte-knoepfe">' +
          (a.nur_neukunden
            ? '<button class="haken" type="button" data-erledigt="' + index + '"' +
              ' aria-label="Schon genutzt – ausblenden" title="Schon genutzt – ausblenden">' +
              ikon("haken") + "</button>"
            : "") +
          '<button class="stern' + (beobachtet ? " an" : "") + '" type="button" data-watch="' + index + '"' +
            ' aria-pressed="' + (beobachtet ? "true" : "false") + '"' +
            ' aria-label="' + (beobachtet ? "Von der Merkliste nehmen" : "Auf die Merkliste setzen") + '">' +
            ikon(beobachtet ? "stern-voll" : "stern") +
          "</button>" +
        "</div>" +
      "</div>";

    var zins =
      '<div class="zins-zeile">' +
        '<span class="zins">' + pct(a.zinssatz_pct) + "</span>" +
        '<span class="zins-dazu">pro Jahr</span>' +
      "</div>" +
      '<div class="werbung">So wirbt die Bank</div>';

    /* Aktionszins: der große Wert gilt nur eine Weile. Das muss auf die
       Karte, sonst wirkt die Euro-Zeile darunter wie ein Rechenfehler. */
    var aktion = "";
    if (a.zinstyp === "aktion" && a.aktionsdauer_monate > 0) {
      aktion =
        '<div class="aktion-hinweis">' + ikon("uhr") +
        "<span><b>Nur " + esc(a.aktionsdauer_monate) + " Monate lang.</b> Danach " +
        pct(a.folgezins_pct) + (a.folgezins_geschaetzt ? " (geschätzt)" : "") +
        " – über zwölf Monate also " + pct(a.brutto_12m_pct) + ".</span></div>";
    }

    /* Der Rechenkasten: die eigentliche Antwort auf "was bringt mir das?" */
    var rechnung =
      '<div class="rechenkasten">' + ikon("muenze") +
        '<div class="rechen-text">' +
          '<div class="rechen-haupt"><b>' + euro(zinsenBrutto) + "</b> Zinsen im ersten Jahr</div>" +
          '<div class="rechen-neben">bei ' + euro(zustand.betrag) + " · " + nettoSatz(a) + "</div>" +
        "</div>" +
      "</div>";

    /* Merkzeichen */
    var pillen = [];
    var sicher = a.einlagensicherung_betrag_eur;
    if (sicher) {
      var gedeckt = zustand.betrag <= sicher;
      pillen.push('<span class="marke-pille ' + (gedeckt ? "gut" : "mittel") + '">' + ikon("schloss") +
        (gedeckt ? "geschützt bis " + euro(sicher) : "nur " + euro(sicher) + " geschützt") + "</span>");
    } else {
      pillen.push('<span class="marke-pille">' + ikon("schloss") + "Schutz unbekannt</span>");
    }

    if (a.rating_gruppe) {
      pillen.push('<span class="marke-pille ' + ratingKlasse(a.rating_gruppe) + '">' +
        esc(landName(land)) + ": " + esc(ratingWort(a.rating_gruppe)) + "</span>");
    }
    if (a.zinstyp === "aktion" && a.aktionsdauer_monate) {
      pillen.push('<span class="marke-pille info">' + ikon("funke") +
        esc(a.aktionsdauer_monate) + " Monate Aktion</span>");
    }
    if (a.nur_neukunden) {
      pillen.push('<span class="marke-pille mittel">' + ikon("person") + "nur für Neukunden</span>");
    }
    if (a.zinstyp === "fest") {
      pillen.push('<span class="marke-pille info">Zins fest</span>');
    }
    if (a.waehrungsrisiko) {
      pillen.push('<span class="marke-pille mittel">Währung ' + esc(a.waehrung) + "</span>");
    }
    var g = grenzenVon(a);
    if (g.min !== null && g.min > 0) {
      pillen.push('<span class="marke-pille' + (zustand.betrag < g.min ? " mittel" : "") + '">ab ' +
        euro(g.min) + "</span>");
    }
    if (a.land_quelle === "quellenland_angenommen") {
      pillen.push('<span class="marke-pille" title="Aus dem Land der Quelle abgeleitet">' +
        ikon("info") + "Land angenommen</span>");
    }
    if (a.qst_reibung) {
      pillen.push('<span class="marke-pille mittel">' + ikon("uhr") + "Steuer erst zurückholen</span>");
    }
    if (a.stale) {
      pillen.push('<span class="marke-pille">' + ikon("uhr") + "Stand " + esc(datumKurz(a.stale_seit || a.stand)) + "</span>");
    }
    if (a.flag === "pruefen") {
      pillen.push('<span class="marke-pille mittel">' + ikon("warnung") + "ungewöhnlich hoch</span>");
    }
    if (a.extraction_tier === 3) {
      pillen.push('<span class="marke-pille">automatisch erkannt</span>');
    }
    if (a.override) {
      pillen.push('<span class="marke-pille info">von Hand geprüft</span>');
    }

    return '<li class="' + klassen.join(" ") + '" data-index="' + index +
      '" style="animation-delay:' + Math.min(index, 9) * 28 + 'ms" tabindex="0"' +
      ' aria-label="' + esc(a.bank) + ", " + pct(a.zinssatz_pct) + ', Einzelheiten öffnen">' +
      kopf + zins + aktion + rechnung +
      '<div class="marken">' + pillen.join("") + "</div>" +
      "</li>";
  }

  function rendern() {
    if (!zustand.daten) return;
    zustand.sichtbar = sortiert(gefiltert());

    var zeigen = Math.min(zustand.limit, zustand.sichtbar.length);
    $("liste").innerHTML = zustand.sichtbar.slice(0, zeigen).map(karteHtml).join("");
    $("leer").hidden = zustand.sichtbar.length > 0;

    var rest = zustand.sichtbar.length - zeigen;
    var mehr = $("btnMehr");
    mehr.hidden = rest <= 0;
    mehr.textContent = rest > 0
      ? "Weitere " + Math.min(rest, SEITE) + " von " + rest + " anzeigen" : "";

    var n = filterAnzahl();
    $("filterAnzahl").textContent = n;
    $("filterAnzahl").hidden = n === 0;
    $("btnFilter").classList.toggle("aktiv", n > 0);

    aktiveFilterZeigen();
    heldZeigen();
    referenzZeigen();
    statistikZeigen();
  }

  var TYP_TEXT = { variabel: "variabler Zins", aktion: "Aktionszins", fest: "fester Zins" };
  var QUELLTYP_TEXT = {
    bank: "direkt von der Bank", plattform: "über eine Zinsplattform",
    portal: "über ein Vergleichsportal",
  };
  var RATING_TEXT = { AAA: "nur sehr sichere Länder", A: "mindestens sicher", BBB: "mindestens solide" };

  function aktiveFilterZeigen() {
    var f = zustand.filter;
    var chips = [];
    if (f.land) chips.push({ k: "land", t: landName(f.land) });
    if (f.typ) chips.push({ k: "typ", t: TYP_TEXT[f.typ] || f.typ });
    if (f.quelltyp) chips.push({ k: "quelltyp", t: QUELLTYP_TEXT[f.quelltyp] || f.quelltyp });
    if (f.rating) chips.push({ k: "rating", t: RATING_TEXT[f.rating] || f.rating });
    if (f.minZins && !isNaN(zahlAusEingabe(f.minZins))) {
      chips.push({ k: "minZins", t: "ab " + pctSchlank(zahlAusEingabe(f.minZins)) });
    }
    if (f.aktion) chips.push({ k: "aktion", t: f.aktion === "nur" ? "nur Aktionen" : "ohne Aktionen" });
    if (f.neukunden) chips.push({ k: "neukunden", t: f.neukunden === "nur" ? "nur für Neukunden" : "ohne Neukunden-Angebote" });
    if (f.nurEur) chips.push({ k: "nurEur", t: "nur Euro" });
    if (f.nurWatch) chips.push({ k: "nurWatch", t: "nur Merkliste" });
    if (f.ohneStale) chips.push({ k: "ohneStale", t: "ohne alte Werte" });
    if (f.passtZuBetrag) chips.push({ k: "passtZuBetrag", t: "passt zu " + euro(zustand.betrag) });
    if (f.vollGesichert) chips.push({ k: "vollGesichert", t: euro(zustand.betrag) + " voll geschützt" });

    var el = $("aktiveFilter");
    el.hidden = chips.length === 0;
    el.innerHTML = chips.map(function (c) {
      return '<button class="filter-chip" type="button" data-filter-weg="' + c.k + '">' +
        esc(c.t) + ikon("x") + "</button>";
    }).join("");
  }

  function heldZeigen() {
    var el = $("heldKarte");
    // Der Held zeigt immer den Spitzenreiter der Empfehlung – unabhängig
    // davon, wonach die Liste gerade sortiert ist.
    var beste = null;
    zustand.sichtbar.forEach(function (a) {
      if (a.stale) return;
      if (!beste || (a[scoreFeld()] || -99) > (beste[scoreFeld()] || -99)) beste = a;
    });

    if (!beste || zustand.suche || zustand.sichtbar.length < 3) { el.hidden = true; return; }
    el.hidden = false;
    el.dataset.key = beste.dedupe_key;

    $("heldSatz").innerHTML = esc(beste.bank) + " zahlt " +
      "<strong>" + pct(beste.zinssatz_pct) + "</strong>" +
      (beste.zinstyp === "aktion" ? " für " + esc(beste.aktionsdauer_monate) + " Monate" : "");
    $("heldSub").textContent = "Das sind " + euro(inEuro(beste.brutto_12m_pct)) +
      " im ersten Jahr bei " + euro(zustand.betrag) + ".";
  }

  function referenzWaehlen() {
    var mir = ((zustand.daten && zustand.daten.referenz) || {}).ezb_mir || {};
    var land = zustand.filter.land;
    if (land && mir[land]) return { land: land, eintrag: mir[land] };
    if (mir.U2) return { land: "U2", eintrag: mir.U2 };
    var keys = Object.keys(mir);
    return keys.length ? { land: keys[0], eintrag: mir[keys[0]] } : null;
  }

  function referenzZeigen() {
    var el = $("referenzZeile");
    if (!zustand.daten) { el.hidden = true; return; }

    var wahl = referenzWaehlen();
    var estr = ((zustand.daten.referenz) || {}).estr || {};
    if (!wahl) { el.hidden = true; return; }
    el.hidden = false;

    var beste = 0;
    (zustand.daten.angebote || []).forEach(function (a) {
      if (!a.stale && istZahl(a.zinssatz_pct) && a.zinssatz_pct > beste) beste = a.zinssatz_pct;
    });

    var schnitt = wahl.eintrag.wert_pct;
    var satz = "Im Schnitt zahlen Banken <strong>" + pct(schnitt) + "</strong> (" +
      esc(landName(wahl.land)) + ").";
    if (beste && istZahl(schnitt)) {
      satz += " Hier gibt es bis zu <strong>" + pct(beste) + "</strong>.";
    }
    $("referenzSatz").innerHTML = satz;
    // Klassenname aus Fremddaten: nur die drei bekannten Werte zulassen.
    var trend = ["steigend", "fallend", "stabil"].indexOf(estr.trend) !== -1 ? estr.trend : "";
    $("referenzPunkt").className = "referenz-punkt " + trend;
  }

  function statistikZeigen() {
    var alle = zustand.daten.angebote || [];
    var gesamt = alle.length;
    var stat = zustand.daten.statistik || {};
    var stand = datumKurz(zustand.daten.stand_datum || zustand.daten.stand);

    var teile = [];
    teile.push(zustand.sichtbar.length === gesamt
      ? gesamt + " Angebote"
      : zustand.sichtbar.length + " von " + gesamt + " Angeboten");
    teile.push("Stand " + stand);

    if (stat.quellen_erfolg && stat.quellen_gesamt) {
      teile.push(stat.quellen_erfolg + " von " + stat.quellen_gesamt + " Quellen erreichbar");
    }
    var veraltet = alle.filter(function (a) { return a.stale; }).length;
    if (veraltet) teile.push(veraltet + " mit älterem Stand");

    var erkannt = alle.filter(function (a) { return a.extraction_tier === 3; }).length;
    if (erkannt) teile.push(erkannt + " automatisch erkannt");

    if (zustand.erledigt.length) teile.push(zustand.erledigt.length + " abgehakt");

    $("fussStatistik").textContent = teile.join(" · ");
  }

  /* ================================================================== Sheet
   *
   * Ein Element für alle Inhalte. `sheetZeigen` bekommt Titel, optionale
   * Reiter und den Körper; Öffnen, Schließen, Zurück-Taste und Fokus
   * laufen immer durch dieselben zwei Funktionen.
   */

  var sheetHistorie = false;   // liegt ein eigener History-Eintrag?
  var eigenesZurueck = false;  // wartet ein selbst ausgelöstes history.back()?
  var aktuelleFolien = null;   // { titel, reiter:[{name, bau}], index }
  var vorherFokus = null;

  function sheetOffen() { return !$("sheet").hidden; }

  function sheetZeigen(opt) {
    var sheet = $("sheet");
    if (!sheetOffen()) vorherFokus = document.activeElement;

    $("sheetTitel").textContent = opt.titel || "";

    var reiterEl = $("sheetReiter");
    if (opt.reiter && opt.reiter.length > 1) {
      aktuelleFolien = { reiter: opt.reiter, index: opt.start || 0 };
      reiterEl.hidden = false;
      reiterEl.innerHTML = opt.reiter.map(function (r, i) {
        return '<button class="reiter' + (i === aktuelleFolien.index ? " aktiv" : "") +
          '" type="button" role="tab" aria-selected="' + (i === aktuelleFolien.index) +
          '" data-folie="' + i + '">' + esc(r.name) + "</button>";
      }).join("");
      folieZeigen(aktuelleFolien.index, 0);
    } else {
      aktuelleFolien = null;
      reiterEl.hidden = true;
      reiterEl.innerHTML = "";
      $("sheetBody").innerHTML = opt.koerper || "";
      $("sheetBody").scrollTop = 0;
    }

    var fuss = $("sheetFuss");
    if (opt.fuss) { fuss.hidden = false; fuss.innerHTML = opt.fuss; }
    else { fuss.hidden = true; fuss.innerHTML = ""; }

    sheet.hidden = false;
    document.body.style.overflow = "hidden";

    historieMerken();

    hintergrundStilllegen(true);

    if (typeof opt.danach === "function") opt.danach();
    // Fokus in den Dialog, sonst hängt er hinter der Abdeckung.
    setTimeout(function () { $("btnSheetX").focus({ preventScroll: true }); }, 30);
  }

  /* Ein eigener History-Eintrag, damit die Android-Zurück-Taste das
     Sheet schließt statt die App zu beenden. */
  function historieMerken() {
    if (sheetHistorie) return;
    try {
      // Steht schon ein verwaister Marker im Verlauf (kann nach einem
      // schnellen Zu-und-wieder-Auf passieren), diesen weiterverwenden
      // statt einen zweiten anzulegen. Sonst braucht die Zurück-Taste
      // hinterher einen Druck mehr.
      if (history.state && history.state.zrSheet) { sheetHistorie = true; return; }
      history.pushState({ zrSheet: true }, "");
      sheetHistorie = true;
    } catch (e) { /* file:// erlaubt kein pushState */ }
  }

  /* Alles hinter dem Sheet für Tastatur und Screenreader abschalten.
     Ohne das läuft die Tabulator-Taste aus dem Dialog in die Liste
     dahinter – bei 190 Karten sind das über 200 erreichbare Elemente.
     `inert` gibt es ab Chrome 102; für ältere WebViews bleibt
     aria-hidden plus das Ausschalten der Tabstopps. */
  function hintergrundStilllegen(an) {
    ["kopfMarker", "hauptbereich", "fussbereich"].forEach(function (id) {
      var el = $(id);
      if (!el) return;
      if (an) {
        el.setAttribute("aria-hidden", "true");
        if ("inert" in el) el.inert = true;
      } else {
        el.removeAttribute("aria-hidden");
        if ("inert" in el) el.inert = false;
      }
    });
    if (!("inert" in document.createElement("div"))) {
      // Notlösung für WebViews ohne inert: Tabstopps einsammeln.
      var liste = $("liste");
      if (liste) {
        Array.prototype.forEach.call(liste.querySelectorAll("[tabindex], button"), function (el) {
          if (an) { el.dataset.tabAlt = el.getAttribute("tabindex") || ""; el.setAttribute("tabindex", "-1"); }
          else if (el.dataset.tabAlt !== undefined) {
            if (el.dataset.tabAlt) el.setAttribute("tabindex", el.dataset.tabAlt);
            else el.removeAttribute("tabindex");
            delete el.dataset.tabAlt;
          }
        });
      }
    }
  }

  function folieZeigen(index, richtung) {
    if (!aktuelleFolien) return;
    var anzahl = aktuelleFolien.reiter.length;
    index = Math.max(0, Math.min(anzahl - 1, index));
    aktuelleFolien.index = index;

    var body = $("sheetBody");
    var punkte = '<div class="folie-punkte">' +
      aktuelleFolien.reiter.map(function (r, i) {
        return '<button class="folie-punkt' + (i === index ? " aktiv" : "") +
          '" type="button" data-folie="' + i + '" aria-label="' + esc(r.name) + '"></button>';
      }).join("") + "</div>";

    body.innerHTML = '<div class="folie' + (richtung < 0 ? " rueckwaerts" : "") + '">' +
      aktuelleFolien.reiter[index].bau() + punkte + "</div>";
    body.scrollTop = 0;

    Array.prototype.forEach.call($("sheetReiter").children, function (knopf, i) {
      knopf.classList.toggle("aktiv", i === index);
      knopf.setAttribute("aria-selected", i === index ? "true" : "false");
    });
  }

  function folieWechseln(schritt) {
    if (!aktuelleFolien) return;
    var neu = aktuelleFolien.index + schritt;
    if (neu < 0 || neu >= aktuelleFolien.reiter.length) return;
    folieZeigen(neu, schritt);
  }

  function sheetSchliessen(vonZurueckTaste) {
    if (!sheetOffen()) return;
    $("sheet").hidden = true;
    $("sheetBody").innerHTML = "";
    aktuelleFolien = null;
    document.body.style.overflow = "";
    hintergrundStilllegen(false);

    if (sheetHistorie) {
      sheetHistorie = false;
      if (!vonZurueckTaste) {
        // history.back() wirkt erst im nächsten Tick. Wird in der
        // Zwischenzeit ein neues Sheet geöffnet, würde das nachlaufende
        // popstate dieses gleich wieder schließen. Deshalb merken, dass
        // das kommende popstate von uns selbst stammt.
        eigenesZurueck = true;
        try { history.back(); } catch (e) { eigenesZurueck = false; }
      }
    }
    if (vorherFokus && typeof vorherFokus.focus === "function") {
      try { vorherFokus.focus({ preventScroll: true }); } catch (e) { /* egal */ }
    }
    vorherFokus = null;
  }

  /* ======================================================= Inhalt: Angebot */

  function detailOeffnen(index) {
    var a = zustand.sichtbar[index];
    if (!a) return;

    sheetZeigen({
      titel: a.bank,
      reiter: [
        { name: "Angebot",     bau: function () { return folieAngebot(a); } },
        { name: "Nach Steuern", bau: function () { return folieSteuern(a); } },
        { name: "Sicherheit",  bau: function () { return folieSicherheit(a); } },
        { name: "Herkunft",    bau: function () { return folieHerkunft(a); } },
      ],
      fuss: '<button class="primaer" type="button" data-watch-key="' + esc(a.dedupe_key) + '">' +
        (zustand.watchlist.indexOf(a.dedupe_key) !== -1 ? "Von der Merkliste nehmen" : "Auf die Merkliste") +
        "</button>" +
        (a.nur_neukunden
          ? '<button class="zweit" type="button" data-erledigt-key="' + esc(a.dedupe_key) + '">' +
            "Schon genutzt</button>"
          : '<button class="zweit" type="button" data-schliessen>Schließen</button>'),
    });
  }

  function folieAngebot(a) {
    var land = a.einlagensicherung_land || a.land;
    var h = [];

    h.push('<div class="gross-zins"><span class="wert">' + pct(a.zinssatz_pct) + "</span>" +
      '<span class="label">So wirbt ' + esc(a.bank) + "</span></div>");

    if (a.zinstyp === "aktion" && a.aktionsdauer_monate > 0) {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("uhr") +
        "Das ist ein Angebot auf Zeit</div>" +
        "Die " + pct(a.zinssatz_pct) + " gibt es " + esc(a.aktionsdauer_monate) +
        " Monate lang. Danach zahlt die Bank " + pct(a.folgezins_pct) +
        (a.folgezins_geschaetzt
          ? " – dieser Wert stand nicht im Angebot und ist geschätzt."
          : ".") +
        " Übers ganze erste Jahr gerechnet sind es deshalb " + pct(a.brutto_12m_pct) + ".</div>");
    }

    if (a.nur_neukunden) {
      h.push('<div class="info-karte"><div class="kopfzeile">' + ikon("person") +
        "Nur für Neukunden</div>Diesen Zins gibt es nur, wenn du dort noch kein " +
        "Konto hattest. Einmal genutzt, ist er für dich weg – dann kannst du das " +
        "Angebot unten abhaken und siehst es nicht mehr in der Liste.</div>");
    }

    h.push("<h3>Was das bei " + euro(zustand.betrag) + " bedeutet</h3>");
    h.push('<div class="schritte">');
    h.push(schritt("Zinsen im ersten Jahr", pct(a.brutto_12m_pct) + " von " + euro(zustand.betrag),
      euroGenau(inEuro(a.brutto_12m_pct))));
    var qstJetzt = qstWert(a);
    h.push(schritt(
      (istZahl(qstJetzt) && qstJetzt > 0) || zustand.einstellungen.abgeltung
        ? "Davon bleiben nach Steuern" : "Davon geht nichts ab",
      "mehr dazu auf der nächsten Seite", euroGenau(inEuro(nettoWert(a))), "summe"));
    h.push("</div>");

    h.push('<p class="satz zart">Der Betrag lässt sich oben in der App jederzeit ändern. ' +
      "Zinsen werden hier einfach gerechnet, ohne Zinseszins innerhalb des Jahres.</p>");

    h.push("<h3>Auf einen Blick</h3>");
    h.push('<dl class="paare">');
    h.push(paar("Produkt", esc(a.produkt || "Tagesgeld")));
    h.push(paar("Land der Bank", esc(landName(land)) +
      (a.land_quelle === "quellenland_angenommen" ? " (angenommen)" : "")));
    h.push(paar("Art des Zinses", { variabel: "variabel – kann sich ändern",
      aktion: "Aktionszins auf Zeit", fest: "fest für die Laufzeit" }[a.zinstyp] || esc(a.zinstyp || "–")));
    h.push(paar("Währung", esc(a.waehrung || "EUR") +
      (a.waehrungsrisiko ? " – Wechselkurs kann den Gewinn auffressen" : "")));

    var g = grenzenVon(a);
    h.push(paar("Mindestanlage", g.min === null ? "keine Angabe" : (g.min === 0 ? "keine" : euro(g.min))));
    h.push(paar("Höchstanlage", g.max === null ? "keine Angabe" : euro(g.max)));
    h.push("</dl>");

    if (g.min !== null && g.min > 0 && zustand.betrag < g.min) {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("info") +
        "Dein Betrag ist zu klein</div>Die Bank verlangt mindestens " + euro(g.min) +
        ", du hast " + euro(zustand.betrag) + " eingestellt.</div>");
    }
    return h.join("");
  }

  function folieSteuern(a) {
    var qst = qstWert(a);
    var grund = zustand.einstellungen.erstattung
      ? a.qst_begruendung_mit_erstattung : a.qst_begruendung_ohne_erstattung;
    var brutto = inEuro(a.brutto_12m_pct);
    var netto = inEuro(nettoWert(a));
    var abzug = (istZahl(brutto) && istZahl(netto)) ? brutto - netto : 0;
    var gehtWasAb = abzug > 0.005;

    var h = [];

    if (gehtWasAb) {
      var anteil = brutto > 0 ? Math.max(0, Math.min(100, netto / brutto * 100)) : 100;
      h.push('<p class="satz">Von den <strong>' + euroGenau(brutto) + "</strong> Zinsen " +
        "gehen <strong>" + euroGenau(abzug) + "</strong> an Steuern ab.</p>");
      h.push('<div class="balken">' +
        '<div class="balken-teil bleibt" style="width:' + anteil.toFixed(1) + '%">' +
          (anteil > 30 ? euro(netto) : "") + "</div>" +
        '<div class="balken-teil steuer" style="width:' + (100 - anteil).toFixed(1) + '%">' +
          (100 - anteil > 30 ? euro(abzug) : "") + "</div>" +
        "</div>");
      h.push('<div class="balken-legende">' +
        '<span><i class="legende-punkt" style="background:var(--akzent)"></i>bleibt dir</span>' +
        '<span><i class="legende-punkt" style="background:var(--rot)"></i>Steuern</span>' +
        "</div>");
    } else {
      h.push('<div class="info-karte"><div class="kopfzeile">' + ikon("muenze") +
        "Hier geht nichts ab</div>Die vollen <strong>" + euroGenau(brutto) +
        "</strong> Zinsen bleiben dir." +
        (zustand.einstellungen.abgeltung ? "" :
          " Die deutsche Abgeltungssteuer ist dabei nicht eingerechnet – " +
          "die kannst du in den Einstellungen einblenden.") + "</div>");
    }

    h.push("<h3>Schritt für Schritt</h3>");
    h.push('<div class="schritte">');
    h.push(schritt("Zinsen im ersten Jahr", pct(a.brutto_12m_pct) + " von " + euro(zustand.betrag),
      euroGenau(brutto)));

    if (istZahl(qst) && qst > 0) {
      h.push(schritt("Quellensteuer " + esc(landName(a.einlagensicherung_land)),
        pctSchlank(qst) + " behält das Land direkt ein",
        "− " + euroGenau(brutto * qst / 100), "abzug"));
    } else {
      h.push(schritt("Quellensteuer", "wird hier nicht fällig", "0,00 €"));
    }

    if (zustand.einstellungen.abgeltung) {
      var vorAbg = zustand.einstellungen.erstattung
        ? a.netto_12m_mit_erstattung_pct : a.netto_12m_ohne_erstattung_pct;
      var vorAbgEuro = inEuro(vorAbg);
      h.push(schritt("Deutsche Abgeltungssteuer", "25 % plus Solidaritätszuschlag",
        (istZahl(vorAbgEuro) && istZahl(netto))
          ? "− " + euroGenau(vorAbgEuro - netto) : "–", "abzug"));
    }

    h.push(schritt("Das bleibt dir", pct(nettoWert(a)) + " im ersten Jahr",
      euroGenau(netto), "summe"));
    h.push("</div>");

    if (grund) {
      h.push('<div class="info-karte"><div class="kopfzeile">' + ikon("info") +
        "Warum?</div>" + esc(grund) + "</div>");
    }

    // Der Score rechnet mit dem Satz nach Steuerabkommen. Wo die Bank aber
    // erst einbehält und du selbst zurückfordern musst, gehört das dazu.
    if (a.qst_reibung) {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("uhr") +
        "Erst weg, dann zurück</div>" + esc(a.qst_reibung) + "</div>");
    }

    if (a.rueckerstattung_formular && (a.qst_reibung || (istZahl(qst) && qst > 0))) {
      h.push('<p class="satz zart">Dafür brauchst du: ' + esc(a.rueckerstattung_formular) +
        (sicherLink(a.rueckerstattung_quelle)
          ? ' · <a href="' + esc(sicherLink(a.rueckerstattung_quelle)) +
            '" target="_blank" rel="noopener noreferrer">zur Behörde</a>'
          : "") + "</p>");
    }

    h.push('<div class="info-karte"><div class="kopfzeile">' + ikon("info") +
      "Was ist Quellensteuer?</div>" +
      "Zinsen aus dem Ausland werden oft schon dort besteuert, bevor das Geld " +
      "bei dir ankommt. Zwischen Deutschland und den meisten Ländern gibt es " +
      "Abkommen, mit denen du dir das zurückholen kannst – gegen Formulare " +
      "und Wartezeit.</div>");

    if (!zustand.einstellungen.abgeltung && gehtWasAb) {
      h.push('<p class="satz zart">Die deutsche Abgeltungssteuer von 25 % plus ' +
        "Solidaritätszuschlag kommt hier noch obendrauf. Sie trifft jeden Anbieter " +
        "gleich und ist deshalb ausgeblendet – einblenden kannst du sie in den " +
        "Einstellungen.</p>");
    }
    return h.join("");
  }

  function folieSicherheit(a) {
    var land = a.einlagensicherung_land || a.land;
    var sicher = a.einlagensicherung_betrag_eur;
    var gedeckt = istZahl(sicher) && zustand.betrag <= sicher;
    var h = [];

    h.push('<div class="info-karte' + (gedeckt ? "" : " warnung") + '">' +
      '<div class="kopfzeile">' + ikon("schloss") +
      (gedeckt ? "Dein Geld ist abgesichert" : "Achtung beim Betrag") + "</div>" +
      (istZahl(sicher)
        ? (gedeckt
            ? "Geht die Bank pleite, bekommst du bis " + euro(sicher) +
              " ersetzt. Deine " + euro(zustand.betrag) + " liegen darunter."
            : "Abgesichert sind nur " + euro(sicher) + ". Von deinen " +
              euro(zustand.betrag) + " wären " + euro(zustand.betrag - sicher) + " ungeschützt.")
        : "Für dieses Angebot liegt keine Angabe zur Einlagensicherung vor.") +
      "</div>");

    if (a.sicherungssystem_name) {
      h.push('<p class="satz zart">Zuständig ist die ' + esc(a.sicherungssystem_name) +
        (sicherLink(a.sicherung_quelle)
          ? ' · <a href="' + esc(sicherLink(a.sicherung_quelle)) +
            '" target="_blank" rel="noopener noreferrer">Website</a>'
          : "") + ".</p>");
    }

    h.push("<h3>Wie stabil ist das Land?</h3>");
    h.push('<p class="satz"><strong>' + esc(landName(land)) + "</strong> gilt als <strong>" +
      esc(ratingWort(a.rating_gruppe)) + "</strong>." +
      (a.staatsrating_sp
        ? " Die Ratingagentur Standard &amp; Poor's vergibt die Note " + esc(a.staatsrating_sp) + "."
        : "") + "</p>");

    if (istZahl(a.risiko_abschlag_pp) && a.risiko_abschlag_pp > 0) {
      h.push('<p class="satz zart">Weil ein Ausfall dort etwas wahrscheinlicher ist, zieht ' +
        "Zinsradar in der Empfehlung " + nfZins.format(a.risiko_abschlag_pp) +
        " Prozentpunkte ab. Der Zins selbst bleibt davon unberührt.</p>");
    } else {
      h.push('<p class="satz zart">Für die Empfehlung wird hier nichts abgezogen – ' +
        "die Bewertung ist so gut, wie sie sein kann.</p>");
    }

    h.push("<h3>Die Empfehlung dieses Angebots</h3>");
    h.push('<div class="schritte">');
    h.push(schritt("Zins nach Steuern", "über zwölf Monate", pct(nettoWert(a))));
    if (istZahl(a.risiko_abschlag_pp) && a.risiko_abschlag_pp > 0) {
      h.push(schritt("Abzug fürs Länderrisiko", esc(landName(land)),
        "− " + nfZins.format(a.risiko_abschlag_pp) + " %", "abzug"));
    }
    h.push(schritt("Empfehlungswert", "danach ist die Liste sortiert",
      pct(a[scoreFeld()], nfFein), "summe"));
    h.push("</div>");

    if (a.waehrungsrisiko) {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("warnung") +
        "Fremde Währung</div>Dieses Konto läuft in " + esc(a.waehrung) +
        ". Ändert sich der Wechselkurs, kann das mehr ausmachen als der ganze Zins.</div>");
    }
    return h.join("");
  }

  function folieHerkunft(a) {
    var h = [];

    h.push('<p class="satz">Diese Zahlen kommen nicht von Zinsradar, sondern von ' +
      "öffentlichen Seiten. Ein Programm liest sie einmal am Tag automatisch aus. " +
      "Vor dem Abschluss also bitte immer beim Anbieter selbst nachsehen.</p>");

    h.push("<h3>Gefunden bei</h3>");
    h.push('<ul class="quellen">');
    (a.quellen || []).forEach(function (q) {
      var wie = q.extraction_tier === 1 ? "aus den strukturierten Daten der Seite"
        : q.extraction_tier === 3 ? "automatisch aus dem Fließtext erkannt"
        : "aus der Tabelle der Seite gelesen";
      h.push('<li class="quelle">' +
        (sicherLink(q.url)
          ? '<a href="' + esc(sicherLink(q.url)) +
            '" target="_blank" rel="noopener noreferrer">' + esc(q.id || q.url) + "</a>"
          : esc(q.id || "unbekannt")) +
        '<span class="klein">' + esc(wie) + "</span></li>");
    });
    h.push("</ul>");

    if (a.quellen_abweichung && a.quellen_abweichung.length) {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("warnung") +
        "Die Quellen sind sich uneinig</div>" +
        esc(a.quellen_abweichung.map(function (q) {
          return q.quelle + " nennt " + pct(q.zinssatz_pct);
        }).join(", ")) + ". Angezeigt wird der Wert der verlässlichsten Quelle.</div>");
    }

    if (a.stale) {
      var tage = tageSeit(a.stale_seit || a.stand);
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("uhr") +
        "Der Wert ist nicht mehr frisch</div>" +
        "Stand vom " + esc(datumKurz(a.stale_seit || a.stand)) +
        (tage !== null ? " – das ist " + tage + " Tage her" : "") + ". " +
        esc(a.stale_grund || "Die Quelle war zuletzt nicht erreichbar.") + "</div>");
    }

    if (a.flag === "pruefen") {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("warnung") +
        "Ungewöhnlich hoher Wert</div>" + esc(a.flag_grund || "") +
        " Das kann ein Lockangebot sein – oder ein Lesefehler. Bitte nachprüfen.</div>");
    }

    if (a.extraction_tier === 3) {
      h.push('<div class="info-karte warnung"><div class="kopfzeile">' + ikon("info") +
        "Automatisch erkannt</div>Ein Sprachmodell hat diesen Eintrag aus dem Seitentext " +
        "gezogen, weil die Seite keine saubere Tabelle hatte. Solche Werte stimmen " +
        "meistens, aber nicht immer.</div>");
    }

    if (a.land_quelle === "quellenland_angenommen") {
      h.push('<div class="info-karte"><div class="kopfzeile">' + ikon("info") +
        "Land angenommen</div>Im Angebot stand nicht, in welchem Land dein Geld " +
        "abgesichert ist. Angenommen wurde das Land der Website. Bei einer " +
        "ausländischen Bank auf einem deutschen Vergleichsportal kann das falsch sein – " +
        "und dann stimmen auch Steuer und Rating nicht.</div>");
    }

    h.push("<h3>Vergleich mit der Zentralbank</h3>");
    if (istZahl(a.ezb_landesdurchschnitt_pct)) {
      h.push('<p class="satz">Banken in ' + esc(landName(a.einlagensicherung_land)) +
        " zahlen laut Europäischer Zentralbank im Schnitt " +
        pct(a.ezb_landesdurchschnitt_pct) + " (Stand " + esc(a.ezb_periode || "?") + "). " +
        "Dieses Angebot liegt " +
        (a.differenz_zu_ezb_pp > 0 ? nfZins.format(a.differenz_zu_ezb_pp) + " Prozentpunkte darüber"
                                   : nfZins.format(Math.abs(a.differenz_zu_ezb_pp || 0)) + " Prozentpunkte darunter") +
        ".</p>");
      h.push('<p class="satz zart">Der Schnitt der Zentralbank enthält auch Girokonten ' +
        "mit null Zinsen. Gute Angebote liegen deshalb fast immer deutlich darüber.</p>");
    } else {
      h.push('<p class="satz zart">Für dieses Land liegt kein Vergleichswert der ' +
        "Zentralbank vor.</p>");
    }
    return h.join("");
  }

  function schritt(text, hilfe, wert, klasse) {
    return '<div class="schritt' + (klasse ? " " + klasse : "") + '">' +
      '<span class="schritt-text">' + text +
        (hilfe ? '<span class="schritt-hilf">' + hilfe + "</span>" : "") + "</span>" +
      '<span class="schritt-wert">' + wert + "</span></div>";
  }

  function paar(dt, dd) {
    return '<div class="paar"><dt>' + dt + "</dt><dd>" + dd + "</dd></div>";
  }

  /* ======================================================== Inhalt: Betrag */

  function betragOeffnen() {
    sheetZeigen({
      titel: "Wie viel möchtest du anlegen?",
      koerper:
        '<p class="satz">Alle Euro-Beträge in der App rechnen mit dieser Zahl.</p>' +
        '<div class="chips" id="betragChips">' +
          BETRAG_VORSCHLAEGE.map(function (b) {
            return '<button class="chip' + (b === zustand.betrag ? " aktiv" : "") +
              '" type="button" data-betrag="' + b + '">' + euro(b) + "</button>";
          }).join("") +
        "</div>" +
        '<label class="feld"><span>Oder einen eigenen Betrag</span>' +
        '<input type="text" id="betragEingabe" inputmode="decimal" ' +
        'autocomplete="off" enterkeyhint="done" value="' + esc(nfEuro.format(zustand.betrag)) +
        '"></label>' +
        '<p class="satz zart">Tipp: Die gesetzliche Einlagensicherung deckt in der ' +
        "ganzen EU 100.000 € je Bank und Person ab. Wer mehr anlegt, verteilt " +
        "besser auf mehrere Banken.</p>",
      fuss: '<button class="primaer" type="button" id="btnBetragSpeichern">Übernehmen</button>',
    });
  }

  function betragSetzen(wert, schliessen) {
    var zahl = Math.round(zahlAusEingabe(wert));
    if (!isFinite(zahl) || zahl < 1) { toast("Bitte einen Betrag über 0 € eingeben"); return; }
    zustand.betrag = Math.min(zahl, 10000000);
    schreib(SPEICHER.betrag, zustand.betrag);
    betragAnzeigen();
    rendern();
    if (schliessen) { sheetSchliessen(); toast("Gerechnet wird jetzt mit " + euro(zustand.betrag)); }
  }

  function betragAnzeigen() {
    $("betragAnzeige").textContent = euro(zustand.betrag);
  }

  /* ======================================================== Inhalt: Filter */

  function filterOeffnen() {
    var laender = {};
    (zustand.daten ? zustand.daten.angebote || [] : []).forEach(function (a) {
      var l = a.einlagensicherung_land || a.land;
      if (l) laender[l] = (laender[l] || 0) + 1;
    });
    var sortiertLaender = Object.keys(laender).sort(function (x, y) {
      return landName(x).localeCompare(landName(y), "de");
    });

    var f = zustand.filter;
    var hatNeukundenDaten = (zustand.daten ? zustand.daten.angebote || [] : [])
      .some(function (a) { return a.nur_neukunden; });

    var wahl = function (id, label, hilfe, optionen, wert) {
      return '<label class="feld"><span>' + label +
        (hilfe ? ' <em class="feld-hilfe">' + hilfe + "</em>" : "") + "</span><select id=\"" + id + "\">" +
        optionen.map(function (o) {
          return '<option value="' + esc(o[0]) + '"' + (String(wert) === String(o[0]) ? " selected" : "") +
            ">" + esc(o[1]) + "</option>";
        }).join("") + "</select></label>";
    };
    var schalter = function (id, an, titel, text) {
      return '<label class="schalter"><input type="checkbox" id="' + id + '"' + (an ? " checked" : "") +
        "><span><strong>" + titel + "</strong><em>" + text + "</em></span></label>";
    };

    sheetZeigen({
      titel: "Filter",
      koerper:
        wahl("fLand", "Land der Bank", "", [["", "alle Länder"]].concat(
          sortiertLaender.map(function (l) {
            return [l, landName(l) + " (" + laender[l] + ")"];
          })), f.land) +

        wahl("fAktion", "Befristete Aktionen", "", [
          ["", "alle Angebote"],
          ["nur", "nur Aktionsangebote"],
          ["ohne", "keine Aktionen – nur Dauerzins"],
        ], f.aktion) +

        // Ältere Datenstände kennen das Feld nicht. Dann führt der Filter
        // nur in eine leere Liste – also gar nicht erst anbieten.
        (hatNeukundenDaten
          ? wahl("fNeukunden", "Neukunden", "", [
              ["", "alle Angebote"],
              ["nur", "nur Neukunden-Angebote"],
              ["ohne", "ohne Neukunden-Angebote"],
            ], f.neukunden)
          : "") +

        wahl("fTyp", "Art des Zinses", "", [
          ["", "alle"],
          ["variabel", "variabel – kann sich ändern"],
          ["aktion", "Aktionszins auf Zeit"],
          ["fest", "fest für die Laufzeit"],
        ], f.typ) +

        wahl("fRating", "Wie stabil muss das Land sein?", "", [
          ["", "egal"],
          ["AAA", "nur sehr sichere Länder"],
          ["A", "mindestens sicher"],
          ["BBB", "mindestens solide"],
        ], f.rating) +

        wahl("fQuelltyp", "Woher das Angebot kommt", "", [
          ["", "alle"],
          ["bank", "direkt von der Bank"],
          ["plattform", "über eine Zinsplattform"],
          ["portal", "über ein Vergleichsportal"],
        ], f.quelltyp) +

        '<label class="feld"><span>Mindestzins</span>' +
        '<input type="text" id="fMinZins" inputmode="decimal" autocomplete="off" ' +
        'placeholder="z. B. 3" value="' + esc(f.minZins) + '"></label>' +

        schalter("fPasst", f.passtZuBetrag, "Nur was zu " + euro(zustand.betrag) + " passt",
          "Blendet aus, wo dein Betrag unter dem Mindest- oder über dem Höchstbetrag liegt.") +
        schalter("fVoll", f.vollGesichert, euro(zustand.betrag) + " voll geschützt",
          "Nur Banken, deren Einlagensicherung deinen ganzen Betrag abdeckt.") +
        schalter("fNurEur", f.nurEur, "Nur Euro", "Kein Wechselkursrisiko.") +
        schalter("fNurWatch", f.nurWatch, "Nur meine Merkliste",
          "Zeigt die " + zustand.watchlist.length + " gemerkten Angebote.") +
        schalter("fOhneStale", f.ohneStale, "Alte Werte ausblenden",
          "Versteckt Angebote, deren Quelle zuletzt nicht erreichbar war."),

      fuss: '<button class="zweit" type="button" id="btnFilterReset">Zurücksetzen</button>' +
        '<button class="primaer" type="button" id="btnFilterFertig">' +
        zustand.sichtbar.length + " Angebote zeigen</button>",

      danach: function () {
        var binde = function (id, schluessel, istSchalter) {
          var el = $(id);
          if (!el) return;
          var reagiere = function (e) {
            zustand.filter[schluessel] = istSchalter ? e.target.checked : e.target.value;
            zustand.limit = SEITE;
            rendern();
            var fertig = $("btnFilterFertig");
            if (fertig) fertig.textContent = zustand.sichtbar.length + " Angebote zeigen";
          };
          el.addEventListener("change", reagiere);
          // Textfelder feuern "change" erst beim Verlassen - für die
          // Live-Zahl im Knopf braucht es "input". (Die Zinsfelder stehen
          // auf type="text", weil type="number" ein Komma verschluckt.)
          if (el.tagName === "INPUT" && el.type !== "checkbox") {
            el.addEventListener("input", reagiere);
          }
        };
        binde("fLand", "land"); binde("fTyp", "typ"); binde("fQuelltyp", "quelltyp");
        binde("fRating", "rating"); binde("fMinZins", "minZins");
        binde("fAktion", "aktion"); binde("fNeukunden", "neukunden");
        binde("fPasst", "passtZuBetrag", true);
        binde("fVoll", "vollGesichert", true);
        binde("fNurEur", "nurEur", true);
        binde("fNurWatch", "nurWatch", true);
        binde("fOhneStale", "ohneStale", true);
      },
    });
  }

  function filterZuruecksetzen() {
    zustand.filter = {
      land: "", typ: "", quelltyp: "", rating: "", minZins: "",
      aktion: "", neukunden: "",
      nurEur: false, nurWatch: false, ohneStale: false, passtZuBetrag: false,
      vollGesichert: false,
    };
    zustand.limit = SEITE;
    zustand.suche = "";
    var feld = $("suche");
    if (feld) { feld.value = ""; $("btnSucheLeeren").hidden = true; }
    rendern();
  }

  /* ================================================= Inhalt: Einstellungen */

  function einstellungenOeffnen() {
    var e = zustand.einstellungen;
    sheetZeigen({
      titel: "Einstellungen",
      koerper:
        "<h3>Steuern</h3>" +
        '<label class="schalter"><input type="checkbox" id="sErstattung"' + (e.erstattung ? " checked" : "") + ">" +
          "<span><strong>Ich hole mir ausländische Steuern zurück</strong>" +
          "<em>Bei Ländern, wo das einfach geht, wird dann mit 0 % Quellensteuer " +
          "gerechnet. Schalte es aus, wenn du den Papierkram nicht machen willst.</em></span></label>" +

        '<label class="schalter"><input type="checkbox" id="sAbgeltung"' + (e.abgeltung ? " checked" : "") + ">" +
          "<span><strong>Deutsche Abgeltungssteuer mitrechnen</strong>" +
          "<em>25 % plus Solidaritätszuschlag. Trifft alle Anbieter gleich und ändert " +
          "die Reihenfolge nicht – deshalb standardmäßig aus.</em></span></label>" +

        genutzteListe() +

        "<h3>Erinnerung</h3>" +
        '<label class="feld"><span>Melde mir Angebote auf meiner Merkliste über … Prozent</span>' +
        '<input type="text" id="sSchwelle" inputmode="decimal" autocomplete="off" value="' +
        esc(String(e.schwelle).replace(".", ",")) + '"></label>' +
        '<label class="schalter"><input type="checkbox" id="sBenachrichtigung"' + (e.benachrichtigung ? " checked" : "") + ">" +
          "<span><strong>Benachrichtigung einschalten</strong>" +
          "<em>Wird beim Aktualisieren geprüft. Es werden keine Daten verschickt.</em></span></label>" +

        "<h3>Daten</h3>" +
        '<label class="feld"><span>Adresse der Zinsdaten</span>' +
        '<input type="url" id="sQuelle" placeholder="' + esc(CFG.datenUrl || "") + '" value="' +
        esc(e.quelle || "") + '"></label>' +
        '<p class="satz zart">Leer lassen heißt: die mitgelieferte Adresse wird benutzt. ' +
        "Aktuell aktiv: " + esc(datenUrl() || "keine") + "</p>" +

        "<h3>Wie Zinsradar sortiert</h3>" +
        '<div class="info-karte">Die <strong>Empfehlung</strong> ist der Zins nach Steuern, ' +
        "abzüglich eines kleinen Abzugs für Länder mit schwächerer Bonität. " +
        "Damit steht nicht automatisch das lauteste Angebot oben, sondern das, " +
        "von dem am ehesten etwas ankommt.</div>" +

        '<p class="satz zart">Version ' + esc(CFG.version || "1.0.0") +
        " · Die Daten liegen auch offline auf dem Gerät.</p>",
      fuss: '<button class="zweit" type="button" data-schliessen>Abbrechen</button>' +
        '<button class="primaer" type="button" id="btnEinstSpeichern">Speichern</button>',
    });
  }

  /* Abgehakte Neukunden-Angebote: hier stehen sie, hier kommen sie zurück. */
  function genutzteListe() {
    return '<div id="genutztBereich">' + genutztInhalt() + "</div>";
  }

  function genutztInhalt() {
    var liste = erledigteAngebote();
    if (!liste.length) {
      return "<h3>Schon genutzte Angebote</h3>" +
        '<p class="satz zart">Noch nichts abgehakt. Neukunden-Angebote kannst du ' +
        "in der Liste mit dem Haken ausblenden, sobald du sie einmal genutzt hast – " +
        "sie tauchen dann hier auf.</p>";
    }
    return "<h3>Schon genutzt (" + liste.length + ")</h3>" +
      '<p class="satz zart">Diese Angebote sind aus der Hauptliste ausgeblendet.</p>' +
      '<ul class="genutzt">' + liste.map(function (a) {
        return '<li class="genutzt-zeile"><span class="genutzt-name">' + esc(a.bank) +
          (a._fehlt ? ' <em class="zart">(nicht mehr im Vergleich)</em>'
                    : ' <em class="zart">' + pct(a.zinssatz_pct) + " · " +
                      esc(landName(a.einlagensicherung_land)) + "</em>") +
          '</span><button class="knopf-klein" type="button" data-erledigt-key="' +
          esc(a.dedupe_key) + '">zurückholen</button></li>';
      }).join("") + "</ul>";
  }

  function einstellungenSpeichern() {
    var vorherQuelle = datenUrl();
    var e = zustand.einstellungen;
    if ($("sErstattung")) e.erstattung = $("sErstattung").checked;
    if ($("sAbgeltung")) e.abgeltung = $("sAbgeltung").checked;
    if ($("sSchwelle")) {
      var schwelle = zahlAusEingabe($("sSchwelle").value);
      e.schwelle = isNaN(schwelle) ? 0 : schwelle;
    }
    if ($("sBenachrichtigung")) e.benachrichtigung = $("sBenachrichtigung").checked;
    if ($("sQuelle")) e.quelle = ($("sQuelle").value || "").trim();

    schreib(SPEICHER.einst, e);
    sheetSchliessen();
    rendern();

    if (e.benachrichtigung) {
      lokaleNotiz("Erinnerung ist an",
        "Du hörst von uns, wenn ein Angebot auf deiner Merkliste über " +
        pct(e.schwelle) + " steigt.");
    }
    if (datenUrl() !== vorherQuelle) laden(true);
    else toast("Gespeichert");
  }

  /* ==================================================== Inhalt: Erklärungen */

  function referenzOeffnen() {
    var ref = (zustand.daten && zustand.daten.referenz) || {};
    var estr = ref.estr || {};
    var mir = ref.ezb_mir || {};
    var pfeil = estr.trend === "steigend" ? "pfeil-hoch"
      : estr.trend === "fallend" ? "pfeil-runter" : "strich-quer";

    var zeilen = Object.keys(mir).sort(function (x, y) {
      return landName(x).localeCompare(landName(y), "de");
    }).map(function (l) {
      return paar(esc(landName(l)), pct(mir[l].wert_pct));
    }).join("");

    sheetZeigen({
      titel: "Woran du dich orientieren kannst",
      koerper:
        '<p class="satz">Die Europäische Zentralbank veröffentlicht jeden Monat, ' +
        "was Banken in einem Land im Schnitt für täglich verfügbares Geld zahlen. " +
        "Das ist der ehrlichste Maßstab dafür, ob ein Angebot wirklich gut ist.</p>" +

        '<div class="info-karte"><div class="kopfzeile">' + ikon(pfeil) +
        "Zins zwischen den Banken</div>" +
        "Aktuell " + pct(estr.aktuell_pct, nfFein) + ", Tendenz " +
        esc(estr.trend || "unbekannt") +
        (istZahl(estr.veraenderung_30t_pp)
          ? " (" + (estr.veraenderung_30t_pp > 0 ? "+" : "") +
            nfFein.format(estr.veraenderung_30t_pp) + " Prozentpunkte in 30 Tagen)"
          : "") +
        ". Zu diesem Satz leihen sich Banken über Nacht gegenseitig Geld. " +
        "Steigt er, steigen die Sparzinsen meist mit – fällt er, geht es bald abwärts.</div>" +

        "<h3>Durchschnitt je Land</h3>" +
        '<dl class="paare">' + (zeilen || paar("keine Daten", "–")) + "</dl>" +

        '<p class="satz zart">Der Durchschnitt enthält auch Girokonten ohne Zinsen. ' +
        "Gute Tagesgeldangebote liegen deshalb fast immer deutlich darüber. " +
        "Stand der Zahlen: " + esc(datumKurz(ref.stand)) + ".</p>",
    });
  }

  /* ============================================= Merkliste und Erinnerung */

  function erledigtUmschalten(key) {
    var i = zustand.erledigt.indexOf(key);
    if (i === -1) {
      zustand.erledigt.push(key);
      toast("Abgehakt – liegt jetzt in den Einstellungen");
    } else {
      zustand.erledigt.splice(i, 1);
      toast("Wieder in der Liste");
    }
    schreib(SPEICHER.erledigt, zustand.erledigt);
    rendern();
  }

  /* Angebote zu den abgehakten Schlüsseln, auch wenn Filter aktiv sind. */
  function erledigteAngebote() {
    var alle = (zustand.daten && zustand.daten.angebote) || [];
    return zustand.erledigt.map(function (key) {
      for (var i = 0; i < alle.length; i++) {
        if (alle[i].dedupe_key === key) return alle[i];
      }
      return { dedupe_key: key, bank: key.split("|")[0], _fehlt: true };
    });
  }

  function watchUmschalten(key) {
    var i = zustand.watchlist.indexOf(key);
    if (i === -1) { zustand.watchlist.push(key); toast("Gemerkt"); }
    else { zustand.watchlist.splice(i, 1); toast("Von der Merkliste genommen"); }
    schreib(SPEICHER.watch, zustand.watchlist);
    rendern();
  }

  function lokaleNotiz(titel, text) {
    var cap = window.Capacitor;
    if (cap && cap.Plugins && cap.Plugins.LocalNotifications) {
      var LN = cap.Plugins.LocalNotifications;
      return LN.requestPermissions().then(function () {
        return LN.schedule({
          notifications: [{
            id: Math.floor(Date.now() % 100000),
            title: titel,
            body: text,
            schedule: { at: new Date(Date.now() + 1000) },
          }],
        });
      }).catch(function () { toast(titel + ": " + text, 5000); });
    }
    if ("Notification" in window) {
      if (Notification.permission === "granted") {
        try { new Notification(titel, { body: text, icon: "icons/icon-192.png" }); return Promise.resolve(); }
        catch (e) { /* WebView ohne Service-Worker-Registrierung */ }
      } else if (Notification.permission !== "denied") {
        return Notification.requestPermission().then(function (p) {
          if (p === "granted") { try { new Notification(titel, { body: text }); } catch (e) { /* egal */ } }
          else { toast(titel + ": " + text, 5000); }
        });
      }
    }
    toast(titel + ": " + text, 5000);
    return Promise.resolve();
  }

  function pruefeSchwelle(daten) {
    if (!zustand.einstellungen.benachrichtigung) return;
    var schwelle = zahlAusEingabe(zustand.einstellungen.schwelle);
    if (isNaN(schwelle) || !zustand.watchlist.length) return;

    var gemeldet = lies(SPEICHER.gemeldet, {}, "objekt");
    var heute = new Date().toISOString().slice(0, 10);
    var treffer = [];

    (daten.angebote || []).forEach(function (a) {
      if (zustand.watchlist.indexOf(a.dedupe_key) === -1) return;
      if (a.stale || !istZahl(a.zinssatz_pct) || a.zinssatz_pct <= schwelle) return;
      if (gemeldet[a.dedupe_key] === heute + "|" + a.zinssatz_pct) return;
      gemeldet[a.dedupe_key] = heute + "|" + a.zinssatz_pct;
      treffer.push(a);
    });

    if (!treffer.length) return;
    schreib(SPEICHER.gemeldet, gemeldet);

    var titel = treffer.length === 1
      ? treffer[0].bank + " zahlt " + pct(treffer[0].zinssatz_pct)
      : treffer.length + " Angebote über " + pct(schwelle);
    var text = treffer.slice(0, 4).map(function (a) {
      return a.bank + " " + pct(a.zinssatz_pct);
    }).join(", ");
    lokaleNotiz(titel, text);
  }

  /* ================================================================= Theme */

  function themeSetzen(wert) {
    if (wert === "auto") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", wert);
    schreib(SPEICHER.theme, wert);

    var dunkel = wert === "dark" ||
      (wert === "auto" && window.matchMedia &&
       window.matchMedia("(prefers-color-scheme: dark)").matches);

    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", dunkel ? "#16181c" : "#faf7f2");

    var knopf = $("btnTheme");
    if (knopf) {
      knopf.innerHTML = '<svg class="ikon-svg"><use href="#i-' + (dunkel ? "mond" : "sonne") + '"></use></svg>';
    }
  }

  function themeUmschalten() {
    var jetzt = lies(SPEICHER.theme, "auto", "text");
    var naechstes = jetzt === "auto" ? "light" : (jetzt === "light" ? "dark" : "auto");
    themeSetzen(naechstes);
    toast(naechstes === "auto" ? "Folgt dem System"
      : naechstes === "light" ? "Immer hell" : "Immer dunkel");
  }

  /* =================================================== Ziehen zum Neuladen */

  function ptrEinrichten() {
    var startY = 0, ziehend = false, ausgeloest = false;
    var ptr = $("ptr");
    var SCHWELLE = 70;

    document.addEventListener("touchstart", function (e) {
      if (window.scrollY > 0 || zustand.laedt || sheetOffen()) return;
      if (!e.touches || e.touches.length !== 1) return;
      startY = e.touches[0].clientY;
      ziehend = true;
      ausgeloest = false;
    }, { passive: true });

    function abbrechen() {
      ziehend = false;
      ausgeloest = false;
      ptr.classList.remove("aktiv", "laedt");
      $("ptrText").textContent = "Zum Aktualisieren ziehen";
    }

    // Ohne touchcancel bleibt der Balken nach einem abgebrochenen Zug auf
    // "Loslassen" stehen - und schlimmer: `ziehend` bleibt true, sodass
    // ein Wischen im offenen Sheet danach einen ganzen Neuladen auslöst.
    document.addEventListener("touchcancel", abbrechen, { passive: true });

    document.addEventListener("touchmove", function (e) {
      if (!ziehend) return;
      if (sheetOffen()) { abbrechen(); return; }
      var delta = e.touches[0].clientY - startY;
      if (delta > 12 && window.scrollY <= 0) {
        ptr.classList.add("aktiv");
        ausgeloest = delta > SCHWELLE;
        $("ptrText").textContent = ausgeloest ? "Loslassen" : "Zum Aktualisieren ziehen";
      } else if (delta <= 0) {
        ptr.classList.remove("aktiv");
        ziehend = false;
      }
    }, { passive: true });

    document.addEventListener("touchend", function () {
      if (!ziehend) return;
      ziehend = false;
      if (sheetOffen()) { abbrechen(); return; }
      if (!ausgeloest) { ptr.classList.remove("aktiv"); return; }
      ptr.classList.add("laedt");
      $("ptrText").textContent = "Wird geholt …";
      laden(true).then(function () {
        ptr.classList.remove("aktiv", "laedt");
        $("ptrText").textContent = "Zum Aktualisieren ziehen";
      });
    });
  }

  /* ============================================================ Ereignisse */

  function ereignisse() {
    $("btnAktualisieren").addEventListener("click", function () { laden(true); });
    $("btnTheme").addEventListener("click", themeUmschalten);
    $("btnEinstellungen").addEventListener("click", einstellungenOeffnen);
    $("betragKarte").addEventListener("click", betragOeffnen);
    $("btnFilter").addEventListener("click", filterOeffnen);
    $("referenzZeile").addEventListener("click", referenzOeffnen);
    $("btnLeerReset").addEventListener("click", filterZuruecksetzen);

    $("btnMehr").addEventListener("click", function () {
      zustand.limit += SEITE;
      rendern();
      // Fokus auf die erste neue Karte, damit die Tastaturbedienung
      // nicht am Seitenanfang landet.
      var neu = $("liste").children[zustand.limit - SEITE];
      if (neu) neu.focus({ preventScroll: true });
    });

    $("heldKarte").addEventListener("click", function () {
      var key = $("heldKarte").dataset.key;
      var i = zustand.sichtbar.findIndex(function (a) { return a.dedupe_key === key; });
      if (i >= 0) detailOeffnen(i);
    });

    var sucheTimer = null;
    $("suche").addEventListener("input", function (e) {
      zustand.suche = e.target.value;
      $("btnSucheLeeren").hidden = !e.target.value;
      clearTimeout(sucheTimer);
      sucheTimer = setTimeout(function () {
        zustand.limit = SEITE;
        rendern();
      }, 140);
    });

    $("btnSucheLeeren").addEventListener("click", function () {
      $("suche").value = "";
      zustand.suche = "";
      $("btnSucheLeeren").hidden = true;
      zustand.limit = SEITE;
      rendern();
    });

    document.querySelectorAll(".sort").forEach(function (knopf) {
      knopf.addEventListener("click", function () {
        document.querySelectorAll(".sort").forEach(function (k) {
          k.classList.remove("aktiv");
          k.setAttribute("aria-selected", "false");
        });
        knopf.classList.add("aktiv");
        knopf.setAttribute("aria-selected", "true");
        zustand.sortierung = knopf.dataset.sort;
        rendern();
      });
    });

    /* Liste: Stern oder Karte */
    $("liste").addEventListener("click", function (e) {
      var haken = e.target.closest("[data-erledigt]");
      if (haken) {
        e.stopPropagation();
        var h = zustand.sichtbar[parseInt(haken.dataset.erledigt, 10)];
        if (h) erledigtUmschalten(h.dedupe_key);
        return;
      }
      var stern = e.target.closest("[data-watch]");
      if (stern) {
        e.stopPropagation();
        var a = zustand.sichtbar[parseInt(stern.dataset.watch, 10)];
        if (a) watchUmschalten(a.dedupe_key);
        return;
      }
      var karte = e.target.closest(".karte");
      if (karte) detailOeffnen(parseInt(karte.dataset.index, 10));
    });

    /* Karten sind per Tastatur erreichbar – dann muss Enter auch öffnen. */
    $("liste").addEventListener("keydown", function (e) {
      if (e.key !== "Enter" && e.key !== " ") return;
      var karte = e.target.closest(".karte");
      // Die Knöpfe in der Karte lösen selbst aus – hier nicht dazwischenfunken.
      if (!karte || e.target.closest("[data-watch], [data-erledigt]")) return;
      e.preventDefault();
      detailOeffnen(parseInt(karte.dataset.index, 10));
    });

    $("aktiveFilter").addEventListener("click", function (e) {
      var chip = e.target.closest("[data-filter-weg]");
      if (!chip) return;
      var k = chip.dataset.filterWeg;
      zustand.filter[k] = typeof zustand.filter[k] === "boolean" ? false : "";
      zustand.limit = SEITE;
      rendern();
    });

    /* Alles im Sheet läuft über einen Delegierten – die Inhalte werden
       ja bei jedem Öffnen neu gebaut. */
    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-schliessen]")) { sheetSchliessen(); return; }

      var folie = e.target.closest("[data-folie]");
      if (folie) {
        var ziel = parseInt(folie.dataset.folie, 10);
        folieZeigen(ziel, aktuelleFolien ? ziel - aktuelleFolien.index : 0);
        return;
      }

      var erledigtKnopf = e.target.closest("[data-erledigt-key]");
      if (erledigtKnopf) {
        var eKey = erledigtKnopf.dataset.erledigtKey;
        var warDrin = zustand.erledigt.indexOf(eKey) !== -1;
        erledigtUmschalten(eKey);
        if (!warDrin) {
          sheetSchliessen();          // aus dem Detail-Sheet heraus
        } else {
          // In den Einstellungen NUR die Liste neu bauen. Ein kompletter
          // Neuaufbau des Sheets würde noch nicht gespeicherte Eingaben
          // (Daten-Adresse, Schalter) still zurücksetzen.
          var bereich = $("genutztBereich");
          if (bereich) bereich.innerHTML = genutztInhalt();
          else einstellungenOeffnen();
        }
        return;
      }

      var watchKnopf = e.target.closest("[data-watch-key]");
      if (watchKnopf) {
        var key = watchKnopf.dataset.watchKey;
        watchUmschalten(key);
        watchKnopf.textContent = zustand.watchlist.indexOf(key) !== -1
          ? "Von der Merkliste nehmen" : "Auf die Merkliste";
        return;
      }

      var betragChip = e.target.closest("[data-betrag]");
      if (betragChip) {
        var eingabe = $("betragEingabe");
        if (eingabe) eingabe.value = betragChip.dataset.betrag;
        betragSetzen(betragChip.dataset.betrag, true);
        return;
      }

      if (e.target.closest("#btnBetragSpeichern")) {
        betragSetzen($("betragEingabe") ? $("betragEingabe").value : zustand.betrag, true);
        return;
      }
      if (e.target.closest("#btnEinstSpeichern")) { einstellungenSpeichern(); return; }
      if (e.target.closest("#btnFilterReset")) { filterZuruecksetzen(); sheetSchliessen(); return; }
      if (e.target.closest("#btnFilterFertig")) { sheetSchliessen(); return; }
    });

    document.addEventListener("keydown", function (e) {
      if (!sheetOffen()) return;
      if (e.key === "Escape") { sheetSchliessen(); return; }
      if (e.key === "ArrowRight") folieWechseln(1);
      if (e.key === "ArrowLeft") folieWechseln(-1);
    });

    /* Wischen zwischen den Folien */
    var wischX = 0, wischY = 0;
    $("sheetBody").addEventListener("touchstart", function (e) {
      if (!e.touches || e.touches.length !== 1) return;
      wischX = e.touches[0].clientX;
      wischY = e.touches[0].clientY;
    }, { passive: true });

    $("sheetBody").addEventListener("touchend", function (e) {
      if (!aktuelleFolien || !e.changedTouches || !e.changedTouches.length) return;
      var dx = e.changedTouches[0].clientX - wischX;
      var dy = e.changedTouches[0].clientY - wischY;
      if (Math.abs(dx) < 60 || Math.abs(dy) > 45) return;
      folieWechseln(dx < 0 ? 1 : -1);
    }, { passive: true });

    // Android-Zurück-Taste schließt das Sheet statt die App.
    window.addEventListener("popstate", function () {
      if (eigenesZurueck) {
        eigenesZurueck = false;
        // Zwischenzeitlich ein neues Sheet geöffnet? Dann hat es seinen
        // History-Eintrag gerade mitverloren und braucht einen neuen.
        if (sheetOffen()) { sheetHistorie = false; historieMerken(); }
        return;
      }
      if (sheetOffen()) sheetSchliessen(true);
    });

    window.addEventListener("online", function () { laden(false); });

    /* Schatten unter der Kopfzeile erst beim Scrollen */
    var ticking = false;
    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        $("kopfMarker").classList.toggle("gescrollt", window.scrollY > 4);
        ticking = false;
      });
    }, { passive: true });

    /* Systemwechsel hell/dunkel mitnehmen, solange "auto" eingestellt ist */
    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var reagiere = function () {
        if (lies(SPEICHER.theme, "auto", "text") === "auto") themeSetzen("auto");
      };
      if (mq.addEventListener) mq.addEventListener("change", reagiere);
      else if (mq.addListener) mq.addListener(reagiere);
    }
  }

  /* ================================================================= Start */

  function start() {
    zustand.einstellungen = Object.assign(zustand.einstellungen,
      lies(SPEICHER.einst, {}, "objekt"));
    zustand.watchlist = lies(SPEICHER.watch, [], "liste")
      .filter(function (k) { return typeof k === "string"; });
    zustand.erledigt = lies(SPEICHER.erledigt, [], "liste")
      .filter(function (k) { return typeof k === "string"; });
    zustand.betrag = lies(SPEICHER.betrag, BETRAG_STANDARD, "zahl");

    var theme = lies(SPEICHER.theme, "auto", "text");
    themeSetzen(["auto", "light", "dark"].indexOf(theme) === -1 ? "auto" : theme);
    betragAnzeigen();
    ereignisse();
    ptrEinrichten();

    var zwischen = lies(SPEICHER.daten, null, "objekt");
    if (zwischen && pruefeStruktur(zwischen.daten)) {
      uebernehmen(zwischen.daten, "start", null, zwischen.geholt);
    }

    laden(false);

    if ("serviceWorker" in navigator && location.protocol !== "file:") {
      navigator.serviceWorker.register("sw.js").catch(function () { /* egal */ });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
