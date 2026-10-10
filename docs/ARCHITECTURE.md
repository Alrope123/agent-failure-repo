# From a private incident to a reproducible task

Updated 2026-10-10.

## Summary

The repository is a collection kit. A contributor's agent investigates selected
history, writes a small task, and prepares evidence for the contributor to review.
Reviewers judge what that evidence supports. There is no background history
collector and no automatic model service.

## Flow

1. Read the owner's selected history into private working notes.
2. Record the earlier requirement, later error, consequence, and uncertainty.
3. Reduce the incident into a task under `problems/`.
4. Check the setup, a correct solution, and an intentionally faulty solution.
5. If authorized, run fresh agents and save every attempt under `results/`.
6. Have the owner review the exact sanitized files before sharing them.

## Package boundaries

`docs/` explains the method. `problems/<id>/` contains the task, environment,
checks, and reference solution. `results/<id>/<run-id>/` contains one attempt's
record and reviewed evidence. `commands/` contains collection tools; each task
documents its own setup and evaluation commands in its manifest.

Inside a problem, `task/` stores ordered prompts and `environment/` stores
initial files. Present only the current stage's permitted prompt and files;
future prompts, reset schedules, and simulated teammate instructions stay
outside the evaluated workspace. Do not copy the whole task directory into it. `checks/`, `reference/`, the incident description, and result
records are reviewer material. Stage a separate workspace. Use a sandbox that
also limits tool access; copying files alone does not provide that isolation.

The example lives separately so synthetic teaching material cannot be mistaken
for a contributed real incident. Private notes live outside Git, preferably in
contributor-controlled storage; `.local/` is also ignored.

## Tool behavior and limitations

The scaffolder copies a template into a new problem directory and refuses to
overwrite an existing one. The validator reads metadata and evidence paths.
It does not run commands from manifests, import submitted implementations,
contact model providers, or certify scientific claims or privacy.

`make check` also runs this repository's trusted unit tests and synthetic
example. Review code before running a modified copy from a contributor.

## Sources

The contributor workflow is defined in [AGENTS.md](../AGENTS.md). Tool behavior
is implemented in [the scaffolder](../commands/new_problem.py) and
[the validator](../commands/validate.py).
