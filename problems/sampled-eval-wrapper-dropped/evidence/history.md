# Historical evidence: Same-settings evaluation drops the operative random-sampling wrapper

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0537:7 — user

~~~~text
Evaluate [path-1] and [path-2] on next-eval queue. Subsample 5000 from every subbencharmks in Endochat. Don't take the fist 5000, sample them uniformly at random. For RexVQA  and pathMMU, don't change anything.
~~~~


### S0537:553 — user

~~~~text
Evaluate [path-3] Same settings.
~~~~


### S0537:570 — assistant

~~~~text
The inferred run ID is `[model-1]`. I’ll submit the same three-job `next-eval` layout as before: ReXVQA unchanged, plus C80+EndoVis and CoPESD with the 5,000-example EndoChat sampling.
~~~~


### S0537:670 — custom_tool_call_output

~~~~text
2068:Done. 17139 results saved to results/[model-2]/[model-1]/c80/test_result.json
4136:Done. 8638 results saved to results/[model-2]/[model-1]/endovis/test_result.json
~~~~


### S0537:674 — assistant

~~~~text
Event `[opaque-1]` was already delivered. PBS job `[job-1]` succeeded, but the requested evaluation settings were not met: no 5,000-item sampling occurred.

- C80: **17,139** examples, normalized exact match **3,870 / 17,139 = 22.58%**. Results (<[path-4]>)
- EndoVis: **8,638** examples, normalized exact match **343 / 8,638 = 3.97%**. Results (<[path-5]>)

The logs confirm full-dat
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0537:716 — assistant

~~~~text
Event `[opaque-2]` was already delivered. PBS job `[job-2]` completed successfully, but the requested 5,000-example sampling requirement was not met.

- CoPESD: **31,717** examples, normalized exact match **1,725 / 31,717 = 5.44%**
- The log reports full-dataset completion and has no uniform-random 5,000-item sampling line.
- Results (<[path-6]>)

This exact-match value is a diagnostic, not an official aggregate score. No resubmission was performed.
~~~~


### S0537:854 — assistant

~~~~text
No. I found a configuration issue: the running EndoChat jobs `[job-3]` and `[job-4]` use a wrapper that does not export `ENDOCHAT_SAMPLE_SIZE=5000` or seed `20260919`; the split launcher also does not set them. They are therefore likely evaluating the full datasets.

The correct sampler exists and uses uniform random sampling with seed `20260919`. I have not canceled or resubmitted the running jobs. Do you want me to cancel `[job-3]`/`[job-4]` and resubmit them with the correct 5,000-example sampler?
~~~~


### S0537:912 — assistant

~~~~text
Done.

Canceled the incorrectly configured jobs:

- `[job-3]` — CoPESD
- `[job-4]` — C80 + EndoVis

Resubmitted with the corrected uniform sampler (`5,000`, seed `20260919`):

- CoPESD: `[job-5]`
- C80 + EndoVis: `[job-6]`

Both replacements are queued on `next-eval`.
~~~~


## Assessment and horizon

Historical expected behavior: Retain uniform-random 5,000-example sampling for every EndoChat subset when applying the same evaluation settings to another model.

Meaning: The delivered evaluation did not satisfy the retained sample-count/sampling contract and spent compute evaluating full datasets. The same-settings delivery also omitted PathMMU, but this reduction isolates sampling.

Contrary evidence and recovery limits: Agent honestly reports configuration failure when inspecting completed outputs. No evidence proves hidden memory loss; an earlier correct wrapper existed and was available in the same session. Later recovery canceled only incorrect jobs and preserved unrelated work.

Earlier anchor: S0537:7. Later decision anchor: S0537:570. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('wrapper')=='standard' and d.get('sampling')=='full'`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
