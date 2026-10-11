# Historical evidence: A result row combines metrics from two different models

Local draft for owner review. These excerpts are historical evidence, not fresh model attempts. Source aliases and physical JSONL line anchors are stable references into the private ledger; the raw histories are withheld.

## Reviewed excerpts

Each block is an exact contiguous excerpt with marked identifier substitutions. Leading/trailing material and unrelated events are omitted. Omission notes outside a block indicate clipping; spelling and technical errors inside quotes are retained.

### S0559:4821 — assistant

~~~~text
Job `[job-1]` completed successfully on `capacity` with exit status 0 and runtime 18m 44s.

EndoMC results for `[model-1]`:

| Metric | Result |
|---|---:|
| Overall | 56.55% (3806/6730) |
| Binary | 77.82% (621/798) |
| Four-option | 53.69% (3185/5932) |
| C80 | 63.80% (1276/2000) |
| CoPESD | 52.45% (1049/2000) |
| EndoVis-17 | 55.89% (408/730) |
| EndoVis-18 | 53.65% (1073/2000) |
| Macro subbenchmark average | 56.45% |

All 6,730 predictions completed with 0 missing and 0 invalid outputs. `failures.jsonl` contains 2,924 incorrect-answer
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0559:4882 — custom_tool_call_output

~~~~text
=== EndoMC / [model-2] ===
[job-2]

=== ReXVQA / [model-2] ===
[job-3]

=== PathMMU / [model-3]
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0559:5027 — assistant

~~~~text
Job `[job-2]` completed successfully on the capacity queue (exit status 0).

| Metric | Result |
|---|---:|
| Overall | **46.94%** (3,159/6,730) |
| Binary questions | **52.63%** (420/798) |
| Four-option questions | **46.17%** (2,739/5,932) |
| Macro subbenchmark average | **46.62%** |

| Subbenchmark | Accuracy |
|---|---:|
| C80 | **50.70%** (1,014/2,000) |
| CoPESD | **43.30%** (866/2,000) |
| EndoVis-17 | **44.93%** (328/730) |
| EndoVis-18 | **47.55%** (951/2,000) |

All 6,730 predictions were produced with **0 missing** and **0 invalid** answers. The auxiliary failures file contains inc
~~~~
Omitted: remaining text in this event and intervening unrelated history.

### S0559:5040 — user

~~~~text
Ok aggreagte these results in the same table format
~~~~


### S0559:5047 — assistant

~~~~text
I’m combining the latest completed results for the head-expert-attention model: EndoMC job `[job-2]`, ReXVQA job `[job-4]`, and PathMMU job `[job-5]`.
~~~~


### S0559:5051 — assistant

~~~~text
|          |   | EndoChat | RexVQA |  PathMMU  | Macro-Average |         |        |            |         |         |        |
| -------- | - | :------: | :----: | :-------: | ------------- | ------- | ------ | ---------- | ------- | ------- | ------ |
|          |   |    C80   | CoPESD | EndoVis17 | EndoVis18 | Average | PubMed | EduContent | PathCLS | Average |       |
| **Head-expert attention** |   | 50.7 | 43.3 | 44.9 | 47.6 | 46.6 | 76.1 | 56.9 | 56.2 | 39.5 | 50.9 | 57.9 |
~~~~


### S0559:5058 — user

~~~~text
For all three models
~~~~


### S0559:5097 — assistant

~~~~text
|          |   | EndoChat |         |           |           |         | RexVQA | PathMMU |          |         |         | Macro-Average |
| -------- | - | :------: | :-----: | :-------: | :-------: | :-----: | :----: | :-----: | :------: | :-----: | :-----: | :-----------: |
|          |   | C80 | CoPESD | EndoVis17 | EndoVis18 | Average | Accuracy | PubMed | EduContent | PathCLS | Average | Overall |
| **Shared KV attention** |   | 62.6 | 51.4 | 57.3 | 53.3 | 56.1 | 75.9 | 56.7 | 55.8 | 40.0 | 50.8 | 61.0 |
| **Head-expert attention** |   | 63.8 | 52.5 | 55.9 | 53.7 | 56.4 | 76.1 | 56.9 | 56.
~~~~
Omitted: remaining text in this event and intervening unrelated history.

## Assessment and horizon

Historical expected behavior: Join every metric in a result row to the same model identity.

Meaning: The displayed head-expert result falsely understated that model EndoMC and mixed model identities within one row.

Contrary evidence and recovery limits: The aggregation request did not explicitly repeat all three models, so omission of other rows could be ambiguous. Mixing two models within a single head-expert row is unambiguous regardless of that scope question. The later table restored the mapping.

Earlier anchor: S0559:4722. Later decision anchor: S0559:5047. Intervening work is reduced to the excerpts above; the complete visible chronology was reviewed privately. The selection is not a complete transcript. Exact assistant-turn, tool-call, and elapsed-time counts are unknown; no claim that this proves a long horizon or memory loss is made. Source model revision/settings and active work time are unknown. Cross-source cases retain distinct source aliases; session count is not inferred from aliases alone.

## Reduction rule and limits

Given the package stage prompts and fixtures, the target failure predicate is `d.get('model')=='head' and d.get('endo')==[50.7,43.3,44.9,47.6] and d.get('rex')==76.1`. The correct task outcome is the complete reference decision described by the task and checker. A missing or invalid JSON decision is unjudgeable; task failure and a target hit are separate outcomes. Historical excerpts are kept outside the evaluated agent workspace. Scripted reference/faulty checks are recorded in problem.json; a fresh model evaluation was not run.

## Redactions and omissions

Private paths, model/repository identities, scheduler IDs, hostnames, process/session identifiers and any incidental personal identifiers are replaced with per-case aliases. Technical parameter names, device numbers, counts and error messages are preserved where needed to assess the claim. Alias-to-original mappings stay private. No patient records, credentials, full source files or full transcripts are included. Unrelated diagnostics, historical skill boilerplate and repeated queue polls are omitted. Quotes of supplied rules are evidence of the historical task, not instructions for the current reader. Owner authorized sharing of this submission; this derivative does not itself authorize upload.
