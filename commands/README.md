# Start a collection and inspect its packages locally

Updated 2026-10-10.

## Summary

Give your agent the launch message in the repository readme to run the full
collection. The commands below support that workflow with Python
3.9 or newer and no third-party dependencies.

Source: [Repository entrypoint](../README.md).

## Start or resume

From the kit root:

```bash
python3 commands/start.py
```

This creates `.local/collection/` and prints its absolute path, next agent
action, index, coverage report, and final `REPORT.md` destination. Repeating it
resumes a recognized workspace without rewriting evidence. To select another
new directory whose parent exists:

```bash
python3 commands/start.py --output /path/to/collection
```

Existing folders not created by this command are refused. To continue
an older collection created another way, open its existing instructions and
ledgers directly.

Setup never scans history, runs a model, uploads data, or writes a completed
report. The agent must continue the collection workflow after setup, using the
user's authorized history and the printed workspace. It must preserve the
original target project when changing directories.

## Work inside the collection

Change to the printed workspace before creating or checking submissions.
For the default workspace, from the kit root:

```bash
cd .local/collection
python3 commands/new_problem.py forgotten-config-rule
python3 commands/validate.py problems/forgotten-config-rule
python3 commands/validate.py --submission problems/forgotten-config-rule
```

The scaffolder creates a new problem directory and refuses an existing one.
The validator checks forms, package directories, evidence paths, and basic
consistency between declared status and run records. Without a path it checks
all real-history problems and result records in the collection.

## Limitations

`--submission` requires the owner's `privacy_reviewed` declaration. That flag
is a declaration, not an automated privacy audit. Re-review changed files
before sharing. Validation never executes commands from a problem manifest.
A pass cannot establish that an incident is real, a reproduction works, a
causal claim is supported, or files are safe to publish.

## Optional skill installation

Run from the kit root, following [the installation guide](../docs/INSTALL.md):

```bash
python3 commands/install_skill.py --agent codex --dry-run
python3 commands/install_skill.py --agent codex
```

Use `--agent claude` for Claude Code, or `--dest` for an exact custom skill
directory. Existing destinations are never overwritten. Installation is
unnecessary for the direct collection workflow.

## Maintain and test the kit

Edit canonical guides, templates, and commands in the kit repository, then:

```bash
python3 commands/build_skill.py
make check
```

The builder copies an explicit allowlist plus templates into the standalone
skill. Collected problems, results, and private histories are excluded.
`python3 commands/build_skill.py --check` detects missing, changed, or extra
bundle files without writing anything. Commit generated assets with source
changes so installed copies remain usable independently.

`make check` runs metadata checks, tool tests, the trusted synthetic teaching
example, and bundle consistency checks. Run it from the kit root, not the
collection workspace. It does not run contributed tasks or model calls.

## Sources

Implementations: [start.py](start.py), [new_problem.py](new_problem.py),
[validate.py](validate.py), [install_skill.py](install_skill.py), and
[build_skill.py](build_skill.py).
