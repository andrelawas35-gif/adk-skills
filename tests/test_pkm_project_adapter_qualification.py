"""Qualification contract for the PKM Project Adapter operational paths."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
PROTOCOL = ROOT / "references" / "SHARED-PROTOCOL.md"
QUALIFICATION = (
    ROOT / ".work-studio" / "objects" / "2026" / "07"
    / "2026-07-15-005-qualify-pkm-project-adapter.md"
)
PLATFORMS = ("codex", "claude-code", "github-copilot")
SKILLS = (
    "investigate-live-question",
    "deploy-with-recovery",
    "diagnose-production-incident",
)
FIXTURES = {
    "investigate-live-question": ROOT / "fixtures" / "slice-3-investigate-live-question.md",
    "deploy-with-recovery": ROOT / "fixtures" / "slice-3-deploy-with-recovery.md",
    "diagnose-production-incident": ROOT / "fixtures" / "slice-3-diagnose-production-incident.md",
}
REQUIRED_BEHAVIOR = {
    "investigate-live-question": (
        "Approved Evidence Bridge",
        "provenance, sensitivity, and limits",
        "answered, reframed, prototype-ready, or unresolved",
    ),
    "deploy-with-recovery": (
        "failed verification",
        "execute the recorded rollback",
        "route to the conductor",
    ),
    "diagnose-production-incident": (
        "linked, bounded Change Work Object",
        "relationship `responds_to` the Incident",
        "retain the Incident's immutable type and evidence history",
    ),
}
REQUIRED_SCENARIOS = {
    "investigate-live-question": (
        "Approved Evidence Bridge with approval, provenance, sensitivity",
        "answered", "reframed", "prototype-ready", "unresolved",
    ),
    "deploy-with-recovery": (
        "Scenario 3 — Failed verification invokes rollback",
        "stops further rollout immediately",
        "verifies the rollback result",
    ),
    "diagnose-production-incident": (
        "Scenario 5 — Prevention becomes a linked bounded Change Work Object",
        "linked follow-up Change Work Object with `responds_to`",
        "does not implement or deploy the prevention action",
    ),
}


class PKMProjectAdapterQualificationContract(unittest.TestCase):
    def test_released_adapter_preserves_the_operational_paths_and_protocol(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        protocol_text = PROTOCOL.read_text()
        for platform in PLATFORMS:
            for skill in SKILLS:
                with self.subTest(platform=platform, skill=skill):
                    adapter_dir = ROOT / "adapters" / platform / "skills" / skill
                    adapter_text = (adapter_dir / "SKILL.md").read_text()
                    core_text = (ROOT / "skills" / "core" / skill / "SKILL.md").read_text()
                    core_body = core_text.split("---", 2)[2].lstrip("\n").rstrip("\n")
                    self.assertIn(core_body, adapter_text)
                    self.assertEqual(
                        protocol_text,
                        (adapter_dir / "references" / "SHARED-PROTOCOL.md").read_text(),
                    )
                    for required_clause in REQUIRED_BEHAVIOR[skill]:
                        self.assertIn(required_clause, adapter_text)

    def test_behavioral_fixtures_exercise_the_three_qualified_paths(self):
        for skill, required_clauses in REQUIRED_SCENARIOS.items():
            fixture_text = FIXTURES[skill].read_text()
            for required_clause in required_clauses:
                with self.subTest(skill=skill, required_clause=required_clause):
                    self.assertIn(required_clause, fixture_text)

    def test_qualification_record_covers_routing_recovery_follow_up_and_gaps(self):
        text = QUALIFICATION.read_text()

        for required_clause in (
            "PKM Project Adapter",
            "Scenario 1 — Inquiry outcome routing",
            "Scenario 2 — Deployment recovery",
            "Scenario 3 — Incident follow-up Change creation",
            "Approved Evidence Bridge",
            "provenance",
            "sensitivity",
            "Verified inquiry path",
            "Verified deployment recovery path",
            "Verified incident follow-up path",
            "Manual or unsupported gaps",
            "Unresolved assumptions",
            "artifact-level verification",
            "does not authorize an external deployment or export",
            "live Personal Institution runtime remains explicitly unverified",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)


if __name__ == "__main__":
    unittest.main()
