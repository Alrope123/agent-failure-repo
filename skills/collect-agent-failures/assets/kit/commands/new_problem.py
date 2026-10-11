#!/usr/bin/env python3
"""Create a local incident package. Never read history or overwrite a package."""
import argparse
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")


def create_problem(slug, root=ROOT):
    if not isinstance(slug, str) or not SLUG.fullmatch(slug):
        raise ValueError("Use lowercase words separated by hyphens, starting with a letter.")
    parent = root / "problems"
    if parent.is_symlink() or not parent.is_dir():
        raise ValueError("problems/ must be a real directory in the repository.")
    destination = parent / slug
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Refusing to overwrite {destination}")
    source = root / "templates" / "problem"
    if (root / "templates").is_symlink() or source.is_symlink() or not source.is_dir():
        raise ValueError("Template must be a real directory in the repository.")
    if any(p.is_symlink() for p in source.rglob("*")):
        raise ValueError("Template must not contain symbolic links.")
    shutil.copytree(source, destination)
    manifest = destination / "problem.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    data["id"] = slug
    manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="A short name, such as forgotten-config-rule")
    args = parser.parse_args()
    try:
        destination = create_problem(args.slug)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot create problem: {exc}\n")
    print(f"Created {destination.relative_to(ROOT)}")
    print("Fill README.md and problem.json. It remains an unreviewed incident draft.")


if __name__ == "__main__":
    main()
