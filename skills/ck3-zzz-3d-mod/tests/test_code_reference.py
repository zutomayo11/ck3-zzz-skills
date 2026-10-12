"""Artificial numeric cases; no production assets or installed mods are read."""
from __future__ import annotations

import importlib
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


class ReferenceTests(unittest.TestCase):
    def module(self, name):
        self.assertTrue((SCRIPTS / "zzz_reference" / (name + ".py")).is_file(),
                        "Missing portable reference module: " + name)
        return importlib.import_module("zzz_reference." + name)

    def test_local_submesh_indices_match_original_winding(self):
        raw = {"m_VertexCount": 6, "m_Indices": [3, 4, 5],
               "m_SubMeshes": [{"topology": "Triangles", "indexCount": 3, "firstVertex": 3}]}
        converted = {"SubmeshList": [{"FaceList": [{"VertexIndices": [2, 1, 0]}]}]}
        self.assertEqual(self.module("conversion").source_faces(raw, converted), [[5, 4, 3]])
        converted["SubmeshList"][0]["FaceList"][0]["VertexIndices"] = [0, 1, 2]
        with self.assertRaises(ValueError):
            self.module("conversion").source_faces(raw, converted)

    def test_truncated_or_out_of_range_topology_is_rejected(self):
        fn = self.module("conversion").source_faces
        for indices in ([0, 1], [0, 1, 3]):
            raw = {"m_VertexCount": 3, "m_Indices": indices,
                   "m_SubMeshes": [{"topology": "Triangles", "indexCount": 3, "firstVertex": 0}]}
            converted = {"SubmeshList": [{"FaceList": [{"VertexIndices": list(indices)[::-1]}]}]}
            with self.assertRaises(ValueError):
                fn(raw, converted)

    def test_invalid_local_indices_cannot_be_hidden_by_vertex_offset(self):
        fn = self.module("conversion").source_faces
        cases = [(3, [-1, -2, -3]), (0, [2., 1., 0.]), (0, [2, True, 0]),
                 (-1, [3, 2, 1]), (False, [2, 1, 0])]
        for offset, indices in cases:
            raw = {"m_VertexCount": 3, "m_Indices": [0, 1, 2],
                   "m_SubMeshes": [{"topology": "Triangles", "indexCount": 3, "firstVertex": offset}]}
            converted = {"SubmeshList": [{"FaceList": [{"VertexIndices": indices}]}]}
            with self.subTest(offset=offset, indices=indices), self.assertRaises(ValueError):
                fn(raw, converted)
        for count in (3.5, True):
            raw = {"m_VertexCount": count, "m_Indices": [0, 1, 2],
                   "m_SubMeshes": [{"topology": "Triangles", "indexCount": 3, "firstVertex": 0}]}
            converted = {"SubmeshList": [{"FaceList": [{"VertexIndices": [2, 1, 0]}]}]}
            with self.subTest(vertex_count=count), self.assertRaises(ValueError):
                fn(raw, converted)

    def test_basis_change_keeps_bind_inverse_consistent(self):
        fn = self.module("conversion").change_basis
        bind = np.eye(4); bind[:3, 3] = [100, 200, 300]
        basis = np.diag([.01, .01, .01, 1])
        actual = fn(bind, basis)
        np.testing.assert_allclose(actual[:3, 3], [1, 2, 3])
        np.testing.assert_allclose(actual @ fn(np.linalg.inv(bind), basis), np.eye(4))
        with self.assertRaises(ValueError):
            fn(bind, np.zeros((4, 4)))

    def test_geometry_reflection_changes_winding_and_normals(self):
        fn = self.module("conversion").convert_geometry
        positions, normals, faces = fn([[0, 0, 0], [1, 0, 0], [0, 1, 0]],
                                      [[0, 0, 1]] * 3, [[0, 1, 2]], np.diag([-1, 1, 1, 1]))
        np.testing.assert_allclose(positions, [[0, 0, 0], [-1, 0, 0], [0, 1, 0]])
        np.testing.assert_allclose(normals, [[0, 0, 1]] * 3)
        np.testing.assert_array_equal(faces, [[2, 1, 0]])

    def test_zero_scale_and_quaternion_sign_are_preserved_semantically(self):
        module = self.module("animation")
        q = np.array([[[0., 0, 0, 1]], [[0., 0, 0, -1]]])
        actual = module.continuous_quaternions(q)
        np.testing.assert_allclose(actual[:, 0], [[0, 0, 0, 1], [0, 0, 0, 1]])
        local = module.local_matrices(np.zeros((2, 1, 3)), q, np.zeros((2, 1, 3)))
        np.testing.assert_allclose(local[:, 0, :3, :3], np.zeros((2, 3, 3)))

    def test_invalid_quaternion_and_fps_are_rejected(self):
        module = self.module("animation")
        with self.assertRaises(ValueError):
            module.continuous_quaternions(np.zeros((1, 1, 4)))
        for fps in (0, float("nan")):
            with self.assertRaises(ValueError):
                module.build_anim_tree(["root"], np.zeros((1, 1, 3)),
                                       [[[0, 0, 0, 1]]], np.ones((1, 1, 3)), fps)

    def test_anim_samples_are_frame_major_and_keep_static_channels(self):
        module = self.module("animation")
        t = np.array([[[0, 0, 0], [0, 1, 0]], [[1, 0, 0], [0, 2, 0]]], dtype=float)
        q = np.tile([0., 0, 0, 1], (2, 2, 1)); s = np.ones((2, 2, 3))
        tree = module.build_anim_tree(["root", "tip"], t, q, s, 30)
        self.assertEqual(tree.find("samples").get("t"), [0., 0, 0, 0, 1, 0, 1, 0, 0, 0, 2, 0])
        self.assertEqual([node.get("sa") for node in tree.find("info")], [["t"], ["t"]])
        self.assertNotIn("q", tree.find("samples").attrib)
        decoded, fps = module.decode_anim_tree(tree)
        self.assertEqual(fps, 30)
        np.testing.assert_allclose(decoded[1, :, :3, 3], [[1, 0, 0], [0, 2, 0]])
        tree.find("samples").set("t", [0.])
        with self.assertRaises(ValueError):
            module.decode_anim_tree(tree)

    def test_duplicate_animation_bone_names_are_rejected(self):
        module = self.module("animation")
        with self.assertRaises(ValueError):
            module.build_anim_tree(["root", "root"], np.zeros((1, 2, 3)),
                                   np.tile([0, 0, 0, 1], (1, 2, 1)), np.ones((1, 2, 3)), 30)

    def test_parent_first_worlds_include_ancestor_translation(self):
        module = self.module("retarget")
        local = np.tile(np.eye(4), (1, 2, 1, 1))
        local[0, 0, :3, 3] = [1, 0, 0]; local[0, 1, :3, 3] = [0, 2, 0]
        actual = module.worlds(local, [-1, 0])
        np.testing.assert_allclose(actual[0, 1, :3, 3], [1, 2, 0])
        with self.assertRaises(ValueError):
            module.worlds(local, [1, -1])

    def test_rotation_transfer_keeps_native_joint_lengths(self):
        module = self.module("retarget")
        rest = np.tile(np.eye(4), (2, 1, 1)); rest[1, :3, 3] = [0, 2, 0]
        rz = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=float)
        local, world = module.solve(rest, [-1, 0], {0: rz, 1: rz})
        np.testing.assert_allclose(local[1, :3, 3], [0, 2, 0])
        np.testing.assert_allclose(world[1, :3, 3], [-2, 0, 0])
        np.testing.assert_allclose(local[1, :3, :3], np.eye(3))
        np.testing.assert_allclose(rest[0], np.eye(4))

    def test_bind_correction_matches_target_pose(self):
        module = self.module("retarget")
        source = np.eye(4)[None]; target = np.eye(4)[None]
        target[0, :3, :3] = [[0, -1, 0], [1, 0, 0], [0, 0, 1]]
        corrections = module.bind_corrections(target, source, {0: 0})
        np.testing.assert_allclose(corrections[0][1], target[0, :3, :3])
        with self.assertRaises(ValueError):
            module.bind_corrections(target, source, {1: 0})

    def test_reflection_is_not_silently_converted_to_rotation(self):
        with self.assertRaises(ValueError):
            self.module("retarget").rotation(np.diag([-1., 1, 1, 1]))

    def test_asset_rendering_uses_explicit_material_and_animation_inputs(self):
        module = self.module("assembly")
        text = module.render_asset("demo", "demo.mesh", [dict(index=0, diffuse="d.dds",
                                   normal="n.dds", properties="p.dds", shader="portrait_attachment",
                                   shader_file="gfx/FX/demo.shader")],
                                   {"demo_idle": "idle.anim"}, {"idle": "demo_idle"}, "idle")
        self.assertIn('texture_specular = "p.dds"', text)
        self.assertIn('default_state = "idle"', text)
        self.assertIn('pdxmesh = "demo_mesh"', text)
        self.assertIn('animation = { id = "demo_idle" type = "idle.anim" }', text)

    def test_assembly_rejects_missing_states_and_script_injection(self):
        module = self.module("assembly")
        material = dict(index=0, diffuse="d.dds", normal="n.dds", properties="p.dds",
                        shader="portrait_attachment", shader_file="gfx/FX/demo.shader")
        for states, default in [({"idle": "missing"}, "idle"), ({"idle": "a"}, "missing")]:
            with self.assertRaises(ValueError):
                module.render_asset("demo", "demo.mesh", [material], {"a": "a.anim"}, states, default)
        with self.assertRaises(ValueError):
            module.render_asset('demo" }', "demo.mesh", [material], {"a": "a.anim"}, {"idle": "a"}, "idle")
        material["index"] = 1
        with self.assertRaises(ValueError):
            module.render_asset("demo", "demo.mesh", [material], {"a": "a.anim"}, {"idle": "a"}, "idle")

    def test_skin_accepts_only_zero_weight_unused_slots(self):
        module = self.module("validation")
        module.validate_skin([[0, -1, -1, -1]], [[1, 0, 0, 0]], 1)
        for indices, weights in [([[0, -1, -1, -1]], [[.5, .5, 0, 0]]),
                                 ([[0, -1, -1, -1]], [[.5, 0, 0, 0]]),
                                 ([[2, -1, -1, -1]], [[1, 0, 0, 0]])]:
            with self.assertRaises(ValueError):
                module.validate_skin(indices, weights, 1)

    def test_skin_bone_count_must_be_a_positive_integer(self):
        module = self.module("validation")
        for count in (2.5, True):
            with self.subTest(count=count), self.assertRaises(ValueError):
                module.validate_skin([[0, -1, -1, -1]], [[1, 0, 0, 0]], count)

    def test_retarget_rejects_non_affine_rest_matrices(self):
        rest = np.eye(4)[None]; rest[0, 3, 0] = 1
        with self.assertRaises(ValueError):
            self.module("retarget").solve(rest, [-1], {})

    def test_reference_resolution_uses_first_vfs_provider_and_rejects_escape(self):
        module = self.module("validation")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); high = root / "high"; low = root / "low"
            high.mkdir(); low.mkdir()
            (high / "ref.txt").write_text("first", encoding="utf-8")
            (low / "ref.txt").write_text("second", encoding="utf-8")
            self.assertEqual(module.resolve_references(["ref.txt"], [high, low]), {"ref.txt": high / "ref.txt"})
            for reference in ("../ref.txt", "missing.txt", "C:/outside.txt", "/outside.txt", "..\\ref.txt"):
                with self.assertRaises((ValueError, FileNotFoundError)):
                    module.resolve_references([reference], [high, low])

    def test_roundtrip_detects_frame_loss_and_nonfinite_values(self):
        module = self.module("validation")
        expected = np.tile(np.eye(4), (2, 1, 1, 1))
        self.assertEqual(module.validate_roundtrip(expected, expected.astype("float32")), 0)
        for actual in (expected[:1], np.full_like(expected, float("nan"))):
            with self.assertRaises(ValueError):
                module.validate_roundtrip(expected, actual)
        changed = expected.copy(); changed[1, 0, 0, 3] = .1
        with self.assertRaises(ValueError):
            module.validate_roundtrip(expected, changed)


if __name__ == "__main__":
    unittest.main()
