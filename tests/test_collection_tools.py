"""Exercise contribution safeguards in temporary repositories, without model calls.

Run with ``python3 -m unittest discover -s tests -v``. Every test copies the
commands and templates before importing or invoking them; the real collection
and contributors' histories are never opened or changed.
"""

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]


def load_copy(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    return module


class CollectionToolsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "collection"
        self.root.mkdir()
        for directory in ("commands", "templates"):
            shutil.copytree(REPOSITORY / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for directory in ("problems", "results"):
            (self.root / directory).mkdir()
        self.scaffold = load_copy(self.root / "commands/new_problem.py", "scaffold_copy")
        self.validator = load_copy(self.root / "commands/validate.py", "validator_copy")
        self.package = self.scaffold.create_problem("forgotten-rule", self.root)
        self.manifest = self.package / "problem.json"
        self.problem = json.loads(self.manifest.read_text(encoding="utf-8"))

    def write_problem(self):
        self.manifest.write_text(json.dumps(self.problem) + "\n", encoding="utf-8")

    def validate(self, submission=False):
        self.write_problem()
        return self.validator.validate_collection(self.root, submission=submission)

    def packaged(self, status="packaged"):
        self.problem["status"] = status
        self.problem["symptoms"] = ["1.1"]
        self.problem["horizon"].update({
            "earlier_event": "A startup validation rule was established.",
            "later_decision": "A later option omitted that validation.",
            "intervening_work": "Another feature and a new session intervened.",
            "mechanism": "The rule remained available in the project guide.",
        })
        self.problem["failure"].update({
            "expected_behavior": "Reject invalid option values before starting.",
            "observed_behavior": "The option accepts an invalid value.",
            "target_predicate": "The later option starts with an invalid value.",
        })
        self.problem["commands"].update({
            "setup": "python3 environment/setup.py",
            "run_agent": "python3 environment/run_agent.py",
            "judge": "python3 checks/judge.py",
            "check_reference": "python3 checks/check_reference.py",
        })

    def result(self, run_id="main-attempt", **updates):
        data = json.loads((self.root / "templates/result.json").read_text(encoding="utf-8"))
        data.update({
            "problem_id": self.problem["id"],
            "run_id": run_id,
            "kind": "model_run",
            "phase": "development",
            "condition": "main",
            "model": "test-model",
            "agent": "test-agent",
            "task_revision": "task-v1",
            "judge_revision": "judge-v1",
            "started_at": "2026-10-10T12:00:00Z",
            "validity": "valid",
            "exclusion_reason": None,
            "preconditions_met": True,
            "failure_opportunity_reached": True,
            "task_success": False,
            "target_failure": True,
            "evidence": ["trace.txt"],
            "notes": "Synthetic test fixture; never a claimed contribution or model run.",
        })
        data.update(updates)
        directory = self.root / "results" / self.problem["id"] / run_id
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "trace.txt").write_text("Synthetic test evidence.\n", encoding="utf-8")
        path = directory / "summary.json"
        self.write_result(path, data)
        reference = path.relative_to(self.root).as_posix()
        if reference not in self.problem["result_records"]:
            self.problem["result_records"].append(reference)
        return path, data

    @staticmethod
    def write_result(path, data):
        path.write_text(json.dumps(data) + "\n", encoding="utf-8")

    def temporal_pair(self):
        self.packaged("temporal_supported")
        self.problem["horizon"]["causal_claim"] = "supported"
        self.problem["commands"]["control"] = "python3 environment/run_control.py"
        self.problem["comparison_note"] = (
            "The paired control restates the earlier rule immediately before the decision; "
            "interpret this one pair cautiously."
        )
        main = self.result(pair_id="pair-one")
        control = self.result("control-attempt", condition="control", pair_id="pair-one",
                              target_failure=False, task_success=True)
        return main, control

    def test_scaffold_assigns_id_and_keeps_an_unreviewed_draft(self):
        self.assertEqual(self.problem["id"], "forgotten-rule")
        self.assertEqual(self.problem["status"], "incident")
        self.assertFalse(self.problem["privacy_reviewed"])
        for name in ("README.md", "task", "environment", "checks", "reference"):
            self.assertTrue((self.package / name).exists())

    def test_scaffold_rejects_invalid_ids_and_path_traversal(self):
        for slug in ("", "../outside", "/outside", "a/b", "Bad-Id", "bad_id",
                     "a--b", "-a", "a-", "2first", "éxample", None, 1):
            with self.subTest(slug=slug), self.assertRaises(ValueError):
                self.scaffold.create_problem(slug, self.root)
        self.assertEqual([p.name for p in (self.root / "problems").iterdir()], ["forgotten-rule"])

    def test_scaffold_refuses_overwrite_without_changing_existing_files(self):
        sentinel = self.package / "owner-notes.txt"
        sentinel.write_text("Keep this owner's work.\n", encoding="utf-8")
        original = self.manifest.read_bytes()
        with self.assertRaises(ValueError):
            self.scaffold.create_problem("forgotten-rule", self.root)
        self.assertEqual(self.manifest.read_bytes(), original)
        self.assertEqual(sentinel.read_text(), "Keep this owner's work.\n")

    def test_scaffold_rejects_a_dangling_destination_symlink(self):
        destination = self.root / "problems/dangling"
        destination.symlink_to(self.root / "missing")
        with self.assertRaises(ValueError):
            self.scaffold.create_problem("dangling", self.root)
        self.assertTrue(destination.is_symlink())

    def test_scaffold_rejects_a_symlinked_problems_directory(self):
        original = self.root / "problems"
        original.rename(self.root / "moved-problems")
        original.symlink_to(self.root / "moved-problems", target_is_directory=True)
        with self.assertRaises(ValueError):
            self.scaffold.create_problem("second-incident", self.root)

    def test_scaffold_rejects_a_symlink_inside_the_template(self):
        (self.root / "templates/problem/copied-evidence").symlink_to(self.manifest)
        with self.assertRaises(ValueError):
            self.scaffold.create_problem("second-incident", self.root)
        self.assertFalse((self.root / "problems/second-incident").exists())

    def test_scaffold_rejects_a_symlinked_template_root(self):
        source = self.root / "templates/problem"
        source.rename(self.root / "template-elsewhere")
        source.symlink_to(self.root / "template-elsewhere", target_is_directory=True)
        with self.assertRaises(ValueError):
            self.scaffold.create_problem("second-incident", self.root)

    def test_incident_draft_accepts_unknown_horizon_and_no_results(self):
        checked = self.validate()
        self.assertEqual(len(checked), 1)
        self.assertEqual(checked[0][1], [])
        self.assertIsNone(checked[0][0]["horizon"]["assistant_turns_between"])

    def test_submission_requires_an_owner_privacy_review(self):
        with self.assertRaisesRegex(self.validator.Invalid, "review"):
            self.validate(submission=True)
        self.problem["privacy_reviewed"] = True
        self.validate(submission=True)

    def test_packaged_task_requires_each_execution_command(self):
        self.packaged()
        baseline = copy.deepcopy(self.problem)
        for field in ("setup", "run_agent", "judge", "check_reference"):
            with self.subTest(field=field):
                self.problem = copy.deepcopy(baseline)
                self.problem["commands"][field] = None
                with self.assertRaisesRegex(self.validator.Invalid, "commands"):
                    self.validate()
        self.problem = baseline
        self.validate()

    def test_validator_never_executes_declared_commands(self):
        self.packaged()
        marker = self.root / "COMMAND-MUST-NOT-RUN"
        self.problem["commands"] = {key: f"touch '{marker}'" for key in self.problem["commands"]}
        self.write_problem()
        completed = subprocess.run([sys.executable, "commands/validate.py"], cwd=self.root,
                                   text=True, capture_output=True, check=False)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertFalse(marker.exists())

    def test_scripted_hit_does_not_establish_model_reproduction(self):
        self.packaged("model_reproduced")
        self.result(kind="scripted_check", model=None, agent=None)
        with self.assertRaisesRegex(self.validator.Invalid, "model run"):
            self.validate()

    def test_model_reproduction_requires_a_main_condition_hit(self):
        self.packaged("model_reproduced")
        path, data = self.result(condition="control")
        with self.assertRaises(self.validator.Invalid):
            self.validate()
        data.update(condition="main", target_failure=False)
        self.write_result(path, data)
        with self.assertRaises(self.validator.Invalid):
            self.validate()
        data["target_failure"] = True
        self.write_result(path, data)
        self.validate()

    def test_valid_result_requires_preconditions_and_failure_opportunity(self):
        path, data = self.result()
        for field in ("preconditions_met", "failure_opportunity_reached"):
            for value in (None, False):
                with self.subTest(field=field, value=value):
                    altered = copy.deepcopy(data)
                    altered[field] = value
                    self.write_result(path, altered)
                    with self.assertRaisesRegex(self.validator.Invalid, "preconditions"):
                        self.validate()

    def test_valid_result_requires_both_separate_outcomes(self):
        path, data = self.result()
        for field in ("task_success", "target_failure"):
            with self.subTest(field=field):
                altered = copy.deepcopy(data)
                altered[field] = None
                self.write_result(path, altered)
                with self.assertRaises(self.validator.Invalid):
                    self.validate()

    def test_invalid_or_unjudgeable_attempt_cannot_claim_either_target_outcome(self):
        path, data = self.result()
        for validity in ("invalid", "unjudgeable"):
            for outcome in (False, True):
                with self.subTest(validity=validity, outcome=outcome):
                    altered = copy.deepcopy(data)
                    altered.update(validity=validity, exclusion_reason="Setup did not finish.",
                                   target_failure=outcome)
                    self.write_result(path, altered)
                    with self.assertRaisesRegex(self.validator.Invalid, "target_failure null"):
                        self.validate()

    def test_excluded_attempt_requires_a_reason(self):
        self.result(validity="invalid", target_failure=None, task_success=None)
        with self.assertRaisesRegex(self.validator.Invalid, "explanation"):
            self.validate()

    def test_known_task_outcome_is_allowed_for_an_invalid_attempt(self):
        self.result(validity="invalid", exclusion_reason="The failure opportunity was not reached.",
                    failure_opportunity_reached=False, target_failure=None, task_success=False)
        self.validate()

    def test_valid_control_can_avoid_the_target_failure(self):
        self.result(condition="control", target_failure=False, task_success=True)
        self.validate()

    def test_task_failure_without_the_target_failure_is_a_valid_outcome(self):
        self.result(target_failure=False, task_success=False)
        self.validate()

    def test_boolean_and_negative_counts_are_rejected(self):
        baseline = copy.deepcopy(self.problem)
        for value in (True, False, -1, 1.5, "12"):
            with self.subTest(value=value):
                self.problem = copy.deepcopy(baseline)
                self.problem["horizon"]["assistant_turns_between"] = value
                with self.assertRaises(self.validator.Invalid):
                    self.validate()
        self.problem = baseline
        path, data = self.result()
        for value in (True, -1, "20", 2.5):
            with self.subTest(actual_tool_calls=value):
                altered = copy.deepcopy(data)
                altered["actual_horizon"]["tool_calls"] = value
                self.write_result(path, altered)
                with self.assertRaises(self.validator.Invalid):
                    self.validate()

    def test_unknown_and_zero_counts_and_fractional_seconds_are_allowed(self):
        self.problem["horizon"].update(assistant_turns_between=0, elapsed_seconds=0.25)
        self.result(actual_horizon={"assistant_turns": None, "tool_calls": 0,
                                    "sessions": 1, "elapsed_seconds": 0.125})
        self.validate()

    def test_result_outcome_numbers_are_not_booleans(self):
        path, data = self.result()
        for field in ("task_success", "target_failure", "preconditions_met", "failure_opportunity_reached"):
            with self.subTest(field=field):
                altered = copy.deepcopy(data)
                altered[field] = 1
                self.write_result(path, altered)
                with self.assertRaisesRegex(self.validator.Invalid, "true, false, or null"):
                    self.validate()

    def test_malformed_metadata_shapes_are_rejected(self):
        baseline = copy.deepcopy(self.problem)
        for field, value in (("source", []), ("horizon", None), ("symptoms", "1.1"),
                             ("commands", "run"), ("result_records", {}),
                             ("privacy_reviewed", 1), ("schema_version", True)):
            with self.subTest(field=field):
                self.problem = copy.deepcopy(baseline)
                self.problem[field] = value
                with self.assertRaises(self.validator.Invalid):
                    self.validate()

    def test_evidence_cannot_escape_its_run_directory(self):
        path, data = self.result()
        outside = self.root / "private.txt"
        outside.write_text("Private fixture.\n", encoding="utf-8")
        for reference in (str(outside), "../../../private.txt"):
            with self.subTest(reference=reference):
                data["evidence"] = [reference]
                self.write_result(path, data)
                with self.assertRaises(self.validator.Invalid):
                    self.validate()

    def test_evidence_symlinks_and_symlinked_parent_directories_are_rejected(self):
        path, data = self.result()
        external = self.root / "outside-evidence"
        external.mkdir()
        (external / "trace.txt").write_text("External fixture.\n", encoding="utf-8")
        (path.parent / "link.txt").symlink_to(external / "trace.txt")
        (path.parent / "linked-directory").symlink_to(external, target_is_directory=True)
        for reference in ("link.txt", "linked-directory/trace.txt"):
            with self.subTest(reference=reference):
                data["evidence"] = [reference]
                self.write_result(path, data)
                with self.assertRaisesRegex(self.validator.Invalid, "Symbolic links"):
                    self.validate()

    def test_missing_empty_or_self_citing_evidence_is_rejected(self):
        path, data = self.result()
        (path.parent / "empty.txt").write_text("", encoding="utf-8")
        for evidence in ([], ["missing.txt"], ["empty.txt"], ["summary.json"], ["./summary.json"]):
            with self.subTest(evidence=evidence):
                data["evidence"] = evidence
                self.write_result(path, data)
                with self.assertRaises(self.validator.Invalid):
                    self.validate()

    def test_missing_linked_result_is_rejected(self):
        self.problem["result_records"] = ["results/forgotten-rule/missing/summary.json"]
        with self.assertRaisesRegex(self.validator.Invalid, "Missing file"):
            self.validate()

    def test_orphan_result_is_rejected_by_whole_collection_validation(self):
        self.result()
        self.problem["result_records"] = []
        with self.assertRaisesRegex(self.validator.Invalid, "Unlinked result"):
            self.validate()

    def test_result_cannot_be_linked_from_a_different_problem(self):
        path, data = self.result()
        data["problem_id"] = "another-incident"
        self.write_result(path, data)
        with self.assertRaisesRegex(self.validator.Invalid, "different problem"):
            self.validate()

    def test_duplicate_result_links_cannot_inflate_the_attempt_count(self):
        self.result()
        self.problem["result_records"] *= 2
        with self.assertRaisesRegex(self.validator.Invalid, "Duplicate result"):
            self.validate()

    def test_symlinked_result_record_is_rejected(self):
        path, _ = self.result()
        moved = self.root / "moved-summary.json"
        path.rename(moved)
        path.symlink_to(moved)
        with self.assertRaisesRegex(self.validator.Invalid, "Symbolic links"):
            self.validate()

    def test_temporal_status_accepts_a_linked_comparison_and_written_note(self):
        self.temporal_pair()
        self.validate()

    def test_temporal_status_requires_a_comparison_note(self):
        self.temporal_pair()
        self.problem["comparison_note"] = None
        with self.assertRaisesRegex(self.validator.Invalid, "written assessment"):
            self.validate()

    def test_temporal_status_requires_a_control_command(self):
        self.temporal_pair()
        self.problem["commands"]["control"] = None
        with self.assertRaisesRegex(self.validator.Invalid, "comparison command"):
            self.validate()

    def test_temporal_status_rejects_unpaired_or_incomparable_controls(self):
        _, (path, control) = self.temporal_pair()
        for field, value in (("pair_id", None), ("pair_id", "another-pair"),
                             ("model", "another-model"), ("agent", "another-agent"),
                             ("task_revision", "task-v2"), ("judge_revision", "judge-v2")):
            with self.subTest(field=field, value=value):
                altered = copy.deepcopy(control)
                altered[field] = value
                self.write_result(path, altered)
                with self.assertRaisesRegex(self.validator.Invalid, "linked comparable"):
                    self.validate()
        altered = copy.deepcopy(control)
        altered["settings"]["seed"] = 999
        self.write_result(path, altered)
        with self.assertRaisesRegex(self.validator.Invalid, "linked comparable"):
            self.validate()

    def test_supported_temporal_claim_cannot_bypass_the_comparison_tier(self):
        self.packaged("model_reproduced")
        self.result()
        self.problem["horizon"]["causal_claim"] = "supported"
        with self.assertRaisesRegex(self.validator.Invalid, "comparison evidence"):
            self.validate()


if __name__ == "__main__":
    unittest.main()
