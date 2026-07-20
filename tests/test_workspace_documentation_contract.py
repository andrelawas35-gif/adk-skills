"""Contract tests for grounded documentation discovery and bootstrap."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "WORKSPACE-DOCUMENTATION-CONTRACT.md"
FIXTURE = ROOT / "fixtures" / "workspace-documentation-contract.md"


class WorkspaceDocumentationContract(unittest.TestCase):
    def test_registry_is_versioned_and_has_all_required_artifact_fields(self):
        text = CONTRACT.read_text()
        self.assertIn("schema_version: 1", text)
        entries = re.split(r"^  - type: ", text, flags=re.MULTILINE)[1:]
        self.assertEqual(11, len(entries))
        for entry in entries:
            for field in (
                "path:", "purpose:", "owner:", "stage_trigger:",
                "required_evidence:", "creation_update_authority:",
                "provenance_freshness:", "supersession:", "status:",
                "validation:",
            ):
                self.assertIn(field, entry)

    def test_contract_prohibits_hallucinated_discovery_and_unscoped_creation(self):
        text = " ".join(CONTRACT.read_text().split())
        for phrase in (
            "Missing Artifact Gap",
            "Do not search plausible alternatives",
            "Explicit `bootstrap` authority creates this file and",
            "cannot activate one",
            "do not edit them directly",
            "requires an ADR and explicit owner approval",
            "its empty per-project ledger",
        ):
            self.assertIn(phrase, text)

    def test_fixture_covers_required_workspace_states(self):
        text = FIXTURE.read_text()
        for scenario in range(1, 7):
            self.assertIn(f"## Scenario {scenario}", text)
        for phrase in (
            "Empty workspace bootstrap", "Docs-only workspace",
            "Code without docs", "Missing reference",
            "Conflicting and stale records", "Generated adapter drift",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
