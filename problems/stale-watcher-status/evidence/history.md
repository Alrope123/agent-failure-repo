# Historical evidence: stale-watcher-status

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

The agent published complete score rows while calling EndoChat jobs still running; direct PBS history later confirmed successful completion and the agent acknowledged a stale snapshot.

Meaning: The reported status misled the user about whether evaluation was finished.

Contrary evidence and recovery: Complete artifacts alone do not prove scheduler termination; the later direct PBS history is the decisive evidence. Scores were valid.

## Observed horizon

```json
{
  "source_range": "S0559:1505\u20131556",
  "visible_message_counts": {
    "assistant": 3,
    "user": 1
  },
  "logged_top_level_tool_calls": 5,
  "first_visible_timestamp": "2026-09-22T04:33:28.553Z",
  "last_visible_timestamp": "2026-09-22T04:56:29.424Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0559:1505 — assistant

```text
Results from the fresh artifacts:

```tsv
Model	C80	CoPESD	EndoVis17	EndoChat Average	ReXVQA	PubMed	EduContent	PathCLS	PathMMU Average
btx_pubmed_..._5k_8bits	86.46	74.55	49.63	70.21	77.50	60.50	61.20	38.55	53.42
btx_pubmed_..._10k_8bits	87.28	74.71	50.00	70.66	77.79	60.21	61.14	39.18	53.51
```

EndoChat artifacts contain 5,000 samples per suite. The EndoChat PBS jobs are still marked running by Aurora, while ReXVQA and PathMMU have completed successfully.
```

### S0559:1512 — user

```text
Are you sure? The endochat ones are done, and you even have the results in your table
```

### S0559:1541 — tool result

```text
Script completed
Wall time 13.1 seconds
Output:

---<job-id>
    Job_Name = ce-btxng5k
    resources_used.walltime = 01:47:44
    job_state = F
    ctime = Tue Sep 22 01:04:12 2026
    mtime = Tue Sep 22 02:57:01 2026
    stime = Tue Sep 22 01:08:45 2026
    comment = Job run at Tue Sep 22 at 01:08 on (<node>:ncpus=208) and f
    Exit_status = 0
---<job-id>
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0559:1556 — assistant

```text
You’re right. I incorrectly relied on a stale Aurora Watch snapshot. Direct PBS history confirms all EndoChat jobs finished successfully with exit code 0:

- `<job-id>`: finished, 1:47:44
- `<job-id>`: finished, 2:05:43
- `<job-id>`: finished, 1:54:27
- `<job-id>`: finished, 2:09:26

The table’s EndoChat results are valid; only my status note was wrong.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('status') == 'running'`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
