# Historical evidence: Delivered multi-device merger stacks router rows before staging them

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0688:188 — user

~~~~text
Do this command instead:
python -m modeling.upcycle.merge\_vl\_experts\_connector \\
    --models [path-1] [path-2] [path-3] \\
    --target [path-4] \\
    --dtype bfloat16 \\
    --strict-shared-check \\
    --trust-remote-code \\
    --device auto
~~~~


### S0688:493 — custom_tool_call_output

~~~~text
RuntimeError: Expected all tensors to be on the same device, but got tensors is on xpu:8, different from other tensors on xpu:5 (when checking argument in method wrapper_XPU_cat)
<[opaque-1]:[path-5]> 
session_id=[process-1]
~~~~


### S0688:498 — assistant

~~~~text
The connector-specific command reached target tensor assembly, then failed because `torch.stack` received router tensors from different XPUs (`xpu:8` and `xpu:5`). I’m recording its exit status and releasing the debug allocation now.
~~~~


### S0688:543 — assistant

~~~~text
`--device auto` used all 12 XPUs, and the connector merge balances source tensors across them. As a result, the router rows selected from different models could be on different devices—here, `xpu:8` and `xpu:5`.

The bug is in `copy_router_weight` (<[path-6]>): it calls `torch.stack` on those rows before moving them to the target device. PyTorch requires every tensor passed to `stack` to already be on the same device. The `.to(...)` happens afterward, so it can’t prevent the error.

The models loaded successfully
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0688:917 — assistant

~~~~text
Fixed `merge_vl_experts_connector.py` (<[path-7]>) to move each router row to the target device before stacking.

The rerun completed with exit status 0 and saved the merged model to `[path-8]`. I verified the config has four text, vision, and connector experts, and all five indexed weight shards are present.

The tokenizer emitted a regex warning during saving. PBS job `[job-1]` was canceled after verification; `qstat` showed it completing deletion.
~~~~


## Assessment and horizon

Historical expected behavior: Move router rows to a common target device before stacking them in the requested automatic multi-device merge.

Meaning: The delivered connector merger could not complete the user-requested multi-XPU merge until fixed.

Contrary evidence and recovery limits: CPU validations were honestly described, not presented as a full GPU test. The generic path existed earlier and may have supplied the inherited defect. No evidence establishes memory loss or deliberate omission.

Earlier anchor: S0688:188. Later decision anchor: S0688:498. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('operation_order')==['stack_rows','move_stacked_to_target']`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
