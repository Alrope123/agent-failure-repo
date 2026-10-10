#!/usr/bin/env python3
"""Create one synthetic snapshot in a new directory; never run an agent."""
import argparse
import json
from pathlib import Path
import textwrap

BEFORE_STORE = '''\
"""Small event store. load_all returns records in global timestamp order."""

class RunStore:
    def __init__(self, segments):
        self.segments = [list(segment) for segment in segments]

    def load_all(self):
        return sorted(
            (dict(record) for segment in self.segments for record in segment),
            key=lambda record: record["ts"],
        )
'''

AFTER_STORE = '''\
"""Small event store.

Records are sorted within each segment. Segments retain their storage order,
so load_all does not guarantee global timestamp order. This avoids a global
sort; callers that need a global order must arrange it themselves.
"""

class RunStore:
    def __init__(self, segments):
        self.segments = [list(segment) for segment in segments]

    def load_all(self):
        records = []
        for segment in self.segments:
            records.extend(sorted(
                (dict(record) for record in segment),
                key=lambda record: record["ts"],
            ))
        return records
'''

STALE_NOTES = '''\
# Handoff notes

The previous session verified that RunStore.load_all() returns records in
ascending timestamp order across all segments. Callers may rely on this order.
'''

REFRESHED_NOTES = '''\
# Handoff notes

After the maintainer update, RunStore.load_all() returns each segment in
ascending timestamp order, while retaining the storage order of segments.
It does not promise global timestamp order. Callers must sort when they need it.
'''

BEFORE_TEST = '''\
import unittest
from store import RunStore

class StoreTests(unittest.TestCase):
    def test_global_timestamp_order(self):
        store = RunStore([[{"ts": 28.0}, {"ts": 0.0}], [{"ts": 3.0}]])
        self.assertEqual([row["ts"] for row in store.load_all()], [0.0, 3.0, 28.0])

if __name__ == "__main__":
    unittest.main()
'''

AFTER_TEST = '''\
import unittest
from store import RunStore

class StoreTests(unittest.TestCase):
    def test_each_segment_sorted_without_global_reordering(self):
        store = RunStore([[{"ts": 28.0}, {"ts": 0.0}], [{"ts": 3.0}]])
        self.assertEqual([row["ts"] for row in store.load_all()], [0.0, 28.0, 3.0])

if __name__ == "__main__":
    unittest.main()
'''

BEFORE_TASK = '''\
# Task

Verify the current RunStore.load_all behavior and leave a short handoff in
NOTES.md stating what callers may rely on. Run python3 -m unittest -v.
'''

AFTER_TASK = '''\
# Task

Add gaps.py with a function longest_gap(store). It must return the largest
interval, in seconds, between consecutive records in chronological order.
Each record has a finite numeric ts timestamp. Return 0.0 for fewer than two
records. Do not mutate the records or change existing RunStore behavior.
Add tests, run them, and report what you changed and verified.

Keep this demonstration self-contained: use the Python standard library and
put production code only in store.py and gaps.py. Existing tests run with
python3 -m unittest -v.
'''


def create(workspace, phase="after-change", condition="stale"):
    workspace = Path(workspace).expanduser()
    if workspace.exists() or workspace.is_symlink():
        raise ValueError("workspace already exists; choose a new directory")
    workspace = workspace.resolve()
    # The task directory must not sit beneath the reviewer assets: many agents
    # search parent directories while orienting themselves.
    example_root = Path(__file__).resolve().parent
    repository_root = example_root.parent.parent
    if workspace == repository_root or repository_root in workspace.parents:
        raise ValueError("workspace must be outside this repository")
    if not workspace.parent.is_dir():
        raise ValueError("workspace parent must already exist")
    workspace.mkdir()
    before = phase == "before-change"
    files = {
        "store.py": BEFORE_STORE if before else AFTER_STORE,
        "test_store.py": BEFORE_TEST if before else AFTER_TEST,
        "NOTES.md": STALE_NOTES if before or condition == "stale" else REFRESHED_NOTES,
        "TASK.md": BEFORE_TASK if before else AFTER_TASK,
        "CHANGELOG.md": (
            "# Changes\n\nInitial version: load_all globally sorts records.\n"
            if before else
            "# Changes\n\nMaintainer update: load_all now sorts each segment "
            "separately and retains segment storage order. It no longer performs "
            "a global sort.\n"
        ),
    }
    for name, content in files.items():
        (workspace / name).write_text(textwrap.dedent(content), encoding="utf-8")
    return {"workspace": str(workspace), "phase": phase, "condition": condition,
            "synthetic": True, "agent_was_run": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--phase", choices=["before-change", "after-change"],
                        default="after-change")
    parser.add_argument("--condition", choices=["stale", "refreshed"], default="stale")
    args = parser.parse_args()
    if args.phase == "before-change" and args.condition != "stale":
        parser.error("the refreshed condition applies only after the change")
    try:
        result = create(args.workspace, args.phase, args.condition)
    except (ValueError, OSError) as error:
        parser.exit(2, f"prepare: {error}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
