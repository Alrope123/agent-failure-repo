#!/usr/bin/env python3
"""Install only the collection skill into a new local directory. No network calls."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
NAME = "collect-agent-failures"


def install(destination, root=ROOT, dry_run=False):
    root = Path(root).absolute()
    source = root / "skills" / NAME
    if any(path.is_symlink() for path in (root, root / "skills", source)):
        raise ValueError("The skill source must not be a symbolic link.")
    if not source.is_dir():
        raise ValueError(f"Skill source is missing: {source}")
    for path in source.rglob("*"):
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            raise ValueError(f"Skill source contains a link or special file: {path}")
    for required in ("SKILL.md", "assets/kit-manifest.json"):
        if not (source / required).is_file():
            raise ValueError(f"Skill source is incomplete: missing {required}")
    destination = Path(destination).expanduser().absolute()
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Refusing to overwrite existing destination: {destination}")
    if source.resolve() in (destination.resolve(), *destination.resolve().parents):
        raise ValueError("Install destination must be outside the source skill directory.")
    if not dry_run:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns(
            "__pycache__", "*.pyc", "*.pyo", ".DS_Store"))
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--agent", choices=("codex", "claude"))
    target.add_argument("--dest", type=Path, help="Exact new skill directory for another agent")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print target; write nothing")
    args = parser.parse_args()
    destination = args.dest or Path.home() / (
        ".agents" if args.agent == "codex" else ".claude") / "skills" / NAME
    try:
        destination = install(destination, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot install skill: {exc}\n")
    print(f"{'Would install' if args.dry_run else 'Installed'} {NAME} at {destination}")


if __name__ == "__main__":
    main()
