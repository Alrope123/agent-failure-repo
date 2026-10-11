# Historical evidence: Missing local cache shards are reported as absent remote weights

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0439:120 — assistant

~~~~text
The root cause is consistent across all ranks: the source script’s model ID, `[model-1]`, resolves to a repository without model weight files. The jobs therefore failed during `from_pretrained`, before training began. I’m checking the repository’s established BTX launchers and local model cache to identify the intended loadable checkpoint; I won’t change the model or resubmit without clear evidence.
~~~~


### S0439:134 — user

~~~~text
No, download the snapshot separately then resubmit, it should exist.
~~~~


### S0439:146 — custom_tool_call_output

~~~~text
model-00001-of-00005.safetensors
model-00002-of-00005.safetensors
model-00003-of-00005.safetensors
model-00004-of-00005.safetensors
model-00005-of-00005.safetensors
16M	[path-1]
Filesystem
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0439:150 — assistant

~~~~text
The snapshot metadata confirms five expected safetensor shards, but none were cached; only the index/config files were present. There is sufficient shared storage, so I’m fetching the complete five-shard snapshot into a dedicated local directory now.
~~~~


### S0439:179 — assistant

~~~~text
The full snapshot download completed successfully, including all five weight shards. I’m validating shard completeness against the index and then switching only the three new launchers to the local snapshot path before resubmission.
~~~~


## Assessment and horizon

Historical expected behavior: Distinguish missing local cache shards from absent remote weights before proposing a model substitution; verify and download the requested snapshot.

Meaning: The user received an incorrect root-cause diagnosis and unnecessary proposal to change model identity.

Contrary evidence and recovery limits: No wrong-model submission occurred: agent asked before substitution. Original loading failure alone did not establish whether Hub weights existed; current metadata/download resolve it. This is a diagnostic evidence error, not demonstrated context loss.

Earlier anchor: S0439:98. Later decision anchor: S0439:120. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('remote_weights_exist') is False and d.get('next_action')=='switch_to_non_v2'`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
