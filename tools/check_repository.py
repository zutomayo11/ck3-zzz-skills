"""Check source-only contents, local links, syntax and skill-file hashes."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
JSON_PATHS = {"source-manifest.json",
              "skills/ck3-portrait-camera/assets/camera_validation_report.template.json",
              "skills/ck3-portrait-camera/tests/behavior_scenarios.json"}
ROOT_NAMES = {"README.md", "LICENSE", ".gitignore", ".gitattributes", "source-manifest.json"}


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
        if path.name not in ROOT_NAMES and path.suffix not in {".py", ".md", ".txt", ".yml", ".yaml", ".gui", ".json"}:
            raise ValueError(f"Non-source payload: {relative}")
        if path.suffix == ".json" and relative not in JSON_PATHS:
            raise ValueError(f"Unexpected data/receipt JSON: {relative}")
        text = path.read_text(encoding="utf-8-sig")
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
