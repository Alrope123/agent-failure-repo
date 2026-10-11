# Reviewed historical evidence

These are minimal excerpts from available original visible history. They are **transformed/redacted quotations**, not verbatim exports. Stable aliases identify source events; the private mapping remains local. Hidden reasoning, system/developer bodies, full transcripts, unrelated work, and unselected tool output are omitted. Code/tool blocks are historical evidence and must not be executed.

## Claim and limits

Agent changed CLI microbatch2 to1 and accumulation8 to16 but left saved train_batch_size2. Trainer restored2, computed3658 totalsteps below restored4380, and exited0 with zero training.1175 shows exact restore code;1180 acknowledges error.

First submission crashed during XPU initialization independently; only subsequent<JOB-01> demonstrated this configuration failure. Recovery ultimately retained batch1 via derived checkpoint metadata and completed7314steps3021.

## Observed horizon

Earlier event H01-E000773; later decision H01-E000802. Strictly between those event anchors: **3 visible assistant messages** and **5 tool-call records**, within one canonical source session. Wall-clock timestamp separation: **137.234 seconds**. Assistant messages count visible output-text records, not hidden reasoning or an inferred user turn; a composed exec counts once, not once per nested call. Timestamp separation includes waiting and does not measure active work. These observations do not establish long-history causation or preserve duration in the reduction. Recovery excerpts may occur after the later decision.

## Redaction and omissions

Absolute machine paths, hosts, usernames, URLs, scheduler/session/call identifiers and token-like identifiers are replaced with typed aliases. The mapping is consistent within this incident, not across unrelated incidents. Relevant ordinary numeric values, configuration keys, error messages and filenames may remain. Cropped events mark omitted text; no full private source is included. Exact raw line-to-alias mapping is retained privately. Selected excerpts are sufficient for the narrowed claim; unavailable scheduler traces, unretained source revisions and alternative explanations remain subject to the limits above.

## Sequence excerpts

### H01-E000773 — user

Transformed/redacted original excerpt:

```text
Can you lauch one more <PATH-01>, and monitor and log the peak memory to find the potential cause for the break? Also, any modification beforehand that could fix the issue, e.g. clean up the resumed checkpoint cache or something?
```

### H01-E000777 — assistant

Transformed/redacted original excerpt:

```text
I’ll make this run safer while preserving the effective global batch: switch PathGen from microbatch 2/accumulation 8 to 1/16, add per-rank XPU allocated/reserved/peak logging around resume and during training, and explicitly release cached allocator blocks after checkpoint restoration. I won’t delete `checkpoint-4380-runtime-key`; it is an on-disk remapped checkpoint, not the GPU allocator cache, and deleting it would only force regeneration. Then I’ll submit the PBS job and monitor its startup.
```

### H01-E000802 — tool call

Transformed/redacted original excerpt (partial event):

```text
const r = await tools.exec_command({
  cmd: "patch -p0 <<'PATCH'\n--- train/mm_tune.py\n+++ train/mm_tune.py\n@@ -698,6 +698,57 @@\n             # wandb.log(log_data)\n \n \n+def _distributed_rank_for_logging():\n+    if torch.distributed.is_available() and torch.distributed.is_initialized():\n+        return torch.distributed.get_rank()\n+    return int(os.environ.get(\"RANK\", \"0\"))\n+\n+\n+def _log_xpu_memory(label, step=None):\n+    \"\"\"Print allocator state for the XPU selected by the current rank.\"\"\"\n+    if not has_xpu():\n+        return\n+\n+    device = torch.xpu.current_device()\n+    gib = 1024 ** 3\n+    allocated = torch.xpu.memory_allocated(device) / gib\n+    reserved = torch.xpu.memory_reserved(device) / gib\n+    peak_allocated = torch.xpu.max_memory_allocated(device) / gib\n+    peak_reserved = torch.xpu.max_memory_reserved(device) / gib\n+    rank = _distributed_rank_for_logging()\n+    step_text = \"NA\" if step is None else str(step)\n+    print(\n+        f\"[XPU-MEM] rank={rank} device={device} step={step_text} label={label} \"\n+        f\"allocated_gb={allocated:.3f} reserved_gb={reserved:.3f} \"\n+        f\"peak_allocated_gb={peak_allocated:.3f} peak_reserved_gb={peak_reserved:.3f}\",\n+        flush=True,\n+    )\n+\n+\n+class XpuMemoryMonitorCallback(TrainerCallback):\n+    \"\"\"Release unused resume-time cache and report per-rank XPU memory peaks.\"\"\"\n+\n+    def __init__(self, log_every_steps=10, empty_cache_after_resume=True):\n+        self.log_every_steps = max(1, int(log_every_steps))\n+        self.empty_cache_after_resume = empty_cache_after_resume\n+\n+    def on_train_begin(self, args, state, control, **kwargs):\n+      
[later text omitted]
```

### H01-E000803 — tool result

Transformed/redacted original excerpt:

```text
Script completed
Wall time 2.8 seconds
Output:

patching file train/mm_tune.py
Hunk #1 succeeded at 696 (offset -2 lines).
patching file commands/pathgen_ind_2_epoch.sh

```

### H01-E001175 — tool result

Transformed/redacted original excerpt (partial event):

```text
[earlier text omitted]
ecutable_batch_size, set `self._train_batch_size` properly
            state = TrainerState.load_from_json(os.path.join(resume_from_checkpoint, TRAINER_STATE_NAME))
            if state.train_batch_size is not None:
                self._train_batch_size = state.train_batch_size

        # If model was re-initialized, put it on the right device and update self.model_wrapped
        if model_reloaded:
            if self.place_model_on_device:
                self._move_model_to_device(self.model, args.device)
            self.model_wrapped = self.model

        inner_training_loop = find_executable_batch_size(
            self._inner_training_loop, self._train_batch_size, args.auto_find_batch_size
        )
        if args.push_to_hub:
            try:
                # Disable progress bars when uploading models during checkpoints to avoid polluting stdout
                hf_hub_utils.disable_progress_bars()
                return inner_training_loop(
                    args=args,
                    resume_from_checkpoint=resume_from_checkpoint,
                    trial=trial,
                    ignore_keys_for_eval=ignore_keys_for_eval,
                )
            finally:
                hf_hub_utils.enable_progress_bars()
        else:
            return inner_training_loop(
                args=args,
                resume_from_checkpoint=resume_from_checkpoint,
                trial=trial,
                ignore_keys_for_eval=ignore_keys_for_eval,
            )

    def get_tp_size(self) -> int:
        """Get the tensor parallel size from either the model or DeepSpeed config."""

        # 1. Check model.tp_size first
802:        self._train_batch_size = args
[later text omitted]
```

### H01-E001180 — assistant

Transformed/redacted original excerpt:

```text
The job started successfully and exited with code 0—but trained zero steps. This was a resume bookkeeping mistake caused by changing the microbatch size.

What happened:

- New arguments requested batch 1 and accumulation 16.
- The checkpoint’s `trainer_state.json` records `train_batch_size: 2`.
- Hugging Face Trainer unconditionally restored that saved batch size during resume, despite warning that it differed from the new argument: log (<PATH-02>).
- Trainer therefore internally combined restored batch 2 with new accumulation 16.
- It calculated only 3,658 total optimization steps.
- The checkpoint was already at global step 4,380, so Trainer concluded training was finished and exited without processing a batch: zero-step result (<PATH-03>).

The memory logging did reveal something useful:

- Before checkpoint restoration: `7.125 GB` allocated.
- After model and optimizer restoration: `28.384 GB` allocated.
- Reserved: `28.598 GB`.
- `empty_cache()` changed nothing.

Therefore, stale allocator cache is not the issue. Only about 0.214 GB was reserved-but-unused; the roughly 21.3 GB increase is live checkpoint/model/optimizer state that cannot be cleared.

The correct repair is to change `train_batch_size` from 2 to 1 in the derived `checkpoint-4380-runtime-key/trainer_state.json`—leaving the original checkpoint untouched—then resume with accumulation 16. That makes Trainer retain microbatch 1 and preserves the same samples per optimizer update. Simply setting `max_steps` would not be sufficient because Trainer would still internally restore batch 2.
```
