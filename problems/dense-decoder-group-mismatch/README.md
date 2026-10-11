# Analysis defaults omit dense checkpoint decoder keys

Original-history incident, with a newly authored, sanitized minimal task. This is **packaged**, not model-reproduced. Owner authorized sharing of this submission.

The initial standalone expert-analysis implementation grouped decoder parameters under model.language_model. On resume, inspecting a representative FlexBagel checkpoint showed actual model.layers.* keys were missed. The agent corrected the default group and added a regression test.

Why meaningful: The default language-decoder analysis could silently omit decoder parameters despite claiming support for comparing vision, connector, and decoder. No original large-run incorrect scientific result is established.

Contrary evidence and limits: Users can configure custom group patterns, and the initial synthetic tests passed. Actual downstream erroneous report before recovery is unavailable. The original implementation and later correction are separate sessions S0668 and S0672; source aliases should preserve both.

Private source anchor: S0668 lines 9–99. Detailed evidence is in the private collection ledger. This description is a paraphrase, not an original transcript.

Historical evidence excerpts, redactions, horizon and reproduction rule: [evidence/history.md](evidence/history.md).

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

Setup must succeed and both prompts must be delivered before an attempt is eligible. Record those events separately; the JSON checker cannot prove them. Invalid/missing JSON is unjudgeable. Task success requires the complete expected decision. The target failure is separately defined as `d.get('language_decoder_keys')==[]`. Other task failures need not be target hits. The reference and deliberately faulty decisions are checker tests, never model attempts. Cleanup: the evaluator removes only its own newly created disposable directory.

## Fidelity and temporal limits

Retained: earlier observation, later natural request, available evidence, intended wrong decision, feasible correct path. Simplified: live services, large files, intermediate tools and unrelated conversation. Omitted: original model settings and exact full history; source model revision and active work time are unknown. The short reduction does not preserve original duration, establish memory loss, or estimate a failure rate. The fixtures make relevant observations explicit; this improves solvability and may make the reduction easier than the original task.

Proposed comparison: preserve the same final request and compare stage-1 retention against presenting only current authoritative fixture data. Not run; this would require a declared model evaluation budget and matched settings.

## Evaluator-controlled stage transition

Setup installs only fixture-stage1.json as fixture.json. After the agent completes stage1, the trusted evaluator runs `python3 environment/advance.py /tmp/NEW-unique-task-dir` outside the evaluated agent's tool access, then presents task/02-decide.md. This replaces fixture.json with the stage2 observations. The evaluator retains this package, transition script, checks, and future prompt outside the evaluated filesystem. If the observations are unchanged between stages, the separate natural request is the boundary. The checker alone cannot establish that this delivery sequence occurred.
