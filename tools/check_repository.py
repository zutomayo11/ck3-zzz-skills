"""Check source/documentation contents, local links, syntax and skill-file hashes."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timedelta, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
JSON_PATHS = {"source-manifest.json",
              "skills/ck3-portrait-camera/assets/camera_validation_report.template.json",
              "skills/ck3-portrait-camera/tests/behavior_scenarios.json"}
ROOT_NAMES = {"README.md", "LICENSE", ".gitignore", ".gitattributes", "source-manifest.json"}
DOCUMENTATION_DIAGRAMS = {
    "skills/ck3-zzz-3d-mod/assets/production-workflow/overview.svg",
    "skills/ck3-zzz-3d-mod/assets/production-workflow/chains.svg",
    "skills/ck3-zzz-3d-mod/assets/production-workflow/boundaries.svg",
    "skills/ck3-zzz-3d-mod/assets/production-workflow/production-workflow.html",
}


class _DiagramParser(HTMLParser):
    """The named documentation files remain text-only, passive diagrams."""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.rsplit(":", 1)[-1]
        if tag in {"script", "img", "image", "foreignobject", "iframe", "object", "embed",
                   "link", "audio", "video", "canvas"}:
            raise ValueError(f"Non-documentation element: {tag}")
        for name, value in attrs:
            if name.startswith("on") or name in {"src", "srcset", "poster", "background"}:
                raise ValueError(f"Active/resource diagram attribute: {name}")
            if name in {"href", "xlink:href"} and not (value or "").startswith("#"):
                raise ValueError(f"Nonlocal diagram reference: {name}")


def validate_diagram(path: Path, text: str) -> None:
    parser = _DiagramParser()
    parser.feed(text)
    parser.close()
    if re.search(r"@import\b", text, re.I):
        raise ValueError("External diagram stylesheet")
    for value in re.findall(r"url\(([^)]*)\)", text, re.I):
        if not value.strip().strip("\"'").startswith("#"):
            raise ValueError("Nonlocal diagram CSS resource")
    if path.suffix == ".svg":
        try:
            root = ElementTree.fromstring(text)
        except ElementTree.ParseError as error:
            raise ValueError("Invalid documentation SVG") from error
        if root.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError("Invalid documentation SVG root")


def payload_files(root: Path) -> list[Path]:
    files = []
    for child in root.iterdir():
        if child.name in {".git", "__pycache__", ".superpowers", ".pytest_cache", ".venv", "venv"}:
            continue
        if child.is_symlink():
            raise ValueError(f"Linked payload: {child.name}")
        if child.is_file():
            if child.name not in ROOT_NAMES:
                raise ValueError(f"Unexpected root payload: {child.name}")
            files.append(child)
        elif child.is_dir():
            if child.name not in {"skills", "tools", "tests"}:
                raise ValueError(f"Unexpected payload directory: {child.name}")
            files.extend(p for p in child.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for path in files:
        relative = path.relative_to(root).as_posix()
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Linked payload: {relative}")
        if relative not in DOCUMENTATION_DIAGRAMS and path.name not in ROOT_NAMES and path.suffix not in {".py", ".md", ".txt", ".yml", ".yaml", ".gui", ".json"}:
            raise ValueError(f"Non-source payload: {relative}")
        if path.suffix == ".json" and relative not in JSON_PATHS:
            raise ValueError(f"Unexpected data/receipt JSON: {relative}")
        text = path.read_text(encoding="utf-8-sig")
        if relative in DOCUMENTATION_DIAGRAMS:
            validate_diagram(path, text)
        if path.suffix == ".py":
            ast.parse(text, filename=relative)
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
                target = target.strip().split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                destination = (path.parent / unquote(target)).resolve()
                if not destination.is_relative_to(root.resolve()) or not destination.is_file():
                    raise ValueError(f"Broken/escaping relative link: {relative} -> {target}")
    return sorted(files)


def _skill_entries(root: Path, files: list[Path]) -> list[dict]:
    return [{"path": p.relative_to(root).as_posix(), "bytes": p.stat().st_size,
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in files if p.is_relative_to(root / "skills")]


def update_manifest(root: Path = ROOT) -> None:
    files = payload_files(root)
    path = root / "source-manifest.json"
    previous = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    entries = _skill_entries(root, files)
    manifest = {"schema_version": 1,
                "snapshot_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
                "source": "Repository-maintained skills and portable code references",
                "file_count": len(entries),
                "skills": sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md")),
                "files": entries}
    origin = previous.get("base_local_snapshot_at")
    if origin is None and previous.get("source") == "Codex user skills":
        origin = previous.get("snapshot_at")
    if origin:
        manifest["base_local_snapshot_at"] = origin
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def verify_repository(root: Path = ROOT) -> dict:
    files = payload_files(root)
    manifest = json.loads((root / "source-manifest.json").read_text(encoding="utf-8"))
    entries = _skill_entries(root, files)
    if manifest["file_count"] != len(entries) or manifest["files"] != entries:
        raise ValueError("Skill manifest paths, sizes or SHA256 differ")
    names = sorted(p.parent.name for p in (root / "skills").glob("*/SKILL.md"))
    if manifest["skills"] != names:
        raise ValueError("Skill names differ from installed directory structure")
    for name in names:
        text = (root / "skills" / name / "SKILL.md").read_text(encoding="utf-8-sig")
        if not text.startswith("---\n"):
            raise ValueError("Missing skill frontmatter: " + name)
        frontmatter = text.split("---", 2)[1]
        if not re.search(r"^name:\s*" + re.escape(name) + r"\s*$", frontmatter, re.M) or not re.search(r"^description:\s*\S", frontmatter, re.M):
            raise ValueError("Invalid skill name/description: " + name)
    return {"skill_files": len(entries), "skill_bytes": sum(e["bytes"] for e in entries),
            "documentation_diagrams": sum(p.relative_to(root).as_posix() in DOCUMENTATION_DIAGRAMS for p in files),
            "source_only": True, "syntax_and_relative_file_links": "PASS"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--update-manifest", action="store_true", help="Update only this repository's skill hash manifest")
    args = parser.parse_args()
    if args.update_manifest:
        update_manifest()
    print(json.dumps(verify_repository(), ensure_ascii=False))


if __name__ == "__main__":
    main()
