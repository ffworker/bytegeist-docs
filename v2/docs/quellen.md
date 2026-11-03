# Projekte und Quellen

<div class="bg-eyebrow">INTERN / QUELLENVERWALTUNG</div>

Hier sammle ich die Dokumentation, die ich beim Betrieb meiner Systeme tatsächlich brauche. Die Projektnavigation entsteht aus meiner privaten Quellenauswahl, nicht aus einer automatischen Spiegelung des gesamten GitHub-Kontos.

## Quellen hinzufügen oder ändern

1. In der lokalen, **nicht eingecheckten** Datei `v2/sources.private.yml` ein gewünschtes Repository auswählen.
2. Für jedes Projekt `README.md`, `docs/` oder beides festlegen.
3. Den Collector `v2/scripts/curate.py` ausführen und Zensical mit `.generated/mkdocs.yml` bauen.
4. Suchfunktion, Links und Quellstand prüfen, danach erst die private statische Website aktualisieren.

**Wichtig:** Ohne private Quellenauswahl enthält die Site nur die Grundseiten dieses Projekts. Es werden keine privaten Repositories automatisch abgerufen.

## Inhaltspflege

Falsche oder veraltete Informationen im **ursprünglichen Repository** korrigieren. Eine gerenderte Kopie wird nicht zur zweiten Quelle der Wahrheit. Der Collector dokumentiert für die ausgewählten Quellen Git-SHA und Abrufzeit im generierten Quellstand.

Neue Quellen brauchen eine bewusste Freigabe. Besonders bei internen Betriebsdaten vor der Aufnahme prüfen, ob sie für diese private Instanz bestimmt sind.
