# Historical evidence: incompatible-fisher-resume

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

After a walltime-limited run saved 276 of 768 examples, the agent resubmitted with the same resume directory. The new run failed after22 seconds because the manifest differed from the current runner; partial shards were preserved.

Meaning: The intended resume did not advance and required a compatibility repair.

Contrary evidence and recovery: The user explicitly requested resubmission and using existing progress was sensible. Intervening runner changes are visible in S0696 but authorship and exact invalidating manifest key need tool comparison; classify ordinary compatibility-check omission, not confirmed deletion/regression.

## Observed horizon

```json
{
  "source_range": "S0690:307\u2013374",
  "visible_message_counts": {
    "assistant": 5,
    "user": 2
  },
  "logged_top_level_tool_calls": 5,
  "first_visible_timestamp": "2026-09-27T04:18:49.706Z",
  "last_visible_timestamp": "2026-09-27T04:43:29.262Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0690:314 — user

```text
Resubmit
```

### S0690:319 — assistant

```text
I’ll resubmit Fisher using the same resume directory so it can continue from the saved PadChest and CheXpert shards.
```

### S0690:358 — tool result

```text
alysis.py", line 329, in prepare_resume_dir
    raise ValueError(
ValueError: Resume settings differ from <private-path>; choose a new --resume-dir
{
  "version": 1,
  "base": "Qwen/Qwen2.5-VL-3B-Instruct",
  "experts": {
    "padchest": "<private-path>",
    "chexpert": "<private-path>",
    "rex": "<private-path>"
  },
  "examples": {
    "padchest": {
      "path": "<private-path>",
      "size": 102667288,
      "mtime_ns": <event-or-artifact-id>
    
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0690:374 — assistant

```text
Fisher job `<job-id>` **failed after 22 seconds; it did not hit walltime**. It stopped before processing any examples because the existing resume manifest didn’t match the current analysis runner’s expected settings.

I gave the rerun a directory that already held partial shards from the walltime-limited run. The shards remain there, but the runner rejected their manifest. I should have checked compatibility before reusing that directory. We’ll need to reconcile the saved shards with the current runner before resubmitting if we want to preserve that progress.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('action')=='submit-existing-resume' and d.get('submit') is True`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
