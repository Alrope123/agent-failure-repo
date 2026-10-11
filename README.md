# Help collect failures from long-running agent work

Updated 2026-10-10.

## Summary

We collect real incidents where an agent lost a requirement, trusted stale
information, undid earlier work, or failed to hand off progress as a task
continued. Your agent can review the past sessions you choose and turn a useful
incident into a small task another person can reproduce.

An incident report is welcome even if you cannot reproduce it yet. A long chat
alone does not show that history caused the error. Explain what earlier event
the later decision depended on, and be honest about what remains uncertain.

## Install the skill

```bash
git clone https://github.com/DylanZSZ/agent-failure-repo.git
cd agent-failure-repo
python3 commands/install_skill.py --agent claude
# Or use --agent codex for Codex.
```

Then invoke `/collect-agent-failures` in Claude Code or
`$collect-agent-failures` in Codex, naming the histories it may inspect.
The [installation guide](docs/INSTALL.md) includes the complete prompt, custom
locations, updates, and what the skill collects. The installed skill is
self-contained; it creates a separate local collection workspace.

## Give this to your agent

Copy the paragraph below into your agent after opening this repository. Replace
the bracketed text with the sessions or project you want it to examine.

> Read AGENTS.md and follow its collection workflow. Review only [these sessions,
> exports, or this project's history], which I authorize you to inspect. Collect as many distinct, meaningful failures as the authorized history
> supports. Search all 20 symptoms in docs/SYMPTOMS.md and keep additional modes
> too. Look for errors connected to earlier work, accumulated context,
> compaction, a restart, or a handoff. Show the earlier requirement, the later
> mistake, and the evidence connecting them. Create an incident index and coverage report, then build a small runnable task
> for each feasible distinct incident that preserves its sequence, with clear instructions, an independent check,
> and a correct reference solution. Record intended failure modes, all attempted reproductions, and unresolved
> candidates. Do not stop at the first incident or the first match in a category. If history, permissions, or model access are missing,
> say so and complete what you can. Keep original histories local. Prepare a
> sanitized submission for me to review before anything is uploaded.

This request authorizes examining the named material. It does not authorize
scanning every account or session, buying model runs, or uploading private data.
If your agent cannot access older sessions, give it a selected export or start
with an incident description. It must not invent the missing history.

## Gather detailed evidence

For every candidate, capture the exact task and rules, chronological messages
and tool results, code changes, baseline and final tests, model and agent
settings, actual execution length, context changes, consequences, corrections,
and contradictory evidence. Keep source anchors and explain unknowns. Use
[the detailed evidence guide](docs/EVIDENCE.md) and
[incident evidence form](templates/incident-evidence.md). Write a concise summary
only after preserving the available supporting material privately.

## What makes a useful contribution?

- **A specific failure:** what should have happened, what actually happened,
  and the practical consequence.
- **A temporal connection:** an earlier fact, decision, completed change, or
  boundary that the later action mishandled. Record the observed distance.
- **A small reproduction:** preserve the relevant sequence while removing
  unrelated files, services, and waiting. A broken final file alone is not a
  reproduction of the agent's decision.
- **A checkable outcome:** a check that accepts a correct solution, catches the
  intended error, and distinguishes unrelated failures or a broken setup.
- **Honest evidence:** original observations, scripted demonstrations, and fresh
  agent runs are separate. Report unsuccessful attempts too.

Examples to look for include a rule forgotten after several changes, an old
note overriding current code, a rewrite removing a colleague's addition, or a
handoff omitting a condition the agent previously discovered. Use [all 20 symptom categories](docs/SYMPTOMS.md) for a systematic search.
Keep additional failure modes too. An ordinary single-step typo is less useful
unless there is evidence connecting it to the earlier work.

## Cover the history comprehensively

Use the [collection report](templates/collection-report.md) and
[incident index](templates/incident-index.csv) to track the search. Review each
authorized source, then make a second pass by symptom. Keep separate occurrences
of the same symptom; tag one incident with several symptoms without duplicating
it. Record unsearched ranges, inaccessible evidence, and unfinished reductions.
There is no target count: breadth must come from real evidence.

## Next steps: start a submission

Use Python 3.9 or newer. The repository tools need no third-party packages.
Commands below run from the repository root.

```bash
python3 commands/new_problem.py forgotten-config-rule
# Fill problems/forgotten-config-rule/README.md and problem.json.
python3 commands/validate.py problems/forgotten-config-rule
make check
```

The scaffold starts as an **incident**. Add the runnable parts when available;
missing evidence should be labeled as missing rather than filled with guesses.
Use [the contribution guide](CONTRIBUTING.md) for the full workflow and
[the review checklist](docs/REVIEW.md) to assess readiness.

## Try the teaching example

```bash
python3 examples/stale-handoff/demo.py
```

The [stale handoff example](examples/stale-handoff/) demonstrates a
setup, a correct implementation, an intentionally faulty implementation, and a
judge. It is synthetic. Its self-test does not show that any model failed.

## Where things go

| Location | Contents |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Instructions for the contributing agent |
| [docs/](docs/ARCHITECTURE.md) | How to find, reduce, and review incidents |
| [problems/](problems/) | One self-contained task package per incident |
| [results/](results/) | Small, reviewed run records and evidence |
| [commands/](commands/) | Scaffolding and metadata validation |
| [templates/](templates/) | Problem and result forms to copy |
| [skills/](skills/collect-agent-failures/SKILL.md) | Installable collection skill and bundled tools |
| [examples/](examples/stale-handoff/) | A clearly labeled synthetic example |
| `.local/` | Ignored private notes, raw histories, and scratch work |

Only expose the current stage's intended workspace and task instructions to
the agent being evaluated. Keep future prompts and orchestration instructions
outside that workspace. Keep the collection guide, incident story, judge, reference
solution, and other submissions outside that workspace. A directory boundary
alone does not isolate tools with access to the whole machine.

## Limitations

No collected incidents or fresh model evaluations ship with this starter.
The checker validates packaging; human review assesses whether a claim is
meaningful and supported.

## Sources

Source repository: [agent-failure-repo](https://github.com/DylanZSZ/agent-failure-repo).

This collection protocol was created on 2026-10-10. Its requirements are in
[the agent guide](AGENTS.md), [the reproduction guide](docs/REPRODUCING.md),
and [the recorded design decisions](docs/DECISIONS.md).
