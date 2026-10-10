# long-horizon-agent-failures — project manifest

<!-- This is the FIRST file a fresh agent or teammate reads. It is the single
     join point between the code, its documentation, and wherever it runs.
     Keep the table true: when anything below moves, update it here. -->

| Field | Value |
|---|---|
| Purpose | Turn real agent failures from long-running work into small reproducible tasks. |
| Codebase | `.` (this repo) |
| Git remote | `local-only` |
| Language / runtime | generic |
| Entrypoints | `src/`, `Makefile` |
| Docs | `README.md`, `docs/ARCHITECTURE.md`, `docs/DECISIONS.md` |
| Status | active |

## Code ↔ bookkeeping ↔ external

<!-- Fill in the rows that apply. Delete the ones that don't. The point is that
     from THIS file a newcomer can reach every other surface of the project. -->

| | Path |
|---|---|
| Code (this repo) | `.` |
| Bookkeeping / plan | _(link to plan / tracker / tasks doc, or "none")_ |
| Artifacts / data | _(where large outputs live — NOT in this repo)_ |
| Reports | _(link, or "none")_ |

## What a newcomer must know

<!-- 1–3 lines of the non-obvious: invariants, gotchas, "never touch X",
     the one command that proves it runs. This is where you save the next
     person an hour. -->

- The one command that proves it runs: `make check`.
