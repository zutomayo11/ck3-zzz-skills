#!/usr/bin/env python3
"""Export a read-only catalogue of CK3 camera definitions from text files."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from audit_camera_chain import CAMERA_DEF, balanced_block, iter_files, line_number

VALUE = re.compile(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*([^\r\n#]+)")
NODE = re.compile(r"(?m)^\s*(position_node|look_at_node)\s*=\s*\{\s*default\s*=\s*([A-Za-z0-9_]+)")


def camera_record(path: Path, text: str, match: re.Match[str]) -> dict:
    block_start = text.find("{", match.start())
    block = balanced_block(text, block_start)
    camera_match = re.search(r"(?s)\bcamera\s*=\s*(\{.*\})", block)
    camera_block = balanced_block(block, camera_match.start(1)) if camera_match else block
    values = {key: value.strip() for key, value in VALUE.findall(camera_block)}
    nodes = {key: value for key, value in NODE.findall(camera_block)}
    name = match.group(1)
    variant = "shared"
    suffix = name.removeprefix("zzz_camera_")
    for character in ("ellen", "rina", "lycaon", "corin"):
        prefix = f"zzz_camera_{character}_"
        if name.startswith(prefix):
            variant = character
            suffix = name.removeprefix(prefix)
            break
    return {
        "id": name,
        "variant": variant,
        "family": suffix,
        "purpose_evidence": "camera_id_name_only",
        "position": values.get("position"),
        "look_at": values.get("look_at"),
        "position_node": nodes.get("position_node"),
        "look_at_node": nodes.get("look_at_node"),
        "fov": values.get("fov"),
        "camera_near_far": values.get("camera_near_far"),
        "source_file": str(path),
        "line": line_number(text, match.start()),
        "evidence": "static_definition_name_and_parameters",
        "runtime_status": "NOT_TESTED",
    }


def export_catalogue(roots: list[Path]) -> dict:
    records = []
    source_hashes = {}
    for path in iter_files(roots):
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue
        source_hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        records.extend(camera_record(path, text, m) for m in CAMERA_DEF.finditer(text))
    counts: dict[str, int] = {}
    families: dict[str, dict] = {}
    for record in records:
        counts[record["variant"]] = counts.get(record["variant"], 0) + 1
        family = families.setdefault(record["family"], {"variants": [], "purpose_evidence": "camera_id_name_only"})
        family["variants"].append(record["id"])
    return {
        "schema": "ck3-portrait-camera/catalogue-v1",
        "scope": {"roots": [str(path) for path in roots], "source_sha256": source_hashes},
        "coverage": {
            "definition_count": len(records),
            "variant_counts": counts,
            "family_count": len(families),
            "static_only": True,
            "runtime_claim": False,
        },
        "families": families,
        "definitions": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path, help="Camera text files or directories")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    result = export_catalogue(args.roots)
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
