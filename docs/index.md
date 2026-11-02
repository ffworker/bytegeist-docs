# Bytegeist Docs — Start here

Das ist meine **private Leseansicht** für ausgewählte Projekt- und Homelab-Dokumentation. Die Originale bleiben in den jeweiligen Git-Repositories; hier lese und suche ich sie gemeinsam. **Dieses Portal ist kein Live-Monitoring und keine zweite editierbare Wiki-Kopie.**

## Ich suche …

| Frage | Wo anfangen? |
| --- | --- |
| Wie ist mein Homelab aufgebaut? | **Repositories → infra-configs → README** (aktuelle Bestandsübersicht und Quellverweise) |
| Wie funktioniert Signaturee? | **Repositories → signaturee-win** (Windows) oder **signaturee-linux** (experimenteller Stand) |
| Was gibt es zum CKA-Lab? | **Repositories → cka-lab** |
| Wie funktioniert der Anthias-Hub? | **Repositories → anthias-hub** |
| Aus welchem Git-Stand stammt diese Seite? | **Sources → Index** (Quell-Commit je Repository) |

Die linke Navigation zeigt importierte Markdown-Dateien nach ihrem ursprünglichen Repository. Die **Suche** hilft mit Dienstnamen, zum Beispiel `Proxmox`, `NAS`, `NetBird`, `Talos` oder `Signaturee`. Ein Suchtreffer ist noch kein Beleg, dass die beschriebene Maschine gerade so läuft.

## Wie aktuell ist das?

- Der private Build liest die **konfigurierten Quellen** bei jeder erfolgreichen Erstellung als frische Git-Snapshots. Für den regulären Publisher ist ein nächtlicher Lauf um **23:45 Uhr (Europe/Berlin)** vorgesehen.
- Unter **Sources → Index** steht der *genaue Quell-Commit*. Das ist der Stand der **Datei**, **nicht** das Datum einer überprüften Maschine oder eines erfolgreichen Restore-Tests.
- Eine fehlende Seite kann an der **Quellenauswahl** liegen; eine angezeigte Seite kann trotzdem **inhaltlich veraltet** sein. Beides muss separat geprüft werden.
- Ein Build- oder Deploy-Fehler kann dazu führen, dass das Portal weiterhin die vorherige erfolgreiche Fassung zeigt.

## Wenn etwas fehlt oder falsch ist

1. Prüfen, **welches Repository** die Informationen besitzt (z. B. `infra-configs` für Host-Betrieb, `homelab-talos` für die Cluster-Implementierung).
2. Fehlende oder falsche Betriebsinformationen **im Quell-Repository** korrigieren — mit überprüftem Sachstand, Datum und möglichst konkretem Prüfergebnis.
3. Falls die Datei im Quell-Repository existiert, aber hier fehlt: die **Import-Auswahl** in `bytegeist-docs/docs-sources.yml` überprüfen. Nicht blind alle Pfade importieren.
4. Nach dem nächsten erfolgreichen privaten Build die **Quellrevision und den Seiteninhalt** erneut prüfen.

**Bekannte Grenze (02.11.2026):** Bei `infra-configs` importiert die aktuelle Konfiguration nur `README.md` und `docs/`. Wertvolle Runbooks unter `hosts/`, `vps/`, `kubernetes/` und `shared/` werden noch nicht direkt ins Portal übernommen; einige Verweise führen deshalb auf die GitHub-Quelle. `homelab-talos` ist bis zur ausdrücklich genehmigten Quell-Leseberechtigung noch nicht aufgenommen. Diese Lücken werden in **BYT-107 / BYT-106** bearbeitet, nicht verschwiegen.

## Die wichtigste Regel

**Quell-Commit ≠ Live-Status ≠ getestete Wiederherstellung.** Lieber eine sichtbar offene Frage als eine elegant gerenderte, aber falsche Anleitung.

Technische Import-/CI-/Deployment-Erklärung und Aufnahme neuer Repositories: siehe README des öffentlichen `bytegeist-docs`-Projekts. Private Inhalte und Zugangsdaten gehören weder in öffentliche PRs noch in CI-Artefakte.
