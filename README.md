# Bytegeist Docs

[![Zensical v2 offline preview CI](https://github.com/ffworker/bytegeist-docs/actions/workflows/v2-preview.yml/badge.svg)](https://github.com/ffworker/bytegeist-docs/actions/workflows/v2-preview.yml)

> **V2 / im Neuaufbau (02.11.2026):** Die alte MkDocs-Veröffentlichung auf VPS02 ist bewusst als Architektur aufgegeben worden. Bytegeist Docs wird mit **Zensical** neu aufgebaut – opt-in, klein und mit einem Design, das ich wirklich benutzen möchte. Ein lokal getesteter Zensical-Build ist **kein** Nachweis einer bereits laufenden privaten Website.

## Der eigentliche Bedarf

Ich habe Dokumentation an vielen Orten: bei den Projekten, in READMEs und in `docs/`. Ich möchte nichts doppelt pflegen. Ich möchte eine **private, durchsuchbare Leseansicht nur der Quellen, die heute wichtig sind**.

Was mir v1 gezeigt hat: viele erfolgreich importierte Seiten und ein grüner Build machen ein Handbuch noch nicht nützlich. Die Geschichte und die zweite Erkenntnis stehen im [Bytegeist-Blog](https://blog.bytegeist.dev/artikel/bytegeist-docs/).

## Stand von v2

- **Renderer:** [Zensical](https://zensical.org/) aus dem Team hinter Material for MkDocs, mit modernem Theme und eigenen Bytegeist-Styles.
- **Quellen:** standardmäßig **keine**. Der Operator wählt jedes Repository explizit mit `README.md` und/oder `docs/` aus – keine automatische GitHub-Konto-Spiegelung.
- **Technik:** `v2/scripts/curate.py` erzeugt bei ausdrücklicher Auswahl neue Quell-Snapshots und ein kurzlebiges Zensical-Build-Verzeichnis. Quell-Commit und Abrufzeit sind dokumentiert, nicht als Live-Monitoring ausgegeben.
- **Sicherheit:** `v2/sources.private.yml` und generierte private HTML-Dateien werden nicht committet. CI testet nur synthetische, nicht private Daten.
- **Tests:** `v2-preview.yml` prüft die Oberfläche und den Source-Collector vollständig offline. Versionsgebundene Toolchain siehe `v2/requirements.txt`.
- **Deployment:** **noch keines**. Zukünftiges Hosting soll **nicht auf VPS02** erfolgen. NetBird-ACL, Offline-Recovery und tatsächliche Live-Abnahme sind noch offen.

## Lokal ansehen

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r v2/requirements.txt
cd v2
zensical serve
```

Das zeigt zunächst ausschließlich synthetische Seiten. **[Vollständige Anleitung und opt-in Quellenwahl](v2/README.md)**.

## Pflege der Originaldokumente

Die Quelle bleibt immer beim jeweiligen Projekt. Eine falsche Anleitung wird **im Projekt-Repository** korrigiert, nicht durch automatische KI-Änderungen am Portal. Ein Git-SHA ist kein Betriebszustandsnachweis.

## Historie und sicherer Rückbau

Die alte v1-Version bewies, dass frische Git-Imports und ein privater statischer Reader funktionieren können. Ich habe sie später bewusst verworfen, weil sie zu viel sammelte, der Workflow nicht gut passte und das Deployment an VPS02 gebunden war. Die v1-CI- und CD-Workflows sind **stillgelegt**; alte technische Dateien bleiben noch als nachvollziehbare Geschichte im Repository.

- [V1 README / ursprüngliche Architektur](legacy/README-v1.md)
- [VPS02-Rückbauplan — noch **nicht ausgeführt**](v1-retirement.md)
- [Private Repo-Auswahl und Source-Review](https://linear.app/bytegeist/issue/BYT-109)
- [Privates Hosting und saubere VPS02-Stilllegung](https://linear.app/bytegeist/issue/BYT-110)

**Keine private Quellliste oder gerenderten Inhalte in öffentliche PRs, Builds oder Artefakte übernehmen.**
