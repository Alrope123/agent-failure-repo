# Create and inspect submissions locally

Updated 2026-10-10.

## Summary

Run these commands from the repository root with Python 3.9 or newer. No
packages, model access, or network connection are required.

```bash
python3 commands/new_problem.py forgotten-config-rule
python3 commands/validate.py problems/forgotten-config-rule
python3 commands/validate.py --submission problems/forgotten-config-rule
make check
```

The scaffolder accepts words in small letters separated by hyphens, creates a new
directory under `problems/`, and refuses an existing destination. It does not
read any conversation history.

The validator checks the forms, required package directories, referenced local
evidence, and basic consistency between declared status and result records.
Without a path it checks all problems and result records. `--submission` also
requires the owner's `privacy_reviewed` declaration. That flag is a declaration,
not an automated privacy audit. Re-review changed files before sharing.

## Limitations

The validator never executes the commands stored in a problem manifest. A pass
does not mean a reproduction works, an incident is real, a causal claim is
supported, or the files are safe to publish. Reviewers make those judgments.

`make check` additionally runs the collection tool tests, the trusted
synthetic teaching example, and the skill bundle consistency check. It does
not run contributed tasks or model calls.

## Install or maintain the skill

Follow [the installation guide](../docs/INSTALL.md) to install the complete
skill for Codex, Claude Code, or another compatible agent:

```bash
python3 commands/install_skill.py --agent codex --dry-run
python3 commands/install_skill.py --agent codex
```

Use `--agent claude` for Claude Code, or `--dest` for an exact custom skill
directory. Existing destinations are never overwritten.

Maintainers edit the canonical guides, templates, and collection commands in
this repository, then rebuild the bundled copy:

```bash
python3 commands/build_skill.py
python3 commands/build_skill.py --check
```

The builder copies an explicit allowlist plus the templates. It excludes
collected problems, results, and private histories. The check writes nothing
and detects missing, changed, or extra bundle files. Commit regenerated assets
with their source changes so the installed skill works independently.

## Sources

Implementations: [new_problem.py](new_problem.py) and [validate.py](validate.py).
