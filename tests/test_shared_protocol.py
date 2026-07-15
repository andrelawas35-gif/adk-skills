#!/usr/bin/env python3
"""Contract tests for the published Personal Institution handoff protocol."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PROTOCOL = ROOT / "references" / "SHARED-PROTOCOL.md"
CORE_SKILLS = (
    ROOT / "skills" / "core" / "conduct-work-object" / "SKILL.md",
    ROOT / "skills" / "core" / "pressure-test-decision" / "SKILL.md",
)


class SharedProtocolContract(unittest.TestCase):
    def setUp(self):
        self.text = PROTOCOL.read_text()

    def test_declares_a_released_version_and_safe_version_mismatch(self):
        self.assertIn("Protocol version: `0.1`", self.text)
        self.assertIn("manual, user-approved summary", self.text)
        self.assertIn("must not directly access", self.text)

    def test_evidence_bridge_requires_approval_and_minimum_provenance(self):
        for required_clause in (
            "User approval",
            "Minimum-necessary",
            "stable private reference",
            "Provenance",
            "Sensitivity",
            "Receiving Work Object",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, self.text)

    def test_personalization_entries_are_revisable_and_not_identity_claims(self):
        for required_clause in (
            "Working-method",
            "Active-lens",
            "Hard-boundary",
            "Supporting evidence",
            "Contrary evidence",
            "Review trigger",
            "must not\nestablish identity",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, self.text)

    def test_expired_revisable_entries_become_inactive(self):
        self.assertIn("become inactive", self.text)
        self.assertIn("Hard-boundary entries remain active", self.text)

    def test_work_studio_never_scans_or_mutates_personal_memory(self):
        self.assertIn("must not scan, read, or mutate", self.text)

    def test_work_studio_core_skills_declare_the_handoff_boundary(self):
        for skill in CORE_SKILLS:
            text = skill.read_text()
            with self.subTest(skill=skill.name):
                self.assertIn("Shared Protocol v0.1", text)
                self.assertIn("Evidence Bridge", text)
                self.assertIn("must not scan, read, or mutate", text)


if __name__ == "__main__":
    unittest.main()
