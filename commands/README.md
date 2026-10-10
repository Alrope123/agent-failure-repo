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

`make check` additionally runs the collection tool tests and the trusted
synthetic teaching example. It does not run contributed tasks or model calls.

## Sources

Implementations: [new_problem.py](new_problem.py) and [validate.py](validate.py).
