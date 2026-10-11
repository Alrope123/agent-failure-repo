# Collect as many real failures as your history supports

Updated 2026-10-10.

## Summary

Ask your agent to search the full history you authorize and collect every distinct credible failure it can find. Use [all 20 symptoms](docs/SYMPTOMS.md) as a search checklist, while retaining other modes too. There is no quota or limit, and finding one example does not finish the search. Incident reports are welcome when a runnable reproduction is not yet feasible.

Start with **historical Claude Code and Codex runs** for your selected project.
The collecting agent checks both tools' transcript stores and reports coverage
separately. The current conversation adds context. See [how histories are found
and read](docs/HISTORY.md).

## Choose how far to take your contribution

| Contribution | What it contains | What it supports |
|---|---|---|
| Incident only | A sanitized account and available evidence | This incident occurred; the proposed cause may be uncertain |
| Packaged reproduction | A reduced environment, tasks, commands, and checks | Others can attempt the task; a model failure is not yet established |
| Model reproduced | Fresh model attempts with complete run records | The intended failure occurred again in the reduced task |
| Temporal evidence supported | Matched attempts that vary the relevant history | Evidence that the earlier work or boundary affects the failure |

These are evidence levels, not a promise that every incident must reach the last one. A single fresh failure does not establish a general failure rate or a cause. A scripted replay or an intentionally broken implementation cannot satisfy the model reproduction level.

## Give your agent a clear scope

Point your agent to [AGENTS.md](AGENTS.md) and name the histories it may inspect. For example:

> Read this repository's AGENTS.md and docs/SYMPTOMS.md. You may inspect the conversation exports I selected and the accompanying project copies. Search the entire authorized scope in multiple passes for all 20 symptoms and any unmatched failure modes. Collect as many distinct credible incidents as you can; do not stop after a few examples or one per class. Inventory every candidate and document coverage and gaps. Build a minimal reproduction for every feasible credible incident; record the reason and next action for anything deferred. Keep raw material private and show me the exact sanitized contribution before uploading anything.

If the agent cannot access your old conversations, give it a selected export or describe an incident. Do not give it broad access to your accounts simply to fill in missing details.

## Prepare the contribution

1. Copy the [collection report](templates/collection-report.md) and [incident index](templates/incident-index.csv) into private working storage. Inventory the authorized sources, then follow [the multi-pass search guide](docs/FINDING_FAILURES.md).
2. Add every candidate to the index with evidence, symptom labels or an unmatched mode, and its disposition. Deduplicate the same event appearing in multiple records; keep different incidents within the same symptom class.
3. Create a directory for each credible distinct contribution with `python3 commands/new_problem.py <slug>`. Use a descriptive name such as `lost-fixture-after-handoff`. Fill in the account, temporal connection, consequence, and available evidence.
4. Build a task for every feasible incident using [the reproduction guide](docs/REPRODUCING.md). If a reproduction or model evaluation is not feasible, keep the incident report and state what is missing and the next action.
5. Put sanitized run summaries and evidence under `results/<slug>/<run-id>/`. Include every attempted run and its condition, even when the model avoids the failure or the setup breaks.
6. Reconcile the index, all symptom searches, completed packages, and deferred work. Run `python3 commands/validate.py` and perform the [owner review](docs/REVIEW.md). Validation checks structure; reviewers still need to inspect scope coverage, tasks, and evidence.
7. Hand the reviewed collection report, index, and packages to the contributor locally. If a shared remote is later available and submission is authorized, use a pull request. State the main limitation and the help needed for each unfinished incident. Do not present a shortlist as the complete collection.

## Keep the parts separate

| Location | What belongs there |
|---|---|
| `docs/` | Shared contributor instructions and methodology |
| `problems/<slug>/` | One incident and its reproducible task package |
| `results/<slug>/<run-id>/` | Sanitized evidence from one attempt |
| `commands/` | Shared repository tools |
| `templates/` | Starter files copied for a contribution |
| `examples/` | Explicitly labeled teaching examples |
| `.local/` | Ignored, private working material that must not be committed |

Keep hidden checks and reference solutions out of the tested agent's workspace. Expose only the current stage's intended messages and files; keep future prompts and the orchestration schedule outside that workspace. Preserve each original run record when adding a later evaluation; explain any changed interpretation rather than replacing the old evidence.

## Before you share

Only share material you are entitled to contribute. Remove secrets, private code, personal details, and other people's messages that you do not have permission to share. Describe any sanitization that changes the task. Review the actual files and staged changes; an ignored directory or a secret scanner is not a guarantee that a package is safe to publish.

Source: [Agent instructions](AGENTS.md), [reproduction requirements](docs/REPRODUCING.md), and [review checklist](docs/REVIEW.md).
