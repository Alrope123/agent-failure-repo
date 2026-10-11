# Historical evidence: missed-separate-evaluation

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

The agent reported no separate evaluation result, then found the separate successful evaluation and reported 71.55% after the user corrected it.

Meaning: The user received an incorrect statement about a completed evaluation.

Contrary evidence and recovery: Training really used skip_eval. The error concerned a separate evaluation, not that training setting; the agent recovered.

## Observed horizon

```json
{
  "source_range": "S0391:352\u2013411",
  "visible_message_counts": {
    "user": 2,
    "assistant": 5
  },
  "logged_top_level_tool_calls": 7,
  "first_visible_timestamp": "2026-09-12T03:08:35.990Z",
  "last_visible_timestamp": "2026-09-12T03:11:56.409Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0391:352 — user

```text
What's the eval result?
```

### S0391:362 — assistant

```text
No evaluation result is available from this run. The command used `--skip_eval`, and the logs confirm evaluation was disabled. I also found no separate evaluation results associated with this checkpoint.

The reported **10.8520 loss is training loss**, not an evaluation score.
```

### S0391:369 — user

```text
I think there was an evaluation job for this model.
```

### S0391:411 — assistant

```text
You’re right—I missed the separate evaluation job. Sorry for the incorrect answer.

**ReXVQA accuracy: 71.55%** — **24,960 / 34,884** correct.

- Job **<job-id>** evaluated this model’s `final` checkpoint and exited successfully.
- Finished **September 11, 19:37 UTC**, after **26 minutes 25 seconds**.
- Five questions with more than 10 images were skipped.

Evaluation log (<private-path>) · Predictions (<private-path>)
```

## Reproduction target

Declared reduced-task failure rule: `d.get('status') == 'unavailable'`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
