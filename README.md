# Bytegeist Docs

> **Neuaufbau (02.11.2026):** Bytegeist Docs v2 wird bewusst **neu mit Zensical** aufgebaut, mit wenigen vom Betreiber ausgewählten Quellen statt einer Vollsammlung. Diese README dokumentiert vor allem die **historische v1-Implementierung**. Der neue [lokale Zensical-Prototyp](v2/README.md) ist noch kein produktiv erreichbares System. Eine Stilllegung von VPS02-Diensten erfolgt erst nach getrennter Betriebsprüfung. [BYT-108](https://linear.app/bytegeist/issue/BYT-108).


[![Documentation CI](https://github.com/ffworker/bytegeist-docs/actions/workflows/ci.yml/badge.svg)](https://github.com/ffworker/bytegeist-docs/actions/workflows/ci.yml)
[![Nightly private documentation CD](https://github.com/ffworker/bytegeist-docs/actions/workflows/nightly.yml/badge.svg)](https://github.com/ffworker/bytegeist-docs/actions/workflows/nightly.yml)

This public repository demonstrates distributed documentation ownership and
safe aggregation. Application, infrastructure, and learning repositories keep
their own canonical README/docs content. Trusted automation retrieves selected
paths, validates the complete documentation universe, and builds a private
static site without committing or publicly storing imported content.

```text
source README/docs
  -> change-triggered aggregate validation
  -> 23:45 Europe/Berlin frozen build
  -> private deployment target: docs.lab.bytegeist.info
```

The public showcase is this repository and its workflows—not a public rendered
documentation website. GitHub Pages is not used. Full builds run only in trusted
workflow contexts with the approved read credential; untrusted fork PRs build
only the safe documentation committed here and never receive private access.

## Warum ich das gebaut habe

Meine Homelab- und Projekt-Dokumentation war auf viele Repositories verteilt.
Ich wollte weder ein zweites zentral gepflegtes Handbuch noch ständig Seiten
an mehreren Stellen aktualisieren. Das Prinzip lautet deshalb:

1. **Eine Quelle pro System:** README und docs/ gehören zum jeweiligen Repo.
2. **Ein privates Lesefenster:** Bytegeist Docs holt freigegebene Quellen und
   baut daraus eine gemeinsame, durchsuchbare MkDocs-Seite.
3. **Keine zweite manuelle Kopie:** Neue Änderungen werden beim nächsten
   validierten Build erneut aus den Quell-Repositories gelesen.
4. **Private Auslieferung:** Das Portal wird über die bestehende NetBird-
   Anbindung auf dem privaten Host bereitgestellt; nicht öffentlich via Pages.

## Neue Repos und Quellenänderungen

Das öffentliche `docs-sources.yml` ist die **explizite Quellenliste**. Sie
erfasst nicht automatisch jedes Repository eines GitHub-Accounts – das wäre
gerade bei privaten Quellen eine unnötig riskante Überraschung. Neue Quellen
werden mit einem überprüfbaren Eintrag aufgenommen:

```yaml
repositories:
  neuer-dienst:
    repo: ffworker/neuer-dienst
```

Ohne `paths` verwendet der Importer automatisch `README.md` und `docs/`,
sofern vorhanden; mindestens eine Markdown-Seite muss existieren. Für
Spezialpfade kann eine explizite `paths`-Liste gesetzt werden, die dann **streng**
validiert wird. Eine Umbenennung benötigt nur eine Manifest-Anpassung. Nicht
mehr benötigte Repos werden durch Entfernen des Eintrags beim nächsten
sauberen Build aus der erzeugten Website entfernt.

```sh
python scripts/import_docs.py --list-sources
python scripts/import_docs.py --clean   # Zugriff auf freigegebene Repos notwendig
mkdocs build --strict -f .generated-mkdocs.yml -d site
```

Bei jedem privaten Vollbuild werden alle aufgenommenen Repos **frisch und flach
auf ihrer aktuellen Default-Branch** geklont. Ein vorhandener Import-Cache
gilt nicht als Nachweis für aktuelle Dokumentation. Die private Seite enthält
eine Übersicht mit dem genauen Quellcommit jeder importierten Version.
Relative Links zwischen tatsächlich importierten Seiten bleiben innerhalb des
Portals; Links zu nicht importierten Dateien zeigen auf einen **festen Commit**
statt auf einen schwebenden `main`-Stand.

Der Ausführungskontext benötigt Leseberechtigung auf **jede** konfigurierte
private Quelle. Fehlt eine Berechtigung, eine Seite oder der vollständige
MkDocs-Build, wird **nicht** die neue Version veröffentlicht. Keine importierten
privaten Inhalte, Git-Tokens, erzeugten HTML-Seiten oder SSH-Schlüssel gehören
ins öffentliche Repository oder in CI-Artefakte. Die Quellen sind trotzdem
vertrauenswürdig zu halten: Der Import ist kein perfekter Secret-Scanner.
Die Portal-Berechtigung über NetBird wird separat administriert und muss
am echten privaten Endpunkt überprüft werden.

Der Parameter `--local-repos-dir` ist nur für bewusst lokale Offline-Tests:
bestehende lokale Checkouts werden **niemals verändert**, können aber älter
sein als die Remote-Repositories.

---

## Bekannte Quellenlücke (02.11.2026)

Der neue private Vollbuild konnte elf Quellen erfolgreich importieren, stoppte
jedoch an `ffworker/homelab-talos`: Das bestehende `DOCS_REPO_TOKEN` kann
dieses Repository nicht lesen (GitHub meldet `Could not resolve to a Repository`).
Die Quelle bleibt deshalb vorerst **bewusst außerhalb der aktiven Liste**.
Sie darf nach gezielter Leseberechtigung im GitHub Actions Secret
`DOCS_REPO_TOKEN` wieder aufgenommen werden. Kein pauschaler Token, keine
stillschweigende unvollständige Veröffentlichung. Das gleiche gilt für
weitere private Repos: erst Token-Leserechte nachweisen, dann einschreiben.

## Ownership

- Application technical docs: the owning application repository.
- Infrastructure operational docs: `infra-configs`.
- Learning, labs, and QA: `cka-lab`.
- Global workflow and cross-repository orchestration: this repository.
- Work/status: Linear; implementation, PRs, CI/CD, and history: GitHub.
- Forgejo: mirror/recovery only.

See [`docs-sources.yml`](docs-sources.yml) for the public manifest of source
repositories and imported paths. Imported contents are generated build inputs,
not editable copies.

## Operations

Optional source-notification workflows notify `ffworker/bytegeist-docs` with a narrow
`repository_dispatch` event after documentation paths change on `main`. Only sources that use push-triggered notification need a secret named `DOCS_DISPATCH_TOKEN` containing a
fine-grained token limited to `ffworker/bytegeist-docs` with only Contents:
Read and write permission (used for the dispatch endpoint). The token must not
be included in event payloads.

The full private build uses `DOCS_REPO_TOKEN` only in trusted workflows. It is
never used by pull-request builds and never uploaded as an Actions artifact.
Static documentation replacement is the only permitted automatic deployment
exception; changes to cluster infrastructure, ingress, DNS, authentication,
networking, storage, or secrets remain approval-gated.

The nightly/manual workflow connects to the existing private NetBird network, transfers the generated site over pinned-key SSH, atomically replaces `/opt/bytegeist-docs/site` on VPS02, and verifies the private HTTPS endpoint. This is the narrow static-content deployment exception; infrastructure changes remain approval-gated.
