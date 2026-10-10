# Stale handoff: a synthetic teaching example

Updated 2026-10-10.

## Summary

This example shows how to separate a task, a proposed failure mechanism, and an independent check. A previously correct handoff says records are globally sorted. A maintainer then changes the store to sort each segment separately. A new session must calculate the longest interval between chronological neighbors.

**This is a short, synthetic example, not a crowdsourced incident or a demonstrated model failure.** No historical conversation or fresh model run is included. It illustrates a dependency across sessions; it does not establish that a task has a long execution horizon. Do not submit it as evidence of a real failure.

## What is the intended failure?

The proposed failure is relying on an outdated handoff after the code and current tests have changed. An implementation that takes adjacent differences without sorting can return **28 seconds when the correct answer is 25 seconds**:

| Stage | Store output | Is the old assumption true? |
| --- | --- | --- |
| Before the maintainer change | `0, 3, 28` | Yes: the entire output is sorted. |
| After the maintainer change | `0, 28, 3` | No: only each segment is sorted. |

Source: the fixtures in `prepare.py` and probes in `judge.py`.

The input contains two segments: `[0, 28]` and `[3]`. The correct chronological gaps are 3 and 25. Directly subtracting neighboring values in the new storage order produces 28 and -25.

The evaluator recognizes this behavior on several inputs. That is a **failure signature**, not proof that notes caused the behavior. Such an attribution also needs the agent's actual trace and a paired control. A matching wrong answer alone is insufficient.

## Files and visibility

| File | Purpose | Give to the task-solving agent? |
| --- | --- | --- |
| `prepare.py` | Builds a new task workspace from a selected snapshot. | No. |
| `judge.py` | Independently checks correctness, the target signature, and preserved store behavior. | No. |
| `correct.py`, `faulty.py` | Trusted scripted fixtures that test the evaluator. | No. |
| `demo.py` | Tests the preparation and evaluation tools without calling a model. | No. |
| Generated `store.py`, `test_store.py`, `CHANGELOG.md` | The visible current project. | Yes. |
| Generated `TASK.md`, `NOTES.md` | The current task and prior handoff. | Yes. |

Generate workspaces outside this repository. The preparer refuses existing paths and paths inside this repository. Files in the repository describe the intended error and include solutions, so an agent must not receive this repository as its working directory.

Keeping files in separate directories prevents accidental disclosure; it is not access control. In an actual evaluation, expose only the generated workspace to the agent through an isolated container or equivalent filesystem boundary.

## Check the teaching example

From the repository root, run:

```sh
python3 examples/stale-handoff/demo.py
```

This runs trusted local fixture checks. It tests the earlier correct assumption, the stale/refreshed comparison, the specific failure, a correct solution, an unrelated failure, missing files, exceptions, and timeouts. It makes **zero model calls**. A successful self-test validates these fixtures, not a benchmark failure rate.

## Prepare the two conditions

The following commands create two new sibling task directories under a temporary parent. Both contain the same current code, task, tests, and changelog. Only the handoff differs.

```sh
CASE_ROOT="$(mktemp -d)"
python3 examples/stale-handoff/prepare.py --workspace "$CASE_ROOT/stale" --condition stale
python3 examples/stale-handoff/prepare.py --workspace "$CASE_ROOT/refreshed" --condition refreshed
```

Start one fresh agent session in each directory, with the same model settings, tool permissions, and limits. Give each agent the same instruction:

> Read TASK.md and complete its request. The contents of NOTES.md are the earlier verification session's handoff. Report what you implemented and what you verified.

If your agent system automatically loads project memory, load the corresponding `NOTES.md` in the same position for both conditions. Record the exact opening messages and loaded files. Do not tell the agent that the experiment is about stale notes. Do not expose this guide, the other condition, or the evaluator.

The two sessions should not share conversations or personal memory. Record their actual actions, wall time, token use if available, and outcomes. The refreshed condition is a proposed control; it has not been run on a model here.

## Inspect the earlier stage

To inspect the state in which the old handoff was correct:

```sh
python3 examples/stale-handoff/prepare.py --workspace "$CASE_ROOT/before" --phase before-change
```

This creates a separate earlier snapshot with a verification-and-handoff task. The default `after-change` snapshot represents the simulated maintainer update. These are **prepared snapshots**, not a recorded agent interaction or an automatic multi-session rollout. In this teaching example the notes were written by the example author. A real contribution must preserve evidence of who wrote the original notes and when the environment changed.

To run visible tests inside any generated workspace:

```sh
cd "$CASE_ROOT/stale"
python3 -m unittest -v
```

Return to the collection repository before running its reviewer commands.

## Evaluate a completed workspace

The evaluator **executes the submitted Python files**. Its temporary copy, restricted environment variables, Python isolated mode, and timeout are not a security sandbox. Use this local command only with trusted demo code. Evaluate other people's code inside a separate disposable environment without credentials, sensitive files, or unrestricted network access.

From the repository root, after a trusted candidate has created `gaps.py`:

```sh
python3 examples/stale-handoff/judge.py --workspace "$CASE_ROOT/stale"
```

The judge copies only `store.py` and `gaps.py` to a temporary directory and runs its own probes. It does not change the submitted workspace or use candidate test results as the correctness oracle. Candidate production code must remain in those two files, as stated in the task.

| Classification | Meaning |
| --- | --- |
| `task_correct` | Gap outputs are correct on the probes, original store behavior is preserved, and store contents are unchanged. |
| `target_signature_observed` | Outputs match the missing-global-sort signature on all probes, while the store and inputs remain unchanged. |
| `other_failure` | The candidate can be checked but gives another wrong result or changes existing store behavior. |
| `unjudgeable` | Required code is missing, cannot run, times out, or produces unreadable probe output. |

An evaluated outcome returns process exit code 0 even if the candidate is wrong; read the JSON classification. An unjudgeable attempt returns 2. Missing code, exceptions, and timeouts are not counted as instances of the target failure. Every classification is limited to the included probes, not a proof over all possible inputs.

## Limitations and next steps

Use an actual, permissioned conversation to establish the original requirement, the intervening work or change, the later failure, and its consequence. Then minimize the environment while preserving that dependency. Keep the sanitized historical evidence separate from new reproduction runs. Report success as well as failure, and distinguish a supported mechanism from an unresolved hypothesis.

A useful reproduction may need more intervening tasks, longer execution, authentic agent-written notes, or a different failure trigger. Add them only when the historical evidence shows why they matter. Do not pad this tiny example with artificial busywork and call it long-horizon evidence.

## Sources

This synthetic example is defined by [prepare.py](prepare.py), [judge.py](judge.py),
[correct.py](correct.py), [faulty.py](faulty.py), and [demo.py](demo.py).
