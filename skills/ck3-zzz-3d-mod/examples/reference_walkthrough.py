"""In-memory walkthrough with hand-authored numbers; prints a summary only."""
from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from zzz_reference import animation, assembly, conversion, retarget, validation


def main() -> None:
    basis = np.diag([.01, .01, .01, 1])
    vertices, normals, faces = conversion.convert_geometry(
        [[0, 0, 0], [100, 0, 0], [0, 100, 0]], [[0, 0, 1]] * 3, [[0, 1, 2]], basis)
    validation.validate_skin([[0, -1, -1, -1]] * 3, [[1, 0, 0, 0]] * 3, 2)
    t = np.array([[[0, 0, 0], [0, 2, 0]], [[1, 0, 0], [0, 2, 0]]], dtype=float)
    q = np.tile([0., 0, 0, 1], (2, 2, 1))
    s = np.ones((2, 2, 3))
    local = animation.local_matrices(t, q, s)
    tree = animation.build_anim_tree(["demo_root", "demo_tip"], t, q, s, 30)
    decoded, fps = animation.decode_anim_tree(tree)
    world = retarget.worlds(local, [-1, 0])
    corrections = retarget.bind_corrections(world[0], world[0], {0: 0, 1: 1})
    desired = {target: retarget.rotation(world[1, source]) @ correction
               for target, (source, correction) in corrections.items()}
    result, _ = retarget.solve(local[0], [-1, 0], desired)
    asset = assembly.render_asset("demo", "demo.mesh", [dict(index=0,
        diffuse="demo_diffuse.dds", normal="demo_normal.dds", properties="demo_properties.dds",
        shader="portrait_attachment", shader_file="gfx/FX/demo.shader")],
        {"demo_idle": "demo_idle.anim"}, {"idle": "demo_idle"}, "idle")
    print(json.dumps({"vertices": len(vertices), "triangles": len(faces), "fps": fps,
                      "roundtrip_error": validation.validate_roundtrip(local, decoded),
                      "preserved_tip_offset": result[1, :3, 3].tolist(),
                      "asset_text_characters": len(asset), "game_validation": "NOT_TESTED",
                      "files_written": 0}, ensure_ascii=False))


if __name__ == "__main__":
    main()
