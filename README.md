# GIGA.GREEN PLZ-Setter (Buchungsseite Outbound-Infocall)

Terminbuchungs-Tool für das Cold-Calling-Team: PLZ eingeben → zuständiger Account Executive wird ermittelt (erste zwei Ziffern der PLZ) → Calendly-Kalender lädt → nach der Buchung Lead-Formular → Versand via Cloudflare-Worker an Make → Zoho CRM.

Eingebunden auf `https://www.giga.green/informationstermin-outbound-call` (Webflow) über:
`https://klickstark-digital-act-gbr.github.io/gigagreen-plz-setter/script.js`

## Architektur

```
Webflow-Seite (.setter-tool div)
  └─ script.js (GitHub Pages, dieses Repo, Branch main)
       ├─ GET  Worker /api/sheet-csv   → PLZ-Konfiguration (Google Sheet)
       ├─ GET  Worker /api/calendly/*  → Invitee-Details, Stornierung
       └─ POST Worker /api/make        → Formulardaten → Make → Zoho-Lead
Worker: https://gigagreen-calendly-proxy.eddie-esche.workers.dev (Cloudflare, Account Eddie)
```

## Konfiguration (Single Source of Truth)

Google Sheet „Calendly-Links AEs" (`1awZbdxPiTlMA3USyHL73Uuvukz3W1XTtUB0l7xbUmSg`), Tab 1.
Relevante Spalten ab v3 — eine Zeile pro AE:

| Spalte | Bedeutung |
|---|---|
| `name` | Anzeigename des AE |
| `plz_prefixes` | Komma-Liste zweistelliger PLZ-Prefixe, z. B. `01,02,03` |
| `calendly_link` | Calendly-URL des AE |
| `zoho_owner_email` | Zoho-User-Email für die Owner-Zuweisung (nur von Zoho genutzt) |

Regeln: Nur Zeilen mit `name` UND `plz_prefixes` zählen. Ungültige Tokens werden ignoriert, bei doppelten Prefixen gewinnt die erste Zeile (jeweils `console.warn`). Die Bundesland-Zeilen darüber sind Legacy (Script bis v2) und werden nach Go-Live 15.08.2026 entfernt.

## Bundesland-Ableitung

Das Bundesland wird nicht mehr ausgewählt, sondern beim Absenden aus der vollen 5-stelligen Formular-PLZ abgeleitet und als `bundesland` im Payload mitgeschickt (fürs Zoho-Reporting; Feldwerte identisch zum alten Dropdown). Quelle: `plz-bundesland.js` — kompakte Range-Tabelle (9.856 PLZs, 199 Ranges, 4,3 KB) generiert aus GeoNames-Daten (CC-BY 4.0) via `tools/build-plz-bundesland.py`. Unbekannte PLZ → leerer String. Grenzfälle (14xxx Berlin/Brandenburg, 97xxx Bayern/BW, 21xxx HH/NI usw.) sind PLZ-genau korrekt.

**Gebietswechsel = nur `plz_prefixes`-Zellen im Sheet ändern.** Kein Deploy nötig. Die Zoho-Owner-Zuweisung (Deluge-Function `assign_owner_by_plz`) liest dieselbe CSV — Website und CRM bleiben automatisch synchron.

## Deploy

Push auf `main` deployt sofort via GitHub Pages auf die Live-Seite. Vorher lokal testen:

```bash
python3 -m http.server 8321 -d . 
```

`index.html` ist der Testharness (Testfälle oben auf der Seite, Konsole wird eingeblendet). Er lädt die echte Worker-CSV.

## Historie

- **v3 (07/2026):** PLZ-basiertes Routing (erste zwei Ziffern), Bundesland-Dropdown entfernt. Formular-PLZ wird aus Schritt 1 vorbefüllt; Warnhinweis bei unbekanntem Prefix; Hinweis bei abweichender Formular-PLZ.
- **v2:** Bundesland-Dropdown, Proxy-Integration (Keys aus dem Client entfernt), Storno-Flow, Zeilenumbruch-Fix fürs Notizenfeld (Make).
