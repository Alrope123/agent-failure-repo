#!/usr/bin/env python3
"""Check collection metadata only. Never execute task or evaluation commands."""
import argparse
import json
import math
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
STATUSES = {"incident", "packaged", "model_reproduced", "temporal_supported"}
SYMPTOMS = {f"{group}.{item}" for group, size in enumerate((3, 4, 3, 2, 5, 3), 1)
            for item in range(1, size + 1)} | {"other"}


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def shape(value, fields, label):
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == set(fields.split()), f"{label} fields must be: {fields}")


def choice(value, values, label):
    require(isinstance(value, str) and value in values, f"Invalid {label}: {value!r}")


def optional_text(value, label):
    require(value is None or nonempty(value), f"{label} must be nonempty text or null")


def counts(data, fields, label):
    shape(data, fields, label)
    for key, value in data.items():
        if value is None:
            continue
        valid = type(value) in (int, float) and math.isfinite(value) and value >= 0
        if "seconds" not in key:
            valid = valid and type(value) is int
        require(valid, f"{label}.{key} must be a nonnegative count or null")


def local_file(base, relative):
    require(nonempty(relative), "File reference must be nonempty text")
    path = Path(relative)
    require(not path.is_absolute() and ".." not in path.parts,
            f"Use a relative file path without '..': {relative}")
    current = base
    for part in path.parts:
        current = current / part
        require(not current.is_symlink(), f"Symbolic links are not accepted: {relative}")
    require(current.resolve().is_relative_to(base.resolve()), f"Path escapes package: {relative}")
    require(current.is_file(), f"Missing file: {current}")
    return current


def read_object(path):
    require(path.stat().st_size <= 2_000_000, f"Metadata file is too large: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"Expected an object in {path}")
    return data


def validate_result(path, problem_id):
    data = read_object(path)
    shape(data, "schema_version problem_id run_id kind phase condition pair_id model agent settings "
          "task_revision judge_revision started_at actual_horizon validity exclusion_reason "
          "preconditions_met failure_opportunity_reached "
          "task_success target_failure evidence notes", "result")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "Unsupported result schema_version")
    require(data["problem_id"] == problem_id, "Result points to a different problem")
    require(nonempty(data["run_id"]) and SLUG.fullmatch(data["run_id"]), "Invalid run_id")
    require(path.parent.name == data["run_id"] and path.parent.parent.name == problem_id,
            "Result path must be results/<problem-id>/<run-id>/summary.json")
    choice(data["kind"], {"model_run", "scripted_check"}, "result kind")
    choice(data["phase"], {"development", "evaluation"}, "result phase")
    choice(data["condition"], {"main", "control"}, "result condition")
    choice(data["validity"], {"valid", "invalid", "unjudgeable"}, "result validity")
    require(isinstance(data["settings"], dict), "settings must be an object")
    for field in ("pair_id", "model", "agent", "task_revision", "judge_revision", "started_at"):
        optional_text(data[field], field)
    require(nonempty(data["notes"]), "Describe the result and limitations in notes")
    counts(data["actual_horizon"], "assistant_turns tool_calls sessions elapsed_seconds", "actual_horizon")
    for key in ("task_success", "target_failure", "preconditions_met", "failure_opportunity_reached"):
        require(data[key] is None or type(data[key]) is bool, f"{key} must be true, false, or null")
    require(isinstance(data["evidence"], list), "evidence must be a list of local file paths")
    require(all(nonempty(p) for p in data["evidence"]), "evidence paths must be text")
    require(len(set(data["evidence"])) == len(data["evidence"]), "Duplicate evidence paths")
    for relative in data["evidence"]:
        evidence = local_file(path.parent, relative)
        require(evidence != path, "A result cannot cite itself as evidence")
        require(evidence.stat().st_size > 0, "Evidence file is empty")
    if data["validity"] == "valid":
        require(data["preconditions_met"] is True and data["failure_opportunity_reached"] is True,
                "A valid scored attempt must meet preconditions and reach the failure opportunity")
        require(data["exclusion_reason"] is None, "Valid attempts must not have exclusion_reason")
        require(type(data["task_success"]) is bool and type(data["target_failure"]) is bool,
                "A valid attempt needs separate task_success and target_failure outcomes")
        require(bool(data["evidence"]), "A valid attempt needs evidence")
        for key in ("task_revision", "judge_revision", "started_at"):
            require(nonempty(data[key]), f"A valid attempt needs {key}")
        if data["kind"] == "model_run":
            require(nonempty(data["model"]) and nonempty(data["agent"]),
                    "A valid model run needs model and agent identifiers")
    else:
        require(nonempty(data["exclusion_reason"]), "Excluded attempts need an explanation")
        require(data["target_failure"] is None,
                "Invalid or unjudgeable attempts must leave target_failure null")
    return data


def validate_problem(package, root=ROOT, submission=False):
    require(package.parent.resolve() == (root / "problems").resolve(),
            "Select a direct child of problems/")
    require(not package.is_symlink(), "Problem directory must not be a symbolic link")
    data = read_object(local_file(package, "problem.json"))
    local_file(package, "README.md")
    for dirname in ("task", "environment", "checks", "reference"):
        directory = package / dirname
        require(directory.is_dir() and not directory.is_symlink(), f"Missing directory: {dirname}")
    shape(data, "schema_version id title status origin privacy_reviewed symptoms source horizon failure commands result_records comparison_note", "problem")
    require(type(data["schema_version"]) is int and data["schema_version"] == 1,
            "Unsupported problem schema_version")
    require(nonempty(data["id"]) and SLUG.fullmatch(data["id"]) and data["id"] == package.name,
            "Problem id must match its directory and use lowercase words separated by hyphens")
    require(nonempty(data["title"]), "title must be nonempty")
    require(isinstance(data["symptoms"], list) and all(isinstance(v, str) and v in SYMPTOMS for v in data["symptoms"]),
            "symptoms must list existing IDs such as 1.1 or other")
    require(len(set(data["symptoms"])) == len(data["symptoms"]), "Duplicate symptom labels")
    optional_text(data["comparison_note"], "comparison_note")
    choice(data["status"], STATUSES, "problem status")
    require(data["origin"] == "real_history", "Synthetic material belongs in examples/, not problems/")
    require(type(data["privacy_reviewed"]) is bool, "privacy_reviewed must be true or false")
    if submission:
        require(data["privacy_reviewed"], "Owner must review the exact files before submission")
    shape(data["source"], "agent model date evidence_note", "source")
    for field in ("agent", "model", "date"):
        optional_text(data["source"][field], f"source.{field}")
    require(nonempty(data["source"]["evidence_note"]), "source.evidence_note is required")
    h = data["horizon"]
    shape(h, "earlier_event later_decision intervening_work mechanism assistant_turns_between "
          "tool_calls_between sessions_spanned elapsed_seconds causal_claim", "horizon")
    for field in ("earlier_event", "later_decision", "intervening_work", "mechanism"):
        optional_text(h[field], f"horizon.{field}")
    count_fields = "assistant_turns_between tool_calls_between sessions_spanned elapsed_seconds"
    counts({k: h[k] for k in count_fields.split()}, count_fields, "horizon")
    choice(h["causal_claim"], {"suspected", "supported"}, "causal_claim")
    require(h["causal_claim"] != "supported" or data["status"] == "temporal_supported",
            "A supported temporal claim requires temporal_supported status and comparison evidence")
    shape(data["failure"], "expected_behavior observed_behavior target_predicate", "failure")
    shape(data["commands"], "setup run_agent judge check_reference control", "commands")
    for group in ("failure", "commands"):
        for key, value in data[group].items():
            optional_text(value, f"{group}.{key}")
    if data["status"] != "incident":
        for field in ("earlier_event", "later_decision", "intervening_work", "mechanism"):
            require(nonempty(h[field]), f"A packaged reproduction needs horizon.{field}")
        require(all(nonempty(v) for v in data["failure"].values()), "Define expected behavior and the specific target failure")
        for key in ("setup", "run_agent", "judge", "check_reference"):
            require(nonempty(data["commands"][key]), f"A packaged reproduction needs commands.{key}")
    refs = data["result_records"]
    require(isinstance(refs, list) and all(nonempty(p) for p in refs), "result_records must be a list of paths")
    require(len(set(refs)) == len(refs), "Duplicate result record references")
    records = []
    for ref in refs:
        parts = Path(ref).parts
        require(len(parts) == 4 and parts[:2] == ("results", data["id"]) and parts[-1] == "summary.json",
                "Use results/<problem-id>/<run-id>/summary.json")
        records.append(validate_result(local_file(root, ref), data["id"]))
    hits = [r for r in records if r["kind"] == "model_run" and r["condition"] == "main"
            and r["validity"] == "valid" and r["target_failure"] is True]
    if data["status"] in {"model_reproduced", "temporal_supported"}:
        require(bool(hits), "Model reproduction needs a valid fresh model run with the target failure")
    if data["status"] == "temporal_supported":
        require(nonempty(data["commands"]["control"]), "Document the comparison command")
        require(nonempty(data["comparison_note"]), "A temporal claim needs a written assessment of the comparison")
        controls = [r for r in records if r["kind"] == "model_run" and r["validity"] == "valid" and r["condition"] == "control"]
        require(any(nonempty(hit["pair_id"]) and hit["pair_id"] == control["pair_id"]
                    and all(hit[k] == control[k] for k in ("model", "agent", "task_revision", "judge_revision"))
                    and all(hit["settings"].get(k) == control["settings"].get(k)
                            for k in ("temperature", "seed", "max_steps", "context_window"))
                    for hit in hits for control in controls),
                "Temporal evidence needs linked comparable main/control runs; describe all other differences in comparison_note")
    # A declared temporal claim still requires human review of the comparison.
    return data, records


def validate_collection(root=ROOT, packages=None, submission=False):
    for dirname in ("problems", "results"):
        require((root / dirname).is_dir() and not (root / dirname).is_symlink(),
                f"{dirname}/ must be a real directory")
    all_packages = packages is None
    if all_packages:
        packages = sorted(p for p in (root / "problems").iterdir() if p.is_dir() or p.is_symlink())
    checked = [validate_problem(p, root, submission) for p in packages]
    referenced = {ref for data, _ in checked for ref in data["result_records"]}
    if all_packages:
        for summary in (root / "results").glob("*/*/summary.json"):
            require(summary.relative_to(root).as_posix() in referenced,
                    f"Unlinked result record: {summary.relative_to(root)}")
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Problem directories, or omit to check the collection")
    parser.add_argument("--submission", action="store_true", help="Also require the owner's privacy-review declaration")
    args = parser.parse_args()
    try:
        packages = [Path(p).absolute() for p in args.paths] if args.paths else None
        checked = validate_collection(ROOT, packages, args.submission)
    except (Invalid, OSError, ValueError, TypeError) as exc:
        parser.exit(1, f"Validation failed: {exc}\n")
    records = sum(len(r) for _, r in checked)
    print(f"Metadata valid: {len(checked)} problem(s), {records} result record(s).")
    print("This checks packaging only; it does not execute tasks or verify evidence, causation, or privacy.")


if __name__ == "__main__":
    main()
