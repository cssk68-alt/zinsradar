"""Netzwerkzugriff: robots.txt, Rate-Limit, Retry, optionales Rendering.

Regeln, die hier hart verdrahtet sind:
  * robots.txt wird LIVE geholt und geparst. Das Feld `robots_txt_erlaubt`
    in sources.yaml ist nur ein Hinweis aus der Recherche und entscheidet
    nichts. Sagt die echte robots.txt "nein", wird die Quelle uebersprungen.
  * Pro Domain hoechstens ein Request alle `min_abstand_pro_domain_s`
    Sekunden (Default 2s). Gilt auch fuer robots.txt selbst.
  * Retry mit exponentiellem Backoff, `Retry-After` wird respektiert.
  * Playwright wird nur fuer rendering: js_required benutzt und ist
    optional - fehlt es, faellt der Fetch auf statisches HTML zurueck.
"""

from __future__ import annotations

import time
import urllib.robotparser
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlsplit, urlunsplit, quote

import httpx

from util import cfg_get, domain_von, log

# Statuscodes, bei denen ein neuer Versuch sinnvoll ist.
RETRY_STATUS = {408, 425, 429, 500, 502, 503, 504}


@dataclass
class Antwort:
    """Ergebnis eines Abrufs. Nie eine Exception nach aussen."""

    url: str
    final_url: str = ""
    status: int | None = None
    text: str = ""
    content_type: str = ""
    ok: bool = False
    fehler: str | None = None
    gesperrt: bool = False          # von robots.txt verboten
    gerendert: bool = False         # ueber Playwright geholt
    dauer_s: float = 0.0
    versuche: int = 0

    @property
    def laenge(self) -> int:
        return len(self.text)


@dataclass
class RobotsInfo:
    """Urteil fuer eine konkrete URL."""

    erlaubt: bool
    grund: str
    crawl_delay: float | None = None


@dataclass
class RobotsEintrag:
    """Was pro Domain gecacht wird."""

    domain_erlaubt: bool          # False = Domain komplett meiden (5xx, unerreichbar)
    grund: str
    parser: urllib.robotparser.RobotFileParser | None = None
    crawl_delay: float | None = None
    zeit: float = field(default_factory=time.monotonic)


def url_normalisieren(url: str) -> str:
    """Nicht-ASCII im Pfad prozent-kodieren.

    Noetig, weil in sources.yaml URLs mit Akzenten stehen koennen
    (z.B. .../poupanca/...). httpx wuerde sonst je nach Version stolpern.
    """
    teile = urlsplit(url)
    pfad = quote(teile.path, safe="/%:@&=+$,-_.!~*'()")
    return urlunsplit((teile.scheme, teile.netloc, pfad, teile.query, teile.fragment))


class Fetcher:
    """Ein Fetcher pro Lauf. Haelt Rate-Limit- und robots-Zustand."""

    def __init__(self, *, user_agent: str | None = None, timeout: float | None = None):
        self.user_agent = user_agent or cfg_get("fetch.user_agent", "ZinsradarBot/1.0")
        self.timeout = timeout if timeout is not None else float(cfg_get("fetch.timeout_s", 30.0))
        self.min_abstand = float(cfg_get("fetch.min_abstand_pro_domain_s", 2.0))
        self.max_versuche = int(cfg_get("fetch.max_versuche", 3))
        self.backoff_faktor = float(cfg_get("fetch.backoff_faktor", 2.0))
        self.backoff_basis = float(cfg_get("fetch.backoff_basis_s", 1.5))
        self.robots_aktiv = bool(cfg_get("fetch.robots_respektieren", True))

        self._letzter_zugriff: dict[str, float] = {}
        self._robots: dict[str, RobotsEintrag] = {}
        self._browser_ctx: Any = None
        self._playwright: Any = None

        self.client = httpx.Client(
            timeout=self.timeout,
            follow_redirects=True,
            headers={
                "User-Agent": self.user_agent,
                "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
                "Accept-Language": "de,en;q=0.8",
            },
        )

    # ------------------------------------------------------------ Rate-Limit

    def _warte_auf_domain(self, url: str, extra_delay: float = 0.0) -> None:
        dom = domain_von(url)
        if not dom:
            return
        abstand = max(self.min_abstand, extra_delay)
        letzter = self._letzter_zugriff.get(dom)
        if letzter is not None:
            rest = abstand - (time.monotonic() - letzter)
            if rest > 0:
                time.sleep(rest)
        self._letzter_zugriff[dom] = time.monotonic()

    # ------------------------------------------------------------ robots.txt

    def _robots_holen(self, url: str) -> RobotsEintrag:
        """Holt robots.txt einer Domain genau einmal pro Cache-Fenster."""
        teile = urlsplit(url)
        robots_url = urlunsplit((teile.scheme, teile.netloc, "/robots.txt", "", ""))
        self._warte_auf_domain(robots_url)

        try:
            r = self.client.get(robots_url, timeout=min(self.timeout, 15.0))
        except httpx.HTTPError as e:
            # Kein Urteil moeglich -> konservativ: Domain meiden.
            return RobotsEintrag(False, f"robots.txt nicht erreichbar: {type(e).__name__}")

        if r.status_code >= 500:
            # RFC 9309: bei 5xx gilt "complete disallow".
            return RobotsEintrag(False, f"robots.txt HTTP {r.status_code} (Serverfehler)")

        parser = urllib.robotparser.RobotFileParser()
        if r.status_code >= 400:
            parser.parse([])
            grund = f"keine robots.txt (HTTP {r.status_code})"
        else:
            parser.parse(r.text.splitlines())
            grund = "robots.txt gelesen"

        delay: float | None = None
        try:
            roh = parser.crawl_delay(self.user_agent)
            if roh is None:
                roh = parser.crawl_delay("*")
            delay = float(roh) if roh is not None else None
        except Exception:
            delay = None

        return RobotsEintrag(True, grund, parser=parser, crawl_delay=delay)

    def robots_pruefen(self, url: str) -> RobotsInfo:
        """Urteil fuer eine konkrete URL. Nutzt den Domain-Cache."""
        if not self.robots_aktiv:
            return RobotsInfo(True, "robots-Pruefung per Config deaktiviert")

        dom = domain_von(url)
        if not dom:
            return RobotsInfo(False, "keine Domain in der URL")

        cache_s = float(cfg_get("fetch.robots_cache_s", 3600))
        eintrag = self._robots.get(dom)
        if eintrag is None or (time.monotonic() - eintrag.zeit) >= cache_s:
            eintrag = self._robots_holen(url)
            self._robots[dom] = eintrag

        if not eintrag.domain_erlaubt:
            return RobotsInfo(False, eintrag.grund, eintrag.crawl_delay)

        if eintrag.parser is None:
            return RobotsInfo(True, eintrag.grund, eintrag.crawl_delay)

        try:
            erlaubt = eintrag.parser.can_fetch(self.user_agent, url)
        except Exception:
            erlaubt = True  # kaputte robots.txt blockiert nicht

        if not erlaubt:
            return RobotsInfo(False, "robots.txt verbietet diesen Pfad", eintrag.crawl_delay)
        return RobotsInfo(True, eintrag.grund, eintrag.crawl_delay)

    # ------------------------------------------------------------ HTTP

    def hole(self, url: str, *, robots: bool = True, header_extra: dict | None = None) -> Antwort:
        """Statischer Abruf mit Retry/Backoff. Wirft nie."""
        url = url_normalisieren(url)
        ant = Antwort(url=url)
        start = time.monotonic()

        if robots:
            info = self.robots_pruefen(url)
            if not info.erlaubt:
                ant.gesperrt = True
                ant.fehler = info.grund
                ant.dauer_s = time.monotonic() - start
                log().info("robots: uebersprungen %s (%s)", url, info.grund)
                return ant
            extra_delay = info.crawl_delay or 0.0
        else:
            extra_delay = 0.0

        wartezeit = self.backoff_basis
        for versuch in range(1, self.max_versuche + 1):
            ant.versuche = versuch
            self._warte_auf_domain(url, extra_delay)
            try:
                r = self.client.get(url, headers=header_extra or {})
                ant.status = r.status_code
                ant.final_url = str(r.url)
                ant.content_type = r.headers.get("content-type", "")
                if r.status_code in RETRY_STATUS and versuch < self.max_versuche:
                    ra = r.headers.get("retry-after")
                    pause = wartezeit
                    if ra:
                        try:
                            pause = max(pause, float(ra))
                        except ValueError:
                            pass
                    log().debug("HTTP %s bei %s - neuer Versuch in %.1fs", r.status_code, url, pause)
                    time.sleep(min(pause, 30.0))
                    wartezeit *= self.backoff_faktor
                    continue
                ant.text = r.text
                ant.ok = 200 <= r.status_code < 300 and bool(r.text)
                if not ant.ok and ant.fehler is None:
                    ant.fehler = f"HTTP {r.status_code}"
                break
            except httpx.HTTPError as e:
                ant.fehler = f"{type(e).__name__}: {e}"
                if versuch < self.max_versuche:
                    time.sleep(min(wartezeit, 30.0))
                    wartezeit *= self.backoff_faktor
                    continue
                break

        ant.dauer_s = time.monotonic() - start
        return ant

    def hole_json(self, url: str, *, robots: bool = True) -> tuple[Antwort, Any]:
        """Wie hole(), aber parst JSON. Zweiter Rueckgabewert ist None bei Fehler."""
        ant = self.hole(url, robots=robots, header_extra={"Accept": "application/json,*/*;q=0.8"})
        if not ant.ok:
            return ant, None
        import json

        try:
            return ant, json.loads(ant.text)
        except (ValueError, TypeError) as e:
            ant.fehler = f"kein gueltiges JSON: {e}"
            return ant, None

    # ------------------------------------------------------------ Playwright

    def _browser(self):
        """Startet Playwright beim ersten Bedarf. None, wenn nicht verfuegbar."""
        if self._browser_ctx is not None:
            return self._browser_ctx
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            log().warning(
                "Playwright nicht installiert - js_required-Quellen werden statisch geholt. "
                "Installation: pip install playwright && playwright install chromium"
            )
            return None
        try:
            self._playwright = sync_playwright().start()
            browser = self._playwright.chromium.launch(headless=True)
            optionen: dict[str, Any] = {
                "locale": "de-DE",
                "viewport": {"width": 1366, "height": 900},
            }
            # Ein gerenderter Chromium IST ein Browser. Ihm den Bot-UA
            # aufzudruecken bringt nur kaputtes Rendering und blockierte
            # Requests - robots.txt wird davon unabhaengig weiter befolgt.
            if not cfg_get("fetch.playwright_eigener_ua", True):
                optionen["user_agent"] = self.user_agent
            self._browser_ctx = browser.new_context(**optionen)
            return self._browser_ctx
        except Exception as e:
            log().warning("Playwright startet nicht (%s) - fallback auf statisches HTML.", e)
            self._playwright = None
            return None

    def hole_gerendert(self, url: str, *, robots: bool = True) -> Antwort:
        """Rendert die Seite im Browser. Faellt auf hole() zurueck, wenn das nicht geht."""
        url = url_normalisieren(url)
        if robots:
            info = self.robots_pruefen(url)
            if not info.erlaubt:
                a = Antwort(url=url, gesperrt=True, fehler=info.grund)
                log().info("robots: uebersprungen %s (%s)", url, info.grund)
                return a

        ctx = self._browser()
        if ctx is None:
            return self.hole(url, robots=False)

        ant = Antwort(url=url)
        start = time.monotonic()
        self._warte_auf_domain(url)
        seite = None
        try:
            seite = ctx.new_page()
            resp = seite.goto(
                url,
                timeout=int(cfg_get("fetch.playwright_timeout_ms", 25000)),
                wait_until=cfg_get("fetch.playwright_warte_auf", "networkidle"),
            )
            ant.status = resp.status if resp else None
            ant.final_url = seite.url
            ant.text = seite.content()
            ant.content_type = "text/html"
            ant.gerendert = True
            ant.ok = bool(ant.text) and (ant.status is None or ant.status < 400)
            if not ant.ok:
                ant.fehler = f"HTTP {ant.status}"
        except Exception as e:
            ant.fehler = f"Playwright: {type(e).__name__}: {e}"
            log().debug("Rendering fehlgeschlagen fuer %s: %s", url, e)
        finally:
            if seite is not None:
                try:
                    seite.close()
                except Exception:
                    pass

        ant.dauer_s = time.monotonic() - start
        ant.versuche = 1

        if not ant.ok:
            log().debug("Rendering ohne Ergebnis - versuche statisch: %s", url)
            statisch = self.hole(url, robots=False)
            if statisch.ok:
                statisch.fehler = f"gerendert fehlgeschlagen ({ant.fehler}), statisch geholt"
                return statisch
        return ant

    # ------------------------------------------------------------ Aufraeumen

    def schliessen(self) -> None:
        try:
            self.client.close()
        except Exception:
            pass
        if self._browser_ctx is not None:
            try:
                self._browser_ctx.close()
            except Exception:
                pass
        if self._playwright is not None:
            try:
                self._playwright.stop()
            except Exception:
                pass
        self._browser_ctx = None
        self._playwright = None

    def __enter__(self) -> "Fetcher":
        return self

    def __exit__(self, *exc) -> None:
        self.schliessen()
