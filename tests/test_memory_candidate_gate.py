"""Contract test for the PKM Memory Candidate admission gate."""

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / "tools" / "generate-adapters.py"
CORE = ROOT / "skills" / "core" / "thinking-turn-signal-into-work" / "SKILL.md"
CONTRACT = ROOT / "fixtures" / "personal-institution-work-studio-contract.md"
QUALIFICATION = (
    ROOT / ".work-studio" / "objects" / "2026" / "07"
    / "2026-07-15-003-qualify-pkm-memory-candidate-gate.md"
)
PLATFORMS = ("codex", "claude-code", "github-copilot")


class MemoryCandidateGateContract(unittest.TestCase):
    def test_memory_candidates_require_an_approved_redacted_evidence_bridge(self):
        text = " ".join(CORE.read_text().split())

        for required_clause in (
            "Memory Candidate gate",
            "approved, redacted Evidence Bridge",
            "must not enter a Work Object",
            "personal-memory content",
            "Explicit activation does not bypass this gate",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_cross_package_fixture_keeps_private_records_out_of_work_objects(self):
        text = CONTRACT.read_text()

        for required_clause in (
            "Private record does not enter a Work Object by default",
            "Approved Evidence Bridge is minimal and attributed",
            "no copied personal-memory text",
            "Scenario 7 — Memory Candidate gate admits only an approved bridge",
            "explicit activation as approval to retrieve or",
            "minimum necessary user-approved summary",
            "**Recovery**: When the user supplies that approved, redacted bridge",
            "route the activated signal to the conductor",
            "stable reference and sensitivity",
            "does not copy the source record",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)

    def test_generated_adapters_preserve_the_gate(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

        for platform in PLATFORMS:
            with self.subTest(platform=platform):
                adapter = ROOT / "adapters" / platform / "skills" / "alawas-turn-signal-into-work" / "SKILL.md"
                self.assertIn("Memory Candidate gate", adapter.read_text())

    def test_qualification_record_evidences_every_slice_2_handoff(self):
        text = QUALIFICATION.read_text()

        for required_clause in (
            "turn-signal-into-work",
            "conduct-work-object",
            "design-tracer-bullet",
            "implement-bounded-change",
            "verify-release-evidence",
            "Verified user path",
            "Verified recovery path",
            "Deviation status: none observed",
            "live-PKM runtime behavior remains explicitly unverified",
        ):
            with self.subTest(required_clause=required_clause):
                self.assertIn(required_clause, text)


if __name__ == "__main__":
    unittest.main()
