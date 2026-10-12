"""Verify source-only packaging and content hashes with artificial documents."""
import importlib
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))


class RepositoryChecks(unittest.TestCase):
    def checker(self):
        self.assertTrue((TOOLS / "check_repository.py").is_file(), "Missing source-only packaging checker")
        return importlib.import_module("check_repository")

    def test_ignored_local_metadata_is_not_part_of_skill_payload(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); skill = root / "skills" / "demo"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: demo\ndescription: demo\n---\nDemo\n", encoding="utf-8")
            local = root / ".superpowers"
            local.mkdir(); (local / "workspace.data").write_bytes(b"local metadata")
            checker.update_manifest(root)
            self.assertEqual(checker.verify_repository(root)["skill_files"], 1)

    def test_manifest_detects_changed_bytes_without_size_change(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); skill = root / "skills" / "demo"
            skill.mkdir(parents=True)
            document = skill / "SKILL.md"
            document.write_text("---\nname: demo\ndescription: demo\n---\nDemo\n", encoding="utf-8")
            checker.update_manifest(root)
            checker.verify_repository(root)
            document.write_text(document.read_text().replace("Demo", "Gone"), encoding="utf-8")
            with self.assertRaises(ValueError):
                checker.verify_repository(root)

    def test_production_payload_and_broken_links_are_rejected(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); skill = root / "skills" / "demo"
            skill.mkdir(parents=True)
            document = skill / "SKILL.md"
            document.write_text("---\nname: demo\ndescription: demo\n---\n[missing](missing.md)\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                checker.update_manifest(root)
            document.write_text("---\nname: demo\ndescription: demo\n---\nDemo\n", encoding="utf-8")
            for name in ("real.dds", "installation.json", "real.npz"):
                forbidden = skill / name
                forbidden.write_bytes(b"artificial")
                with self.assertRaises(ValueError):
                    checker.update_manifest(root)
                forbidden.unlink()


if __name__ == "__main__":
    unittest.main()
