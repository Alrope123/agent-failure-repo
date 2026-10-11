# Historical evidence: Analysis defaults omit dense checkpoint decoder keys

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0668:9 — user

~~~~text
Implement **three standalone analysis methods** for Qwen2.5-VL experts fine-tuned from the same base:

1. **Task-vector similarity and update magnitude.** Subtract the base checkpoint from each expert to obtain its fine-tuning updates. Calculate pairwise cosine similarity between updates, plus their absolute magnitude and magnitude relative to the base weights.
2. **Sign conflicts among substantial updates.** Retain a configurable percentage of the largest-magnitude, nonzero updates within each parameter group. For each expert pair, report how much their selected coordinates overlap and how of
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0668:36 — assistant

~~~~text
The checkpoint code uses `model.visual.blocks` for vision, `model.visual.merger` for the connector, and `model.language_model` for the decoder. I’ll make the group rules configurable and let component groups overlap with the expertized FFN and shared-parameter groups.
~~~~


### S0672:83 — custom_tool_call_output

~~~~text
model.layers.0.input_layernorm.weight
model.layers.0.mlp.experts.0.down_proj.weight
model.layers.0.mlp.experts.0.gate_proj.weight
model.layers.0.mlp.experts.0.up_proj.weight
model.layers.0.mlp.experts.1.down_proj.weight
model.layers.0.mlp.experts.1.gate_proj.weight
model.layers.0.mlp.experts.1.up_pr
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0672:93 — assistant

~~~~text
The targeted tests pass with third party pytest plugins disabled; the normal pytest run crashes during plugin startup. I also found a real grouping bug: the default `language_decoder` pattern misses this project’s `model.layers.*` checkpoint keys. I’m correcting that and adding a regression check against the checkpoint key layout.
~~~~


### S0672:135 — assistant

~~~~text
Resumed the expert adaptation analysis in FlexBagel. I fixed the default decoder group so it matches `model.layers.*` checkpoint keys, made sign conflict analysis process tensors incrementally, and added a regression test and documentation.

All 5 targeted tests pass with third party pytest plugins disabled. The normal pytest startup crashes in this environment, so I could not verify that invocation. The changes are uncommitted in expert_analysis.py ([path-1]), [test_expert_analysis.py]([path-2]
~~~~
Omitted: remaining text in this event and intervening unrelated history.

## Assessment and horizon

Historical expected behavior: Match analysis groups to actual checkpoint parameter keys so the requested language-decoder analysis includes its parameters.

Meaning: The default language-decoder analysis could silently omit decoder parameters despite claiming support for comparing vision, connector, and decoder. No original large-run incorrect scientific result is established.

Contrary evidence and recovery limits: Users can configure custom group patterns, and the initial synthetic tests passed. Actual downstream erroneous report before recovery is unavailable. The original implementation and later correction are separate sessions S0668 and S0672; source aliases should preserve both.

Earlier anchor: S0668:9. Later decision anchor: S0668:36. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('language_decoder_keys')==[]`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
