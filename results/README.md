# Record every attempt, including attempts that did not reproduce the error

Updated 2026-10-10.

## Summary

Use `results/<problem-id>/<run-id>/summary.json` for each attempt. Copy
[the result form](../templates/result.json), keep run identifiers unique, and
place reviewed evidence beside the record. Paths in `evidence` are relative to
that record's directory. Link the record from the problem's `result_records`
using a repository-relative path.

A `model_run` means an agent actually attempted the task. A `scripted_check`
means code such as a known correct or deliberately faulty solution was tested.
Do not report a scripted check as model reproduction.

Record setup validity separately from task correctness and the target failure.
Use `unjudgeable` and a null target outcome when evidence is insufficient. An infrastructure crash,
missing dependency, or a run that never reached the relevant situation is not
a clean success or a target failure. Explain exclusions. Keep each attempt and
each control; do not save only the most interesting run.

The `pair_id` links comparable main and control runs, if a paired design was
used. It does not assert that their random execution was identical. Record
actual settings, model, code revision, and observed duration in every attempt.
Set unknown values to null. Do not merge model runs with incident counts or
scripted checks when calculating a frequency.

## Limitations

Keep large or private originals outside Git. Submit the smallest reviewed
evidence that supports the claim. If originals cannot be shared, describe what
was withheld and how that limits independent checking in the problem description.
Never overwrite an earlier result to make it match a revised judge; append a
new assessment and preserve the old one.

No model evaluation records are included in this starter.

Create records only for actual attempts. If evaluation was not run, state
that and the reason in the problem and collection summaries; do not commit
the untouched result template. See [what to push](../docs/SUBMITTING.md).

A valid scored attempt requires both `preconditions_met` and
`failure_opportunity_reached` to be true. Invalid or unjudgeable attempts have
a null `target_failure`; independently known task correctness can still be
recorded. An agent-caused product crash can be a valid target failure if that
is the defined behavior being tested.

Use `phase` to separate `development` from `evaluation` after freezing the task
and judge. Keep the frozen plan and chosen sample size in the problem description.
For `temporal_supported`, link a main/control pair with `pair_id`, preserve
comparable model/settings and task/judge revisions, and write `comparison_note`
in the problem manifest. That note must assess the evidence and confounds;
metadata consistency alone does not establish causation.
