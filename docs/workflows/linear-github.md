# Linear to GitHub

The permanent work workflow is:

```text
Dennis
  ↓
Hermes / Larry
  ↓
Linear issue
  ↓
triage
  ↓
implementation required?
  ├── no → work/result remains in Linear
  └── yes
       ↓
   select canonical repo
       ↓
   Linear-ID branch
       ↓
   implementation
       ↓
   GitHub PR
       ↓
   CI
       ↓
   review / approval
       ↓
   merge
       ↓
   CD according to repository policy
       ↓
   verification
       ↓
   Linear Done
```

Linear is the only normal task queue. Do not duplicate normal Linear tickets as GitHub Issues. Merge is not automatically Done; Done requires the relevant verification.

## Issue Collector

Explicit capture intents such as `capture:`, `issue:`, `add to linear:`, `remember for later:`, and `go to linear triage:` create one Linear issue per clearly separate thought in the Bytegeist team's `Backlog` state. Preserve the raw wording, add a concise title and minimal context, and assign no priority or repository unless Dennis says so. Capture acknowledges the thought and stops; it does not investigate, implement, delegate, branch, or create a GitHub Issue.
