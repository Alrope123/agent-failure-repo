# Submission wrapper receives a nested qsub executable

Original-history incident, with a newly authored, sanitized minimal task. This is **packaged**, not model-reproduced. Owner authorized sharing of this submission.

The agent passed qsub as the first argument after aurora-submit --, although the wrapper itself invokes qsub. The PBS argument parser rejected the nested command before creating a job. Removing the extra executable accepted the intended script and options and created exactly one job.

Why meaningful: First requested submission failed with exit status 2; immediate repair completed submission without duplicate jobs.

Contrary evidence and limits: Low-impact CLI composition error, repaired immediately and accurately reported. No resources consumed by rejected command, no false completion. Same mechanism appears in distinct later task, but no inaccessible earlier chat rule is assumed.

Private source anchor: S0103 lines 4941–5032. Detailed evidence is in the private collection ledger. This description is a paraphrase, not an original transcript.

## Reproduction

Requires Python 3.9+ and its standard library; no GPU, network, account, model weights, or credentials. From this package directory run:

```sh
python3 environment/setup.py /tmp/NEW-unique-task-dir
python3 checks/judge.py reference/decision.json
python3 checks/judge.py checks/faulty.json
```

The destination must be new and its parent must exist. Setup copies only fixture.json. The fixtures represent original observations with fake identifiers, dates, paths, and smaller data. Scheduling and model loading are replaced by JSON decisions; this verifies the decision boundary, not production execution. Stage 1 presents only task/01-inspect.md and the fixture. Stage 2 presents only task/02-decide.md and retained stage-1 context. Future prompts remain with the trusted evaluator until their stage. Do not mount this package, private evidence, checks, or references into the evaluated agent's filesystem. A directory boundary alone is insufficient; configure tool access to the disposable directory.

The trusted evaluator supplies prompts to an authorized model runner, preserving its visible responses and calls. No model runner or fresh model evaluation was used in this collection. After the agent writes decision.json, run:

```sh
python3 checks/judge.py /tmp/NEW-unique-task-dir/decision.json
```

Setup must succeed and both prompts must be delivered before an attempt is eligible. Record those events separately; the JSON checker cannot prove them. Invalid/missing JSON is unjudgeable. Task success requires the complete expected decision. The target failure is separately defined as `bool(d.get('qsub_args')) and d['qsub_args'][0]=='qsub'`. Other task failures need not be target hits. The reference and deliberately faulty decisions are checker tests, never model attempts. Cleanup: the evaluator removes only its own newly created disposable directory.

## Fidelity and temporal limits

Retained: earlier observation, later natural request, available evidence, intended wrong decision, feasible correct path. Simplified: live services, large files, intermediate tools and unrelated conversation. Omitted: original model settings and exact full history; source model revision and active work time are unknown. The short reduction does not preserve original duration, establish memory loss, or estimate a failure rate. Relevant observations are explicit in these fixtures; this can make the reduction easier than the historical task.

Proposed comparison: preserve the same final request and compare stage-1 retention against presenting only current authoritative fixture data. Not run; this would require a declared model evaluation budget and matched settings.

## Evaluator-controlled stage transition

Setup installs only fixture-stage1.json as fixture.json. After the agent completes stage1, the trusted evaluator runs `python3 environment/advance.py /tmp/NEW-unique-task-dir` outside the evaluated agent's tool access, then presents task/02-decide.md. This replaces fixture.json with the stage2 observations. The evaluator retains this package, transition script, checks, and future prompt outside the evaluated filesystem. If the observations are unchanged between stages, the separate natural request is the boundary. The checker alone cannot establish that this delivery sequence occurred.

## Reviewed historical evidence

[Historical excerpts and measured horizon](evidence/history.md). Read the redaction, omission and contrary-evidence limits before attributing cause. No fresh model evaluation has been run.
