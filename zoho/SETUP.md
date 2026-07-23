# Zoho-Setup: PLZ-basierte Owner-Zuweisung

Stand 2026-07-23. Org: `crm.zoho.eu/crm/org20094831717`

## Bausteine

1. **Custom Function** `assign_owner_by_plz` (Code: `assign_owner_by_plz.dg`)
   - Einstellungen → Entwicklerbereich (Developer Hub) → Funktionen → Neue Funktion
   - Name: `assign_owner_by_plz`, Kategorie: **Automatisierung**
   - Argument: `leadId` (Typ String)
   - Code aus `assign_owner_by_plz.dg` einfügen (ohne die erste Signaturzeile,
     falls der Editor die Signatur selbst erzeugt), speichern.
   - Test im Editor: „Ausführen" mit `leadId` = ID eines Testleads mit gesetzter
     `Standort Postleitzahl`.

2. **Workflow-Rule A** — Neuanlage mit PLZ
   - Einstellungen → Automatisierung → Workflow-Regeln → Neue Regel, Modul Leads
   - Name: `PLZ Lead Assignment - Create`
   - WANN: Bei Datensatzaktion → **Erstellen**
   - BEDINGUNG: `Standort Postleitzahl` **ist nicht leer**
   - SOFORTIGE AKTION: Funktion → `assign_owner_by_plz`, Argument
     `leadId` = `${Leads.Lead Id}`
   - **Nach dem Anlegen DEAKTIVIERT lassen bis Go-Live 15.08.**

3. **Workflow-Rule B** — PLZ-Änderung
   - Wie A, aber WANN: **Feldaktualisierung** von `Standort Postleitzahl`
     (Änderung zu beliebigem Wert)
   - Name: `PLZ Lead Assignment - Update`
   - **Ebenfalls deaktiviert lassen bis Go-Live.**

## Go-Live 15.08.

1. Config-Sheet: `plz_prefixes`-Zellen auf „Aufteilung ab 15.08." umstellen,
   Boris-Zeile mit `zoho_owner_id` + Calendly-Link ergänzen.
2. Rules A + B **aktivieren**.
3. Alte Rule „New Infocall Lead Assignment" (Bundesland-basiert,
   `.../workflow-rules/657604000014206004`) **deaktivieren** (nicht löschen).
4. Testlead mit PLZ anlegen → Owner-Zuweisung prüfen.

## Verhalten der Function

| Fall | Ergebnis |
|---|---|
| PLZ fehlt/ungültig | keine Änderung (SKIP im Log) |
| Prefix ohne Mapping | Mail an Eddie, optional Fallback (`FALLBACK_OWNER_ID`, aktuell leer — wartet auf Klärung GIGA.GREEN) |
| CSV nicht erreichbar | Mail an Eddie, keine Änderung |
| Owner schon korrekt | keine Änderung (verhindert Re-Assign-Schleifen) |

## Referenz: bestätigte Zoho-User-IDs (aktive AEs)

| AE | Email | zoho_owner_id |
|---|---|---|
| Daniel Budisky | d.budisky@giga.green | 657604000024787343 |
| Christian Thiemann | c.thiemann@giga.green | 657604000017656100 |
| Chirag Thakkar | c.thakkar@giga.green | 657604000045935001 |
| Fabian Hirschler | f.hirschler@giga.green | 657604000008619001 |
| (Fallback-Kandidatin) Viktoria Kirchhöfer | v.kirchhoefer@giga.green | 657604000017246001 |

Boris/Michael: Stand 23.07. weder in Zoho noch in Calendly angelegt — IDs
nachtragen, sobald GIGA.GREEN die User erstellt hat.
