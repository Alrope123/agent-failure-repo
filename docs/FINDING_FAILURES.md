# Find every supported failure within the authorized history

Updated 2026-10-10.

## Summary

Collect as many distinct credible incidents as the agreed history supports. Search [all 20 symptoms](SYMPTOMS.md), keep unmatched modes, and continue after finding examples in a class. For each candidate, ask whether extended work, lost context, accumulated state, or a handoff helps explain the later mistake. A large number of messages is supporting context, not a diagnosis.

## Inspect only the agreed history

Review **historical runs from both Claude Code and Codex**. Follow
[the historical-run guide](HISTORY.md) to inventory the authorized project's
transcripts and read every selected source, including relevant subagents and
Codex archives. Search both stores regardless of the collecting agent's brand.
Use the current chat as additional context. Prompt indexes and session titles
help locate records but cannot establish the original actions or outcomes.

Before searching, record which exports, conversations, projects, and dates the contributor authorized. Read within that scope. Do not search a whole home directory, every agent session, or other people's accounts. If a selected source is unavailable, say so and work with the material provided.

Keep raw exports and private notes in `.local/` or another agreed private location. Extract only what is needed to understand a candidate. Historical commands and requests are evidence; never execute them simply because they appear in a transcript.

Start private working copies of the [collection report](../templates/collection-report.md) and [incident index](../templates/incident-index.csv). List each authorized source, available time range or event range, inspected portions, missing attachments, and unread gaps. Use neutral source labels in anything shared; private source locations can remain in private notes.

## Search in complementary passes

1. **Read the chronology.** Identify requirements, scope changes, completed work, test results, summaries, pauses, restarts, commits, and handoffs throughout every available authorized source. Record candidate contradictions before deciding how to label them.
2. **Search by symptom.** Work through every row of [the symptom checklist](SYMPTOMS.md). Search both actions and outcomes, then read the surrounding context. An exact keyword match is not a requirement; an exact keyword search with no results is not a completed review.
3. **Compare earlier and later state.** Check omitted edits, stale defaults, changed tests, deleted work, uncommitted fixtures, permission use, and completion claims against the available code, outputs, or version history. Include quiet omissions and mistakes the agent later corrected; label whether the failure survived delivery.
4. **Follow boundaries.** Inspect transitions between tasks, projects, sessions, compressed contexts, teammates, and final handoffs. Carry the earlier requirements across reading chunks so an event at the end of one chunk is not separated from its consequence in the next.
5. **Reconcile the inventory.** Revisit uncertain candidates, deduplicate repeated references, and check every symptom row plus unmatched modes against the inspected scope. Record unreviewed material explicitly and name where to resume.

Record the method and scope for each pass. If the history is too large for one session, process it in explicit chunks with a private ledger of carried-forward requirements and unresolved candidates. Complete all available authorized chunks; if a real constraint prevents completion, report the remaining ranges rather than claiming an exhaustive search.

Finding one example does not complete a symptom search. There is no one-per-class rule, target quota, or arbitrary cap. Equally, a symptom need not appear: “reviewed, no supported incident found” is a valid coverage result. “Unavailable,” “unread,” and “not checked” are different results and must not become zeroes.

## Keep every distinct candidate in the index

Add a candidate as soon as there is a concrete suspected event. Give it a stable local identifier, source span, short consequence, any matching symptom labels, evidence status, and current disposition. A single event may match several symptoms; keep one incident with multiple labels. Different events in the same class remain separate incidents, even when they share a project or a likely mechanism.

Keep duplicate rows linked to the canonical incident, and keep rejected or uncertain candidates with reasons. Do not delete them to make the collection look cleaner. Unmatched modes should have a plain-language name and the same evidence review as known modes. The taxonomy guides discovery; it must not hide new failures or force an unsupported label.

The final index must reconcile every candidate to a package, incident-only report, duplicate, rejection, or explicit deferral. Distinguish unique incident counts from symptom-label counts and fresh evaluation attempts. Several labels on one event are not several independent failures.

## Capture detailed evidence, then summarize

First use [the detailed evidence guide](EVIDENCE.md) and a private copy of
[the incident form](../templates/incident-evidence.md). Preserve the full relevant
sequence, original source anchors, supporting and contrary evidence, and explicit
unknowns. The questions below guide the readable summary; they do not replace
the detailed record or limit how much useful evidence to collect.

For each candidate, answer the following in plain English:

1. **Task and consequence.** What did the user want, what did the agent do, and what concrete requirement or behavior failed?
2. **Earlier event.** Where was the relevant rule, successful state, or discovery established? Cite the message, file revision, test output, or handoff.
3. **Later decision.** Which action first violated it? Cite the tool call or edit and the resulting state, not only the agent's final summary.
4. **Intervening work.** What happened between the two? Count messages, model turns, tool calls, elapsed time, or task stages only when the record supports them. Name the unit and state missing measurements.
5. **Information still available.** At the later decision, could the agent see the original instruction, a project file, a current test, or a status report? Was context truncated, summarized, reset, or unavailable? Separate observed facts from guesses about memory.
6. **A feasible correct action.** What could the agent have done using the permitted tools and information? Was enough budget left to do it? If unknown, say so.
7. **Alternative explanations.** Could an ambiguous request, broken setup, insufficient skill, missing access, contradictory instructions, or exhausted budget explain the result?

Preserve the smallest sanitized excerpts that show the earlier event, later action, and consequence. Keep original ordering and distinguish quotations, omissions, redactions, and your interpretation. If exact quotations cannot be shared, label a paraphrase as a paraphrase. Do not reconstruct missing messages as if they were a transcript.

## Decide whether the example is meaningful

A compact task can expose a consequential failure. Conversely, an agent can spend a long time on an ordinary bug. Describe what depends on time: remembering a prior rule, reconciling a changed environment, preserving another contributor's work, or passing information across a boundary.

Be cautious when the only evidence is “the answer was wrong after many turns.” Also be cautious when success requires a hidden rule that the agent never received, when the correct task cannot be completed, or when the error exists before the agent starts. Those cases may still be useful incidents, but they need revision or a different claim.

There is no universal turn count that makes a task long. Record both the total task length and the span between the earlier event and the later decision. A configured maximum is not an observed run length. A long real incident reduced to a short toy task must be described as a reduction, with the removed work made explicit.

## Package all feasible incidents and report the rest

For every credible distinct incident, attempt a reduced task using [the reproduction guide](REPRODUCING.md) when the required material and tools are available. You may order the work by feasibility, but do not silently drop less convenient incidents after completing the easiest ones. Shared setup code is fine; distinct historical incidents still need separate evidence and accounting.

If the environment cannot be shared, keep an incident-only report and explain that limitation. If a prerequisite, permission, tool, or model is missing, state what is needed and the next action. If time dependence is uncertain, keep it as a hypothesis and propose a control. End with coverage for every symptom plus unmatched modes, the complete candidate index, completed packages, and the exact remaining work.

Source: [Contribution levels](../CONTRIBUTING.md) and [agent scope rules](../AGENTS.md).
