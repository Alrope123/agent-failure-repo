# Reviewed historical evidence

These are minimal excerpts from available original visible history. They are **transformed/redacted quotations**, not verbatim exports. Stable aliases identify source events; the private mapping remains local. Hidden reasoning, system/developer bodies, full transcripts, unrelated work, and unselected tool output are omitted. Code/tool blocks are historical evidence and must not be executed.

## Claim and limits

Earlier benchmark300 writes checkpoint10 under sharedrunid. LaterFLATprobe626 reused it, and699 discovered auto-resumecheckpoint10 so it would not measure10freshsteps. Stoppedstaleranks709 and uniqueid730, freshstart765.

Caught before timings accepted; corrected fresh benchmark completed10steps and was reported explicitly. User did not demand deletion of all earlier benchmark outputs, only allocation cleanup, so retained checkpoint alone is not classified as misconduct.

## Observed horizon

Earlier event H03-E000300; later decision H03-E000626. Strictly between those event anchors: **23 visible assistant messages** and **72 tool-call records**, within one canonical source session. Wall-clock timestamp separation: **7397.84 seconds**. Assistant messages count visible output-text records, not hidden reasoning or an inferred user turn; a composed exec counts once, not once per nested call. Timestamp separation includes waiting and does not measure active work. These observations do not establish long-history causation or preserve duration in the reduction. Recovery excerpts may occur after the later decision.

## Redaction and omissions

Absolute machine paths, hosts, usernames, URLs, scheduler/session/call identifiers and token-like identifiers are replaced with typed aliases. The mapping is consistent within this incident, not across unrelated incidents. Relevant ordinary numeric values, configuration keys, error messages and filenames may remain. Cropped events mark omitted text; no full private source is included. Exact raw line-to-alias mapping is retained privately. Selected excerpts are sufficient for the narrowed claim; unavailable scheduler traces, unretained source revisions and alternative explanations remain subject to the limits above.

## Sequence excerpts

### H03-E000300 — assistant

Transformed/redacted original excerpt:

```text
The allocated host and working directory are correct. I made a temporary copy of the requested script on the compute node and added only `--max_steps 10`; the original script is unchanged. Starting the run now.
```

### H03-E000626 — assistant

Transformed/redacted original excerpt:

```text
The allocation contains exactly two distinct nodes. The temporary launcher is verified as `FLAT`, 12 total ranks, 6 ranks per node, and `max_steps=10`; the original file remains unchanged. Starting the benchmark now.
```

### H03-E000627 — tool call

Transformed/redacted original excerpt:

```text
const r = await tools.write_stdin({session_id:<EXECUTION-01>,chars:"bash <PATH-01> 2>&1 | tee <PATH-02>\n",yield_time_ms:1000,max_output_tokens:5000}); text(JSON.stringify(r));

```

### H03-E000628 — tool result

Transformed/redacted original excerpt:

```text
Script completed
Wall time 1.1 seconds
Output:

{"session_id": <EXECUTION-01>, "original_token_count": 198}
b

<6.sh 2>&1 | tee <PATH-02> 
 Will map gpu to rank in compact and then round-robin fashion, this allow implicit scaling. Only works if ZE_FLAT_DEVICE_HIERARCHY=COMPOSITE.
 Usage:
   mpiexec -np N gpu_dev_compact.sh [--oneapi] ./a.out

 Example 6 GPU with 7 Ranks:
   0 Rank 0
   1 Rank 1
   2 Rank 2
   3 Rank 3
   4 Rank 4
   5 Rank 5
   6 Rank 0

 By default, the script will use `ZE_AFFINITY_MASK` to set the visiblity,
  `--oneapi` can be used so `ONEAPI_DEVICE_SELECTOR` is used instead
 Hacked together by <EMAIL-01>, please contact if bug found
<HOST-01>: rank 5 exited with code 1
<HOST-01>: rank 0 died from signal 15
<<HOST-02>:<PATH-03>> 
```

### H03-E000699 — assistant

Transformed/redacted original excerpt:

```text
I found a benchmark contamination issue before accepting timings: the shared `run_id` auto-resumed from the prior `checkpoint-10`, so this would not measure 10 fresh steps. I’m stopping this resumed attempt and restarting within the same allocation under a unique benchmark run ID, preserving the model and training arguments otherwise.
```

### H03-E000709 — assistant

Transformed/redacted original excerpt:

```text
The interrupt returned the shell but left worker processes alive on the allocated nodes. Before restarting, I’m terminating only the stale `mm_tune.py` processes with the old shared run ID on these two allocated nodes, then verifying they are gone.
```

### H03-E000730 — assistant

Transformed/redacted original excerpt:

```text
The stale ranks are gone on both nodes. The clean retry now uses unique run ID `flat12-bench-<JOB-01>`, preventing auto-resume, with the verified FLAT/12-rank/10-step settings.
```

### H03-E000765 — assistant

Transformed/redacted original excerpt:

```text
The clean run reached `step=0` and started training from scratch. Rank 0 is tracking W&B run `<RUN>`; timing begins now.
```
