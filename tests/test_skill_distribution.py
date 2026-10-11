"""Exercise offline skill packaging without touching an installed user skill."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]


def load(path, name):
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), module.__dict__)
    return module


class SkillDistributionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "source"
        self.root.mkdir()
        self.builder = load(REPOSITORY / "commands/build_skill.py", "builder")
        self.installer = load(REPOSITORY / "commands/install_skill.py", "installer")
        for name in self.builder.FILES:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            canonical = REPOSITORY / name
            path.write_bytes(canonical.read_bytes() if canonical.exists() else b"Fixture guide.\n")
        shutil.copytree(REPOSITORY / "templates", self.root / "templates",
                        ignore=shutil.ignore_patterns("__pycache__"))
        self.skill = self.root / self.builder.SKILL
        (self.skill / "scripts").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("---\nname: collect-agent-failures\n---\nOffline fixture.\n")
        (self.skill / "scripts/fixture.py").write_text("print('offline')\n")
        self.builder.build(self.root)
        self.kit = self.skill / "assets/kit"
        self.destination = self.base / "installed/collect-agent-failures"

    @staticmethod
    def snapshot(root):
        return {p.relative_to(root).as_posix(): (p.read_bytes(), p.stat().st_mtime_ns)
                for p in root.rglob("*") if p.is_file()}

    def test_build_allowlist_excludes_histories_results_and_other_skills(self):
        for name in ("README.md", ".local/history.txt", "results/private/transcript.txt",
                     "problems/private/source.py", "docs/secret.md", "other-skill/SKILL.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Do not distribute.\n")
        cache = self.root / "templates/__pycache__/cached.pyc"
        cache.parent.mkdir()
        cache.write_bytes(b"cache")
        self.builder.build(self.root)
        actual = self.builder.tree_files(self.kit)
        self.assertEqual(actual, self.builder.expected_files(self.root))
        self.assertNotIn("README.md", actual)
        self.assertFalse(any("secret" in p or "history" in p or "cached" in p for p in actual))

    def test_manifest_matches_every_bundled_file(self):
        manifest = json.loads((self.skill / "assets/kit-manifest.json").read_text())
        self.assertEqual(manifest["format_version"], 1)
        self.assertEqual(manifest["files"], {
            name: hashlib.sha256(data).hexdigest()
            for name, data in self.builder.tree_files(self.kit).items()})

    def test_check_does_not_write_files(self):
        before = self.snapshot(self.root)
        self.builder.build(self.root, check=True)
        self.assertEqual(before, self.snapshot(self.root))

    def test_check_rejects_changed_canonical_source(self):
        (self.root / "AGENTS.md").write_text("Changed source.\n")
        before = self.snapshot(self.root)
        with self.assertRaises(ValueError):
            self.builder.build(self.root, check=True)
        self.assertEqual(before, self.snapshot(self.root))

    def test_check_rejects_missing_modified_and_extra_kit_files(self):
        for mutation in ("missing", "modified", "extra"):
            with self.subTest(mutation=mutation):
                self.builder.build(self.root)
                if mutation == "missing":
                    (self.kit / "AGENTS.md").unlink()
                elif mutation == "modified":
                    (self.kit / "AGENTS.md").write_text("Drift.\n")
                else:
                    (self.kit / "unexpected.txt").write_text("Extra.\n")
                before = self.snapshot(self.root)
                with self.assertRaises(ValueError):
                    self.builder.build(self.root, check=True)
                self.assertEqual(before, self.snapshot(self.root))

    def test_check_rejects_manifest_drift(self):
        (self.skill / "assets/kit-manifest.json").write_text("{}\n")
        with self.assertRaises(ValueError):
            self.builder.build(self.root, check=True)

    def test_check_rejects_extra_empty_directory(self):
        (self.kit / "extra-empty-directory").mkdir()
        with self.assertRaises(ValueError):
            self.builder.build(self.root, check=True)

    def test_builder_rejects_source_symlink_before_changing_kit(self):
        original = self.snapshot(self.skill)
        path = self.root / "templates/linked.md"
        path.symlink_to(self.root / "AGENTS.md")
        with self.assertRaises(ValueError):
            self.builder.build(self.root)
        self.assertEqual(original, self.snapshot(self.skill))

    def test_builder_rejects_generated_symlink_without_touching_target(self):
        outside = self.base / "owner.txt"
        outside.write_text("Keep me.\n")
        (self.kit / "unexpected-link").symlink_to(outside)
        with self.assertRaises(ValueError):
            self.builder.build(self.root)
        self.assertEqual(outside.read_text(), "Keep me.\n")
        self.assertTrue((self.kit / "unexpected-link").is_symlink())

    def test_installer_copies_only_skill_and_runs_without_original_checkout(self):
        (self.root / "private-history.txt").write_text("Private.\n")
        self.installer.install(self.destination, root=self.root)
        self.assertEqual(set(self.snapshot(self.destination)), set(self.snapshot(self.skill)))
        self.assertFalse((self.destination / "private-history.txt").exists())
        shutil.rmtree(self.root)
        result = subprocess.run([sys.executable, str(self.destination / "scripts/fixture.py")],
                                cwd=self.base, capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout.strip(), "offline")
        # The installed kit can seed a separate collection without any checkout.
        collection = self.base / "collection"
        shutil.copytree(self.destination / "assets/kit", collection)
        subprocess.run([sys.executable, str(collection / "commands/new_problem.py"),
                        "test-incident"], cwd=self.base, capture_output=True, check=True)
        self.assertTrue((collection / "problems/test-incident/problem.json").is_file())

    def test_dry_run_creates_no_directories(self):
        before = self.snapshot(self.base)
        self.installer.install(self.destination, root=self.root, dry_run=True)
        self.assertEqual(before, self.snapshot(self.base))
        self.assertFalse(self.destination.parent.exists())

    def test_installer_refuses_existing_empty_directory(self):
        self.destination.mkdir(parents=True)
        with self.assertRaises(ValueError):
            self.installer.install(self.destination, root=self.root)
        self.assertEqual(list(self.destination.iterdir()), [])

    def test_installer_refuses_existing_file_and_dangling_symlink(self):
        self.destination.parent.mkdir()
        self.destination.write_text("Owner data.\n")
        with self.assertRaises(ValueError):
            self.installer.install(self.destination, root=self.root)
        self.assertEqual(self.destination.read_text(), "Owner data.\n")
        self.destination.unlink()
        self.destination.symlink_to(self.base / "missing")
        with self.assertRaises(ValueError):
            self.installer.install(self.destination, root=self.root)
        self.assertTrue(self.destination.is_symlink())

    def test_installer_refuses_source_links(self):
        (self.skill / "dangling").symlink_to(self.base / "missing")
        with self.assertRaises(ValueError):
            self.installer.install(self.destination, root=self.root)
        self.assertFalse(self.destination.parent.exists())

    def test_installer_refuses_destination_inside_source(self):
        destination = self.skill / "nested/new-copy"
        with self.assertRaises(ValueError):
            self.installer.install(destination, root=self.root)
        self.assertFalse(destination.parent.exists())

    def test_installer_cli_rejects_ambiguous_target(self):
        result = subprocess.run([sys.executable, str(REPOSITORY / "commands/install_skill.py"),
                                 "--agent", "codex", "--dest", str(self.destination), "--dry-run"],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.destination.parent.exists())


if __name__ == "__main__":
    unittest.main()
