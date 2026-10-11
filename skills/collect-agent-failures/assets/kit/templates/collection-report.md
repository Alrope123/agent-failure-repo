# Coverage of the selected interaction history

Updated 2026-10-10.

## Summary

Copy this form into private working storage before searching. Record the date,
contributor-approved scope, and search progress. It is a working inventory, not
an evaluation result. Do not publish private source names, paths, or excerpts.
An owner-reviewed, sanitized version may later be stored under docs/collections/.

## Scope and access

- Collection date and responsible contributor:
- Authorized projects, sessions, exports, and date ranges:
- Sources actually available and inspected, including start/end boundaries:
- Unavailable sources, truncated exports, or inaccessible tools:
- Search method and counting units:
- Raw history storage: retain privately; do not copy its path into a public report.

## Historical runs from both tools

Keep both rows, even if a tool has no accessible records. Start at **not checked**.
Record found, not present at checked root, inaccessible, no matching project,
or unsupported format as appropriate. None of those means zero failures.
Inventorying is separate from reading; count transcript files separately from
logical sessions and explain replay or duplicate handling.

| Tool | Access status and checked roots (private) | Matching files / logical sessions | Reviewed ranges | Gaps and next action |
| --- | --- | --- | --- | --- |
| Claude Code | not checked | unknown | none | Include related subagent transcripts |
| Codex | not checked | unknown | none | Check active and archived transcripts |

Source: [historical-run discovery](../docs/HISTORY.md) and the local history index.
The current conversation and supplied exports should have their own source rows.

For every source, record its private source ID, fingerprint, raw line ranges
reviewed, next unread line, parsing gaps, missing attachments, compaction,
and links to candidate records. Save carried-forward rules and open questions
between chunks. Do not add file line counts together and call them agent turns.

## Collection outcome

Summarize the useful findings and the biggest evidence gaps. Report distinct
incidents separately from symptom labels: one incident can have several labels.
Use the incident index as the source for counts. Include uncertain candidates;
label their uncertainty instead of silently discarding them.

- Distinct candidates recorded:
- Distinct incidents supported by evidence:
- Packaged reproductions:
- Fresh model reproductions:
- Rejected or duplicate candidates, with reasons in the index:
- Deferred candidates and unsearched ranges:

## Symptom coverage

For every row choose: **unsearched**, **found**, **not found in reviewed scope**,
or **insufficient evidence**. The default is unsearched. A found row is not
finished after its first hit: search the remaining authorized sources too.
List all matching incident IDs and any gaps. A negative search result applies
only to the reviewed sources and method, never to the contributor's whole history.

| Symptom | Search status | Incident IDs | Gaps or limits |
| --- | --- | --- | --- |
| 1.1 — Forgetting a standing project rule | unsearched | — | — |
| 1.2 — Changing code that does not control the behavior | unsearched | — | — |
| 1.3 — Only partly removing a withdrawn feature | unsearched | — | — |
| 2.1 — Applying one module's rule to another | unsearched | — | — |
| 2.2 — Old memory overriding an explicit current rule | unsearched | — | — |
| 2.3 — Carrying one project's conventions into another | unsearched | — | — |
| 2.4 — Following stale notes despite current evidence | unsearched | — | — |
| 3.1 — Breaking earlier completed work | unsearched | — | — |
| 3.2 — Overwriting a colleague's committed changes | unsearched | — | — |
| 3.3 — Resuming and overwriting another agent's work | unsearched | — | — |
| 4.1 — Copying a temporary secret into a durable artifact | unsearched | — | — |
| 4.2 — Using disallowed production credentials to unblock work | unsearched | — | — |
| 5.1 — Claiming completion although acceptance requirements fail | unsearched | — | — |
| 5.2 — Rerunning until green and declaring a fix | unsearched | — | — |
| 5.3 — Breaking correct code to satisfy a wrong new test | unsearched | — | — |
| 5.4 — Updating expectations to accept a new regression | unsearched | — | — |
| 5.5 — Blaming a self-caused failure on existing code | unsearched | — | — |
| 6.1 — Losing or reversing key facts in a handoff | unsearched | — | — |
| 6.2 — Omitting necessary files from the delivered commit | unsearched | — | — |
| 6.3 — Ignoring an instruction to wrap up and report | unsearched | — | — |
| Other symptoms | unsearched | — | — |

Source: the contributor's incident index and the source ranges listed above.
The search categories come from [the symptom guide](../docs/SYMPTOMS.md).

## What was searched

Record chronological passes and targeted symptom searches, including searches
that found nothing. Prefer source labels over private paths. State search terms
and limits when relevant. Read surrounding actions before labeling a keyword hit.
Include corrections after a claimed finish and later sessions that expose a
missed requirement or false report.

## Reduction queue

Every distinct candidate needs a disposition: investigate, incident only,
packaged, model reproduced, temporal evidence supported, duplicate, rejected,
or deferred. Explain deferrals and rejections. Prioritize strong consequences
and clear evidence, but do not silently drop the rest after packaging one example.

## Limitations and remaining work

State whether the authorized available scope has been fully inspected. If not,
list the exact remaining ranges and the next useful action. A context limit,
time limit, missing tool, or cost limit is a reason to leave a resumable queue,
not to call the entire search complete. Record what would be needed to finish.

## Sharing review

The owner reviews exact files and changes, including paths, metadata, comments,
fixtures, and result evidence. Raw history stays private. Record which items
were approved and any redactions that weaken evidence. Do not mark approval on
the owner's behalf. No publication is required to use this collection kit.
