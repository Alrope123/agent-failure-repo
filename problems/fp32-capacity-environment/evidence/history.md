# Historical evidence: fp32-capacity-environment

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

The agent submitted three capacity jobs but left the FP32 job on flexolmo-next-train; after a user reminder it confirmed the mismatch while the job was still queued.

Meaning: The submission was configured with the wrong runtime, requiring replacement before execution.

Contrary evidence and recovery: The other two jobs used the correct environment. No compute-time failure was established; the mismatched job remained queued.

## Observed horizon

```json
{
  "source_range": "S0471:9\u2013110",
  "visible_message_counts": {
    "user": 2,
    "assistant": 5
  },
  "logged_top_level_tool_calls": 17,
  "first_visible_timestamp": "2026-09-16T05:10:44.435Z",
  "last_visible_timestamp": "2026-09-16T05:16:22.155Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0471:9 — user

```text
Submit <private-path>
<private-path>
<private-path> onto capacity queue.
```

### S0471:78 — assistant

```text
No duplicate of these jobs is currently queued. I’ll submit three one-node jobs with the established FlexBagel environment: 9-hour limits for the two 20k-sample runs and 6 hours for the 15k-sample FP32 run, all explicitly overriding the wrapper to `capacity`. Each will be registered to this session for completion follow-up.
```

### S0471:83 — user

```text
Be careful that capacity queue and next eval queue has different environement, don't forget to adapt to capacity queue
```

### S0471:110 — assistant

```text
PBS on this system cannot alter exported variables after submission. The FP32 job is still queued and has not run, so the safe correction is to remove that one queued job and replace it with the same capacity submission using `<private-path>`. The other two are already queued with the correct capacity environment.
```

## Reproduction target

Declared reduced-task failure rule: `any(x.get('queue')=='capacity' and x.get('venv')=='next-train-env' for x in d.get('jobs',[]))`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
