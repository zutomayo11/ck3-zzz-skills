from __future__ import annotations

import json
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit_camera_chain.py"
EXPORTER = ROOT / "scripts" / "export_camera_catalogue.py"
FIXTURE = ROOT / "tests" / "fixtures" / "broken"


class CameraChainTests(unittest.TestCase):
    def audit_source(self, source):
        spec = importlib.util.spec_from_file_location("camera_audit", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "camera.txt"
            path.write_text(source, encoding="utf-8")
            return module.audit([path])

    def test_private_camera_ids_are_resolved_without_name_family_guess(self):
        names = ("zzz_p4c043_camera_event_left", "zzz_p4diag_alice_horse_head", "zzz_p4c044_camera_save_load")
        source = "\n".join(
            f'{name} = {{ camera = {{ distance = 1 }} }}\n'
            f'zzz_cam_camera_route_{i} = {{ type = character text = {{ localization_key = ROUTE_{i} }} }}\n'
            f' ROUTE_{i}:0 "{name}"'
            for i, name in enumerate(names)
        )
        data = self.audit_source(source)
        self.assertEqual({r["returned_value"] for r in data["expected_returns"]}, set(names))
        self.assertEqual(data["camera_ids_absent_from_scan_scope"], [])

    def test_missing_private_camera_is_reported_as_absent_from_scope(self):
        source = '''zzz_cam_camera_route = { type = character text = { localization_key = ROUTE } }
 ROUTE:0 "zzz_p4diag_missing_horse_head"
'''
        data = self.audit_source(source)
        self.assertEqual([r["returned_value"] for r in data["camera_ids_absent_from_scan_scope"]], ["zzz_p4diag_missing_horse_head"])
        self.assertFalse(data["coverage"]["runtime_claim"])

    def test_localized_expressions_are_not_treated_as_literal_camera_ids(self):
        source = '''zzz_cam_camera_route = { type = character
 text = { localization_key = ROUTE_A }
 text = { localization_key = ROUTE_B }
 text = { localization_key = ROUTE_C }
}
 ROUTE_A:0 "$OTHER_KEY$"
 ROUTE_B:0 "[Character.Custom('zzz_cam_camera_route')]"
 ROUTE_C:0 "Human readable text"
'''
        data = self.audit_source(source)
        self.assertEqual(len(data["expected_returns"]), 3)
        self.assertEqual(data["camera_ids_absent_from_scan_scope"], [])

    def run_audit(self):
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(FIXTURE)],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_balanced_parser_keeps_nested_block_and_nodes(self):
        data = self.run_audit()
        self.assertTrue(data["coverage"]["static_only"])
        self.assertFalse(data["coverage"]["runtime_claim"])
        self.assertEqual(data["definitions"][0]["name"], "zzz_camera_event_center")
        self.assertEqual(data["definitions"][0]["position_nodes"], ["zzz_cam_torso"])
        self.assertEqual(data["definitions"][0]["look_at_nodes"], ["zzz_cam_head"])

    def test_route_and_call_are_separate_from_definition(self):
        data = self.run_audit()
        self.assertEqual(data["routes"][0]["name"], "zzz_cam_camera_event_center")
        self.assertEqual(data["calls"][0]["route_key"], "zzz_cam_camera_event_center")
        self.assertEqual(data["routes"][0]["runtime_status"], "NOT_TESTED")
        self.assertIn("GetCamera", data["dynamic_api_references"])

    def test_catalogue_export_keeps_parameters_and_runtime_boundary(self):
        result = subprocess.run(
            [sys.executable, "-B", str(EXPORTER), str(FIXTURE / "camera.txt")],
            check=True,
            capture_output=True,
            text=True,
        )
        data = json.loads(result.stdout)
        self.assertEqual(data["coverage"]["definition_count"], 1)
        camera = data["definitions"][0]
        self.assertEqual(camera["position_node"], "zzz_cam_torso")
        self.assertEqual(camera["look_at_node"], "zzz_cam_head")
        self.assertEqual(camera["runtime_status"], "NOT_TESTED")
        self.assertFalse(data["coverage"]["runtime_claim"])

    def test_behavior_scenario_structure(self):
        data = json.loads((ROOT / "tests" / "behavior_scenarios.json").read_text(encoding="utf-8"))
        scenarios = data["scenarios"]
        ids = [item["id"] for item in scenarios]
        self.assertEqual(len(ids), len(set(ids)))
        for item in scenarios:
            self.assertTrue(item["request"].strip())
            self.assertTrue(item["required_decision"].strip())
            self.assertIn(item["expected_status"], {"PASS", "FAIL", "NOT_TESTED", "BLOCKED"})


if __name__ == "__main__":
    unittest.main()
