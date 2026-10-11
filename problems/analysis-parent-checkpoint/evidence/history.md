# Historical evidence: analysis-parent-checkpoint

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

The new RRG24 analysis command selected the ReX parent directory instead of its usable final subdirectory. Both submitted analysis jobs failed while loading Qwen2Config rather than the VL configuration. The user corrected the path; the combined checkpoint analysis subsequently succeeded.

Meaning: Two GPU jobs failed before producing requested outputs.

Contrary evidence and recovery: The nearby pre-existing upcycle command also used the parent path; copying it explains the choice without proving memory loss. The initial check established directory existence, not a loadable checkpoint. The Fisher retry additionally encountered a stale manifest.

## Observed horizon

```json
{
  "source_range": "S0690:9\u2013253",
  "visible_message_counts": {
    "user": 5,
    "assistant": 15
  },
  "logged_top_level_tool_calls": 34,
  "first_visible_timestamp": "2026-09-26T19:08:49.352Z",
  "last_visible_timestamp": "2026-09-26T21:32:33.657Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0690:9 — user

```text
Create another set of commands under <private-path> so I can do with a different set of models.
```

### S0690:67 — assistant

```text
The alternate checkpoints and their three JSONL files are present. I’ll add a matching command trio for PadChest, CheXpert, and ReX, with a separate output directory so their results and Fisher resume shards stay isolated.
```

### S0690:96 — user

```text
Good, submit them as well. Combine the first two experiment as one job. Third as a standalone job. Submit everything onto next-eval queue.
```

### S0690:253 — assistant

```text
The corrected Fisher job failed before processing any examples. Its resume folder had a manifest from the earlier run that recorded ReX’s old parent path. Since the command now points to `.../final`, the runner rejected the mismatched resume settings.

The fix is to use a fresh resume directory and submit Fisher again. The existing folder contains only its manifest; no Fisher progress was saved. I haven’t resubmitted the failed job.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('model_path')=='models/rex' and d.get('submit') is True`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
