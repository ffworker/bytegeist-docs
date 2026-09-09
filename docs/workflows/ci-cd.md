# CI/CD

PR and trusted source-change validation run `mkdocs build --strict` without
persisting generated documentation. Untrusted pull requests build only the
safe documentation committed in this public repository.

Trusted workflows retrieve the latest default branches from the declared source
repositories and build the full private documentation transiently.

At **23:45 Europe/Berlin**, the nightly workflow rebuilds the full documentation
from current sources for the private `docs.lab.bytegeist.info` runtime. It also
supports `workflow_dispatch`. No private build is uploaded as a GitHub Actions artifact, committed, published to GitHub Pages, or put in a public image. The only persisted copy is the private runtime's static site after authenticated deployment.
