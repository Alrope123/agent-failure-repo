# Long-Horizon Agent Failures

> Turn real agent failures from long-running work into small reproducible tasks.

<!-- One paragraph: what this is, who it's for, and the single most important
     thing a newcomer must understand before touching it. Keep it current. -->

## Quickstart

```bash
# document the one command that proves the project runs
make check
```

## Repository map

| Path | What it is |
|---|---|
| [`PROJECT.md`](PROJECT.md) | **Read first.** Manifest — what this is, where everything lives, status |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | How the pieces fit and why |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Decision log (ADRs) — *why* it's built this way |
| [`CHANGELOG.md`](CHANGELOG.md) | Notable changes, newest first |
| `src/` | Source |
| `tests/` | Tests |

## Documentation

Docs are treated as part of the code, not an afterthought:

- **[PROJECT.md](PROJECT.md)** — the manifest and join point (start here)
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — design and data flow
- **[docs/DECISIONS.md](docs/DECISIONS.md)** — why each non-obvious choice was made
- **[CHANGELOG.md](CHANGELOG.md)** — what changed and when

## Development

Run the hygiene check before every commit (CI runs the same thing):

```bash
make check
```

## License

Add a `LICENSE` file (or state the license here). Unlicensed/private until then.
