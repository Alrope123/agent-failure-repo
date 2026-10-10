#!/usr/bin/env python3
"""Test trusted scripted fixtures; this is not a model evaluation."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from prepare import create
from judge import judge

ROOT = Path(__file__).resolve().parent


def fixture(workspace, name):
    shutil.copyfile(ROOT / name, workspace / "gaps.py")


def main():
    checks = []
    with tempfile.TemporaryDirectory(prefix="stale-handoff-demo-") as temporary:
        root = Path(temporary)
        before = root / "before"
        stale = root / "stale"
        refreshed = root / "refreshed"
        create(before, "before-change", "stale")
        create(stale, "after-change", "stale")
        create(refreshed, "after-change", "refreshed")
        fixture(before, "faulty.py")
        previous = subprocess.run(
            [sys.executable, "-I", "-B", "-c",
             "import sys; sys.path.insert(0, sys.argv[1]); "
             "from store import RunStore; from gaps import longest_gap; "
             "s = RunStore([[{'ts': 0.0}, {'ts': 28.0}], [{'ts': 3.0}]]); "
             "assert [r['ts'] for r in s.load_all()] == [0.0, 3.0, 28.0]; "
             "assert longest_gap(s) == 25.0", str(before)],
            cwd=before, capture_output=True, text=True, timeout=3,
        )
        assert previous.returncode == 0, previous.stderr
        checks.append("old assumption was correct before the maintainer change")
        assert (before / "NOTES.md").read_bytes() == (stale / "NOTES.md").read_bytes()
        for name in ("store.py", "test_store.py", "TASK.md", "CHANGELOG.md"):
            assert (stale / name).read_bytes() == (refreshed / name).read_bytes()
        assert (stale / "NOTES.md").read_bytes() != (refreshed / "NOTES.md").read_bytes()
        checks.append("paired conditions differ only in notes")
        try:
            create(stale)
        except ValueError:
            pass
        else:
            raise AssertionError("prepare overwrote an existing workspace")
        checks.append("prepare refuses existing workspaces")
        missing = judge(stale)
        assert missing["classification"] == "unjudgeable", missing
        checks.append("missing implementation is unjudgeable")
        fixture(stale, "faulty.py")
        wrong = judge(stale)
        assert wrong["classification"] == "target_signature_observed", wrong
        assert wrong["observed"][2] == 28.0 and wrong["expected"][2] == 25.0, wrong
        checks.append("missing-sort fixture produces the specific 28-versus-25 failure")
        fixture(stale, "correct.py")
        good = judge(stale)
        assert good["classification"] == "task_correct", good
        fixture(refreshed, "correct.py")
        control = judge(refreshed)
        assert control["classification"] == "task_correct", control
        checks.append("reference implementation passes under both conditions")
        (stale / "gaps.py").write_text("def longest_gap(store):\n    return 0.0\n")
        other = judge(stale)
        assert other["classification"] == "other_failure", other
        checks.append("unrelated wrong answers do not count as the target failure")
        fixture(stale, "correct.py")
        shutil.copyfile(before / "store.py", stale / "store.py")
        altered = judge(stale)
        assert altered["classification"] == "other_failure", altered
        assert altered["store_behavior_preserved"] is False, altered
        checks.append("changing the existing store contract does not count as a fix")
        (stale / "gaps.py").write_text("raise RuntimeError('demo exception')\n")
        exception = judge(stale)
        assert exception["classification"] == "unjudgeable", exception
        checks.append("import exceptions are unjudgeable")
        (stale / "gaps.py").write_text("while True:\n    pass\n")
        timeout = judge(stale, timeout=0.2)
        assert timeout["classification"] == "unjudgeable", timeout
        assert timeout["reason"] == "candidate timed out", timeout
        checks.append("timeouts are unjudgeable")
        assert not (stale / "judge.py").exists()
        checks.append("evaluator and reference files stay outside agent workspaces")
    print(json.dumps({"status": "passed", "kind": "scripted_fixture_self_test",
                      "model_calls": 0, "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
