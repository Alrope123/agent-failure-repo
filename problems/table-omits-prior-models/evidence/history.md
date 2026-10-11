# Historical evidence: Table formatting omits the two models just reported

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0557:103 — assistant

~~~~text
Both jobs in the “Get routing pattern” session completed successfully.

| Job | Status | Runtime |
|---|---|---:|
| `[job-1]` — `[model-1]` | PBS exit 0; delivered | ~13m |
| `[job-2]` — `[model-2]` | PBS exit 0; delivered | ~14m |

Both produced routing results for ReXVQA, EndoChat/C80, and PathMMU/PubMed using 100 samples each. No benchmark failures occurred; only harmless Transformers warnings about the `temperature` generation flag appeared.

Main finding: the `8bits_5k` model had relatively balanced vision routing, while the c
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0557:110 — user

~~~~text
Fill in the table in a google sheet friendly format:
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0557:120 — assistant

~~~~text
Assuming all three rows use the model `Standard Flex Untrained`, paste this tab-separated data into Google Sheets:
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0557:127 — user

~~~~text
No you have two models right? Add to the table I give you.
~~~~


### S0557:132 — assistant

~~~~text
Yes. The two completed models were added below the three existing rows.
~~~~
Omitted: remaining text in this event and intervening unrelated history.

## Assessment and horizon

Historical expected behavior: Include the two just-reported models when filling the comparison table, or clarify the terse formatting request before assuming baseline-only scope.

Meaning: The first delivered table did not include the results that motivated the follow-up.

Contrary evidence and recovery limits: The terse user request did not literally say append these two models. This is a narrow conversational scope omission with user clarification, not an unambiguous standing-project-rule violation.

Earlier anchor: S0557:7. Later decision anchor: S0557:120. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `set(d.get('rows',[]))=={'baseline-endo','baseline-rex','baseline-path'}`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
