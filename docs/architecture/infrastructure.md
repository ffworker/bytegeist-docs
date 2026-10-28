# Infrastructure

`infra-configs` is the infrastructure desired-state and operational-knowledge
monorepo. `homelab-talos` owns the current production Talos cluster deployment
source; `infra-configs` owns the surrounding inventory, operations, and
recovery knowledge. Infrastructure changes use Linear for work tracking,
GitHub for reviewed implementation history, and approval-gated deployment.

Exact host identities and addresses remain in the private infrastructure
records. Retired infrastructure material is not part of the current production
documentation surface.
