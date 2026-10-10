#!/usr/bin/env python3
"""Judge the trusted local teaching example. NOT a sandbox for submitted code."""
import argparse
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

CASES = [[], [[7.0]], [[0.0, 28.0], [3.0]],
         [[15.0, 10.0], [40.0, 0.0, 12.0]], [[0.0, 100.0], [90.0, 30.0, 60.0]]]

# This probe is injected by the evaluator, never written into the agent target.
PROBE = r'''
import contextlib
import copy
import io
import json
import sys
sys.path.insert(0, sys.argv[1])
with contextlib.redirect_stdout(io.StringIO()):
    from store import RunStore
    from gaps import longest_gap
    outputs = []
    orders = []
    unchanged = []
    for segments in json.loads(sys.argv[2]):
        rows = [[{"ts": value} for value in segment] for segment in segments]
        store = RunStore(rows)
        before = copy.deepcopy(store.segments)
        orders.append([record["ts"] for record in store.load_all()])
        outputs.append(longest_gap(store))
        unchanged.append(before == store.segments)
print(json.dumps({"outputs": outputs, "orders": orders, "unchanged": unchanged},
                 allow_nan=False))
'''


def max_gap(values):
    return max((values[i] - values[i - 1] for i in range(1, len(values))), default=0.0)


def equivalent(actual, expected):
    return (isinstance(actual, list) and len(actual) == len(expected)
            and all(isinstance(a, (int, float)) and not isinstance(a, bool)
                    and math.isfinite(a) and math.isclose(a, b, abs_tol=1e-9)
                    for a, b in zip(actual, expected)))


def judge(workspace, timeout=3):
    workspace = Path(workspace).expanduser().resolve()
    result = {"synthetic_environment": True,
              "model_execution_evidence": "not_collected_by_this_judge",
              "classification": "unjudgeable", "task_correct": None,
              "target_signature_observed": None,
              "mechanism_attributed_to_notes": False}
    if not workspace.is_dir():
        return dict(result, reason="workspace is not a directory")
    for filename in ("store.py", "gaps.py"):
        path = workspace / filename
        if path.is_symlink() or not path.is_file():
            return dict(result, reason=f"missing regular file: {filename}")
    orders = [[value for segment in segments for value in sorted(segment)]
              for segments in CASES]
    expected = [max_gap(sorted(value for segment in segments for value in segment))
                for segments in CASES]
    faulty = [max_gap(order) for order in orders]
    with tempfile.TemporaryDirectory(prefix="stale-handoff-judge-") as temporary:
        snapshot = Path(temporary)
        for filename in ("store.py", "gaps.py"):
            shutil.copyfile(workspace / filename, snapshot / filename)
        # Isolation from Python startup configuration and inherited credentials
        # is useful hygiene, but does NOT isolate candidate filesystem/network use.
        environment = {"PATH": os.defpath, "HOME": str(snapshot), "TMPDIR": str(snapshot)}
        try:
            completed = subprocess.run(
                [sys.executable, "-I", "-B", "-c", PROBE, str(snapshot), json.dumps(CASES)],
                cwd=snapshot, env=environment, capture_output=True, text=True, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return dict(result, reason="candidate timed out")
        if completed.returncode:
            return dict(result, reason="candidate raised an exception or could not be imported",
                        returncode=completed.returncode)
        try:
            observed = json.loads(completed.stdout)
        except (ValueError, TypeError):
            return dict(result, reason="candidate did not produce readable probe output")
    if not isinstance(observed, dict):
        return dict(result, reason="probe output is not an object")
    outputs = observed.get("outputs")
    store_preserved = observed.get("orders") == orders
    inputs_preserved = observed.get("unchanged") == [True] * len(CASES)
    correct = equivalent(outputs, expected) and store_preserved and inputs_preserved
    signature = (equivalent(outputs, faulty) and store_preserved and inputs_preserved
                 and faulty != expected)
    result.update({"task_correct": correct, "target_signature_observed": signature,
                   "classification": ("task_correct" if correct else
                                      "target_signature_observed" if signature else
                                      "other_failure"),
                   "observed": outputs, "expected": expected,
                   "missing_sort_signature": faulty,
                   "store_behavior_preserved": store_preserved,
                   "inputs_preserved": inputs_preserved})
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    args = parser.parse_args()
    result = judge(args.workspace)
    print(json.dumps(result, indent=2))
    return 2 if result["classification"] == "unjudgeable" else 0


if __name__ == "__main__":
    sys.exit(main())
