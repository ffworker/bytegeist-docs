# Was ist wirklich bestätigt?

<div class="bg-eyebrow">DOKUMENTATION / EVIDENZ</div>

Eine optisch schöne Anleitung kann trotzdem falsch oder veraltet sein. Deshalb sollen ihre Aussagen nicht mehr versprechen, als wir geprüft haben.

| Information | Was sie beweist | Was sie nicht beweist |
| --- | --- | --- |
| Git-Commit | Welcher Text aus dem Repo stammt | Ob die Maschine noch so läuft |
| Abrufdatum | Wann die Quelle zuletzt abgeholt wurde | Ob die Anleitung inhaltlich richtig ist |
| Erfolgreicher Site-Build | Dokumentation konnte verarbeitet werden | Ob Backup, SSH oder NFS funktionieren |
| Datiertes, beobachtetes Ergebnis | Was beim konkreten Test tatsächlich sichtbar war | Dauerhafte Gesundheit aller Systeme |
| Isolierter Restore-Test | Der dokumentierte Wiederherstellungsfall wurde getestet | Dass jeder andere Ausfall beherrschbar ist |

!!! warning "Lieber unbekannt als erfunden"
    Wenn kein aktueller Live-Test vorliegt, steht dort **nicht geprüft**. Eine im Repo gelesene Behauptung darf keinen künstlichen grünen Status bekommen.

## Verfügbarkeit bei einem echten Ausfall

Das neue Docs-Hosting soll **nicht auf VPS02** laufen. Für einen Kubernetes-Ausfall muss es trotzdem einen einfachen lokalen/offline Zugriff auf die wichtigsten Runbooks geben. Der konkrete Zielhost wird erst nach einem Vergleich zwischen privatem Talos-Ingress und einem unabhängigen, stets laufenden Host gewählt.
