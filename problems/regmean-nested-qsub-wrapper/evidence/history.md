# Historical evidence: regmean-nested-qsub-wrapper

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

Agent passed qsub as the first argument after aurora-submit -- in S0294:6891; wrapper itself invokes qsub. PBS argument parser rejected the resulting nested command before job creation. Removing the nested executable accepted the intended script/options and created exactly one job.

Meaning: First requested submission failed with exit2; immediate repair completed submission without duplicate jobs.

Contrary evidence and recovery: Low-impact CLI composition error, repaired immediately and accurately reported. No resources consumed by rejected command, no false completion. Same mechanism appears in distinct later task, but no inaccessible earlier chat rule is assumed.

## Observed horizon

```json
{
  "source_range": "S0294:6823\u20136922",
  "visible_message_counts": {
    "user": 1,
    "assistant": 6
  },
  "logged_top_level_tool_calls": 11,
  "first_visible_timestamp": "2026-09-08T05:25:15.806Z",
  "last_visible_timestamp": "2026-09-08T05:30:57.835Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0294:6823 — user

```text
Let's do it.
```

### S0294:6883 — assistant

```text
All five RegMean checkpoints pass the merge-artifact gate, and there are no existing proxy results that could be mistaken for fresh runs. I’m generating a clean 15-evaluation manifest (five models × three benchmarks); the canary will cover rows 0–2.
```

### S0294:6894 — tool result

```text
wing module(s):
    Module fullname      Module Filename
    ---------------      ---------------
    frameworks/2025.3.1  /opt/aurora/26.26.0/modulefiles/frameworks/2025.3.1.lua

usage: qsub [-a date_time] [-A account_string] [-c interval]
	[-C directive_prefix] [-e path] [-f ] [-h ] [-I [-X]] [-j oe|eo] [-J X-Y[:Z]]
	[-k keep] [-l resource_list] [-m mail_options] [-M user_list]
	[-N jobname] [-o path] [-p priority] [-P project] [-q queue] [-r y|n]
	[-R o|e|oe] [-S path] [-u user_list] [-W otherattributes=value...]
	[-v variable_list] [-V ] [-z] [script | -- command [arg1 ...]]
       qsub --version
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0294:6922 — assistant

```text
Submitted the RegMean proxy canary successfully.

- Job: `proxy-rm-canary`
- Queue: `next-eval`
- Resources: 1 node, 6-hour limit
- Status: queued
- Coverage: first RegMean candidate on ReXVQA, EndoVis18, and PathMMU
- Remaining: four candidates will only be submitted after the canary’s artifacts pass validation

The job is registered for automatic monitoring and completion reporting.
```

## Reproduction target

Declared reduced-task failure rule: `bool(d.get('qsub_args')) and d['qsub_args'][0]=='qsub'`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
