# Bytegeist Documentation Automation

This public repository demonstrates how documentation owned by multiple
repositories is continuously validated and frozen for private delivery.

```text
source README/docs
  -> trusted retrieval
  -> strict validation during the day
  -> 23:45 Europe/Berlin frozen build
  -> private documentation runtime
```

The rendered documentation product is private. This public repository contains
only safe workflow/orchestration documentation, a source manifest, and build
 tooling. Imported repository contents and generated site output are transient
workflow data only.

- Linear is the canonical work system.
- GitHub is the implementation, PR, CI, and CD platform.
- Forgejo is mirror/recovery only.
- Hermes/Larry orchestrates without replacing those systems.
