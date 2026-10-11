# Historical evidence: Text-only support omits distributed unused-branch handling

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0585:456 — user

~~~~text
Can you make it an output for mm\_tune to work with no image data?
~~~~


### S0585:688 — assistant

~~~~text
Implemented in mm_tune.py ([path-1]):

- Preserves text-only rows with `images=[]`.
- Supports missing `images` fields.
- Adds a stable mixed image/text Arrow schema.
- Allows batches without `pixel_values` or `image_grid_thw`.
- Keeps image-backed training behavior intact.

Verified with:

- Actual synthetic datasets: 8/8 text-only examples retained.
- Text-only VLM collator batch.
- Mixed image/text-only collator batch.
- Syntax check.
~~~~


### S0585:820 — custom_tool_call_output

~~~~text
Expected to have finished reduction in the prior iteration before starting a new one. This error indicates that your module has parameters that were not used in producing loss. You can enable unused parameter detection by passing the keyword argument `find_unused_parameters=True` to `torch.nn.parall
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0585:832 — assistant

~~~~text
The last four jobs split into two failures and two successes:

- `[job-1]` — 4-expert, 10k synthetic: failed after 5m05s, exit `143`. Dataset loading succeeded, but DDP raised an unused-parameter reduction error because text-only data leaves vision parameters unused. No final checkpoint was produced. Log (<[path-2]>)

- `[job-2]` — 3-expert FP32, 10k synthetic: same DDP unused-parameter failure after 4m15s. Log (<[path-3]>)

- `[job-3]` — 4-expert, 5k vision-on
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0585:946 — assistant

~~~~text
Added `--ddp_find_unused_parameters True` to both launchers and resubmitted:

- `[job-4]`
- `[job-5]`

Both are queued on `next-eval` with 6-hour walltime.
~~~~


## Assessment and horizon

Historical expected behavior: Make text-only training work through distributed backward, accounting for vision parameters that do not participate in the loss.

Meaning: Text-only data reached training but the requested distributed jobs still could not complete.

Contrary evidence and recovery limits: Preprocessing and collator checks genuinely passed. The delivered summary scoped its verification to those checks and did not claim a successful distributed run. DDP was an existing downstream issue exposed by modality change; no long-history causal attribution.

Earlier anchor: S0585:456. Later decision anchor: S0585:688. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('find_unused_parameters') is False and d.get('trainable_vision') is True and d.get('ready') is True`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
