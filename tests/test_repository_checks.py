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

    def test_named_documentation_diagrams_are_included_in_manifest(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            skill = root / "skills" / "ck3-zzz-3d-mod"
            diagrams = skill / "assets" / "production-workflow"
            diagrams.mkdir(parents=True)
            (skill / "SKILL.md").write_text(
                "---\nname: ck3-zzz-3d-mod\ndescription: demo\n---\nDemo\n", encoding="utf-8")
            svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720"><title>Demo</title><desc>Artificial diagram</desc><rect width="4" height="4"/></svg>'
            (diagrams / "overview.svg").write_text(svg, encoding="utf-8")
            (diagrams / "production-workflow.html").write_text(
                '<!doctype html><html><body><a href="#overview">Overview</a>' + svg + '</body></html>', encoding="utf-8")
            checker.update_manifest(root)
            result = checker.verify_repository(root)
            self.assertEqual(result["skill_files"], 3)
            self.assertEqual(result["documentation_diagrams"], 2)
            (diagrams / "unexpected.svg").write_text(svg, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Non-source payload"):
                checker.payload_files(root)

    def test_diagram_names_do_not_allow_active_or_embedded_resources(self):
        checker = self.checker()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            diagrams = root / "skills" / "ck3-zzz-3d-mod" / "assets" / "production-workflow"
            diagrams.mkdir(parents=True)
            svg_path = diagrams / "overview.svg"
            cases = [
                '<svg xmlns="http://www.w3.org/2000/svg"><script>demo()</script></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg" xmlns:s="http://www.w3.org/2000/svg"><s:script>demo()</s:script></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg"><image href="data:image/png;base64,AAAA"/></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg"><rect onload="demo()"/></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg"><use href="https://example.invalid/model.svg"/></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg"><style>@import "https://example.invalid/font.css";</style></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg"><style>rect {fill:url(data:image/png;base64,AAAA)}</style></svg>',
                '<svg xmlns="http://www.w3.org/2000/svg"><foreignObject/></svg>',
                '<svg',
            ]
            for source in cases:
                with self.subTest(source=source):
                    svg_path.write_text(source, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        checker.payload_files(root)
            svg_path.unlink()
            html_path = diagrams / "production-workflow.html"
            for source in ('<html><script>demo()</script></html>', '<html><img src="local.png"></html>'):
                with self.subTest(source=source):
                    html_path.write_text(source, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        checker.payload_files(root)


if __name__ == "__main__":
    unittest.main()
