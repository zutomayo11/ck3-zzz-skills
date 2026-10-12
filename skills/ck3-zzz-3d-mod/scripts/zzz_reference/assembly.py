"""Minimal explicit asset declarations, adapted from build_assets.make_asset."""
from __future__ import annotations

import re
from typing import Mapping, Sequence


def _quoted(value: str) -> str:
    if not isinstance(value, str) or not value or any(c in value for c in '\\"\r\n\0{}'):
        raise ValueError("Asset string contains unsupported quoting or syntax")
    return '"' + value + '"'


def render_asset(prefix: str, mesh_file: str, materials: Sequence[Mapping],
                 animations: Mapping[str, str], states: Mapping[str, str], default_state: str,
                 *, looping: Mapping[str, bool] | None = None) -> str:
    """Return text only. Real actor adapters must preserve their complete state trees."""
    if not isinstance(prefix, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", prefix):
        raise ValueError("Resource prefix must be an ASCII identifier")
    indices = [row["index"] for row in materials]
    if not indices or any(type(index) is not int for index in indices) or sorted(indices) != list(range(len(indices))):
        raise ValueError("Material part indices must be unique and consecutive from zero")
    if not animations or not states or default_state not in states or set(states.values()) - set(animations):
        raise ValueError("Default/state animation references must be declared")
    if looping is None:
        looping = {state: True for state in states}
    if set(looping) != set(states) or any(type(value) is not bool for value in looping.values()):
        raise ValueError("Looping flags must explicitly match every state")
    lines = ["pdxmesh = {", f'\tname = "{prefix}_mesh"', f"\tfile = {_quoted(mesh_file)}"]
    for row in sorted(materials, key=lambda item: item["index"]):
        lines += ["\tmeshsettings = {", f'\t\tname = "{prefix}Shape"', f'\t\tindex = {row["index"]}']
        for target, key in (("texture_diffuse", "diffuse"), ("texture_normal", "normal"),
                            ("texture_specular", "properties"), ("shader", "shader"), ("shader_file", "shader_file")):
            lines.append(f"\t\t{target} = {_quoted(row[key])}")
        lines.append("\t}")
    for name, path in animations.items():
        lines.append(f"\tanimation = {{ id = {_quoted(name)} type = {_quoted(path)} }}")
    lines += ["}", "", "entity = {", f'\tname = "{prefix}_entity"', f'\tpdxmesh = "{prefix}_mesh"',
              f"\tdefault_state = {_quoted(default_state)}"]
    for state, animation in states.items():
        lines.append(f"\tstate = {{ name = {_quoted(state)} animation = {_quoted(animation)} looping = {'yes' if looping[state] else 'no'} }}")
    return "\n".join(lines + ["}", ""])
