#!/usr/bin/env python3
"""Prepare or resume a private collection. This setup command does not inspect history."""
import argparse
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]
MARKER = Path('.local/start.json')
REQUIRED_FILES = (
    '.gitignore', 'AGENTS.md', 'README.md', 'CONTRIBUTING.md',
    'docs/SYMPTOMS.md', 'docs/EVIDENCE.md', 'docs/FINDING_FAILURES.md',
    'docs/REPRODUCING.md', 'docs/REVIEW.md',
    'commands/new_problem.py', 'commands/validate.py',
    'templates/incident-evidence.md', 'templates/problem/problem.json',
    'templates/problem/README.md', '.local/collection-report.md',
    '.local/incident-index.csv',
)
REQUIRED_DIRS = ('docs', 'commands', 'templates', 'problems', 'results',
                 '.local', '.local/incidents')


def resume(workspace):
    """Recognize only our own complete workspace without changing any content."""
    marker_path = workspace / MARKER
    for name in (*REQUIRED_DIRS, *REQUIRED_FILES, str(MARKER)):
        path = workspace
        for part in Path(name).parts:
            path = path / part
            if path.is_symlink():
                raise ValueError(f'Workspace contains a linked required path: {name}')
    if not marker_path.is_file() or marker_path.stat().st_size > 4096:
        raise ValueError('Existing output is not a workspace created by this command.')
    marker = json.loads(marker_path.read_text(encoding='utf-8'))
    if (not isinstance(marker, dict)
            or set(marker) != {'format_version', 'created_by', 'workspace'}
            or type(marker['format_version']) is not int
            or marker['format_version'] != 1
            or type(marker['created_by']) is not str
            or marker['created_by'] != 'commands/start.py'
            or type(marker['workspace']) is not str
            or marker['workspace'] != str(workspace)):
        raise ValueError('Workspace marker is invalid or belongs to another location.')
    for name in REQUIRED_FILES:
        if not (workspace / name).is_file():
            raise ValueError(f'Existing workspace is incomplete: missing {name}')
    for name in REQUIRED_DIRS:
        if not (workspace / name).is_dir():
            raise ValueError(f'Existing workspace is incomplete: missing {name}/')


def start(output=None, root=ROOT):
    root = Path(root).resolve()
    destination = (root / '.local/collection' if output is None
                   else Path(output).expanduser().absolute())
    if destination.is_symlink():
        raise ValueError('Output must not be a symbolic link.')
    if destination.is_relative_to(root / '.local') and (root / '.local').is_symlink():
        raise ValueError('The source repository .local directory must not be a symbolic link.')
    workspace = destination.resolve()
    if workspace.is_relative_to(root):
        relative = workspace.relative_to(root)
        if len(relative.parts) < 2 or relative.parts[0] != '.local':
            raise ValueError('Inside the source repository, use a directory beneath .local/.')
    if workspace.exists():
        if not workspace.is_dir():
            raise ValueError('Output already exists and is not a directory.')
        resume(workspace)
        status = 'resumed'
    else:
        if output is None:
            private = root / '.local'
            if private.is_symlink():
                raise ValueError('The source repository .local directory must not be a symbolic link.')
            private.mkdir(mode=0o700, exist_ok=True)
        if not workspace.parent.is_dir():
            raise ValueError('The output parent directory must already exist.')
        script = root / 'skills/collect-agent-failures/scripts/init_collection.py'
        initializer = runpy.run_path(str(script))['initialize']
        initializer(workspace)
        (workspace / MARKER).write_text(json.dumps({
            'format_version': 1,
            'created_by': 'commands/start.py',
            'workspace': str(workspace),
        }, indent=2) + '\n', encoding='utf-8')
        status = 'created'
    return {
        'status': status,
        'workspace': str(workspace),
        'agent_next_action': (
            f'Continue collection in this turn: read {workspace / "AGENTS.md"}, '
            'then follow its collection workflow using authorized available history. '
            'Setup is not completion.'
        ),
        'report': str(workspace / '.local/collection-report.md'),
        'summary_report': str(workspace / 'REPORT.md'),
        'index': str(workspace / '.local/incident-index.csv'),
        'setup_only': True,
        'history_scanned': False,
        'model_run': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        help='Collection directory; defaults to this repository\'s .local/collection.')
    args = parser.parse_args()
    try:
        result = start(args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Cannot start collection: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
