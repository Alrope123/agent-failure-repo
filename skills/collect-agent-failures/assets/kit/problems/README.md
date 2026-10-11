# One problem directory per incident

Create a package with `python3 commands/new_problem.py your-short-name`.
Start with the incident description and evidence; fill in runnable components
when available. Do not fabricate a task or successful reproduction to fill a form.

Each package contains:

```text
your-short-name/
  README.md        # incident, meaning, horizon, reduction, limits
  problem.json     # small machine-readable record and commands
  task/            # ordered messages and handoff instructions for the agent
  environment/     # initial files and local fixtures
  checks/          # reviewer-owned checks and outcome definitions
  reference/       # one correct solution and, optionally, a known bad fixture
```

The evaluated agent must not receive the reviewer files. Document exactly
which files and messages it receives at each stage, what persists, and how
sessions or compaction are handled. Follow [the reproduction guide](../docs/REPRODUCING.md).

No real incidents have been added to this starter.
