# Historical evidence: opd-nested-qsub-wrapper

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

Agent passed qsub as the first argument after aurora-submit -- in S0103:5017; wrapper itself invokes qsub. PBS argument parser rejected the resulting nested command before job creation. Removing the nested executable accepted the intended script/options and created exactly one job.

Meaning: First requested submission failed with exit2; immediate repair completed submission without duplicate jobs.

Contrary evidence and recovery: Low-impact CLI composition error, repaired immediately and accurately reported. No resources consumed by rejected command, no false completion. Same mechanism appears in distinct later task, but no inaccessible earlier chat rule is assumed.

## Observed horizon

```json
{
  "source_range": "S0103:4941\u20135032",
  "visible_message_counts": {
    "user": 1,
    "assistant": 6
  },
  "logged_top_level_tool_calls": 19,
  "first_visible_timestamp": "2026-09-02T05:48:17.218Z",
  "last_visible_timestamp": "2026-09-02T05:52:13.932Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0103:4941 — user

```text
Resubmit job on capacity queue, with a save\_steps of 100
```

### S0103:5016 — assistant

```text
Validation passed: the config is valid JSON, both shell scripts parse cleanly, the new output path does not exist, and the PBS script already targets `capacity`. I’m submitting this fresh attempt now and binding its completion analysis to this session.
```

### S0103:5018 — tool result

```text
Script completed
Wall time 3.5 seconds
Output:

{"chunk_id":"c47744","wall_time_seconds":0.000003889,"exit_code":2,"original_token_count":107,"output":"usage: qsub [-a date_time] [-A account_string] [-c interval]\n\t[-C directive_prefix] [-e path] [-f ] [-h ] [-I [-X]] [-j oe|eo] [-J X-Y[:Z]]\n\t[-k keep] [-l resource_list] [-m mail_options] [-M user_list]\n\t[-N jobname] [-o path] [-p priority] [-P project] [-q queue] [-r y|n]\n\t[-R o|e|oe] [-S path] [-u user_list] [-W otherattributes=value...]\n\t[-v variable_list] [-V ] [-z] [script | -- command [arg1 ...]]\n       qsub --version\n"}
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0103:5032 — assistant

```text
Resubmitted successfully.

- Job ID: `<scheduler-host>`
- State: `Q` (queued)
- Queue: `capacity`
- Walltime: 72 hours
- `save_steps`: **100**
- New output: `<private-path>`
- Failed-run artifacts remain untouched.

The job is registered for monitoring and completion will return to this Codex session. Configuration: opd_config.example.json (<private-path>).
```

## Reproduction target

Declared reduced-task failure rule: `bool(d.get('qsub_args')) and d['qsub_args'][0]=='qsub'`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
