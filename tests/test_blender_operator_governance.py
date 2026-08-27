"""Governance tests for production-operate-blender (WO 2026-08-24-014)."""

import sys
import unittest
from pathlib import Path

TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
sys.path.insert(0, str(TOOLS_PRODUCTION))

from blender_operator import governance  # noqa: E402


class TestProtectFields(unittest.TestCase):
    def test_mutating_name_is_checked_against_protect(self):
        error = governance.validate_command(
            "object.set_transform",
            {"name": "HeroCamera", "protect": ["HeroCamera"]},
            ["HeroCamera"],
        )
        self.assertEqual(error["code"], "protected_element")
        self.assertEqual(error["target"], "HeroCamera")

    def test_read_only_command_ignores_protect(self):
        self.assertIsNone(
            governance.validate_command(
                "scene.get_objects",
                {"protect": ["HeroCamera"]},
                ["HeroCamera"],
            )
        )


class TestPythonEscalationGate(unittest.TestCase):
    def test_execute_blender_python_requires_director_authority(self):
        error = governance.validate_command("execute_blender_python", {}, None)
        self.assertEqual(error["code"], "requires_director_authority")

    def test_execute_blender_python_accepts_director_authority_record(self):
        self.assertIsNone(
            governance.validate_command(
                "execute_blender_python",
                {
                    "authority": {
                        "granted_by": "director",
                        "work_object": "2026-08-24-014",
                    }
                },
                None,
            )
        )


if __name__ == "__main__":
    unittest.main()
