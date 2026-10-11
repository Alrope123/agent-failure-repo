# Historical evidence: A queue switch retains the previous queue-only interpreter

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0585:203 — user

~~~~text
Submit [path-1] on capacity queue with 12h walltime.
~~~~


### S0585:231 — assistant

~~~~text
Aurora Watch’s session resolver is unavailable in this environment because the managed standalone Codex install is missing, so I’m proceeding with the equivalent explicit PBS submission and will verify it directly. The launcher was already corrected to use the next-eval training Python override.
~~~~


### S0585:284 — custom_tool_call_output

~~~~text
Training Python is not executable: [path-2]
~~~~


### S0585:289 — assistant

~~~~text
Job `[job-1]` failed during wrapper setup, before training started.

- State: `F` (finished)
- Exit status: `2`
- Runtime: ~2 seconds
- Cause: `[path-2]` was not executable on the capacity node.
- No model loading or GPU training occurred.

The Lmod warnings were benign. The output is in [flex-rexgradient-btx-capacity.o[job-1]] (redacted path).
~~~~


### S0585:303 — assistant

~~~~text
The failure was caused by using the next-eval-only training venv on `capacity`. I’ll resubmit with the capacity-available `[path-4]` environment while keeping the launcher’s `FLEXBAGEL_PYTHON` override intact, then verify the new job.
~~~~


### S0585:333 — assistant

~~~~text
Fixed the submission configuration to use the capacity-compatible `[path-4]` environment and resubmitted successfully.

- Job: `[job-2]`
- State: queued (`Q`)
- Queue: `capacity`
- Walltime: 12 hours
- Logs: `[path-5]`
~~~~


## Assessment and horizon

Historical expected behavior: Use an interpreter available on the requested capacity queue while retaining the requested 12-hour walltime.

Meaning: A requested training allocation performed no training and required a new submission.

Contrary evidence and recovery limits: The launch script itself was intentionally made portable using FLEXBAGEL_PYTHON. The submission variable, not that script edit, caused failure. Earlier S0471 is a separate episode; no claim that memory mechanism is proven.

Earlier anchor: S0585:203. Later decision anchor: S0585:231. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('queue')=='capacity' and d.get('train_venv')=='venvs/next-train' and d.get('submit') is True`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
