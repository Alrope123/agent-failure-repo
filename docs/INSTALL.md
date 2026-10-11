# Install the failure-collection skill

Updated 2026-10-10.

## Summary

To start immediately, give your agent the ready-to-use message in the
repository readme. It handles setup and collection in the same
conversation; installation and restarting the agent are unnecessary for that
path. This page covers optional installation for reuse in later sessions.

Source: [Repository entrypoint](../README.md).

Install `collect-agent-failures` once, then invoke it in an agent that can read
historical Claude Code and Codex runs you select. Either host agent checks both
tools' available transcripts. It searches all 20 symptom categories and new
modes, captures detailed evidence, and builds small reproduction tasks. The
installed folder includes the guides, templates, and tools; it works without
keeping this repository clone. Installation itself does not read any history.

## Install from the repository

Requires Git and Python 3.9 or newer. Clone the repository and inspect the skill
and installer before running them:

```bash
git clone https://github.com/DylanZSZ/agent-failure-repo.git
cd agent-failure-repo
```

For Claude Code:

```bash
python3 commands/install_skill.py --agent claude
```

For Codex:

```bash
python3 commands/install_skill.py --agent codex
```

Choose the command for your agent. The installer copies only the skill folder.
It makes no network calls, installs no dependencies, and refuses to overwrite
an existing installation. Use `--dry-run` to see the destination without writing.

| Agent | Default installation directory | Invocation |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/collect-agent-failures` | `/collect-agent-failures` |
| Codex | `~/.agents/skills/collect-agent-failures` | `$collect-agent-failures` |

Source: [Claude Code skill locations](https://code.claude.com/docs/en/skills) and [OpenAI skill locations](https://learn.chatgpt.com/docs/build-skills).

If the skill does not appear, start a new agent session. Managed settings can
restrict custom skills.

For another compatible agent or a custom location, supply the exact skill
folder to create:

```bash
python3 commands/install_skill.py --dest /path/to/skills/collect-agent-failures
```

Use the folder your agent discovers; copying a folder cannot add skill support
to a product that does not have it. For older Codex setups, `--dest` also lets
you select a configured legacy skill directory. Do not install duplicate copies
under several discovery roots.

## Ask it to collect comprehensively

In Claude Code, begin with `/collect-agent-failures`. In Codex, begin with
`$collect-agent-failures`. Append this request, replacing the bracketed scope:

> Review historical Claude Code and Codex runs for [these projects, sessions, exports,
> and dates], which I authorize you to inspect. Check both tools regardless of
> which agent you are. Use the current conversation as supplementary evidence.
> Collect as many distinct failures as the evidence supports, using all 20
> symptom categories and additional modes.
> Get as much relevant information as possible for each candidate: exact requests,
> messages, tool results, edits, tests, context changes, model settings, outcomes,
> corrections, and counterevidence. Preserve source references and unknowns.
> Keep a complete inventory and coverage report; do not stop after a few examples.
> Build a minimal reproduction for every feasible credible incident and document
> the intended error and checks. Keep originals local, show me the sanitized
> material before sharing, and leave exact continuation points for unfinished work.

The agent creates a separate collection workspace. It does not write collected
histories into the installed skill. It follows [the historical-run guide](HISTORY.md)
and records each tool's coverage separately. If it cannot access prior sessions, provide
selected exports or an authorized path; installation cannot unlock chat history.

## What you should receive

- A source inventory and search coverage for all 20 symptoms plus other modes.
- A complete candidate index, including uncertain, duplicate, and rejected cases.
- A detailed evidence record for each candidate, with missing fields explained.
- Runnable task packages where feasible, plus concrete deferral reasons.
- Every reproduction attempt and comparison, with claims matched to evidence.
- A console explanation of findings, proposed submission files, checks, and gaps,
  with links to the complete local material.

The [submission guide](SUBMITTING.md) defines the reviewed collection reports,
problem packages, and actual run records to push after owner approval.

## Update or remove

The installer never merges into or deletes an existing skill. To update, review
the new version, move your existing skill folder to a backup outside the skill
search directories, then rerun the installer. Preserve any local changes you
made. To uninstall, remove only this skill's installed directory after checking
that you stored no personal work inside it. Collection workspaces remain separate.

## Limitations

The package uses ordinary skill files. Copying, initialization, and metadata
checks are tested locally; those checks do not establish successful skill
loading in every agent version. The local history reader supports known
Claude Code and Codex transcript formats and reports gaps. It cannot recover
deleted logs or unlock inaccessible cloud chats. There is no paid model runner
or automatic upload.
A model run requires a separately authorized model/tool configuration.

## Sources

- Skill entrypoint: [collect-agent-failures](../skills/collect-agent-failures/SKILL.md).
- Installer: [install_skill.py](../commands/install_skill.py).
- Detailed evidence checklist: [EVIDENCE.md](EVIDENCE.md).
- Local skill discovery: [OpenAI documentation](https://learn.chatgpt.com/docs/build-skills)
  and [Claude Code documentation](https://code.claude.com/docs/en/skills).
