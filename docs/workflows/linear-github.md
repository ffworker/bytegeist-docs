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
