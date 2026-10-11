# Incident evidence: <short descriptive title>

Template updated 2026-10-10. Record the actual collection and event dates below.

## Summary

Copy this form to `.local/incidents/<incident-id>.md` or another owner-approved private location. Adjust the guide links for the record's new location: from `.local/incidents/`, use `../../docs/`. This is a working evidence record, not permission to publish its contents. Complete a separate, owner-reviewed sanitized copy for sharing. Follow [the evidence guide](../docs/EVIDENCE.md).

For **each field**, enter a supported value and source, or `Unknown`, `Unavailable`, `Not applicable`, or `Withheld`, with a reason. Label recollections `Contributor-reported` and conclusions `Inferred`. Do not invent missing settings, messages, counts, or model reasoning. Empty cells are unfinished work, not zero or “none.” Add rows and attachments as needed; there is no incident or evidence quota.

## Identity and disposition

- Incident ID:
- Short title:
- Collection/source labels:
- Collector and contributor aliases:
- Collection date and timezone:
- Record version and later amendments:
- Status: candidate / confirmed observed failure / rejected / duplicate / needs more evidence.
- Matching symptom IDs and names from [SYMPTOMS.md](../docs/SYMPTOMS.md), or `other`:
- Reason for each label:
- One-sentence observed behavior:
- Current disposition: incident only / reproduction in progress / packaged / evaluated / deferred.
- Incident-index row and problem package path, if present:
- Duplicate of, related incidents, or causal chain IDs:
- Reason records are distinct or duplicates; whether they share an earlier state:

## Authorized scope and sharing boundary

- Authorization source and date:
- Authorized histories, projects, accounts, date ranges, attachments, and local paths (private locators):
- Explicit exclusions:
- Available sources and inaccessible portions:
- Source ranges actually inspected:
- Unread ranges and exact continuation point:
- Private original location:
- Private redaction-map location:
- Proposed sanitized output location:
- Owner review status, date, exact reviewed version, and sharing scope:

Do not treat permission to inspect as permission to upload. Do not inspect unrelated personal data. Do not place originals, credentials, or a reversible redaction map in the shared package.

## Source inventory

| Source ID | Type and provenance | Export/collection method and date | Stable private locator | Available range and gaps | Sanitized locator, if reviewed |
|---|---|---|---|---|---|
| | Conversation export, repository state, CI log, attachment, owner recollection, etc. | | | | |

- Export format and any known filtering, truncation, or dropped tool results:
- Source integrity notes; optional hash of a non-sensitive export or sanitized artifact:
- Search methods and symptom passes already completed:
- Related authorized sources followed, and unavailable sources that would resolve uncertainty:

## User goal and applicable requirements

- Original user goal:
- Acceptance criteria:
- Requested scope and delivery format:
- Exact relevant user instruction, with event anchor:
- Standing rules, permissions, ownership boundaries, and their scope:
- Later changes, exceptions, or revocations, with anchors:
- Requirement in force at the failure decision and why it applied:
- Permitted correct action, including any acceptable blocked report:
- Ambiguities or conflicting instructions:
- What the agent could know then versus what the investigator learned afterward:

## Agent, runtime, and context

| Field | Value or evidence state and reason | Source |
|---|---|---|
| Agent product, version, extensions, and relevant skills | | |
| Configured model and provider | | |
| Served model/revision, if exposed | | |
| Routing changes, fallbacks, or provider notices | | |
| Available sampling/reasoning settings and seed | | |
| OS, architecture, language, dependencies, container/image | | |
| Repository identity alias, commit, branch, dirty state | | |
| Available system/developer instructions and loading order | | |
| Repository instructions, user prompts, persistent notes | | |
| Tool names, definitions or versions, and limitations | | |
| File, network, shell, sandbox, and approval permissions | | |
| Shared writers, concurrent work, ownership notices | | |
| Configured context limit and advertised model limit | | |
| Actual logged context/token usage | | |
| Compaction, truncation, reset, pause, and resume events | | |
| Memory or handoff text carried across boundaries | | |
| Configured turn/tool/token/time/cost limits | | |
| Budget warnings and remaining budget actually reported | | |
| Termination reason and delivery mechanism | | |
| Relevant dependency/service/environment failures | | |

Use only available observable records. Do not request private chain-of-thought, hidden instructions, or provider-internal reasoning. Mark unexposed instructions unavailable; do not reconstruct them from the model's behavior.

## Earlier state and baseline

- Relevant earlier rule, discovery, working behavior, completed delivery, or teammate addition:
- Event when it was established:
- Evidence that it was correct or functioning:
- Exact baseline commit or snapshot and relevant dirty/untracked/ignored files:
- Baseline test commands, outputs, exit codes, and state under test:
- Existing failures and unrelated known limitations:
- Where this information remained available to the later agent:
- Evidence the later agent actually read it, or explicit statement that only availability is established:

## Complete relevant chronology

Use one row per relevant event; add intervening ranges with accurate counts when individual content is unrelated. Retain contrary evidence and recovery. Preserve event order even when time is unavailable.

| Event ID and source anchor | Timestamp, timezone, and type of time | Session/stage and actor | Message, call, result, or state change | Visibility at that moment | What this supports or contradicts |
|---|---|---|---|---|---|
| | Event time / export time / unknown | | | In context / loaded note / discoverable / unavailable / evaluator only | |

- Exact earlier relevant instruction or finding:
- Intervening tasks, context boundaries, teammate edits, and environment changes:
- Exact later request:
- Decision message, if any, as an observable statement:
- Executed action and complete relevant tool result:
- Delivery or completion claim:
- First evidence of the consequence:
- User correction or complaint:
- Subsequent agent response, correction, rollback, recovery, recurrence, or unresolved state:

## Excerpt and artifact register

Keep enough context to interpret each excerpt. Preserve call/result pairs and omitted sections explicitly; do not paraphrase a quote or silently merge separate events.

| Evidence ID | Source anchor and role/actor | Exact private excerpt or artifact locator | Omitted/truncated material | Sanitized excerpt or artifact locator | Redaction/substitution notes |
|---|---|---|---|---|---|
| | | | | | |

- Timestamp precision and any ordering uncertainty:
- Contradictory evidence not included in the short narrative:
- Unavailable attachments, outputs, or code states and their impact:
- Optional hashes of non-sensitive/sanitized artifacts; do not hash secrets for publication:

## File changes and effective behavior

| File or state alias | Before version | Change and actor | After/delivered version | Evidence of actual effect | Shared artifact path |
|---|---|---|---|---|---|
| | | | | | |

- Relevant diff, including deletions, renames, snapshots, generated files, and fixtures:
- Tracked, untracked, and ignored files needed for execution or delivery:
- Effective configuration or runtime path and precedence:
- Teammate changes and proof of compatibility with the requested task:
- State visible to the agent, delivered state, and tested state; explain any differences:

## Checks and counterfactuals

Record **every relevant result**, including a pass after a failure on unchanged code. Distinguish commands the agent ran from commands run later by an investigator. Do not rerun unsafe original actions against real services.

| Check ID | Actor and time | Purpose: baseline / agent / acceptance / investigator / counterfactual | Exact command and tested state | Outcome, exit code, and evidence | Available to the agent before delivery? |
|---|---|---|---|---|---|
| | | | | | |

- Known check limitations, skipped cases, nondeterminism, environment differences, and missing outputs:
- Counterfactual change made and everything else held constant:
- Whether the result actually attributes the failure to the agent's change:
- Evidence that the evaluator itself is correct; unresolved rubric ambiguity:

## Actual horizon

- Start event: the earlier obligation, fact, or working state that later mattered.
- Decision event: the later action that may mishandle it.
- End event: observed failure, delivery, or discovery; specify which.

| Measure | Start/end anchors | Observed value or evidence state | Counting rule, estimate method, and limits |
|---|---|---|---|
| Assistant replies | | | One reply may contain multiple tool calls. |
| User messages | | | |
| Tool calls and executed commands | | | Keep them separate when one call contains several commands. |
| Tasks or stages | | | |
| Sessions, resets, handoffs, compactions | | | |
| Pauses, repository switches, teammate changes | | | |
| Elapsed wall time and active work time | | | Do not infer active time from a gap in timestamps. |
| Input/output/cached/cumulative tokens | | | Use logged quantities; distinguish current context from cumulative usage. |
| Distance from last relevant reminder to decision | | | Name the measure and whether the reminder was read. |

- Information that needed to survive the span:
- Its availability at the later decision:
- Why intervening work or a boundary might matter:
- Temporal conclusion: observed sequence / suspected contribution / comparison supports contribution / no temporal connection established.
- Evidence supporting that conclusion and strongest alternative explanation:

## Intended failure and meaningfulness

- Observable symptom and primary label:
- Failure opportunity and required preconditions:
- Exact hit rule and required evidence:
- Exact miss rule:
- Invalid or unjudgeable conditions:
- User-task outcome, recorded separately from target-failure outcome:
- Actual consequence, affected work, user impact, and evidence:
- Measured recovery time, lost work, or other cost, if available:
- Potential consequence, clearly labeled hypothetical and kept separate:
- Feasible correct action using information available then:
- Why this is a meaningful obligation or boundary rather than a cosmetic preference:
- Why it may also be an ordinary short-task mistake, an ambiguous request, or a weak example:

## Explanation and competing evidence

| Proposed explanation | Supporting observations | Contrary observations or alternative | Evidence/comparison needed | Current confidence and reason |
|---|---|---|---|---|
| | | | | |

- Separate observed behavior from inferred mechanism:
- Agent's own visible explanation, if present; why it is or is not independently supported:
- Other causes checked: missing information, task ambiguity, local task difficulty, search scope, evaluator error, tool/service failure, teammate activity, or another cause:
- Evidence that could overturn the current account:

## Reproduction mapping and all attempts

- Proposed problem ID and package path:
- Smallest sequence preserving the earlier state, intervening event, later opportunity, and consequence:
- Agent-visible material at each stage:
- Evaluator-only material and safeguards against exposing it:
- Correct reference path and independent task/failure checks:

| Original detail | Retained / sanitized / simplified / omitted / unavailable | Reproduction equivalent | Effect on fidelity and temporal claim |
|---|---|---|---|
| | | | |

| Attempt ID | Kind: setup / checker test / replay / faulty fixture / fresh model / control | Task, judge, model, and state versions | Inputs and commands | Outcome and eligibility | Complete evidence path and next action |
|---|---|---|---|---|---|
| | | | | | |

- Evaluation plan and stopping rule set before observing outcomes, if applicable:
- Results by condition: attempted / eligible / hits / misses / invalid / unjudgeable, with denominator definition:
- Missing attempts, exclusions, aborted runs, provider failures, and reasons:
- Existing evaluation artifacts requested and received, including negative results and controls:
- Not run or deferred work, reason, required capability, and next action:

## Limitations and next steps: final account and owner review

Write this section **after** preserving the evidence above.

- Short account: what the user wanted, what happened, and the concrete consequence:
- Strongest evidence and its anchors:
- What is still unknown, unavailable, withheld, or disputed:
- Supported temporal claim and its limit:
- Contribution level actually achieved:
- Remaining work and exact continuation point:
- Sanitized files proposed for sharing, with versions:
- Private originals and redaction map confirmed outside the staged/shared files:
- Owner review of these exact files completed: yes / no; evidence and date:
- Collection index and coverage report reconciled: yes / no; remaining differences:

Before calling this record complete, account for supporting and contrary evidence, later recovery, every reproduction attempt, and every unknown field. Completion means the authorized evidence has been accounted for; it does not mean the failure has been reproduced or its cause established.
