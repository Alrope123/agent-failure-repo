# Describe the failure in one sentence

Status: incident report; reproduction not yet attempted.

Symptom labels: choose all that fit from docs/SYMPTOMS.md, or use other.
One incident may have multiple labels; do not count it as multiple incidents.

## What happened and why it matters

Describe the user's legitimate task, the expected behavior, the agent's actual
action, and the concrete consequence. Explain whether this is a meaningful
workflow error or an ordinary local bug. A report that the agent merely seemed
confused is not enough.

## Evidence from the original history

Record the agent/model if known and the date. Quote only reviewed, short excerpts
with stable event or turn references. Label paraphrases. Include the earlier
instruction or correct state, the later action, and the observed consequence.
State which source material is unavailable or withheld. Never paste raw secrets.

## Why the earlier work matters

Describe the earlier event, intervening work, and later decision. What needed
to persist: a rule, a fact, a file change, a boundary, or a status? Could the
agent recover it from current files? Did it actually read the relevant evidence?

Record observed turns, tool calls, session changes, and elapsed time when known.
Define the counting unit and endpoints. Distinguish configured budgets from
actual execution. Explain plausible alternative causes; a long session alone
does not establish causation.

## Intended failure and how to identify it

Write the specific wrong action or output the check should catch. Define the
preconditions, the observable failure predicate, and evidence required. Define
correct task completion separately. Explain how unrelated errors, missing
exposure, invalid setup, and unjudgeable runs are classified.

## Minimal reproduction

State what the agent receives at every stage, which files persist, what resets,
and what simulates a teammate or environment change. Keep judge, reference, and
incident narrative outside the evaluated workspace. List changes from the real
incident, what mechanism each preserves, and what the reduction loses.

Describe dependencies, supported operating systems, installation, network use,
expected cost, and safe disposable execution. Use fake data and local services.
Give copyable setup, agent-run, judge, reference-check, and control commands with
working directories and expected outputs. If unavailable, say not implemented.

## Correct solution and judge checks

Show that a correct solution is feasible and passes. Show that a deliberately
faulty solution is rejected for the intended reason. Test an unrelated error
and a broken setup so they are not mistaken for the target failure. These are
scripted checks, not fresh agent reproduction.

## Fresh evaluations and comparison

Link every result record, including misses and excluded attempts. Record exact
model/settings and task/judge revision. Report hits over eligible attempts,
total attempts, and reasons for exclusions. Report development trials separately
from any evaluation after the task and judge were frozen.

Compare with a condition that changes only the relevant history or reminder,
while preserving the final task, environment, model settings, and budget as far
as possible. Specify the comparison before running it. Describe uncertainty;
one pair is not a reliable frequency estimate. If not run, say not run.

## Limits and review

State what is observed, inferred, or untested. Note sanitization changes that
may change the mechanism. The owner must review the exact staged files before
sharing. Record permissions for any third-party material or use a rewrite you
are allowed to share.
