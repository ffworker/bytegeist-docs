# Prüfstand und Recovery

<div class="bg-eyebrow">INTERN / BETRIEBSVERTRAUEN</div>

Eine erfolgreich gebaute Dokumentationsseite beweist, dass Markdown gerendert wurde – nicht, dass die beschriebene Infrastruktur noch genauso läuft.

| Nachweis | Aussage | Grenze |
| --- | --- | --- |
| Git-Commit | Aus welcher Revision der Text stammt | Kein Beweis für den aktuellen Host-Zustand |
| Abrufzeit | Wann die Quelle importiert wurde | Keine inhaltliche Prüfung |
| Erfolgreicher Zensical-Build | Seiten lassen sich ausliefern | Kein Service- oder Restore-Test |
| Datiertes Betreiberergebnis | Ein konkreter Funktionstest gelang | Keine garantierte künftige Verfügbarkeit |
| Isolierter Restore | Der dokumentierte Wiederherstellungsfall funktioniert | Andere Ausfallarten bleiben separat zu prüfen |

!!! warning "Ungeprüft bleibt ungeprüft"
    Bei einem Störungsfall zuerst feststellen, ob eine Anleitung aktuell und für die betroffene Systemversion gültig ist. Einen Git-Pin niemals mit einem Live-Health-Check verwechseln.

## Wenn die Infrastruktur ausfällt

Bytegeist Docs soll unabhängig vom alten VPS02-Docs-Deployment privat bereitstehen. Zusätzlich gehört eine **offline nutzbare Kopie der wichtigsten Recovery-Runbooks** zum Betriebsverfahren. Die tatsächliche Wiederherstellung ist separat zu testen; ein erfolgreicher Build genügt nicht.
