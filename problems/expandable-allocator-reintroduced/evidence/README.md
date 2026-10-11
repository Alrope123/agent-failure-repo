# Reviewed historical evidence

These are minimal excerpts from available original visible history. They are **transformed/redacted quotations**, not verbatim exports. Stable aliases identify source events; the private mapping remains local. Hidden reasoning, system/developer bodies, full transcripts, unrelated work, and unselected tool output are omitted. Code/tool blocks are historical evidence and must not be executed.

## Claim and limits

Earlier2460 oneCCL invalid USM error established expandable_segments unusable, user2466 requested removal and2492 confirmed it. Later3653/3663 added the same setting to conversion and training;3668 verified exports;3671 submitted.3702 first broadcast again failed invalidUSM.

The new DeepSpeed converter changed other code and collectives, so the setting is not independently proven the sole cause of later pointer failure. Original removal request scoped PathGen script; transferability is inferred from same runtime and pointer constraints rather than universal prohibition.

## Observed horizon

Earlier event H01-E002460; later decision H01-E003653. Strictly between those event anchors: **96 visible assistant messages** and **230 tool-call records**, within one canonical source session. Wall-clock timestamp separation: **77381.8 seconds**. Assistant messages count visible output-text records, not hidden reasoning or an inferred user turn; a composed exec counts once, not once per nested call. Timestamp separation includes waiting and does not measure active work. These observations do not establish long-history causation or preserve duration in the reduction. Recovery excerpts may occur after the later decision.

## Redaction and omissions

Absolute machine paths, hosts, usernames, URLs, scheduler/session/call identifiers and token-like identifiers are replaced with typed aliases. The mapping is consistent within this incident, not across unrelated incidents. Relevant ordinary numeric values, configuration keys, error messages and filenames may remain. Cropped events mark omitted text; no full private source is included. Exact raw line-to-alias mapping is retained privately. Selected excerpts are sufficient for the narrowed claim; unavailable scheduler traces, unretained source revisions and alternative explanations remain subject to the limits above.

## Sequence excerpts

### H01-E002460 — assistant

Transformed/redacted original excerpt:

```text
Job `<JOB-01>` started after waiting about 34 minutes, but failed before any training steps.

`expandable_segments:True` is incompatible with the current oneCCL/XPU stack. During the first distributed barrier, oneCCL rejected the expandable-segment allocation:

[code fence removed]text
oneCCL ... allreduce - invalid usm pointer type:
unknown for device type: gpu
[code fence removed]

All 12 ranks encountered it, and the job exited with status 1 after 2:57. This was not an OOM, and checkpoint 4380 was not modified.

The error is in pathgen_ind_2_epoch.o<JOB-01> (<PATH-01>).

So both allocator workarounds are unusable here:

- Periodic `empty_cache()` causes a GPU page fault immediately afterward.
- `expandable_segments` produces pointers oneCCL cannot use.

The environment setting is still present in the command script and should be removed before another submission.
```

### H01-E002492 — assistant

Transformed/redacted original excerpt:

```text
Removed `PYTORCH_ALLOC_CONF=expandable_segments:True` and its echo. The script validates successfully; batch size remains 2 and gradient accumulation remains 8. No job was submitted.
```

### H01-E003653 — tool call

Transformed/redacted original excerpt:

```text
const p=`7a8
> export PYTORCH_ALLOC_CONF=expandable_segments:True
`;
const r=await tools.write_stdin({session_id:<EXECUTION-01>,chars:p+"\u0004\u0004",yield_time_ms:1000,max_output_tokens:500}); text(JSON.stringify(r));

```

### H01-E003654 — tool result

Transformed/redacted original excerpt:

```text
Script completed
Wall time 0.1 seconds
Output:

{"exit_code": 0, "original_token_count": 35}
7a8
> export PYTORCH_ALLOC_CONF=expandable_segments:True
patching file codes/FlexBagel/commands/convert_surge396k_checkpoint_to_zero1.sh

```

### H01-E003663 — tool call

Transformed/redacted original excerpt:

```text
const p=`6a7
> export PYTORCH_ALLOC_CONF=expandable_segments:True
`;
const r=await tools.write_stdin({session_id:<EXECUTION-02>,chars:p+"\u0004\u0004",yield_time_ms:1000,max_output_tokens:500}); text(JSON.stringify(r));

```

### H01-E003717 — assistant

Transformed/redacted original excerpt:

```text
There is no active job and no partial destination checkpoint, so the failed attempt did not leave cache to clean. The converter currently hands a CPU-loaded model directly to DeepSpeed; on this stack, that internal move is producing the invalid pointer seen by oneCCL. I’m checking the exact engine implementation before changing it.
```
