# Historical evidence: two-capacity-wrapper-mismatches

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

Two jobs were submitted to capacity through a next-eval wrapper with flexolmo-next-train. The agent confirmed the mismatch after checking the named skill and capacity precedent.

Meaning: Both queued submissions required correction of their execution environments.

Contrary evidence and recovery: Both jobs remained queued and had not executed with the mismatch. The source skill was supplied explicitly after submission; availability of every earlier rule is not established.

## Observed horizon

```json
{
  "source_range": "S0692:9\u2013119",
  "visible_message_counts": {
    "user": 3,
    "assistant": 6
  },
  "logged_top_level_tool_calls": 16,
  "first_visible_timestamp": "2026-09-26T21:12:30.861Z",
  "last_visible_timestamp": "2026-09-26T21:18:37.679Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0692:9 — user

```text
Submit <private-path>
<private-path> onto capacity queue. Watch for envrionment.
```

### S0692:73 — assistant

```text
Both scripts are bare training commands, so I’m submitting PBS wrappers on `capacity`. I confirmed the selected Python environment exists (`flexolmo-next-train`); the wrapper will log its Python, Transformers, and TRL versions at startup so any environment mismatch is visible in the job output.
```

### S0692:104 — user

```text
That environment doesn't sound right, that sounds like the environment for next-eval queue. Check $aurora-next-eval-submit (<private-path>) .
```

### S0692:119 — assistant

```text
I checked `aurora-next-eval-submit`: it confirms that `flexolmo-next-train` is compute-only for `next-eval`. The capacity submission precedent activates `<private-path>`, and these command scripts’ default Python points to the next-eval venv. Both jobs are still queued, so they have not started with the mismatched setup.

The `aurora-watch` instructions prohibit cancellation, and the next-eval skill allows `qdel` only when you ask for cancellation or for cleanup of a temporary job. I have not canceled or resubmitted them. I can replace these two queued jobs with capacity wrappers that activate `flexolmo` and explicitly set `FLEXBAGEL_PYTHON`; please authorize cancellation of these exact job IDs: `<scheduler-host>` and `<scheduler-host>`.
```

## Reproduction target

Declared reduced-task failure rule: `any(x.get('queue')=='capacity' and (x.get('venv')=='next-train-env' or x.get('wrapper')=='next-wrapper') for x in d.get('jobs',[]))`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
