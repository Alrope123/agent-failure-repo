"""Exercise one-command setup and non-destructive resume in disposable copies."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]


class StartTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.root = self.base / 'repository'
        (self.root / 'commands').mkdir(parents=True)
        shutil.copyfile(REPOSITORY / 'commands/start.py', self.root / 'commands/start.py')
        shutil.copytree(REPOSITORY / 'skills/collect-agent-failures',
                        self.root / 'skills/collect-agent-failures',
                        ignore=shutil.ignore_patterns('__pycache__'))
        self.default = self.root / '.local/collection'

    def call(self, *args):
        return subprocess.run([sys.executable, '-B', str(self.root / 'commands/start.py'), *args],
                              cwd=self.base, capture_output=True, text=True)

    @staticmethod
    def snapshot(root):
        return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in root.rglob('*') if p.is_file()}

    def test_default_works_from_another_cwd_and_created_collection_is_usable(self):
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data['status'], 'created')
        self.assertEqual(data['workspace'], str(self.default))
        self.assertTrue(data['setup_only'])
        self.assertFalse(data['history_scanned'])
        self.assertFalse(data['model_run'])
        self.assertIn(str(self.default / 'AGENTS.md'), data['agent_next_action'])
        self.assertTrue(Path(data['report']).is_file())
        self.assertTrue(Path(data['index']).is_file())
        self.assertEqual(data['summary_report'], str(self.default / 'REPORT.md'))
        self.assertFalse(Path(data['summary_report']).exists())
        self.assertEqual((self.root / '.local').stat().st_mode & 0o777, 0o700)
        for command, args in [('new_problem.py', ['observed-incident']), ('validate.py', [])]:
            check = subprocess.run([sys.executable, str(self.default / 'commands' / command), *args],
                                   cwd=self.base, capture_output=True, text=True)
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertTrue((self.default / 'problems/observed-incident/problem.json').is_file())
        self.assertFalse((self.default / '.git').exists())

    def test_repeat_preserves_report_index_and_incident_artifacts(self):
        self.assertEqual(self.call().returncode, 0)
        for relative in ('.local/collection-report.md', '.local/incident-index.csv',
                         '.local/incidents/details.md', 'problems/work-in-progress.txt'):
            (self.default / relative).write_text(f'Contributor work: {relative}\n')
        before = self.snapshot(self.root)
        result = self.call()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['status'], 'resumed')
        self.assertEqual(before, self.snapshot(self.root))

    def test_custom_output_and_resume(self):
        output = self.base / 'my collection'
        for expected in ('created', 'resumed'):
            result = self.call('--output', str(output))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], expected)
        self.assertFalse((self.root / '.local').exists())

    def test_arbitrary_existing_directory_is_unchanged(self):
        output = self.base / 'existing'
        output.mkdir()
        (output / 'owner.txt').write_text('Keep this content.\n')
        before = self.snapshot(output)
        result = self.call('--output', str(output))
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stderr)
        self.assertEqual(before, self.snapshot(output))

    def test_output_symlinks_are_refused_even_when_target_is_our_workspace(self):
        self.assertEqual(self.call().returncode, 0)
        for target in (self.default, self.base / 'absent'):
            link = self.base / 'linked-output'
            link.symlink_to(target)
            result = self.call('--output', str(link))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(link.is_symlink())
            link.unlink()
        self.assertFalse((self.base / 'absent').exists())

    def test_marker_tampering_is_rejected_without_rewriting(self):
        self.assertEqual(self.call().returncode, 0)
        marker = self.default / '.local/start.json'
        original = json.loads(marker.read_text())
        for changed in ([], {**original, 'format_version': True},
                        {**original, 'created_by': 1},
                        {**original, 'workspace': str(self.base / 'elsewhere')}):
            with self.subTest(changed=changed):
                marker.write_text(json.dumps(changed))
                before = self.snapshot(self.root)
                result = self.call()
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr)
                self.assertEqual(before, self.snapshot(self.root))

    def test_incomplete_workspace_is_refused_without_repair(self):
        self.assertEqual(self.call().returncode, 0)
        (self.default / 'AGENTS.md').unlink()
        before = self.snapshot(self.root)
        result = self.call()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('incomplete', result.stderr)
        self.assertEqual(before, self.snapshot(self.root))

    def test_linked_required_paths_are_rejected_on_resume(self):
        self.assertEqual(self.call().returncode, 0)
        report = self.default / '.local/collection-report.md'
        outside = self.base / 'private-report.md'
        report.rename(outside)
        report.symlink_to(outside)
        before = outside.read_bytes()
        result = self.call()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(before, outside.read_bytes())
        self.assertTrue(report.is_symlink())

    def test_repository_source_and_installed_skill_destinations_are_refused(self):
        for destination in (self.root / 'problems', self.root / 'docs/new-collection',
                            self.root / 'skills/collect-agent-failures/new-collection',
                            self.root / '.local'):
            with self.subTest(destination=destination):
                result = self.call('--output', str(destination))
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(destination.exists())

    def test_missing_custom_parent_is_not_created(self):
        output = self.base / 'missing-parent/collection'
        result = self.call('--output', str(output))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.parent.exists())

    def test_linked_default_parent_is_refused(self):
        outside = self.base / 'outside'
        outside.mkdir()
        (self.root / '.local').symlink_to(outside)
        result = self.call()
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue((self.root / '.local').is_symlink())
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
