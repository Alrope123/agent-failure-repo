# What contributors should push

Updated 2026-10-10.

## Summary

Submit a reviewed collection summary, every shareable credible incident, its
minimal reproduction when feasible, and records of every evaluation actually
attempted. Include enough sanitized evidence for another person to assess the
claim. Collect broadly across historical Claude Code and Codex runs and all
20 symptoms; keep new modes too. There is no quota or one-per-symptom limit.

Prepare this material locally before requesting the owner's review. An
incident-only contribution is useful when code or evaluation is unavailable.
State the achieved evidence level and missing work honestly.

## Files to include

Choose a unique collection ID and descriptive problem IDs without personal
identifiers. Paths below are relative to the destination repository.

| Path | What to include | When required |
| --- | --- | --- |
| `docs/collections/<collection-id>/README.md` | Collection summary, findings, package links, limits, and next actions. | Every submission. |
| `docs/collections/<collection-id>/incidents.csv` | Sanitized candidate index, including uncertain, duplicate, rejected, and deferred entries. | Every submission. |
| `docs/collections/<collection-id>/coverage.md` | Separate Claude Code and Codex coverage, all symptom searches, and unread or inaccessible ranges. | Every submission. |
| `problems/<id>/README.md` and `problem.json` | The original incident, its meaning and horizon, the intended error, evidence level, and runnable commands. | Every shared incident. |
| `problems/<id>/evidence/` | Reviewed excerpts, tool calls/results, relevant diffs, checks, and redaction notes. | When supporting material can be shared. |
| `problems/<id>/task/`, `environment/`, `checks/`, `reference/` | Ordered prompts, minimal starting files, evaluators, and a correct solution. | Runnable content for packaged reproductions; explanatory files for incident-only reports. |
| `results/<id>/<run-id>/summary.json` and supporting files | Actual attempt settings, outcomes, commands, and sanitized evidence. | Every attempt that was made. |

Source: [problem layout](../problems/README.md), [result format](../results/README.md),
and [contribution levels](../CONTRIBUTING.md).

Use reviewed derivatives of the private index and coverage report. Replace
machine paths and sensitive identifiers with consistent source aliases; make
every shared link resolve to a shared file. Account for withheld incidents
with neutral labels and reasons where shareable. If even a count is sensitive,
state that the public inventory is incomplete and why. Keep the complete
private ledger; never quietly drop candidates or count withheld records as
reviewed evidence available to the reader.

For each incident, answer explicitly:

1. **What happened?** The user's task, expected behavior, observed action, and
   concrete consequence, supported by the original record where available.
2. **Was the horizon long?** The earlier event, intervening work, later decision,
   and observed turns, calls, sessions, or time with counting rules. Use unknown
   for missing measurements; separate observation from a causal claim.
3. **Why is it meaningful?** What work, requirement, or boundary was affected,
   what a correct agent could have done, and plausible alternative explanations.
4. **What error should the reproduction trigger and detect?** The preconditions,
   exact failure rule, correct task outcome, and invalid or unjudgeable cases.

Retain enough of the relevant sequence to assess those answers, including
contrary evidence and later recovery. Excerpts can span multiple files; keep
stable event anchors and label omissions, paraphrases, and redactions. Do not
replace available evidence with a polished narrative alone. If evidence cannot
be shared, explain the limitation and narrow the claim accordingly.

## Minimum submission and optional progress

An **incident-only** submission includes the collection files and a problem
created by the scaffolder. Keep `status` as `incident`; document unavailable
evidence or reproduction work. Keep the scaffold's four task directories and
their explanatory files so the required structure survives Git. Unimplemented
commands remain null. With no attempts, `result_records` is empty and no run
record is created. Do not upload an untouched result template as an evaluation.

A **packaged reproduction** adds actual stage prompts, starting files, fixtures,
dependencies, setup and run commands, separate task and failure checks, and a
correct reference. Record the scripted checks you ran. Preserve the earlier
event and later decision; an already broken final file is insufficient.

For **fresh model evaluations**, include every attempt: hits, misses, invalid
or unjudgeable attempts, development trials, and controls. Record model and
settings when exposed, actual length, task/judge versions, preconditions,
whether the failure opportunity occurred, and both task and failure outcomes.
Request existing results from the contributor when a claimed reproduction has
no supporting records. If none exist or a fresh run is unavailable, write
**not run** with the reason and next action; do not invent results.

Link every actual run's `summary.json` from `problem.json` using the repository
path. Inside each run record, evidence paths are relative to that run's
directory. Put original historical evidence in the problem account or its
`evidence/` directory; the original incident is not a fresh evaluation.
Describe that evidence in `source.evidence_note` and link it from the problem
readme; do not invent additional manifest fields.

## Material that stays local

Keep these outside the outgoing commit and its history:

- `.local/`, including history indexes, raw reader pages, private incident
  notes, and the mapping from sanitized aliases to real identities.
- Original Claude Code/Codex transcript stores, prompt indexes, credentials,
  account configuration, unrelated conversations, and full private checkouts.
- The working `REPORT.md` when it links to private notes. Publish its reviewed
  summary under the collection directory above.
- Secrets, private source without sharing permission, personal or customer
  data, unreviewed logs, dependency caches, and disposable environments.

Evidence and reference solutions belong in the submitted repository for
reviewers. During evaluation, expose only the intended prompts and starting
files to the tested agent; keep the judge, reference, and historical failing
answers outside its accessible workspace.

Ordinary incident submissions add collection, problem, and result files.
Put task-specific setup and checking scripts inside their problem package.
Changes to shared kit instructions, `commands/`, templates, or the installed
skill are separate maintenance work and should be explained as such.

## Review, verify, and push the selected files

Use a clean checkout of the destination repository and a new contribution
branch. Copy only the proposed submission files from the private collection;
do not copy the collection workspace wholesale. Use a fork when the contributor
does not have write access to the shared repository. Prepare a pull request
against `DylanZSZ/agent-failure-repo` on `main` after sharing is authorized.

Before any upload, show the owner an exact repository-relative file list and
the contents or diff of those files. Review every file beneath the selected
directories, including collection summaries and evidence. Set each problem's
`privacy_reviewed` field to true only after the owner has reviewed those exact
files; the collecting agent cannot supply that approval itself.

If these exact files and destination are already approved, continue without
asking again. Otherwise finish the reviewable material and request approval
to share it. Permission to inspect histories alone is not upload permission.

Stage only those reviewed paths. Inspect the staged file list and diff:

```bash
git diff --cached --name-only
git diff --cached
python3 commands/validate.py --submission
```

The validator checks problem/result structure and the problem's review
declaration. It does not validate collection reports, certify privacy, or verify
that an incident or reproduction is correct. Review the collection files too.

For a runnable package, check a clean copy of the proposed committed files:
follow its documented setup and scripted checking commands, and confirm all
required fixtures and dependencies are present. Reuse recorded model results;
this check does not require buying new model runs. Check that outgoing commits
contain only reviewed material; deleting a private file in a later commit does
not remove it from earlier history. Then push the contribution branch and open
the authorized pull request. Preserve existing submissions and run records.

## Tell the contributor in the console too

In the final chat response, provide:

- What was found, how many distinct incidents were packaged, and the main gaps.
- The exact files proposed for sharing, or the files actually committed and pushed.
- Which scripted checks and model evaluations ran, and which were not run.
- The local report path and, if uploaded, the branch, commit, and pull-request link.
- What still needs review, evidence, reproduction work, or evaluation.

Do not report “pushed” until it succeeded. A local collection awaiting review
must be labeled local. A report link alone is not the console explanation.

Source: [owner review](REVIEW.md), [reproduction requirements](REPRODUCING.md),
and [detailed evidence](EVIDENCE.md).
