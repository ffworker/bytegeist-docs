# Bytegeist Documentation

Public-safe documentation for Bytegeist architecture, development, CI/CD, and documentation ownership.

This output is intentionally built only from `docs/public/`. It does not retrieve or include private repository documentation, infrastructure internals, credentials, or private host details.

## Public boundary

```text
docs/public/
  -> public-safe MkDocs build
  -> optional public Pages deployment
```

The full private documentation build is a separate GitHub Actions artifact and is never used as public Pages input.
