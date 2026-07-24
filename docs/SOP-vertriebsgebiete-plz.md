# SOP: Vertriebsgebiete per PLZ pflegen (GIGA.GREEN)

Stand: 23.07.2026 | Verantwortlich: Sarah Schelter (Commercial Ops) | Technik: Eddie Esche (Klickstark)

## Wie das System funktioniert

Die Buchungsseite für das Calling-Team (giga.green/informationstermin-outbound-call) und die Besitzer-Zuweisung in Zoho lesen **dieselbe Konfigurationstabelle** (Google Sheet „Calendly-Links AEs"). Die Zuordnung läuft über die **ersten zwei Ziffern der Postleitzahl**. Änderst du das Sheet, gilt die neue Zuordnung sofort — auf der Website beim nächsten Laden der Seite, in Zoho beim nächsten Lead. Es muss nichts deployt oder umprogrammiert werden.

Config-Sheet: https://docs.google.com/spreadsheets/d/1awZbdxPiTlMA3USyHL73Uuvukz3W1XTtUB0l7xbUmSg/edit

## Die relevanten Spalten

| Spalte | Bedeutung | Beispiel |
|---|---|---|
| `name` | Anzeigename des AE (sieht das Calling-Team) | Daniel Budisky |
| `plz_prefixes` | Komma-Liste der PLZ-Gebiete (immer 2-stellig) | 01,02,03,04 |
| `calendly_link` | Calendly-URL des AE | https://calendly.com/d-budisky-giga/informationstermin-giga-green |
| `zoho_owner_email` | Zoho-Login-Email des AE | d.budisky@giga.green |
| `zoho_owner_id` | Zoho-User-ID (für die automatische Besitzer-Zuweisung) | 657604000024787343 |

Eine Zeile pro AE. Die Spalten `Bundesland` und `NEU` sind Altbestand und werden nach dem 15.08. entfernt.

## Gebietswechsel durchführen (Standardfall)

Beispiel: Ein AE übernimmt Gebiete von einem anderen.

1. Öffne das Config-Sheet.
2. Verschiebe die betroffenen 2-stelligen Prefixe von der einen `plz_prefixes`-Zelle in die andere (Komma-getrennt, führende Null beachten: „01", nicht „1").
3. Prüfe kurz: Jeder Prefix darf nur **einmal** im Sheet stehen (bei Dopplern gewinnt die obere Zeile).
4. Test: Buchungsseite öffnen, eine PLZ aus dem verschobenen Gebiet eingeben — es muss der neue AE mit seinem Kalender erscheinen. (Nichts buchen, nur ansehen.)

Fertig. Zoho übernimmt die Änderung automatisch für alle neuen bzw. geänderten Leads.

## Neuen AE aufnehmen

Dafür braucht es einmalig drei Dinge — bitte kurz mit Eddie koordinieren:

1. **Zoho-User** angelegt und aktiv (daraus ergibt sich die `zoho_owner_id` — steht in Zoho unter Einstellungen → Benutzer in der URL des Users, oder Eddie liest sie per API aus).
2. **Calendly-Konto** in eurer Organisation mit einem Event-Typ analog „informationstermin-giga-green".
3. Neue Zeile im Config-Sheet mit allen fünf Spalten, dann Prefixe zuweisen (siehe oben).

## Fahrplan 2026 (Copy-Paste-Vorlagen)

Werte für die `plz_prefixes`-Zellen je Phase. Quelle: eure Gebietsaufteilung, Stand Juli.

**Ab 15.08.2026** (Umschaltung macht Klickstark, inkl. Zoho):

| AE | plz_prefixes |
|---|---|
| Daniel Budisky (Ost + Nord komm.) | 01,02,03,04,06,07,08,09,10,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,29 |
| Boris — Mitte, NEU | 30,31,34,36,37,38,39,96,98,99 |
| Christian Thiemann (West 1) | 32,33,40,41,42,44,45,46,47,48,49,50,51,52,53,57,58,59 |
| Chirag Thakkar (West 2) | 35,54,55,56,60,61,63,64,65,66,67,68,69 |
| Fabian Hirschler (Süd) | 70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95 |

Offen (bitte entscheiden): **28** (Bremen — bisher Daniel) und **97** (Würzburg — bisher Chirag) sind in der Aufteilung ab 15.08. keinem Gebiet zugeordnet.

**Ab 01.10.2026** (kann Sarah selbst per Sheet-Edit):

| AE | plz_prefixes |
|---|---|
| Daniel Budisky (Ost) | 01,02,03,04,06,07,08,09,10,12,13,14,15,16,17 |
| Michael — Nord, NEU | 18,19,20,21,22,23,24,25,26,27,29 |
| übrige | unverändert |

**Q4/2026** (kann Sarah selbst, sobald Süd-Ost-AE steht):

| AE | plz_prefixes |
|---|---|
| Süd-Ost — NEU | 80,81,82,83,84,85,86,90,91,92,93,94,95 |
| Fabian Hirschler (dann Süd-West) | 70,71,72,73,74,75,76,77,78,79,87,88,89 |

## Regeln und Fallstricke

- Immer **2-stellig** mit führender Null („06", nicht „6"), Komma-getrennt. Leerzeichen sind egal.
- Diese PLZ-Zonen existieren in Deutschland nicht: 00, 05, 11, 43, 62 — nicht zuweisen.
- Jeder existierende Prefix sollte genau einem AE zugewiesen sein. Lücken führen dazu, dass Caller einen Warnhinweis sehen und kein Kalender lädt.
- Zeilen von AEs nicht löschen, solange sie aktiv sind — nur die `plz_prefixes`-Zelle leeren bzw. umverteilen.
- Das Bundesland wählt niemand mehr aus: Es wird automatisch aus der vollen PLZ abgeleitet und weiter ins CRM geschrieben (Reporting bleibt wie gewohnt).

## Was passiert bei Problemen

| Situation | Verhalten |
|---|---|
| Caller gibt PLZ ohne zugewiesenes Gebiet ein | Website zeigt Warnhinweis, kein Kalender lädt |
| Lead in Zoho mit PLZ ohne Gebiet | Keine Zuweisung, automatische Benachrichtigung an Eddie |
| Config-Sheet nicht erreichbar | Zoho lässt den Lead unangetastet und benachrichtigt Eddie |
| Lead ohne PLZ (z. B. Inbound) | Keine automatische Zuweisung (Fallback-Regelung in Klärung) |

Fragen oder etwas kaputt: Eddie Esche (Klickstark) via Slack.
