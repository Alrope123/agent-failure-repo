"""Check the actual initializer in a standalone temporary installation."""
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]
NAME = "collect-agent-failures"


class SkillInitializationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        checkout = self.base / "throwaway-checkout"
        (checkout / "commands").mkdir(parents=True)
        shutil.copyfile(REPOSITORY / "commands/install_skill.py", checkout / "commands/install_skill.py")
        shutil.copytree(REPOSITORY / "skills" / NAME, checkout / "skills" / NAME,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        self.skill = self.base / "installed" / NAME
        subprocess.run([sys.executable, str(checkout / "commands/install_skill.py"),
                        "--dest", str(self.skill)], cwd=self.base, capture_output=True, check=True)
        # All remaining commands run from the installed copy, after its original
        # checkout disappears. No writes occur in the real repository or home.
        shutil.rmtree(checkout)
        self.output = self.base / "collection"
        self.kit = self.skill / "assets/kit"
        self.manifest = self.skill / "assets/kit-manifest.json"

    def initialize(self, output=None):
        return subprocess.run([sys.executable, str(self.skill / "scripts/init_collection.py"),
                               "--output", str(output or self.output)], cwd=self.base,
                              capture_output=True, text=True)

    def command(self, script, *arguments):
        return subprocess.run([sys.executable, str(self.output / "commands" / script), *arguments],
                              cwd=self.output, capture_output=True, text=True)

    def assert_rejected_without_output(self):
        result = self.initialize()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Cannot initialize collection:", result.stderr)
        self.assertFalse(self.output.exists())

    def test_standalone_initialization_creates_private_ledgers_and_working_commands(self):
        before = {p.relative_to(self.skill): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.skill.rglob("*") if p.is_file()}
        result = self.initialize()
        self.assertEqual(result.returncode, 0, result.stderr)
        private = self.output / ".local"
        self.assertEqual(stat.S_IMODE(private.stat().st_mode), 0o700)
        self.assertTrue((private / "incidents").is_dir())
        for name in ("collection-report.md", "incident-index.csv"):
            self.assertEqual((private / name).read_bytes(), (self.kit / "templates" / name).read_bytes())
        self.assertIn("/.local/", (self.output / ".gitignore").read_text())
        self.assertIn("Your local agent failure collection", (self.output / "README.md").read_text())
        self.assertFalse((self.output / ".git").exists())
        checked = self.command("validate.py")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        created = self.command("new_problem.py", "forgotten-rule")
        self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
        problem = json.loads((self.output / "problems/forgotten-rule/problem.json").read_text())
        self.assertEqual(problem["id"], "forgotten-rule")
        self.assertEqual(problem["status"], "incident")
        self.assertFalse(problem["privacy_reviewed"])
        checked = self.command("validate.py")
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        unreviewed = self.command("validate.py", "--submission", "problems/forgotten-rule")
        self.assertNotEqual(unreviewed.returncode, 0)
        after = {p.relative_to(self.skill): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.skill.rglob("*") if p.is_file()}
        self.assertEqual(before, after, "Initializing and using a collection must not modify the skill.")

    def test_refuses_existing_directory_without_changing_owner_contents(self):
        self.output.mkdir()
        empty = self.initialize()
        self.assertNotEqual(empty.returncode, 0)
        self.assertEqual(list(self.output.iterdir()), [])
        owner_file = self.output / "owner-notes.txt"
        owner_file.write_text("Preserve existing notes.\n")
        existing = self.initialize()
        self.assertNotEqual(existing.returncode, 0)
        self.assertEqual(owner_file.read_text(), "Preserve existing notes.\n")
        self.assertEqual(list(self.output.iterdir()), [owner_file])

    def test_refuses_existing_and_dangling_output_symlinks(self):
        owner = self.base / "owner-directory"
        owner.mkdir()
        (owner / "notes.txt").write_text("Private owner data.\n")
        self.output.symlink_to(owner, target_is_directory=True)
        self.assertNotEqual(self.initialize().returncode, 0)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual((owner / "notes.txt").read_text(), "Private owner data.\n")
        self.output.unlink()
        self.output.symlink_to(self.base / "absent-directory", target_is_directory=True)
        self.assertNotEqual(self.initialize().returncode, 0)
        self.assertTrue(self.output.is_symlink())
        self.assertFalse((self.base / "absent-directory").exists())

    def test_rejects_changed_bundle_content_before_creating_output(self):
        (self.kit / "AGENTS.md").write_text("Unverified replacement.\n")
        self.assert_rejected_without_output()

    def test_rejects_changed_manifest_hash_before_creating_output(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["files"]["AGENTS.md"] = "0" * 64
        self.manifest.write_text(json.dumps(manifest))
        self.assert_rejected_without_output()

    def test_rejects_unsupported_manifest_before_creating_output(self):
        manifest = json.loads(self.manifest.read_text())
        manifest["format_version"] = 999
        self.manifest.write_text(json.dumps(manifest))
        self.assert_rejected_without_output()

    def test_rejects_extra_bundle_file_before_creating_output(self):
        (self.kit / "unexpected-history.txt").write_text("Must not be copied.\n")
        self.assert_rejected_without_output()

    def test_rejects_missing_bundle_file_before_creating_output(self):
        (self.kit / "AGENTS.md").unlink()
        self.assert_rejected_without_output()

    def test_rejects_bundle_symlink_before_creating_output(self):
        (self.kit / "unexpected-link").symlink_to(self.base / "missing")
        self.assert_rejected_without_output()

    def test_rejects_output_inside_installed_skill(self):
        nested = self.skill / "collection"
        result = self.initialize(nested)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the installed skill", result.stderr)
        self.assertFalse(nested.exists())


if __name__ == "__main__":
    unittest.main()
