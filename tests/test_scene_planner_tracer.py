"""Focused COMP-045 dry-run tracer tests."""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
FIXTURE_REGISTRY = (
    Path(__file__).resolve().parent.parent
    / "fixtures"
    / "production"
    / "scene_planner"
    / "asset_registry.yaml"
)
sys.path.insert(0, str(TOOLS_PRODUCTION))

from scene_planner import plan_scene, plan_scene_yaml  # noqa: E402


class TestScenePlannerTracer(unittest.TestCase):
    def test_selects_known_asset_and_reports_missing_landscape(self):
        plan = plan_scene("Make him feel tiny against the landscape", FIXTURE_REGISTRY)

        self.assertEqual(plan["asset_matches"][0]["asset_id"], "protagonist-hero")
        self.assertEqual(plan["asset_gaps"], [{
            "need": "landscape",
            "reason": "no_registered_asset_match",
            "fabricated": False,
        }])
        self.assertEqual(plan["composition"]["emotional_read"], "vulnerable_against_scale")
        self.assertTrue(all(
            command["op"] in {"object.import_mesh", "camera.set", "light.set", "render.preview"}
            for command in plan["blender_command_plan"]
        ))

    def test_yaml_contains_structured_scene_fields(self):
        output = plan_scene_yaml("Make him feel tiny against the landscape", FIXTURE_REGISTRY)

        for field in (
            "intent:", "asset_matches:", "asset_gaps:", "camera:", "lighting:",
            "composition:", "render_passes:", "blender_command_plan:",
        ):
            self.assertIn(field, output)

    def test_planner_does_not_execute_tools(self):
        with patch("subprocess.run", side_effect=AssertionError("tool execution")) as run:
            plan_scene("Make him feel tiny against the landscape", FIXTURE_REGISTRY)
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
