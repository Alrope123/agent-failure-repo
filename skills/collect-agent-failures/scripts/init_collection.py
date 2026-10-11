#!/usr/bin/env python3
"""Create a new local collection from the installed skill; never inspect history."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

SKILL = Path(__file__).resolve().parents[1]


def initialize(output, skill=SKILL):
    output = Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError('Output already exists; resume there or choose a new directory.')
    if not output.parent.is_dir():
        raise ValueError('The output parent directory must already exist.')
    if output.resolve().is_relative_to(skill.resolve()):
        raise ValueError('Create collections outside the installed skill.')
    kit = skill / 'assets' / 'kit'
    manifest_path = skill / 'assets' / 'kit-manifest.json'
    if (skill / 'assets').is_symlink() or kit.is_symlink() or manifest_path.is_symlink():
        raise ValueError('Bundled assets must not be symbolic links.')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest.get('format_version') != 1 or not isinstance(manifest.get('files'), dict):
        raise ValueError('Invalid kit manifest.')
    files = manifest['files']
    if any(p.is_symlink() for p in kit.rglob('*')):
        raise ValueError('Bundled files must not be symbolic links.')
    actual = {p.relative_to(kit).as_posix() for p in kit.rglob('*') if p.is_file()}
    if actual != set(files):
        raise ValueError('Bundled file inventory does not match the manifest.')
    for relative, digest in files.items():
        path = Path(relative)
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Unsafe bundle path.')
        if hashlib.sha256((kit / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f'Bundled file has changed: {relative}')
    shutil.copytree(kit, output)
    private = output / '.local'
    private.mkdir(mode=0o700)
    for name in ('collection-report.md', 'incident-index.csv'):
        shutil.copyfile(output / 'templates' / name, private / name)
    (private / 'incidents').mkdir()
    (output / 'README.md').write_text(
        '# Your local agent failure collection\n\n'
        'Read [AGENTS.md](AGENTS.md) and [the symptom guide](docs/SYMPTOMS.md).\n'
        'Track scope and candidates in `.local/`. Keep raw history and detailed\n'
        'unreviewed evidence there. Use [the evidence form](templates/incident-evidence.md)\n'
        'for each candidate. Put sanitized task packages in `problems/` and\n'
        'reviewed run records in `results/`. The initializer does not create a\n'
        'Git repository or upload anything. If this directory is inside an existing\n'
        'repository, check its tracking state before adding private material.\n\n'
        'Review historical runs from both Claude Code and Codex using\n'
        '[the historical-run guide](docs/HISTORY.md) and `commands/history.py`.\n'
        'Use the authorized target project from before setup, not this kit.\n'
        'Record each tool\'s coverage and gaps separately.\n\n'
        'From this directory, run `python3 commands/new_problem.py short-name`\n'
        'to start a package and `python3 commands/validate.py` to check metadata.\n',
        encoding='utf-8',
    )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        output = initialize(args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Cannot initialize collection: {exc}\n')
    print(f'Created collection: {output}')
    print('Start with AGENTS.md and .local/collection-report.md. No history was read or uploaded.')


if __name__ == '__main__':
    main()
