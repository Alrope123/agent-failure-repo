# Capture the evidence before reducing the task

Updated 2026-10-10.

## Summary

Collect enough information for another investigator to reconstruct what happened, check competing explanations, and build a faithful reproduction. Search every authorized source against [all 20 symptoms](SYMPTOMS.md), retain other symptoms, and record every distinct candidate. There is no maximum number of incidents, no quota per symptom, and no requirement to fill every category.

Use one private copy of the [incident evidence form](../templates/incident-evidence.md) for each incident. Link it from the incident index. Capture relevant evidence first; write the short account and choose a minimal task afterward. The richer incident record and the smaller runnable task serve different purposes.

## Start with scope and access

Record the contributor's authorization: which histories, repositories, accounts, dates, and attachments may be inspected, and any exclusions. A request to contribute failures does not authorize searching every file or account. Follow authorized references to recover missing context; ask for an additional source only when its owner can provide it and it would materially help. Do not repeatedly request unavailable material or broaden access silently.

List available sources before selecting examples. Record inspected ranges, unread ranges, inaccessible attachments, search methods, and a continuation point. Keep both keyword matches and a chronological review: a deleted method, changed test expectation, or wrong handoff may have no obvious failure keyword. Record histories with no matching incidents so that absence of a finding can be distinguished from absence of a search.

Keep raw histories, unreviewed extracts, private source locators, and the redaction map under ignored `.local/` or another owner-approved private location. Check that private material is untracked before staging a contribution; an ignore rule does not protect a file already tracked. Use the exact owner-reviewed, sanitized files for any sharing. [AGENTS.md](../AGENTS.md) and the [review checklist](REVIEW.md) govern that handoff.

## Use explicit evidence states

Every requested field must contain a supported value or one of the following states. Never fill gaps with plausible guesses, generated messages, reconstructed timestamps, or an assumed model setting.

| State | Meaning | Required explanation |
|---|---|---|
| Observed | The available record directly supports the value | Source and event or artifact anchor |
| Contributor-reported | The owner recalls or supplies the information, without a confirming record | Who supplied it and when, using a shareable alias |
| Inferred | A conclusion drawn from identified observations | Supporting evidence, alternatives, and uncertainty |
| Unknown | Available evidence does not determine the value | What is missing or contradictory |
| Unavailable | A relevant source exists or is expected but cannot be accessed | Access or retention limit and any next step |
| Not applicable | The field does not apply to this incident | A short reason |
| Withheld | Information exists but is intentionally excluded | The type of omission and its effect on interpretation; do not reveal the omitted value |

Use these states field by field. A report may know the model name but not its revision, and have a complete final diff but an incomplete earlier transcript. For numeric fields, unknown is not zero. Label estimates and state how they were calculated. Do not downgrade a withheld field to an apparently observed sanitized value without explaining the substitution.

## Recover the complete sequence

For each incident, capture the following before explaining its cause:

1. **Original intent.** The user's goal, acceptance criteria, scope, standing rules, later changes to those rules, permissions, and permitted stopping options. Preserve exact relevant wording where authorized. Identify which instructions actually applied at the decision time.
2. **Earlier state.** The rule, working implementation, discovery, completed delivery, or teammate addition that the later action mishandled. Record what shows it existed and worked. A passing import or unrelated test is weaker than a check of the relevant behavior.
3. **Intervening work.** Every relevant task, pause, repository switch, context reset, compaction, memory edit, tool-output truncation, teammate action, or environment change. Record unrelated work by its actual extent when it contributes to the measured span; do not collect unrelated personal content.
4. **Decision and action.** The later request, evidence available then, messages and tool calls, complete relevant tool results, actual file or state changes, and any report of completion. Separate what the agent said it would do from commands that ran and effects that occurred.
5. **Consequence.** Independent checks, user corrections, lost work, incorrect output, exposure to an unauthorized destination, or blocked follow-on work. Record measured impact separately from hypothetical impact.
6. **Recovery and recurrence.** What happened after discovery: correction, rollback, retry, explanation, successful handoff, unresolved damage, or the same mistake again. Keep later recovery; it may change the conclusion even when it does not erase the original failure.

Capture supporting and contradictory evidence with equal care. Keep a failed diagnostic attempt, an earlier correct decision, a successful recovery, an unread reminder, and evidence that a teammate or environment caused the result. Do not select only the lines that make the failure look obvious.

## Make every important claim traceable

Give source files stable local IDs, then give relevant events stable anchors such as `history-03/message-147` or `run-02/tool-18/result`. Prefer exported message IDs and tool-call IDs when available; otherwise record the file, line or byte range, and extraction method. Preserve timestamps, timezone or offset, and whether a timestamp describes the event, export, or collection. If timestamps are missing, preserve order and state that elapsed time is unknown.

Each excerpt should identify its speaker or actor, session, role, source anchor, surrounding context, omissions, and redactions. Preserve call/result associations, error output, exit codes, stdout/stderr distinctions, truncation notices, and attached artifacts when relevant. Record a proposed command separately from its executed call and returned result. A command printed in a final answer is not evidence that it ran.

Record the export method and date. Optional content hashes can detect accidental changes to non-sensitive exported files or sanitized artifacts; hashes do not establish the original account's accuracy. Do not publish hashes of low-entropy secrets, private identifiers, or withheld text as a substitute for redaction. Preserve originals privately without rewriting them to make the chronology cleaner.

Use observable messages, tool calls, tool results, and artifacts. Do not request private chain-of-thought, hidden model reasoning, or provider-internal traces. If the agent wrote an explanation in an ordinary visible message, quote it as a statement it made, not proof of its internal cause.

## Capture the environment and effective state

Collect the details that are available and relevant; mark the rest explicitly rather than blocking the entire contribution:

- **Agent and model:** product or agent name and version; configured model and provider; served model revision if exposed; dates; routing and fallback notices; sampling and reasoning settings only if available.
- **Runtime:** operating system, architecture, language and dependency versions; container or image identity; repository commit, branch, dirty state, and working directory alias; installed extensions or hooks affecting behavior.
- **Instructions:** available system/developer instructions, user requests, repository guidance, skill versions, persistent memory, and their loading order. Mark instructions that are not exposed as unavailable.
- **Tools and permissions:** tool names and schemas or versions; file, network, and shell access; approval rules; actual approvals or rejections; sandbox and workspace boundaries; shared writers.
- **Context handling:** advertised context limit, configured limit, actual usage if logged, compaction/reset/truncation events, retained memory and summaries, and files available for rediscovery.
- **Budget and delivery:** configured turn, tool, token, cost, or wall-time limits; remaining-budget notices; delivery mechanism; who or what ended the run and why.
- **External conditions:** dependency availability, provider errors, flaky services, filesystem state, concurrent jobs, clock behavior, and relevant network responses.

Do not equate the configured model with a verified served revision, the advertised context window with actual context usage, or a configured maximum with actual work. Do not infer a reset or compaction from a surprising answer alone.

For code and file changes, preserve the smallest relevant before/after snapshots and diffs, including renames, deletions, generated files, untracked and ignored dependencies, and commits. Record which state was agent-visible, which state was delivered, and which state the evaluator actually tested. Include effective configuration precedence when the edited file may not control runtime behavior.

For tests, retain the exact command, relevant environment, state under test, output, exit code, and time. Distinguish baseline checks, checks run by the agent, hidden acceptance checks, later investigator checks, and counterfactual checks. Save all repeated results on the same state, including failures followed by passes. A post-hoc test is useful evidence, but it was not information available to the original agent.

## Measure the horizon rather than calling it long

Record the earliest relevant event, the later decision, and the failure or discovery event. Measure the span between clearly named endpoints using whatever the source actually provides:

- Sessions and task stages; session resets, pauses, compactions, handoffs, and repository switches.
- Assistant replies, user messages, tool calls, executed commands, and intervening tasks. State the counting rule: one assistant reply may contain several tool calls.
- Elapsed wall time and active work time when separately available. An overnight pause is not an overnight reasoning process.
- Tokens and context utilization when actually logged. Separate input, output, cached, and cumulative usage; cumulative tokens are not the context present at one decision.
- The information that had to survive and its distance from the later decision. Record whether it was in the current context, an automatically loaded note, a discoverable file, or unavailable after a reset.

Do not set a universal number of turns that makes an incident “long horizon.” Explain why the intervening work or boundary might matter for this case. Classify the temporal claim honestly: an observed sequence, a suspected contribution of extended work, or support from a comparison. A long session containing an ordinary local mistake remains useful if documented as such.

## Separate symptom, significance, and explanation

Use [SYMPTOMS.md](SYMPTOMS.md) to label observable behavior. Write an operational failure rule: which action or final state, under which prerequisites, counts as a hit; which evidence makes it a miss; and when it cannot be judged. Record the user's task outcome separately. A feature can work while another obligation is violated.

Explain why the incident matters using actual consequences and a feasible correct action given the information available then. Do not call a case meaningful merely because the transcript is long, or trivial merely because the patch is small. A one-line change can destroy a critical boundary. Keep ambiguity in the original request visible.

Then evaluate the proposed mechanism. List evidence for and against memory loss, stale memory, local imitation, missing search, budget pressure, test overfitting, or another explanation. Compare these with short-task difficulty, ambiguous requirements, unavailable information, a flawed evaluator, service failures, and teammate interference. State what comparison would distinguish them. A similar earlier rule and later wrong code do not establish that one caused the other.

Link related incidents and repeated references. Use one incident ID for one episode even when it matches several symptoms; use separate IDs for distinct episodes. Record `duplicate_of` and the reason for merging records. Preserve dependencies between incidents: a missing handoff and a later false completion may be separate observed events in one chain rather than independent samples.

## Preserve attempts and reduction decisions

Follow [REPRODUCING.md](REPRODUCING.md) to build a minimal task. Keep a mapping from original facts to reproduction details: what was retained, replaced with fake data, simplified, omitted, or made unavailable. Keep the temporal link, available reminders, legitimate success path, and opportunity to make the mistake. A minimal environment is not a reason to erase uncertainty from the incident record.

Record every attempted setup, checker test, replay, fresh model attempt, and control, including failures, misses, aborts, and infrastructure errors. Give each attempt an ID, its inputs and versions, commands, outcome, evidence path, and any exclusion reason. Keep a failed prototype when it explains why the next version changed. Do not count a scripted defect or a checker test as the model reproducing the error.

If evaluation is not possible, finish the evidence record with the missing requirement and next action. Ask for existing evaluation artifacts when available: complete attempt lists, raw observable trajectories, exact task and judge versions, model settings, negative results, controls, eligibility decisions, and later reviews. Do not ask only for successful reproductions or headline rates.

## Limitations

A record can establish an observed error without establishing its cause or how often it occurs. For every comparison, report the sample size, eligible denominator, exclusions, and selection method. A comparison with only one attempt per condition is a case study, not a reliable rate estimate. A collection drawn from friends' reported failures cannot estimate general prevalence without a defined sampling frame. Missing history may prevent judging whether a reminder was available, a baseline worked, or the same action would fail in a shorter task.

## Next steps: finish with an evidence audit

- Every incident in the index has a record or an explicit deferral reason; duplicates and rejected cases remain accounted for.
- Every confirmed failure has an applicable requirement, observed action or state, and consequence or declared failure predicate with sources.
- Every numeric claim names endpoints and a counting rule; missing fields carry their own state and reason.
- Contrary evidence, later corrections, unsuccessful attempts, and alternative explanations remain visible.
- Shared excerpts preserve relevant relationships while removing restricted content; the private redaction map stays private.
- The owner can see exactly what would be shared, what remains uncertain, and what work has not yet been completed.

## Sources

This collection procedure follows the repository's [agent instructions](../AGENTS.md), [symptom evidence requirements](SYMPTOMS.md), and [reproduction guide](REPRODUCING.md). It defines what contributors should record; it reports no new model evaluation results.
