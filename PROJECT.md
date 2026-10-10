# Long-Horizon Agent Failures — project manifest

| Field | Value |
| --- | --- |
| Purpose | Collect real incidents and small reproductions of failures during long-running agent work. |
| Codebase | This repository |
| Git remote | Local only, as requested on 2026-10-10 |
| Language / runtime | Python 3.9 or newer; standard library only |
| Entrypoints | `commands/new_problem.py`, `commands/validate.py`, `make check` |
| Docs | `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/` |
| Status | active |

## Code ↔ bookkeeping ↔ external

| Material | Location |
| --- | --- |
| Instructions and decisions | `docs/` |
| Task packages | `problems/` |
| Reviewed evaluation records | `results/` |
| Private source material | Contributor-controlled storage, or ignored `.local/` |
| Current evidence | No contributed incidents or model evaluations yet |
| External services | None required by the repository tools |

The synthetic example verifies mechanics only. Contributed task code is
untrusted: inspect it and use a disposable, credential-free sandbox when
running an agent or judge. Repository validation never executes task commands.
