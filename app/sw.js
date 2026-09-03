/* Service Worker: App-Shell offline halten, Daten frisch holen wenn möglich.
 *
 * Shell  -> cache-first  (ändert sich nur beim Release)
 * Daten  -> network-first mit Cache-Fallback (täglich neu, muss aber
 *           auch im Funkloch etwas anzeigen)
 */
var VERSION = "zinsradar-v3";
var SHELL_CACHE = VERSION + "-shell";
var DATEN_CACHE = VERSION + "-daten";

var SHELL = [
  "./",
  "index.html",
  "app.css",
  "app.js",
  "config.js",
  "manifest.webmanifest",
  "icons/icon.svg",
  "icons/icon-192.png",
  "icons/icon-512.png",
  "data/zinsen.json",
];

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(SHELL_CACHE).then(function (cache) {
      // Einzeln, damit eine fehlende Datei die Installation nicht kippt.
      return Promise.all(SHELL.map(function (pfad) {
        return cache.add(pfad).catch(function () { return null; });
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (namen) {
      return Promise.all(namen.map(function (name) {
        if (name !== SHELL_CACHE && name !== DATEN_CACHE) return caches.delete(name);
        return null;
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

function istDaten(url) {
  return url.pathname.indexOf("zinsen.json") !== -1 ||
         url.pathname.indexOf("referenz.json") !== -1 ||
         url.hostname.indexOf("raw.githubusercontent.com") !== -1;
}

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;

  var url;
  try { url = new URL(e.request.url); } catch (err) { return; }
  if (url.protocol !== "http:" && url.protocol !== "https:") return;

  if (istDaten(url)) {
    e.respondWith(
      fetch(e.request).then(function (antwort) {
        if (antwort && antwort.ok) {
          var kopie = antwort.clone();
          caches.open(DATEN_CACHE).then(function (c) { c.put(e.request, kopie); });
        }
        return antwort;
      }).catch(function () {
        // Gezielt im Datencache nachsehen. caches.match() ohne Angabe
        // durchsucht die Caches in Anlagereihenfolge und liefert dann die
        // aeltere, mitgelieferte Kopie aus dem Shell-Cache statt der
        // frischeren aus dem Datencache.
        return caches.open(DATEN_CACHE).then(function (c) {
          return c.match(e.request).then(function (treffer) {
            return treffer || caches.match("data/zinsen.json");
          });
        });
      })
    );
    return;
  }

  if (url.origin !== self.location.origin) return;

  // App-Shell: stale-while-revalidate.
  // Aus dem Cache antworten (schnell und offline-fest), im Hintergrund
  // trotzdem neu holen. Ohne das bekämen Nutzer nach einem Update so
  // lange die alte Oberfläche, bis jemand VERSION hier hochzählt.
  e.respondWith(
    caches.match(e.request).then(function (treffer) {
      var frisch = fetch(e.request).then(function (antwort) {
        if (antwort && antwort.ok && antwort.type === "basic") {
          var kopie = antwort.clone();
          caches.open(SHELL_CACHE).then(function (c) { c.put(e.request, kopie); });
        }
        return antwort;
      }).catch(function () {
        if (treffer) return treffer;
        if (e.request.mode === "navigate") return caches.match("index.html");
        return new Response("", { status: 504, statusText: "offline" });
      });
      return treffer || frisch;
    })
  );
});
