package de.zinsradar.app;

import com.getcapacitor.BridgeActivity;

/**
 * Huelle um die PWA.
 *
 * Die eigentliche Anwendung liegt in assets/public und wird von der
 * Capacitor-Bridge in einer WebView geladen. Plugins werden ueber
 * assets/capacitor.plugins.json registriert, deshalb ist hier nichts
 * weiter zu tun.
 */
public class MainActivity extends BridgeActivity {
}
