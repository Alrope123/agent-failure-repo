# Review the exact files before sharing

Updated 2026-10-10.

## Summary

The contributor should review the complete collection and sanitized packages before an agent uploads them. Check that the agent searched the authorized scope comprehensively, accounted for every candidate, and built every feasible reproduction rather than returning a shortlist. Review also protects the people and projects in the history. A valid file layout is only the first check.

## Collection coverage review

- The [collection report](../templates/collection-report.md) lists the exact authorized sources, inspected portions, search passes, unavailable material, and unread gaps.
- Coverage is recorded for [all 20 symptoms](SYMPTOMS.md) and unmatched modes. “No supported incident found” is used only for reviewed material; missing or unread material is not counted as absence.
- The [incident index](../templates/incident-index.csv) includes every distinct candidate, including uncertain, rejected, duplicate, and deferred cases with reasons.
- Repeated references to one event are deduplicated. Different incidents in one symptom class remain separate. Multiple symptom labels on one incident do not inflate the unique incident count.
- Search did not stop after one example, a preferred handful, or one hit per class. Any actual constraint has an explicit continuation point; completeness is not claimed across an unread gap.
- Every credible incident links to a completed package or an incident-only account. Every deferred reproduction or evaluation names the missing prerequisite and next action.
- Counts in the report reconcile with the index, packages, and attempts. A priority order for future work has not replaced the full inventory.

## Owner review

- **Scope:** the agent inspected only the histories and project copies you authorized. It states which sources were unavailable.
- **Permission:** you are entitled to share the included code, messages, and other material. Other people's private messages are omitted unless you have permission to include them.
- **Privacy:** inspect all proposed files, including logs, patches, screenshots, filenames, metadata, and test fixtures. Remove credentials, personal details, private repository addresses, customer data, and private home paths. Use stable fake names where relationships matter.
- **Private working files:** raw exports and unreviewed notes stay in `.local/` or your chosen private location. Check the actual staged diff, file list, and commits being shared; an ignore rule does not remove already tracked files or their history.
- **Faithfulness:** quotations and paraphrases are distinguished. Redactions and changes to the original environment are disclosed. Sanitization has not silently removed the reason the failure happened.
- **Publication:** approve the specific files that will be shared. Authorization to inspect history or prepare a task does not by itself authorize uploading that history.

## Task and evidence review

- The account identifies the earlier event, later decision, actual consequence, and intervening work or boundary.
- The task states whether long history is a hypothesis, a reproduced association, or supported by a meaningful comparison.
- The actual observed length is separate from the configured maximum. Missing measurements are marked unknown.
- The reduced task preserves the relevant sequence and information available to the agent. It gives the agent a feasible correct path.
- The setup and commands are complete enough for another person to attempt. Dependencies, network effects, and cleanup are explicit.
- At every stage, the agent workspace excludes hidden checks, reference solutions, historical failing answers, and descriptions that reveal the target failure. Future prompts and the reset or teammate-change schedule remain outside that workspace.
- The correct reference passes the task check. A deliberately faulty version is used only to test the checker and is labeled accordingly.
- Task completion and the intended error have separate checks. Preconditions and reaching the failure opportunity are recorded explicitly. Invalid runs, misses, and missing evidence are handled consistently.
- Infrastructure failures are distinguished from agent-caused product failures. A product crash is neither automatically excluded nor automatically counted as the target error.
- Every evaluation attempt is accounted for. Reported denominators exclude invalid or unjudgeable attempts openly, with reasons.
- Original incidents, replays, synthetic examples, fresh model attempts, and temporal comparisons are clearly distinguished.
- A claimed reproduction links to the actual sanitized trace and outcome. A claimed temporal effect includes the control and its limitations.

## Maintainer decision

Accept incident-only reports when they are clear and useful, even without a runnable environment. Ask for missing evaluation results when a contribution claims a model reproduction or a temporal effect. Do not demand that contributors invent a stronger evidence level to get their incident reviewed. Ask for the complete index and explicit search gaps when only selected examples are presented.

Request revision if the task depends on an undisclosed rule, starts after the crucial mistake, has no feasible correct solution, confuses ordinary task failure with the named error, or claims a fresh model failure from a scripted example. Ask for a narrower claim when privacy or unavailable logs prevents verification.

Record the decision, the evidence level accepted, its main limitation, and the specific work needed next. Preserve the submitted results when interpretations change; add a dated review rather than silently rewriting the run.

Source: [Contribution process](../CONTRIBUTING.md), [history review](FINDING_FAILURES.md), and [reproduction requirements](REPRODUCING.md).
