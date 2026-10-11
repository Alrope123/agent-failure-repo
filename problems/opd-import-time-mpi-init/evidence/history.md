# Historical evidence: opd-import-time-mpi-init

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

New trainer imports mpi4py.MPI at module scope (937), and CPU tests import trainer helpers (967). First test run aborts in internal_Init_thread with exit15 (979). Agent moves MPI import into setup_distributed (984,988); subsequent CPU suite succeeds (1137).

Meaning: CPU verification cannot import non-distributed helper functions until the module import is repaired.

Contrary evidence and recovery: Caught and repaired before final delivery; no failed production job or false final completion. Facility MPI itself requires a compute context. This is an authored integration omission, not evidence of long-horizon memory loss.

## Observed horizon

```json
{
  "source_range": "S0103:888\u20131137",
  "visible_message_counts": {
    "user": 2,
    "assistant": 8
  },
  "logged_top_level_tool_calls": 53,
  "first_visible_timestamp": "2026-08-27T00:59:24.507Z",
  "last_visible_timestamp": "2026-08-27T01:21:09.957Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0103:888 — user

```text
Ok don't worry about the data preparation, write a training pipeline (code) for me and give me protocal for data format. If you need to know anything, ask me before you proceed.
```

### S0103:922 — user

```text
Update me on Slack, too.
```

### S0103:926 — assistant

```text
I’ll add privacy-safe Slack updates at meaningful milestones and completion. The first data-contract module is now in place; I’m pausing implementation briefly to load the Slack notification rules before sending anything.
```

### S0103:1137 — assistant

```text
The CPU verification pass is clean: syntax, lint, routing, data validation, deterministic stream resume, configuration-resume protection, and numerical KL/gradient tests all pass. I also added bounded image/video preprocessing, train/validation leakage detection, entropy and teacher-likelihood metrics, and collective checkpoint-failure propagation. Next I’m preparing a minimal generated dataset solely to exercise the complete trainer on Aurora.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('mpi_import_location')=='module'`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
