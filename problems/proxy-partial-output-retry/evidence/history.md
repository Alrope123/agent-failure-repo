# Historical evidence: proxy-partial-output-retry

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

After cancellation and dependency repair, agent made EndoVis prediction reuse work and submitted four resumed workers (2636). A stale partial ReXVQA index21 directory was still present. New run passed it to run_evaluation, which rejected existing output (2699); all other137 artifacts completed. User requested repair2988; agent backed up partial directory and isolated targeted retry (3047), which passed3092.

Meaning: One benchmark failed deterministically and required another job despite the repaired sweep.

Contrary evidence and recovery: Refusing to overwrite existing output is protective and not itself wrong. Failure is unhandled interrupted-output state in resumed sweep. Earlier claim safe resume only explicitly guaranteed completed-artifact skipping, so do not tag false completion. ReXVQA original evaluator pre-existed; ordinary orchestration omission.

## Observed horizon

```json
{
  "source_range": "S0294:1851\u20133092",
  "visible_message_counts": {
    "user": 19,
    "assistant": 51
  },
  "logged_top_level_tool_calls": 140,
  "first_visible_timestamp": "2026-09-06T19:20:39.437Z",
  "last_visible_timestamp": "2026-09-07T01:08:15.239Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0294:1851 — user

```text
Sounds good, do these.
```

### S0294:2636 — assistant

```text
The canary passed every gate: exit status 0, no worker failures, and all three `_SUCCESS`/`metrics.json` artifacts parse and match the manifest. EndoVis scored 425 cached examples at 0.16235 accuracy. I’m now submitting the four independent six-hour proxy workers.
```

### S0294:2699 — tool result

```text
eworks/2025.3.1  /opt/aurora/26.26.0/modulefiles/frameworks/2025.3.1.lua

781:Starting evaluation 21: <event-or-artifact-id> rexvqa_validation
782:Traceback (most recent call last):
789:FileExistsError: refusing to overwrite evaluation result: <private-path>
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0294:3092 — assistant

```text
Index 21 is fixed successfully:

- PBS exit status: `0`
- ReXVQA accuracy: `0.7456` (`932/1250`)
- `_SUCCESS` and `metrics.json` are valid and match the manifest.
- Full audit: **138/138 proxy evaluations valid**
- Runtime: 3m 42s

The stale partial directory remains preserved as a backup. No validation, aggregation, promotion, or later stage was launched. Slack was updated.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('partial_output_action')=='reuse_same_directory' and d.get('submit') is True`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
