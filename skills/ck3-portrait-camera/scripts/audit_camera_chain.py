#!/usr/bin/env python3
"""Read-only CK3 portrait camera/routing audit.

The parser uses balanced braces for named blocks. It reports static evidence only;
it never edits files, starts CK3/Blender, or claims runtime selection.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Iterable

CAMERA_DEF = re.compile(r"(?m)^\s*([A-Za-z0-9_]+)\s*=\s*\{\s*camera\s*=\s*\{")
ROUTE_DEF = re.compile(r"(?m)^\s*([A-Za-z0-9_]*camera[A-Za-z0-9_]*)\s*=\s*\{")
CUSTOM = re.compile(r"(?:Character\.)?Custom\(\s*['\"]([^'\"]+)['\"]\s*\)")
NODE = re.compile(r"\b(?:position_node|look_at_node)\s*=\s*\{[^{}]*?default\s*=\s*([A-Za-z0-9_]+)", re.S)
LOC_VALUE = re.compile(r'(?m)^\s*([A-Za-z0-9_]+):\d+\s+"([^"\\]*(?:\\.[^"\\]*)*)"')

TEXT_SUFFIXES = {".txt", ".gui", ".asset", ".anim", ".json", ".yml", ".yaml", ".info"}


def balanced_block(text: str, open_index: int) -> str:
    """Return a brace-balanced block from an opening `{`, respecting quoted strings."""
    depth = 0
    quoted = False
    escaped = False
    for i in range(open_index, len(text)):
        ch = text[i]
        if escaped:
            escaped = False
            continue
        if ch == "\\" and quoted:
            escaped = True
            continue
        if ch == '"':
            quoted = not quoted
            continue
        if quoted:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[open_index : i + 1]
    return text[open_index:]


def iter_files(roots: Iterable[Path]) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if root.is_file() and root.suffix.lower() in TEXT_SUFFIXES:
            files.append(root)
        elif root.is_dir():
            files.extend(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_SUFFIXES)
    return sorted(set(files))


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def audit(files: list[Path]) -> dict:
    definitions: list[dict] = []
    routes: list[dict] = []
    calls: list[dict] = []
    nodes: dict[str, list[dict]] = {}
    keyword_hits: dict[str, list[dict]] = {k: [] for k in ("GetCamera", "SaveGameItem", "BookmarkCharacter")}
    localization_values: dict[str, list[dict]] = {}

    for path in files:
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            continue
        display = str(path)
        for match in CAMERA_DEF.finditer(text):
            block = balanced_block(text, text.find("{", match.start()))
            position_nodes = re.findall(r"position_node\s*=\s*\{[^{}]*?default\s*=\s*([A-Za-z0-9_]+)", block, re.S)
            look_nodes = re.findall(r"look_at_node\s*=\s*\{[^{}]*?default\s*=\s*([A-Za-z0-9_]+)", block, re.S)
            definitions.append({
                "name": match.group(1), "file": display,
                "line": line_number(text, match.start()),
                "position_nodes": position_nodes, "look_at_nodes": look_nodes,
                "evidence": "static_definition", "runtime_status": "NOT_TESTED",
            })
        for match in ROUTE_DEF.finditer(text):
            block = balanced_block(text, text.find("{", match.start()))
            if not re.search(r"\btype\s*=\s*character\b", block):
                continue
            returned = re.findall(r"localization_key\s*=\s*([A-Za-z0-9_]+)", block)
            routes.append({
                "name": match.group(1), "file": display,
                "line": line_number(text, match.start()),
                "localization_keys": returned,
                "evidence": "static_route", "runtime_status": "NOT_TESTED",
            })
        for match in CUSTOM.finditer(text):
            calls.append({"route_key": match.group(1), "file": display,
                          "line": line_number(text, match.start()),
                          "evidence": "static_call", "runtime_status": "NOT_TESTED"})
        for match in LOC_VALUE.finditer(text):
            localization_values.setdefault(match.group(1), []).append({
                "value": match.group(2), "file": display,
                "line": line_number(text, match.start()),
            })
        found_nodes = []
        for match in NODE.finditer(text):
            found_nodes.append({"node": match.group(1), "line": line_number(text, match.start())})
        if found_nodes:
            nodes[display] = found_nodes
        for keyword in keyword_hits:
            for match in re.finditer(re.escape(keyword), text):
                keyword_hits[keyword].append({"file": display, "line": line_number(text, match.start()), "evidence": "static_reference"})

    definition_names = {item["name"] for item in definitions}
    route_names = {item["name"] for item in routes}
    absent_from_scan = []
    resolved_returns = []
    for route in routes:
        for key in route["localization_keys"]:
            values = localization_values.get(key, [])
            if not values:
                continue
            for item in values:
                returned_id = item["value"].strip()
                entry = {"route": route["name"], "localization_key": key, "returned_value": returned_id,
                         "route_file": route["file"], "route_line": route["line"],
                         "localization_file": item["file"], "localization_line": item["line"],
                         "evidence": "static_expected_return", "runtime_status": "NOT_TESTED"}
                resolved_returns.append(entry)
                if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", returned_id):
                    if returned_id not in definition_names:
                        absent_from_scan.append(entry)
    return {
        "schema": "ck3-portrait-camera/audit-v1",
        "scope": {"files": [str(p) for p in files], "file_count": len(files)},
        "definitions": definitions,
        "routes": routes,
        "expected_returns": resolved_returns,
        "calls": calls,
        "node_references": nodes,
        "dynamic_api_references": keyword_hits,
        "camera_ids_absent_from_scan_scope": absent_from_scan,
        "coverage": {
            "definition_count": len(definitions),
            "route_count": len(routes),
            "call_count": len(calls),
            "expected_return_count": len(resolved_returns),
            "camera_ids_absent_from_scan_scope": len(absent_from_scan),
            "static_only": True,
            "runtime_claim": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("roots", nargs="+", type=Path, help="Files or directories to inspect")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    args = parser.parse_args()
    files = iter_files(args.roots)
    result = audit(files)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
