# Reviewed historical evidence

These are minimal excerpts from available original visible history. They are **transformed/redacted quotations**, not verbatim exports. Stable aliases identify source events; the private mapping remains local. Hidden reasoning, system/developer bodies, full transcripts, unrelated work, and unselected tool output are omitted. Code/tool blocks are historical evidence and must not be executed.

## Claim and limits

User530 requests FLAT benchmarking. Agent626 launched FLAT with inherited gpu_dev_compact wrapper;628 tool output rejects because wrapper only supports COMPOSITE.632 admits failure beforetraining;647 selects gpu_tile_compact;664correctedlaunch.

Fixed inside the same allocation, without an additional PBS job; benchmark eventually completed. No earlier universal wrapper rule is required to establish this local mode incompatibility.

## Observed horizon

Earlier event H03-E000530; later decision H03-E000626. Strictly between those event anchors: **5 visible assistant messages** and **22 tool-call records**, within one canonical source session. Wall-clock timestamp separation: **286.2 seconds**. Assistant messages count visible output-text records, not hidden reasoning or an inferred user turn; a composed exec counts once, not once per nested call. Timestamp separation includes waiting and does not measure active work. These observations do not establish long-history causation or preserve duration in the reduction. Recovery excerpts may occur after the later decision.

## Redaction and omissions

Absolute machine paths, hosts, usernames, URLs, scheduler/session/call identifiers and token-like identifiers are replaced with typed aliases. The mapping is consistent within this incident, not across unrelated incidents. Relevant ordinary numeric values, configuration keys, error messages and filenames may remain. Cropped events mark omitted text; no full private source is included. Exact raw line-to-alias mapping is retained privately. Selected excerpts are sufficient for the narrowed claim; unavailable scheduler traces, unretained source revisions and alternative explanations remain subject to the limits above.

## Sequence excerpts

### H03-E000530 — user

Transformed/redacted original excerpt:

```text
Now can we try using FLAT (12 GPUs) instead, and getting two nodes for debug using <PATH-01>

```

### H03-E000626 — assistant

Transformed/redacted original excerpt:

```text
The allocation contains exactly two distinct nodes. The temporary launcher is verified as `FLAT`, 12 total ranks, 6 ranks per node, and `max_steps=10`; the original file remains unchanged. Starting the benchmark now.
```

### H03-E000627 — tool call

Transformed/redacted original excerpt:

```text
const r = await tools.write_stdin({session_id:<EXECUTION-01>,chars:"bash <PATH-02> 2>&1 | tee <PATH-03>\n",yield_time_ms:1000,max_output_tokens:5000}); text(JSON.stringify(r));

```

### H03-E000628 — tool result

Transformed/redacted original excerpt:

```text
Script completed
Wall time 1.1 seconds
Output:

{"session_id": <EXECUTION-01>, "original_token_count": 198}
b

<6.sh 2>&1 | tee <PATH-03> 
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
<<HOST-02>:<PATH-04>> 
```

### H03-E000647 — assistant

Transformed/redacted original excerpt:

```text
Aurora’s correct wrapper for `FLAT` is `gpu_tile_compact.sh`; it maps one flat GPU tile per rank. I’ll keep your requested 12 total ranks across two nodes (`6` per node), meaning 12 flat devices total. This uses half of each node’s 12 flat devices; using every flat device on both nodes would instead require 24 ranks.
```

### H03-E000664 — assistant

Transformed/redacted original excerpt:

```text
The corrected launch is healthy: all 12 ranks started across both nodes with `ZE_FLAT_DEVICE_HIERARCHY=FLAT`, each bound to one flat device. Model loading is in progress.
```
