#!/usr/bin/env python3
"""Build the skill's allowlisted offline kit, or check it without changing files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("skills/collect-agent-failures")
FILES = (
    ".gitignore", "AGENTS.md", "CONTRIBUTING.md",
    "commands/new_problem.py", "commands/validate.py", "commands/history.py",
    "problems/README.md", "results/README.md",
    *(f"docs/{name}.md" for name in (
        "FINDING_FAILURES", "HISTORY", "REPRODUCING", "REVIEW", "SUBMITTING", "SYMPTOMS", "EVIDENCE")),
)
CACHE_NAMES = {"__pycache__", ".pytest_cache", ".DS_Store"}


def real_path(path, boundary):
    """Do not follow links within the source tree, including parent directories."""
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError(f"Symbolic links are not allowed: {part}")
        if part == boundary:
            return
    raise ValueError(f"Path is outside the source tree: {path}")


def tree_files(directory, omit_caches=False):
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError(f"Expected a real directory: {directory}")
    files = {}
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            raise ValueError(f"Only regular files and directories are allowed: {path}")
        if omit_caches and (CACHE_NAMES.intersection(relative.parts)
                            or path.suffix in {".pyc", ".pyo"}):
            continue
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    return files


def expected_files(root):
    files = {}
    for name in FILES:
        path = root / name
        real_path(path, root)
        if not path.is_file():
            raise ValueError(f"Missing canonical source file: {path}")
        files[name] = path.read_bytes()
    real_path(root / "templates", root)
    files.update({f"templates/{name}": data for name, data in
                  tree_files(root / "templates", omit_caches=True).items()})
    return dict(sorted(files.items()))


def build(root=ROOT, check=False):
    root = Path(root).absolute()
    expected = expected_files(root)
    manifest = (json.dumps({"format_version": 1, "files": {
        name: hashlib.sha256(data).hexdigest() for name, data in expected.items()
    }}, indent=2) + "\n").encode()
    assets = root / SKILL / "assets"
    kit = assets / "kit"
    receipt = assets / "kit-manifest.json"
    real_path(kit, root)
    real_path(receipt, root)
    if check:
        actual = tree_files(kit)
        expected_dirs = {str(parent) for name in expected for parent in Path(name).parents
                         if str(parent) != "."}
        actual_dirs = {p.relative_to(kit).as_posix() for p in kit.rglob("*") if p.is_dir()}
        if (actual != expected or actual_dirs != expected_dirs or not receipt.is_file()
                or receipt.read_bytes() != manifest):
            raise ValueError("Skill kit is stale; run python3 commands/build_skill.py")
        return len(expected)
    # This directory is generated exclusively by this command. Refuse links or
    # special files before replacing it; never remove another skill directory.
    if kit.exists():
        tree_files(kit)
    if receipt.exists() and not receipt.is_file():
        raise ValueError(f"Expected a regular manifest file: {receipt}")
    assets.mkdir(parents=True, exist_ok=True)
    if kit.exists():
        shutil.rmtree(kit)
    kit.mkdir()
    for name, data in expected.items():
        destination = kit / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    receipt.write_bytes(manifest)
    return len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on any kit drift; write nothing")
    args = parser.parse_args()
    try:
        count = build(check=args.check)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot {'check' if args.check else 'build'} skill kit: {exc}\n")
    print(f"{'Checked' if args.check else 'Built'} {count} allowlisted kit files.")


if __name__ == "__main__":
    main()
