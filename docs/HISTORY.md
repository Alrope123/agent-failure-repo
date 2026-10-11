# Read historical Claude Code and Codex runs

Updated 2026-10-10.

## Summary

Review past runs from **both Claude Code and Codex** for the authorized project.
Either agent can collect from both tools when it has local file access. The
current conversation is supplementary evidence. Search all available matching
transcripts, preserve the sequence of actions, and account for missing records.

The helper below only inventories and reads local files. The collecting agent
must still review their contents, identify failures, and build reproductions.
It never starts or resumes the historical agents or executes recorded commands.

## Find the project's transcripts

Record the target project's absolute path before switching into the collection
workspace. From that workspace, run:

```bash
python3 commands/history.py inventory --project /path/to/target-project --output .local/history-index.json
```

The command checks both providers. It selects sources using recorded working
directories, not a guess from an encoded folder name. A working directory must
equal the authorized project path or be inside it. Unrelated sessions are
excluded from content review. Sessions with missing or conflicting project
metadata require scope resolution; do not silently count them as reviewed.

| Tool | Default local transcript location | Custom root |
| --- | --- | --- |
| Claude Code | `~/.claude/projects/` transcripts, including subagents and saved alternative versions | `CLAUDE_CONFIG_DIR` or `--claude-home` |
| Codex | `~/.codex/sessions/**/*.jsonl` and `~/.codex/archived_sessions/**/*.jsonl` | `CODEX_HOME` or `--codex-home` |

Sources: [Claude Code session storage](https://code.claude.com/docs/en/claude-directory#application-data), [Claude Code environment variables](https://code.claude.com/docs/en/env-vars), and [Codex transcript locations](https://learn.chatgpt.com/docs/reference/troubleshooting).
Storage formats can change; the helper supports the record shapes described below.

`CLAUDE_CONFIG_DIR` is the environment variable for Claude Code's storage root.
`CODEX_HOME` is the equivalent root variable for Codex. The explicit command
options override those variables for this read without changing your settings.

Use an explicit root when the contributor has identified a different local
installation or a copied transcript store:

```bash
python3 commands/history.py inventory --project /path/to/target-project --claude-home /path/to/claude-store --codex-home /path/to/codex-store --output .local/history-index-custom.json
```

For a moved checkout or another authorized worktree, repeat `--project` with
the exact additional path. Do not broaden it to the entire home directory to
make matches appear. Older path aliases and external projects need explicit
scope. The helper does not discover other accounts, remote machines, or cloud
histories. Supplied exports can be reviewed separately and listed in coverage.

The helper filters by project, not by date or named conversation. If permission
is narrower than a whole project's history, select only authorized sources and
ranges before reading content; use a scoped export when metadata cannot establish
those boundaries. Do not treat the helper's eligibility flag as broader permission.

The index records checked locations, access problems, matching sources, parse
problems, and source fingerprints. It contains no transcript message bodies,
but its paths and identifiers are private. Output files are created with owner
read/write permissions and never overwritten. Use a new filename to refresh
an inventory. Keep old fingerprints with existing evidence references.

## Read every selected source through its end

For each eligible source in the index, substitute its `id` below:

```bash
python3 commands/history.py read --index .local/history-index.json --source SOURCE_ID --start-line 1 --max-lines 200
```

Read the returned events in order. Each has an original source line anchor.
`next_start_line` is the starting line for the next page; `eof` means the end
of the file. Continue until `eof` is true. The page size controls
one read, not how much of the source to inspect. There is no newest-only filter
or maximum number of sessions. If a tool truncates output, reduce the page
size and revisit that page; for a single oversized record, save the page in
private storage and read its visible fields in smaller pieces.

Save reviewed line ranges, remaining ranges, requirements carried forward,
and open candidates in `.local/collection-report.md`. A file in the index has
only been discovered. It is reviewed only after its available content has
been read and its omissions accounted for. Read the middle of long sessions
as carefully as their beginnings and endings.

The reader checks file identity, size, modification time, and project metadata
against the index. If those changed, it asks for a fresh inventory. It records
a full content hash during inventory and uses line checkpoints for fast page
reads. For an active run, make a new inventory and reconcile the changed ranges
without overwriting old evidence. Do not restart a past run to inspect it: that would create new actions
instead of reading the original record.

Reader output is **private, unredacted evidence** and may contain credentials,
code, or personal information from ordinary messages and tools. Keep saved
pages under `.local/`; it is not a sanitizer. Never paste raw pages into a
public issue or commit them. Follow [the sharing review](REVIEW.md).

## Preserve actions, relationships, and gaps

| Source detail | How to use it |
| --- | --- |
| Claude user and assistant records | Read ordinary text, tool requests, and tool results. Keep message and parent IDs, model metadata, timestamps, and original line anchors where recorded. |
| Claude subagent records | Inspect files under a matched parent's `subagents/` directory too. Some versions omit their own project or timestamp; retain the parent link and mark missing timing unknown. |
| Claude saved versions | Treat saved alternatives as versions, not independent runs. |
| Separate large outputs | Follow relevant `tool-results/` references; account for missing files. |
| Codex response items | Read visible messages, function/custom/shell calls, and their outputs. Preserve call IDs so actions can be paired with results. |
| Codex event messages | Some mirror response items. Retain provenance and distinguish duplicate representations from new actions before counting turns or incidents. |
| Resumed or forked histories | Preserve file identity and ancestry; reconcile replayed events before counting. |
| Compaction or reset | Record the boundary and any available summary. It does not reconstruct removed messages or prove which earlier information remained in the model's context. |
| Unsupported or malformed records | Record their line anchors and types. Resolve using an authorized export or a reader adapted to that version; retain an explicit gap if unresolved. |

Source: [the local reader](../commands/history.py), whose supported formats are
tested with synthetic records. These are format-handling rules, not a claim
that every historical version uses an identical schema.

Source: Claude Code's [application-data layout](https://code.claude.com/docs/en/claude-directory#application-data) documents saved alternatives and separate large tool outputs.
Include `.orphaned-…jsonl` and `.jsonl.superseded-…` records as alternative
versions. A referenced history does not grant access to another project.
The JSON reader does not automatically open those separate output files. Read
relevant referenced outputs privately, preserve their file anchors, and record
missing files. Avoid scanning unrelated session folders for extra material.

The reader deliberately omits private thinking/reasoning blocks and binary
attachments. It reports omissions and unknown shapes instead of dumping
arbitrary record bodies. Use observable messages, actions, outputs, code, and
tests as evidence. Missing attachments or unhandled tool-output formats can
limit a finding; identify them. Do not request hidden reasoning to fill a gap.

Never treat JSON lines, transcript files, or replayed messages as independent
agent turns or runs. State the counting rule and verified endpoints for the
observed horizon. Preserve raw anchors even when combining related histories.
Do not discard identical actions merely because their text repeats: an agent
may actually have retried the same command.

## Report coverage and limitations for both tools

Keep a Claude Code row and a Codex row in the coverage report. For each, record
the checked root, access status, matching files, logical sessions where known,
reviewed ranges, and remaining work. Distinguish these outcomes:

- **Reviewed:** identify the exact sources and ranges, with unresolved omissions.
- **No matching project:** the checked records have no verified match; confirm
  an authorized old path or worktree if the contributor expects more.
- **Missing or inaccessible:** state which store could not be read. Continue
  with the other tool and request a selected export only if needed.
- **Unknown or unsupported:** record the metadata or parsing problem and the
  next action; do not label the session empty.

Histories may have been deleted, retained elsewhere, or never persisted.
Prompt indexes such as `history.jsonl`, session titles, and Git logs are leads
or corroboration; they cannot substitute for an agent's complete interaction
record. Record unavailable evidence honestly. Absence of logs is not evidence
of absence of failures.

Continue with [the failure-search passes](FINDING_FAILURES.md),
[all 20 symptoms](SYMPTOMS.md), and [the evidence checklist](EVIDENCE.md).
The final report must say what was actually reviewed from each tool.
