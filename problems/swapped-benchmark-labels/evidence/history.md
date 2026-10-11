# Historical evidence: swapped-benchmark-labels

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

The user challenged EduContent/PathCLS labels; the agent confirmed it had swapped the columns although the files were correctly named.

Meaning: Category accuracy was attributed to the wrong benchmark, affecting comparisons.

Contrary evidence and recovery: Underlying result artifacts and overall average were not reported as corrupted; the correction repaired the mapping.

## Observed horizon

```json
{
  "source_range": "S0559:4206\u20134358",
  "visible_message_counts": {
    "assistant": 7,
    "user": 5
  },
  "logged_top_level_tool_calls": 12,
  "first_visible_timestamp": "2026-10-05T01:40:27.765Z",
  "last_visible_timestamp": "2026-10-05T05:56:59.496Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0559:4213 — user

```text
This format:&#x20;

|          |   | EndoChat | RexVQA |  PathMMU  | Macro-Average |         |        |            |         |         |        |      |
| -------- | - | :------: | :----: | :-------: | ------------- | ------- | ------ | ---------- | ------- | ------- | ------ | ---- |
|          |   |    C80   | CoPESD | EndoVis17 | EndoVis18     | Average | PubMed | EduContent | PathCLS | Average |        |      |
| **Base** |   |   35.3   |  30.6  |    36.4   | *36.9*        | *34.8*  | *61.2* | 53.5       | 50.0    | 30.0    | *44.5* | 46.8 |
```

### S0559:4238 — assistant

```text
Values are percentages; averages are macro-averages.

| Model |  | EndoChat |  |  |  |  | RexVQA | PathMMU |  |  |  | Macro-Average |
| -------- | - | :------: | :------: | :--------: | :--------: | :------: | :------: | :------: | :----------: | :------: | :------: | :------------: |
|  |  | C80 | CoPESD | EndoVis17 | EndoVis18 | Average | Average | PubMed | EduContent | PathCLS | Average |  |
| `<model-alias>` |  | 67.8 | 63.6 | 60.4 | 61.3 | 63.3 | 77.9 | 60.3 | 40.0 | 61.1 | 53.8 | 65.0 |
| `<model-alias>` |  | 68.0 | 63.5 | 60.5 | 58.5 | 62.6 | 77.9 | 60.5 | 40.1 | 60.8 | 53.8 | 64.8 |
| `<model-alias>` |  | 66.7 | 61.9 | 60.4 | 61.3 | 62.6 | 77.9 | 60.5 | 40.0 | 61.1 | 53.9 | 64.8 |
| `<model-alias>` |  | 66.7 | 64.1 | 61.0 | 60.7 | 63.1 | 77.8 | 60.3 | 40.3 | 61.1 | 53.9 | 64.9 |
| `endochat_rexgradient_pathgen_router_tuned_8bits_5k_from_avg` |  | 56.8 | 65.3 | 58.4 | 56.1 | 59.2 | 75.1 | 58.8 | 39.8 | 57.7 | 52.1 | 62.1 |
| `endo_rex_pathgen_combined_from_avg` |  | 55.0 | 54.5 | 54.7 | 55.4 | 54.9 | 59.1 | 52.5 | 36.1 | 54.5 | 47.7 | 53.9 |
```

### S0559:4245 — user

```text
Why are the numbers for the attention moe one so similar?
```

### S0559:4358 — assistant

```text
Yes—you’re right. I accidentally swapped the **EduContent** and **PathCLS** labels in the table; the underlying result files are correctly named.

Correct mapping:

`PubMed | EduContent | PathCLS | Average`

For the first model:

`60.3 | 61.1 | 40.0 | 53.8`

The correct PathMMU columns for all six models are:

```text
Model                                                        PubMed  EduContent  PathCLS  Average
<model-alias> 60.3    61.1        40.0     53.8
<model-alias>    60.5    60.8        40.1     53.8
<model-alias>   60.5    61.1        40.0     53.9
<model-alias>      60.3    61.1        40.3     53.9
endochat_rexgradient_pathgen_router_tuned_8bits_5k_from_avg   58.8    57.7        39.8     52.1
endo_rex_pathgen_combined_from_avg                            52.5    54.5        36.1     47.7
```

The files confirm that `EduContent_test` has 1,683 examples and `PathCLS_test` has 952.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('EduContent')==40.0 and d.get('PathCLS')==61.1`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
