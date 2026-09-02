/* Zinsradar - Konfiguration.
 *
 * WICHTIG: `datenUrl` auf das eigene Repo zeigen lassen, sonst findet die
 * App keine Daten. Format:
 *   https://raw.githubusercontent.com/<NUTZER>/<REPO>/<BRANCH>/data/zinsen.json
 *
 * Die URL lässt sich auch zur Laufzeit in den Einstellungen ändern; der
 * Wert dort gewinnt gegen diese Datei.
 */
window.ZINSRADAR_CONFIG = {
  version: "1.0.0",

  // Zeigt auf das Repo cssk68-alt/zinsradar. Bei einem Fork hier anpassen.
  datenUrl: "https://raw.githubusercontent.com/cssk68-alt/zinsradar/main/data/zinsen.json",

  // Mitgelieferte Kopie: greift beim allerersten Start ohne Netz und in der APK.
  lokalerFallback: "data/zinsen.json",

  // Netzwerk-Timeout in Millisekunden, danach wird der Cache benutzt.
  timeoutMs: 12000,
};
