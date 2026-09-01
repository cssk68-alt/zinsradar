/* Zinsradar - Vanilla JS, kein Framework, kein Build-Step.
 *
 * Datenfluss:
 *   GitHub Actions -> data/zinsen.json -> raw.githubusercontent -> hier.
 *   Kein Server, keine API. Geladene Daten landen im localStorage und
 *   im Service-Worker-Cache, damit die App offline weiterläuft.
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
  };

  var zustand = {
    daten: null,
    sortierung: "score",
    suche: "",
    filter: { land: "", typ: "", betrag: "", quelltyp: "", nurEur: false, nurWatch: false, ohneStale: false },
    einstellungen: {
      erstattung: true,
      abgeltung: false,
      schwelle: 3.5,
      benachrichtigung: false,
      quelle: "",
    },
    watchlist: [],
    laedt: false,
  };

  // ------------------------------------------------------------- Hilfen

  var $ = function (id) { return document.getElementById(id); };

  var nfProzent = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var nfProzent3 = new Intl.NumberFormat("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 3 });
  var nfGeld = new Intl.NumberFormat("de-DE", { maximumFractionDigits: 0 });

  function pct(wert, formatierer) {
    if (wert === null || wert === undefined || isNaN(wert)) return "–";
    return (formatierer || nfProzent).format(wert) + " %";
  }

  function geld(wert) {
    if (wert === null || wert === undefined || isNaN(wert)) return "–";
    return nfGeld.format(wert) + " €";
  }

  function datumKurz(iso) {
    if (!iso) return "–";
    var d = new Date(iso);
    if (isNaN(d.getTime())) return String(iso).slice(0, 10);
    return d.toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit", year: "numeric" });
  }

  function escape(text) {
    return String(text === null || text === undefined ? "" : text)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function lies(schluessel, standard) {
    try {
      var roh = localStorage.getItem(schluessel);
      return roh ? JSON.parse(roh) : standard;
    } catch (e) { return standard; }
  }

  function schreib(schluessel, wert) {
    try { localStorage.setItem(schluessel, JSON.stringify(wert)); } catch (e) { /* voll o. privat */ }
  }

  var toastTimer = null;
  function toast(text, dauer) {
    var el = $("toast");
    el.textContent = text;
    el.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { el.hidden = true; }, dauer || 2600);
  }

  // ------------------------------------------------------- Daten laden

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
    var kette;

    if (!url) {
      kette = Promise.reject(new Error("Keine Daten-URL gesetzt"));
    } else {
      kette = holeMitTimeout(url).then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      });
    }

    return kette
      .then(function (daten) {
        if (!pruefeStruktur(daten)) throw new Error("Unerwartetes Datenformat");
        schreib(SPEICHER.daten, { geholt: new Date().toISOString(), daten: daten });
        uebernehmen(daten, "netz");
        if (erzwingen) toast("Aktualisiert: " + daten.angebote.length + " Angebote");
        pruefeSchwelle(daten);
      })
      .catch(function (fehler) {
        var zwischen = lies(SPEICHER.daten, null);
        if (zwischen && pruefeStruktur(zwischen.daten)) {
          uebernehmen(zwischen.daten, "cache", fehler.message, zwischen.geholt);
          if (erzwingen) toast("Offline – zeige gespeicherten Stand");
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
    if (quelle === "netz") {
      hinweis.hidden = true;
    } else {
      hinweis.hidden = false;
      hinweis.className = "hinweis";
      if (quelle === "cache") {
        hinweis.textContent = "Kein Netz – gespeicherter Stand vom " + datumKurz(geholtAm) +
          (fehlertext ? " (" + fehlertext + ")" : "");
      } else {
        hinweis.textContent = "Mitgelieferte Daten werden angezeigt. Datenquelle in den " +
          "Einstellungen prüfen" + (fehlertext ? " (" + fehlertext + ")" : "") + ".";
      }
    }
    landfilterFuellen();
    referenzleiste();
    rendern();
  }

  function zeigeFehler(text) {
    $("ladeanzeige").hidden = true;
    var hinweis = $("hinweis");
    hinweis.hidden = false;
    hinweis.className = "hinweis fehler";
    hinweis.innerHTML = "Daten konnten nicht geladen werden (" + escape(text) + ").<br>" +
      "Bitte die JSON-URL in den Einstellungen prüfen.";
  }

  // -------------------------------------------------- Referenzleiste (F4)

  function referenzWaehlen() {
    var ref = (zustand.daten && zustand.daten.referenz) || {};
    var mir = ref.ezb_mir || {};
    var land = zustand.filter.land;
    if (land && mir[land]) return { land: land, eintrag: mir[land] };
    if (mir.U2) return { land: "Euroraum", eintrag: mir.U2 };
    var ersteKeys = Object.keys(mir);
    if (ersteKeys.length) return { land: ersteKeys[0], eintrag: mir[ersteKeys[0]] };
    return null;
  }

  function referenzleiste() {
    var ref = (zustand.daten && zustand.daten.referenz) || {};
    var leiste = $("referenzleiste");
    if (!zustand.daten) { leiste.hidden = true; return; }
    leiste.hidden = false;

    var wahl = referenzWaehlen();
    if (wahl) {
      $("mirLabel").textContent = "EZB-Schnitt " + (wahl.land === "Euroraum" ? "Euroraum" : wahl.land);
      $("mirWert").textContent = pct(wahl.eintrag.wert_pct);
      $("mirSub").textContent = wahl.eintrag.periode || "";
    } else {
      $("mirLabel").textContent = "EZB-Schnitt";
      $("mirWert").textContent = "–";
      $("mirSub").textContent = "keine Daten";
    }

    var estr = ref.estr || {};
    $("estrWert").textContent = pct(estr.aktuell_pct, nfProzent3);
    var pfeil = estr.trend === "steigend" ? "▲" : (estr.trend === "fallend" ? "▼" : "▬");
    var delta = estr.veraenderung_30t_pp;
    $("estrSub").textContent = pfeil + " " + (estr.trend || "unbekannt") +
      (delta !== null && delta !== undefined ? " (" + (delta > 0 ? "+" : "") + nfProzent3.format(delta) + " pp)" : "");
    $("estrSub").className = "referenz-sub " + (estr.trend || "");

    $("standWert").textContent = datumKurz(zustand.daten.stand_datum || zustand.daten.stand);
    var stat = zustand.daten.statistik || {};
    $("standSub").textContent = (stat.angebote || zustand.daten.angebote.length) + " Angebote";
  }

  // ------------------------------------------------------ Filter/Sortierung

  function landfilterFuellen() {
    var sel = $("fLand");
    var vorher = sel.value;
    var laender = {};
    (zustand.daten.angebote || []).forEach(function (a) {
      var l = a.einlagensicherung_land || a.land;
      if (l) laender[l] = (laender[l] || 0) + 1;
    });
    var keys = Object.keys(laender).sort();
    sel.innerHTML = '<option value="">alle Länder</option>' + keys.map(function (l) {
      return '<option value="' + escape(l) + '">' + escape(l) + " (" + laender[l] + ")</option>";
    }).join("");
    sel.value = vorher;
  }

  function nettoFeld() {
    return zustand.einstellungen.erstattung
      ? "netto_12m_mit_erstattung_pct" : "netto_12m_ohne_erstattung_pct";
  }

  function scoreFeld() {
    return zustand.einstellungen.erstattung ? "score_mit_erstattung" : "score_ohne_erstattung";
  }

  function anzeigeNetto(a) {
    if (zustand.einstellungen.abgeltung) {
      return a[zustand.einstellungen.erstattung
        ? "netto_nach_abgeltungssteuer_mit_erstattung_pct"
        : "netto_nach_abgeltungssteuer_ohne_erstattung_pct"];
    }
    return a[nettoFeld()];
  }

  function gefiltert() {
    var f = zustand.filter;
    var suche = zustand.suche.trim().toLowerCase();
    var betrag = parseFloat(f.betrag);

    return (zustand.daten.angebote || []).filter(function (a) {
      if (suche) {
        var heu = ((a.bank || "") + " " + (a.produkt || "") + " " + (a.land || "")).toLowerCase();
        if (heu.indexOf(suche) === -1) return false;
      }
      if (f.land && (a.einlagensicherung_land || a.land) !== f.land) return false;
      if (f.typ && a.zinstyp !== f.typ) return false;
      if (f.nurEur && a.waehrung && a.waehrung !== "EUR") return false;
      if (f.ohneStale && a.stale) return false;
      if (f.nurWatch && zustand.watchlist.indexOf(a.dedupe_key) === -1) return false;
      if (f.quelltyp) {
        var typen = (a.quellen || []).map(function (q) { return q.typ; });
        if (typen.indexOf(f.quelltyp) === -1) return false;
      }
      if (!isNaN(betrag) && betrag > 0) {
        var min = a.mindestanlage_eur !== null && a.mindestanlage_eur !== undefined
          ? a.mindestanlage_eur : a.mindestanlage;
        var max = a.hoechstanlage_eur !== null && a.hoechstanlage_eur !== undefined
          ? a.hoechstanlage_eur : a.hoechstanlage;
        if (min !== null && min !== undefined && betrag < min) return false;
        if (max !== null && max !== undefined && betrag > max) return false;
      }
      return true;
    });
  }

  function sortiert(liste) {
    var s = zustand.sortierung;
    var kopie = liste.slice();
    var zahl = function (wert) {
      return (wert === null || wert === undefined || isNaN(wert)) ? -999 : wert;
    };
    kopie.sort(function (a, b) {
      switch (s) {
        case "brutto": return zahl(b.brutto_12m_pct) - zahl(a.brutto_12m_pct);
        case "netto": return zahl(anzeigeNetto(b)) - zahl(anzeigeNetto(a));
        case "bank": return (a.bank || "").localeCompare(b.bank || "", "de");
        case "land":
          var la = (a.einlagensicherung_land || ""), lb = (b.einlagensicherung_land || "");
          if (la !== lb) return la.localeCompare(lb, "de");
          return zahl(b[scoreFeld()]) - zahl(a[scoreFeld()]);
        default: return zahl(b[scoreFeld()]) - zahl(a[scoreFeld()]);
      }
    });
    return kopie;
  }

  // ------------------------------------------------------------- Rendern

  var RATING_KLASSE = { AAA: "gut", AA: "gut", A: "mittel", BBB: "mittel" };

  function ratingKlasse(gruppe) {
    return RATING_KLASSE[gruppe] || (gruppe ? "schlecht" : "neutral");
  }

  function karteHtml(a, index) {
    var netto = anzeigeNetto(a);
    var beobachtet = zustand.watchlist.indexOf(a.dedupe_key) !== -1;
    var klassen = ["karte"];
    if (a.stale) klassen.push("stale");
    if (beobachtet) klassen.push("watch");

    var badges = [];
    var sicher = a.einlagensicherung_betrag_eur;
    badges.push('<span class="badge ' + (sicher >= 100000 ? "gut" : (sicher ? "mittel" : "neutral")) + '">' +
      "&#128274; " + (sicher ? geld(sicher) : "Sicherung unbekannt") + "</span>");

    if (a.staatsrating_sp) {
      badges.push('<span class="badge ' + ratingKlasse(a.rating_gruppe) + '">' +
        escape(a.einlagensicherung_land || "") + " " + escape(a.staatsrating_sp) + "</span>");
    }
    if (a.zinstyp === "aktion" && a.aktionsdauer_monate) {
      badges.push('<span class="badge info">Aktion ' + a.aktionsdauer_monate + " Mon.</span>");
    }
    if (a.waehrungsrisiko) {
      badges.push('<span class="badge mittel">' + escape(a.waehrung) + "-Währungsrisiko</span>");
    }
    if (a.extraction_tier === 3) {
      badges.push('<span class="badge neutral">automatisch erkannt</span>');
    }
    if (a.flag === "pruefen") {
      badges.push('<span class="badge schlecht">prüfen</span>');
    }
    if (a.stale) {
      badges.push('<span class="badge neutral">Stand ' + escape(a.stale_seit || a.stand || "") + "</span>");
    }
    if (a.override) {
      badges.push('<span class="badge info">manuell geprüft</span>');
    }

    if (a.land_quelle === "quellenland_angenommen") {
      badges.push('<span class="badge neutral" title="Sicherungsland aus der Quelle abgeleitet">' +
        "Land angenommen</span>");
    }

    var nettoText = zustand.einstellungen.abgeltung
      ? "netto " + pct(netto) + " über 12 Monate, nach Quellen- und Abgeltungssteuer"
      : "netto " + pct(netto) + " über 12 Monate, nach Quellensteuer";

    // Bei einer befristeten Aktion ist der grosse Zins nicht das, was über
    // 12 Monate hängen bleibt. Das muss auf der Karte stehen, sonst wirkt
    // die Netto-Zeile wie ein Rechenfehler.
    var aktionszeile = "";
    if (a.zinstyp === "aktion" && a.aktionsdauer_monate > 0) {
      aktionszeile = '<div class="netto-zeile"><span>' +
        pct(a.zinssatz_pct) + " für " + a.aktionsdauer_monate + " Monate, danach " +
        pct(a.folgezins_pct) + (a.folgezins_geschaetzt ? " (geschätzt)" : "") +
        " · brutto " + pct(a.brutto_12m_pct) + " über 12 Monate</span></div>";
    }

    return '<li class="' + klassen.join(" ") + '" data-index="' + index + '">' +
      '<div class="karte-kopf">' +
        '<span class="bank">' + escape(a.bank) + "</span>" +
        '<span class="zins">' + pct(a.zinssatz_pct) +
          (a.zinstyp === "aktion" ? "<small>Aktion</small>" : "") + "</span>" +
      "</div>" +
      aktionszeile +
      '<div class="netto-zeile">' +
        '<span class="netto-wert">' + escape(nettoText) + "</span>" +
        '<span class="tipp">Rechnung ansehen</span>' +
      "</div>" +
      '<div class="badges">' + badges.join("") + "</div>" +
      '<div class="karte-fuss">' +
        "<span>" + escape(a.produkt || "Tagesgeld") + " · Score " +
          (a[scoreFeld()] !== null && a[scoreFeld()] !== undefined ? nfProzent.format(a[scoreFeld()]) : "–") +
          " · " + (a.quellen_anzahl || 1) + " Quelle" + ((a.quellen_anzahl || 1) > 1 ? "n" : "") + "</span>" +
        '<button class="stern' + (beobachtet ? " an" : "") + '" data-watch="' + index +
          '" aria-label="Zur Watchlist" title="Watchlist">' + (beobachtet ? "&#9733;" : "&#9734;") + "</button>" +
      "</div>" +
    "</li>";
  }

  var sichtbar = [];

  function rendern() {
    if (!zustand.daten) return;
    sichtbar = sortiert(gefiltert());

    $("liste").innerHTML = sichtbar.map(karteHtml).join("");
    $("leer").hidden = sichtbar.length > 0;

    var aktiv = 0, f = zustand.filter;
    ["land", "typ", "betrag", "quelltyp"].forEach(function (k) { if (f[k]) aktiv++; });
    ["nurEur", "nurWatch", "ohneStale"].forEach(function (k) { if (f[k]) aktiv++; });
    $("filterAnzahl").textContent = aktiv;
    $("filterAnzahl").hidden = aktiv === 0;
    $("btnFilter").classList.toggle("aktiv", aktiv > 0);

    var stat = zustand.daten.statistik || {};
    var tiers = stat.tier_verteilung || {};
    var tierText = Object.keys(tiers).sort().map(function (t) {
      return "Stufe " + t + ": " + tiers[t];
    }).join(" · ");
    $("fussStatistik").textContent = sichtbar.length + " von " + (zustand.daten.angebote || []).length +
      " Angeboten sichtbar" + (tierText ? " · " + tierText : "") +
      (stat.stale ? " · " + stat.stale + " veraltet" : "");

    referenzleiste();
  }

  // ------------------------------------------------- Detail-Sheet (F2)

  function detailHtml(a) {
    var erst = zustand.einstellungen.erstattung;
    var qst = erst ? a.qst_effektiv_mit_erstattung_pct : a.qst_effektiv_ohne_erstattung_pct;
    var grund = erst ? a.qst_begruendung_mit_erstattung : a.qst_begruendung_ohne_erstattung;
    var netto = erst ? a.netto_12m_mit_erstattung_pct : a.netto_12m_ohne_erstattung_pct;
    var score = a[scoreFeld()];
    var dauer = a.aktionsdauer_monate || 0;
    var rest = Math.max(0, 12 - Math.min(dauer, 12));

    var h = [];
    h.push('<h2 id="sheetTitel">' + escape(a.bank) + "</h2>");
    h.push('<p class="klein">' + escape(a.produkt || "Tagesgeld") + " · " +
      escape(a.einlagensicherung_land || a.land || "?") + " · " + escape(a.waehrung || "EUR") + "</p>");

    h.push("<h3>Bruttozins über 12 Monate</h3>");
    h.push('<table class="rechnung">');
    if (dauer > 0) {
      h.push("<tr><td>Aktionszins " + pct(a.zinssatz_pct) + " × " + Math.min(dauer, 12) + " Monate</td><td>" +
        nfProzent3.format(a.zinssatz_pct * Math.min(dauer, 12) / 12) + " pp</td></tr>");
      h.push("<tr><td>Folgezins " + pct(a.folgezins_pct) +
        (a.folgezins_geschaetzt ? " <em>(geschätzt)</em>" : "") + " × " + rest + " Monate</td><td>" +
        nfProzent3.format((a.folgezins_pct || 0) * rest / 12) + " pp</td></tr>");
    } else {
      h.push("<tr><td>Zins " + pct(a.zinssatz_pct) + " × 12 Monate</td><td>" +
        nfProzent3.format(a.zinssatz_pct) + " pp</td></tr>");
    }
    h.push('<tr class="summe"><td>Brutto 12 Monate</td><td>' + pct(a.brutto_12m_pct, nfProzent3) + "</td></tr>");
    h.push("</table>");
    h.push('<div class="formel">brutto_12m = (aktionszins × min(aktionsdauer,12)\n' +
           "              + folgezins × max(0, 12 − aktionsdauer)) / 12</div>");

    h.push("<h3>Quellensteuer</h3>");
    h.push('<table class="rechnung">');
    h.push("<tr><td>Standardsatz " + escape(a.einlagensicherung_land || "") + "</td><td>" +
      pct(a.qst_standard_pct) + "</td></tr>");
    h.push("<tr><td>Mit DBA</td><td>" + pct(a.qst_mit_dba_pct) + "</td></tr>");
    h.push("<tr><td>Rückerstattung</td><td>" + escape(a.rueckerstattung_aufwand || "unbekannt") + "</td></tr>");
    h.push('<tr class="zwischen"><td colspan="2">' + escape(grund || "") + "</td></tr>");
    h.push('<tr class="summe"><td>Effektiv angesetzt</td><td>' + pct(qst) + "</td></tr>");
    h.push("</table>");
    if (a.rueckerstattung_formular) {
      h.push('<p class="klein">Formular: ' + escape(a.rueckerstattung_formular) +
        (a.rueckerstattung_quelle ? ' · <a href="' + escape(a.rueckerstattung_quelle) +
          '" target="_blank" rel="noopener">Behörde</a>' : "") + "</p>");
    }

    h.push("<h3>Netto und Score</h3>");
    h.push('<table class="rechnung">');
    h.push("<tr><td>Brutto 12 Monate</td><td>" + pct(a.brutto_12m_pct, nfProzent3) + "</td></tr>");
    h.push("<tr><td>abzüglich Quellensteuer " + pct(qst) + "</td><td>" + pct(netto, nfProzent3) + "</td></tr>");
    h.push("<tr><td>Risikoabschlag Rating " + escape(a.staatsrating_sp || "?") +
      " (" + escape(a.rating_gruppe || "?") + ")</td><td>− " +
      nfProzent3.format(a.risiko_abschlag_pp || 0) + " pp</td></tr>");
    h.push('<tr class="summe"><td>Score</td><td>' + pct(score, nfProzent3) + "</td></tr>");
    if (zustand.einstellungen.abgeltung) {
      h.push('<tr class="zwischen"><td>Nach dt. Abgeltungssteuer (nur Anzeige)</td><td>' +
        pct(anzeigeNetto(a), nfProzent3) + "</td></tr>");
    }
    h.push("</table>");
    h.push('<div class="formel">netto_12m = brutto_12m × (1 − qst_effektiv)\n' +
           "score     = netto_12m − risiko_abschlag[staatsrating_sp]</div>");
    h.push('<p class="klein">Die deutsche Abgeltungssteuer ist bewusst nicht im Score: ' +
           "sie trifft alle Anbieter gleich und würde die Reihenfolge nicht ändern.</p>");

    h.push("<h3>Konditionen</h3>");
    h.push('<table class="rechnung">');
    h.push("<tr><td>Zinstyp</td><td>" + escape(a.zinstyp || "–") + "</td></tr>");
    h.push("<tr><td>Aktionsdauer</td><td>" + (dauer ? dauer + " Monate" : "keine") + "</td></tr>");
    h.push("<tr><td>Mindestanlage</td><td>" + (a.mindestanlage === null || a.mindestanlage === undefined
      ? "keine Angabe" : geld(a.mindestanlage_eur !== null && a.mindestanlage_eur !== undefined
        ? a.mindestanlage_eur : a.mindestanlage)) + "</td></tr>");
    h.push("<tr><td>Höchstanlage</td><td>" + (a.hoechstanlage === null || a.hoechstanlage === undefined
      ? "keine Angabe" : geld(a.hoechstanlage_eur !== null && a.hoechstanlage_eur !== undefined
        ? a.hoechstanlage_eur : a.hoechstanlage)) + "</td></tr>");
    h.push("<tr><td>Einlagensicherung</td><td>" + geld(a.einlagensicherung_betrag_eur) + "</td></tr>");
    h.push("<tr><td>Sicherungsland</td><td>" + escape(a.einlagensicherung_land || "?") +
      (a.land_quelle === "quellenland_angenommen" ? " (angenommen)" : "") + "</td></tr>");
    if (a.sicherungssystem_name) {
      h.push('<tr class="zwischen"><td colspan="2">' + escape(a.sicherungssystem_name) +
        (a.sicherung_quelle ? ' · <a href="' + escape(a.sicherung_quelle) +
          '" target="_blank" rel="noopener">Quelle</a>' : "") + "</td></tr>");
    }
    if (a.ezb_landesdurchschnitt_pct !== null && a.ezb_landesdurchschnitt_pct !== undefined) {
      h.push("<tr><td>EZB-Landesdurchschnitt (" + escape(a.ezb_periode || "") + ")</td><td>" +
        pct(a.ezb_landesdurchschnitt_pct) + "</td></tr>");
      h.push("<tr><td>Abstand zum Durchschnitt</td><td>" +
        (a.differenz_zu_ezb_pp > 0 ? "+" : "") + nfProzent.format(a.differenz_zu_ezb_pp || 0) + " pp</td></tr>");
    }
    h.push("</table>");

    if (a.flag === "pruefen" && a.flag_grund) {
      h.push('<p class="hinweis">' + escape(a.flag_grund) + "</p>");
    }
    if (a.stale) {
      h.push('<p class="hinweis">Veralteter Wert: ' + escape(a.stale_grund || "") +
        " (seit " + escape(a.stale_seit || "?") + ")</p>");
    }
    if (a.extraction_tier === 3) {
      h.push('<p class="hinweis">Dieser Eintrag wurde automatisch aus dem Seitentext erkannt ' +
        "(Sprachmodell). Vor Abschluss unbedingt beim Anbieter prüfen.</p>");
    }
    if (a.land_quelle === "quellenland_angenommen") {
      h.push('<p class="hinweis">Das Sicherungsland stand nicht im Angebot und wurde vom Land ' +
        "der Quelle übernommen. Quellensteuer und Rating beruhen deshalb auf einer Annahme – " +
        "bei einer ausländischen Bank auf einem deutschen Vergleichsportal kann das falsch sein.</p>");
    }
    if (a.quellen_abweichung && a.quellen_abweichung.length) {
      h.push('<p class="hinweis">Quellen widersprechen sich: ' +
        escape(a.quellen_abweichung.map(function (q) {
          return q.quelle + " meldet " + q.zinssatz_pct + " %";
        }).join(", ")) + "</p>");
    }

    h.push("<h3>Quellen</h3>");
    h.push('<ul class="quellenliste">');
    (a.quellen || []).forEach(function (q) {
      h.push("<li>" + (q.url ? '<a href="' + escape(q.url) + '" target="_blank" rel="noopener">' +
        escape(q.id || q.url) + "</a>" : escape(q.id || "unbekannt")) +
        " · " + escape(q.typ || "?") + " · Stufe " + escape(q.extraction_tier) +
        " (" + escape(q.extraction_method || "?") + ")</li>");
    });
    h.push("</ul>");

    h.push('<div class="sheet-aktionen">' +
      '<button class="primaer" data-watch-detail="' + escape(a.dedupe_key) + '">' +
      (zustand.watchlist.indexOf(a.dedupe_key) !== -1 ? "Aus Watchlist entfernen" : "Zur Watchlist") +
      '</button><button class="text-knopf" data-schliessen>Schließen</button></div>');

    return h.join("");
  }

  function detailOeffnen(index) {
    var a = sichtbar[index];
    if (!a) return;
    $("sheetBody").innerHTML = detailHtml(a);
    $("sheet").hidden = false;
    document.body.style.overflow = "hidden";
  }

  function sheetsSchliessen() {
    $("sheet").hidden = true;
    $("einstellungen").hidden = true;
    document.body.style.overflow = "";
  }

  // -------------------------------------------- Watchlist + Meldung (F6)

  function watchUmschalten(key) {
    var i = zustand.watchlist.indexOf(key);
    if (i === -1) { zustand.watchlist.push(key); toast("Zur Watchlist hinzugefügt"); }
    else { zustand.watchlist.splice(i, 1); toast("Aus der Watchlist entfernt"); }
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
          if (p === "granted") { try { new Notification(titel, { body: text }); } catch (e) {} }
          else { toast(titel + ": " + text, 5000); }
        });
      }
    }
    toast(titel + ": " + text, 5000);
    return Promise.resolve();
  }

  function pruefeSchwelle(daten) {
    if (!zustand.einstellungen.benachrichtigung) return;
    var schwelle = parseFloat(zustand.einstellungen.schwelle);
    if (isNaN(schwelle)) return;
    if (!zustand.watchlist.length) return;

    var gemeldet = lies(SPEICHER.gemeldet, {});
    var heute = new Date().toISOString().slice(0, 10);
    var treffer = [];

    (daten.angebote || []).forEach(function (a) {
      if (zustand.watchlist.indexOf(a.dedupe_key) === -1) return;
      if (a.stale) return;
      var wert = a.zinssatz_pct;
      if (wert === null || wert === undefined || wert <= schwelle) return;
      if (gemeldet[a.dedupe_key] === heute + "|" + wert) return;
      gemeldet[a.dedupe_key] = heute + "|" + wert;
      treffer.push(a);
    });

    if (!treffer.length) return;
    schreib(SPEICHER.gemeldet, gemeldet);

    var titel = treffer.length === 1
      ? treffer[0].bank + ": " + pct(treffer[0].zinssatz_pct)
      : treffer.length + " Angebote über " + pct(schwelle);
    var text = treffer.slice(0, 4).map(function (a) {
      return a.bank + " " + pct(a.zinssatz_pct);
    }).join(", ");
    lokaleNotiz(titel, text);
  }

  // ------------------------------------------------------------ Theme (F8)

  function themeSetzen(wert) {
    if (wert === "auto") document.documentElement.removeAttribute("data-theme");
    else document.documentElement.setAttribute("data-theme", wert);
    schreib(SPEICHER.theme, wert);
    var farbe = wert === "dark" ? "#0d1117" : (wert === "light" ? "#ffffff" : "#0f172a");
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", farbe);
  }

  function themeUmschalten() {
    var jetzt = lies(SPEICHER.theme, "auto");
    var naechstes = jetzt === "auto" ? "light" : (jetzt === "light" ? "dark" : "auto");
    themeSetzen(naechstes);
    toast("Farbschema: " + (naechstes === "auto" ? "System" : naechstes === "light" ? "hell" : "dunkel"));
  }

  // ------------------------------------------------- Pull-to-Refresh (F8)

  function ptrEinrichten() {
    var startY = 0, ziehend = false, ausgeloest = false;
    var ptr = $("ptr");
    var SCHWELLE = 70;

    document.addEventListener("touchstart", function (e) {
      if (window.scrollY > 0 || zustand.laedt) return;
      if (!e.touches || e.touches.length !== 1) return;
      startY = e.touches[0].clientY;
      ziehend = true;
      ausgeloest = false;
    }, { passive: true });

    document.addEventListener("touchmove", function (e) {
      if (!ziehend) return;
      var delta = e.touches[0].clientY - startY;
      if (delta > 12 && window.scrollY <= 0) {
        ptr.classList.add("aktiv");
        ausgeloest = delta > SCHWELLE;
        $("ptrText").textContent = ausgeloest ? "Loslassen zum Aktualisieren" : "Zum Aktualisieren ziehen";
      } else if (delta <= 0) {
        ptr.classList.remove("aktiv");
        ziehend = false;
      }
    }, { passive: true });

    document.addEventListener("touchend", function () {
      if (!ziehend) return;
      ziehend = false;
      if (ausgeloest) {
        ptr.classList.add("laedt");
        $("ptrText").textContent = "Wird aktualisiert …";
        laden(true).then(function () {
          ptr.classList.remove("aktiv", "laedt");
        });
      } else {
        ptr.classList.remove("aktiv");
      }
    });
  }

  // ------------------------------------------------------- Einstellungen

  function einstellungenOeffnen() {
    var e = zustand.einstellungen;
    $("sErstattung").checked = !!e.erstattung;
    $("sAbgeltung").checked = !!e.abgeltung;
    $("sSchwelle").value = e.schwelle;
    $("sBenachrichtigung").checked = !!e.benachrichtigung;
    $("sQuelle").value = e.quelle || "";
    $("sQuelle").placeholder = CFG.datenUrl || "";
    $("quelleStatus").textContent = "Aktiv: " + (datenUrl() || "keine URL gesetzt");
    $("appVersion").textContent = CFG.version || "1.0.0";
    $("einstellungen").hidden = false;
    document.body.style.overflow = "hidden";
  }

  function einstellungenSpeichern() {
    var vorherQuelle = datenUrl();
    zustand.einstellungen.erstattung = $("sErstattung").checked;
    zustand.einstellungen.abgeltung = $("sAbgeltung").checked;
    zustand.einstellungen.schwelle = parseFloat($("sSchwelle").value) || 0;
    zustand.einstellungen.benachrichtigung = $("sBenachrichtigung").checked;
    zustand.einstellungen.quelle = ($("sQuelle").value || "").trim();
    schreib(SPEICHER.einst, zustand.einstellungen);
    sheetsSchliessen();
    rendern();

    if (zustand.einstellungen.benachrichtigung) {
      lokaleNotiz("Benachrichtigung aktiv",
        "Du bekommst Bescheid, wenn ein Wert aus der Watchlist über " +
        pct(zustand.einstellungen.schwelle) + " liegt.");
    }
    if (datenUrl() !== vorherQuelle) laden(true);
    else toast("Gespeichert");
  }

  // ------------------------------------------------------------ Ereignisse

  function ereignisse() {
    $("btnAktualisieren").addEventListener("click", function () { laden(true); });
    $("btnTheme").addEventListener("click", themeUmschalten);
    $("btnEinstellungen").addEventListener("click", einstellungenOeffnen);
    $("btnEinstellungenSpeichern").addEventListener("click", einstellungenSpeichern);

    $("btnFilter").addEventListener("click", function () {
      var b = $("filterBereich");
      b.hidden = !b.hidden;
    });

    $("suche").addEventListener("input", function (e) {
      zustand.suche = e.target.value;
      rendern();
    });

    document.querySelectorAll(".sort").forEach(function (knopf) {
      knopf.addEventListener("click", function () {
        document.querySelectorAll(".sort").forEach(function (k) { k.classList.remove("aktiv"); });
        knopf.classList.add("aktiv");
        zustand.sortierung = knopf.dataset.sort;
        rendern();
      });
    });

    var filterFelder = {
      fLand: "land", fTyp: "typ", fBetrag: "betrag", fQuelltyp: "quelltyp",
    };
    Object.keys(filterFelder).forEach(function (id) {
      $(id).addEventListener("change", function (e) {
        zustand.filter[filterFelder[id]] = e.target.value;
        rendern();
      });
      if (id === "fBetrag") {
        $(id).addEventListener("input", function (e) {
          zustand.filter.betrag = e.target.value;
          rendern();
        });
      }
    });
    [["fNurEur", "nurEur"], ["fNurWatchlist", "nurWatch"], ["fOhneStale", "ohneStale"]]
      .forEach(function (paar) {
        $(paar[0]).addEventListener("change", function (e) {
          zustand.filter[paar[1]] = e.target.checked;
          rendern();
        });
      });

    $("btnFilterReset").addEventListener("click", function () {
      zustand.filter = { land: "", typ: "", betrag: "", quelltyp: "", nurEur: false, nurWatch: false, ohneStale: false };
      $("fLand").value = ""; $("fTyp").value = ""; $("fBetrag").value = ""; $("fQuelltyp").value = "";
      $("fNurEur").checked = false; $("fNurWatchlist").checked = false; $("fOhneStale").checked = false;
      rendern();
    });

    $("liste").addEventListener("click", function (e) {
      var stern = e.target.closest("[data-watch]");
      if (stern) {
        e.stopPropagation();
        var a = sichtbar[parseInt(stern.dataset.watch, 10)];
        if (a) watchUmschalten(a.dedupe_key);
        return;
      }
      var karte = e.target.closest(".karte");
      if (karte) detailOeffnen(parseInt(karte.dataset.index, 10));
    });

    document.addEventListener("click", function (e) {
      if (e.target.closest("[data-schliessen]")) { sheetsSchliessen(); return; }
      var wd = e.target.closest("[data-watch-detail]");
      if (wd) {
        watchUmschalten(wd.dataset.watchDetail);
        wd.textContent = zustand.watchlist.indexOf(wd.dataset.watchDetail) !== -1
          ? "Aus Watchlist entfernen" : "Zur Watchlist";
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") sheetsSchliessen();
    });

    window.addEventListener("online", function () { laden(false); });
  }

  // ------------------------------------------------------------- Start

  function start() {
    zustand.einstellungen = Object.assign(zustand.einstellungen, lies(SPEICHER.einst, {}));
    zustand.watchlist = lies(SPEICHER.watch, []);
    themeSetzen(lies(SPEICHER.theme, "auto"));

    var zwischen = lies(SPEICHER.daten, null);
    if (zwischen && pruefeStruktur(zwischen.daten)) {
      uebernehmen(zwischen.daten, "cache", null, zwischen.geholt);
    }

    ereignisse();
    ptrEinrichten();
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
