# Build a faithful small task for every feasible incident

Updated 2026-10-10.

## Summary

A reproduction should let a new agent face the decision that produced the original failure. Build one for every feasible credible incident in the collection index; do not stop after the first successful package or one per symptom. Preserve the earlier event and the later opportunity to mishandle it. A fixture containing already broken code demonstrates a bug, not an agent making that mistake.

## Account for the whole collection

Use the [incident index](../templates/incident-index.csv) to track each distinct candidate and the [collection report](../templates/collection-report.md) to track overall coverage. Begin with the [history search](FINDING_FAILURES.md) and [all symptom classes](SYMPTOMS.md). Feasibility can determine work order, but it should not silently determine which incidents appear in the report.

For each credible incident, create a runnable package or an incident-only account that names the missing prerequisite and next action. Link the resulting package and every attempt from the index. Do not fabricate reproductions to satisfy completeness. An unavailable dependency, restricted source, missing history, or unavailable model can justify deferral; “we already have that symptom” cannot.

## Keep the temporal mechanism

Write the sequence before implementing the environment:

1. Establish the relevant rule, completed behavior, discovery, or ownership boundary.
2. Include the intervening work or state change that might make it hard to retain or apply.
3. Give a natural later request that creates an opportunity for the error.
4. Check whether the setup was valid, the agent reached that opportunity, the user's task was completed, and the intended error occurred.

For example, to study a rule lost after a session reset, first let the agent complete work under that rule. Keep the durable reminder available in the same way it was available originally. Then reset the conversation and give the next task. Starting with “ignore the old rule” or handing the agent a broken implementation would change the question.

Remove unrelated dependencies, data, and setup. Keep details that could explain the failure, including an accessible reminder, conflicting local examples, a teammate's edit, the correct stopping option, or the originally available budget. Document every material change from the original incident. If a reduction removes the long span, explain what temporal claim remains testable.

## Package the task

Create a starter with `python3 commands/new_problem.py <slug>`. Document the following in the problem's description and metadata:

- A short account of the original incident, its evidence, and what can be shared.
- The intended failure, its concrete consequence, and the reason earlier work may matter.
- The exact starting state, software versions, prerequisites, environment variables, and any network needs.
- The sequence of prompts, session resets, teammate changes, and context carried between stages.
- Exact commands for setup, task execution, checking, reset, and cleanup; state what each creates or changes.
- The agent-visible files and instructions, with checks and reference material kept outside that workspace.
- A correct reference or another concrete demonstration that the requested task can be completed.
- The proposed comparison, known limitations, and the strongest evidence level currently supported.

Put requests in `task/`, local setup and fixtures in `environment/`, checks in `checks/`, and the correct implementation or walkthrough in `reference/`. Shared repository commands belong in `commands/`; commands specific to one task belong with that task. The repository does not supply a universal model runner: document the adapter or manual procedure you actually used.

Define visibility separately for every stage. Present only the current stage's permitted message and files, plus the history or memory that should carry forward. Future requests, reset schedules, and simulated teammate changes are evaluator instructions. Keep them outside the evaluated workspace rather than copying the entire `task/` directory into it.

Use disposable directories, fake identities, and local mock services. Do not mount real credentials, personal histories, or unrelated source trees into an agent workspace. Keep model-provider credentials with the trusted caller rather than exposing them to the tested agent. Run both the task and the evaluator with limited permissions; a check that imports task code can execute it.

## Define two separate checks

**Task check:** did the delivered work satisfy the user's request? Prefer observable behavior, a clean-checkout test, or another independent acceptance check. A model saying “done” is not task completion.

**Failure check:** did the specified erroneous action occur? Define the exact evidence required. For “calls its own regression pre-existing,” require evidence that the test passed initially, the agent caused the later failure, and its report assigned the wrong origin. A failed final test alone is insufficient.

Record preconditions such as a correct earlier implementation, a successful teammate change, and a visible reminder. Record arrival at the later decision separately using the result form:

- `preconditions_met` — whether the required starting conditions were established.
- `failure_opportunity_reached` — whether the agent reached the situation in which the intended mistake could occur.

Fill both from evidence, using null for unknown, rather than inferring them from the final answer. Use explicit outcomes:

- **Hit:** a valid, judgeable attempt meets the failure rule.
- **Miss:** a valid, judgeable attempt reaches the opportunity and does not meet it.
- **Invalid or unjudgeable:** a prerequisite fails, the agent never reaches the opportunity, evidence is missing, or the checker cannot decide.

Keep task success separate from these outcomes. An agent can fail the task without exhibiting the target failure, or finish the requested feature while deleting someone else's work.

A broken runner, missing setup dependency, or infrastructure crash can make an attempt invalid or unjudgeable. An agent-caused product crash is different: it can be the specified failure if the preconditions, opportunity, and evidence satisfy the declared rule. Do not exclude crashes categorically or count every crash as a hit.

Check the checker against a correct reference and a deliberately faulty version. Label those as checker tests; neither is a model reproduction. If text judgment is needed, record the rubric, evaluator, and uncertainty rather than disguising a subjective decision as an objective test.

## Separate kinds of evidence

| Evidence | What actually happened |
|---|---|
| Original incident | An authorized historical record shows the observed failure |
| Scripted replay | Recorded actions were replayed to recover their effects |
| Deliberately faulty version | A human or script inserted the suspected defect |
| Fresh model attempt | A model received the task and chose its own actions |
| Temporal comparison | Fresh attempts differ in one relevant history condition |

A replay helps verify a consequence. A faulty version helps test a checker. Only a fresh model attempt can show the model making the mistake again. Synthetic teaching examples must remain labeled synthetic and must not enter crowdsourced failure counts.

## Evaluate the explanation, when feasible

Start with a fresh model attempt. Predeclare the conditions, model settings, number of attempts or stopping rule, and judging rule before examining outcomes. Preserve every attempt, including timeouts and service errors. Keep model name, version if available, prompts, tool definitions, context handling, budget, and actual observed run length in the run record.

Then change one plausible cause while keeping the final task and its difficulty as comparable as possible. Options include removing the intervening work, keeping the session continuous, replacing stale notes with current ones, or restoring an earlier reminder. Explain what else that change affects. If the control hands over the solution or makes the final task easier, it cannot isolate the effect of a long history.

Use multiple attempts when estimating rates. Match seeds when the provider supports them, but do not assume a shared seed makes two runs identical. Report the hit count and eligible denominator for each condition, plus all excluded attempts and reasons. State the main limitation: a single matching pair supports a case study; it does not establish a reliable causal effect.

Save sanitized evidence and `summary.json` in `results/<slug>/<run-id>/`. Retain the original record when adding a later review. If no model evaluation was run, say “not run” and list what is needed. Do not substitute checker tests or synthetic transcripts for unavailable model results. Return to the incident index after each package or evaluation and update the remaining work for that incident.

## Validate before owner review

Run `python3 commands/validate.py` to check the submission structure. Separately run each completed task's documented commands in a fresh disposable workspace. Record which commands you actually ran and their outcomes. Reconcile every credible incident with a completed package or a concrete deferral reason and next action. Finish with [the owner review](REVIEW.md) before uploading any material.

Source: [Evidence levels](../CONTRIBUTING.md), [finding the temporal mechanism](FINDING_FAILURES.md), and [agent operating rules](../AGENTS.md).
