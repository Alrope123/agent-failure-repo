# Reviewed historical evidence

These are minimal excerpts from available original visible history. They are **transformed/redacted quotations**, not verbatim exports. Stable aliases identify source events; the private mapping remains local. Hidden reasoning, system/developer bodies, full transcripts, unrelated work, and unselected tool output are omitted. Code/tool blocks are historical evidence and must not be executed.

## Claim and limits

ReXGPUbenchmarktwicefailedonlinecache227/233; offlineworked254. Agent513 carriedfixintoReXandSurgesubmissionsbutnotPathGen. Afteruser525submitthree,PathGenmissing-shardfailed562whileotherstworan;578confirmedonlyPathGenlackedofflinevars;607fixedresubmitted.

PathGen earlier online benchmark had succeeded; cache race was nondeterministic and exact root mechanism is diagnosed rather than independently instrumented. No explicit standing rule required offline mode; this is incomplete propagation of a verified same-model launch condition.

## Observed horizon

Earlier event H05-E000227; later decision H05-E000513. Strictly between those event anchors: **17 visible assistant messages** and **66 tool-call records**, within one canonical source session. Wall-clock timestamp separation: **1594.63 seconds**. Assistant messages count visible output-text records, not hidden reasoning or an inferred user turn; a composed exec counts once, not once per nested call. Timestamp separation includes waiting and does not measure active work. These observations do not establish long-history causation or preserve duration in the reduction. Recovery excerpts may occur after the later decision.

## Redaction and omissions

Absolute machine paths, hosts, usernames, URLs, scheduler/session/call identifiers and token-like identifiers are replaced with typed aliases. The mapping is consistent within this incident, not across unrelated incidents. Relevant ordinary numeric values, configuration keys, error messages and filenames may remain. Cropped events mark omitted text; no full private source is included. Exact raw line-to-alias mapping is retained privately. Selected excerpts are sufficient for the narrowed claim; unavailable scheduler traces, unretained source revisions and alternative explanations remain subject to the limits above.

## Sequence excerpts

### H05-E000227 — assistant

Transformed/redacted original excerpt:

```text
ReXGradient’s first attempt failed before data loading because one rank briefly saw an incomplete Hugging Face shard cache while the other ranks were loading the same model concurrently. PathGen had already proven the model itself is valid; the shared cache is now populated, so I’m retrying the unchanged isolated 10-step wrapper within the same allocation. The failed attempt produced no model checkpoint.
```

### H05-E000233 — assistant

Transformed/redacted original excerpt:

```text
The second ReXGradient launch hit the same transient shard-resolution failure on a different rank, confirming a concurrent online cache-resolution race rather than a bad rank or dataset. I’m switching only the launch environment to Hugging Face offline mode, which forces all ranks to use the already-cached model bytes and leaves the training configuration unchanged.
```

### H05-E000254 — assistant

Transformed/redacted original excerpt:

```text
The offline ReXGradient launch has passed the failure point and initialized its ZeRO-1 optimizer successfully. It is now in the 10-step loop; I’ll use this successful run’s timing only, excluding the two failed pre-training launches from the estimate.
```

### H05-E000513 — assistant

Transformed/redacted original excerpt:

```text
The allocation is now fully gone from `qstat`. I’m also carrying the successful launch condition into the ReXGradient and Surge396K PBS files: Hugging Face offline mode for model loading, which prevents the exact concurrent shard-cache race observed during debugging while leaving W&B reporting and all training settings unchanged.
```

### H05-E000514 — tool call

Transformed/redacted original excerpt:

```text
const r = await tools.exec_command({"cmd":"sed -i '/^echo \"Training start\"/i export HF_HUB_OFFLINE=1\\nexport TRANSFORMERS_OFFLINE=1\\n' <PATH-01> <PATH-02>; for f in <PATH-03> <PATH-01> <PATH-02>; do bash -n \"$f\" || exit 1; done; rg -n '^#PBS -l walltime|^export HF_HUB|^export TRANSFORMERS|^bash commands/' <PATH-04>,rexgradient_ind_from_pub,surge396k_ind_2_from_pub}.sh; test ! -e <PATH-05>; test ! -e <PATH-06>; qstat -u \"$USER\"","workdir":"<PATH-07>","yield_time_ms":10000,"max_output_tokens":5000,"sandbox_permissions":"require_escalated","justification":"May I add and verify the tested offline-cache environment to the ReXGradient and Surge396K submissions, then perform the final cleanup and job-status checks?"});
text(r.output);

```

### H05-E000515 — tool result

Transformed/redacted original excerpt:

```text
Script completed
Wall time 3.9 seconds
Output:

<PATH-08> -l walltime=56:00:00
<PATH-09> HF_HUB_OFFLINE=1
<PATH-10> TRANSFORMERS_OFFLINE=1
<PATH-11> commands/surge396k_ind_2_from_pub.sh
<PATH-12> -l walltime=33:00:00
<PATH-13> HF_HUB_OFFLINE=1
<PATH-14> TRANSFORMERS_OFFLINE=1
<PATH-15> commands/rexgradient_ind_from_pub.sh
<PATH-16> -l walltime=28:00:00
<PATH-17> commands/pathgen_ind_from_pub.sh

```

### H05-E000562 — assistant

Transformed/redacted original excerpt:

```text
Yes—PathGen job `<JOB-01>` failed after 1 minute 24 seconds. Rank 8 hit the same Hugging Face shard-cache race seen during debugging: it could not resolve `model-00001-of-00002.safetensors`, then MPI terminated the other ranks. ReXGradient and Surge396K are still running; I’m checking their logs briefly to confirm they have reached training steps rather than only remaining alive.
```

### H05-E000578 — assistant

Transformed/redacted original excerpt:

```text
It was a concurrent Hugging Face cache-resolution race, not a corrupt model.

All 12 MPI ranks called `from_pretrained()` simultaneously against the same shared Hugging Face cache. In online mode, each rank checks repository metadata and resolves shard paths independently. Rank 8 briefly observed an incomplete/inconsistent cache snapshot and reported:

`model-00001-of-00002.safetensors` missing

Once rank 8 exited, MPI terminated the remaining ranks, producing exit status `143`.

Why only PathGen failed:

- ReXGradient and Surge396K submissions had `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`.
- PathGen did not.
- Offline mode uses the already-complete cached snapshot without concurrent online metadata resolution.

Evidence that the model itself is intact: the same model successfully loaded during debugging and in the two currently running jobs. The fix is to add those two offline variables to PathGen and resubmit it.
```

### H05-E000607 — assistant

Transformed/redacted original excerpt:

```text
PathGen was corrected and resubmitted successfully.

- New job: `<JOB-02>`
- State: queued
- Queue: `capacity`
- Walltime: 28 hours
- Offline Hugging Face cache protection enabled
```
