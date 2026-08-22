import tempfile
import unittest
from pathlib import Path

from tools.ws.component_governance import governance_domain_for_skill
from tools.ws.design_asset_routing import FRONTIER_OWNERS, route_asset_record


ROOT = Path(__file__).resolve().parents[1]


class DesignManageAssetsTests(unittest.TestCase):
    def test_skill_contract_names_boundaries_and_routes(self):
        text = (
            ROOT / "skills" / "core" / "design-manage-assets" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(text.lower().split())
        self.assertIn("name: design-manage-assets", text)
        self.assertIn("## Governing principle", text)
        self.assertIn("## Design asset pipeline", text)
        self.assertIn("references/DESIGN-ASSET-PIPELINE.md", text)
        self.assertIn("references/DESIGN-ASSET-REGISTRY.md", text)
        self.assertIn("does not create", normalized)
        self.assertIn("does not become the source of truth", normalized)
        self.assertIn("route to exactly one next owning skill", normalized)

    def test_reviewbadge_identity_routes_to_asset_manager(self):
        path = ROOT / ".work-studio" / "design-assets" / "reviewbadge.asset.md"
        route = route_asset_record(path)
        self.assertEqual("`asset.design.reviewbadge`", route.asset_id)
        self.assertEqual("component-family", route.asset_kind)
        self.assertEqual("active", route.status)
        self.assertEqual("identity", route.frontier)
        self.assertEqual("design-manage-assets", route.owner)
        self.assertEqual((), route.gaps)

    def test_frontier_routes_are_single_owner(self):
        expected = {
            "tokens": "design-compose-design-system",
            "ux-pattern": "design-steward-experience-patterns",
            "implementation": "alawas-engineering-implement-bounded-change",
            "projection": "design-project-asset-workbench",
        }
        for frontier, owner in expected.items():
            self.assertEqual(owner, FRONTIER_OWNERS[frontier])

    def test_unknown_frontier_is_gap_not_guess(self):
        path = ROOT / ".work-studio" / "design-assets" / "reviewbadge.asset.md"
        route = route_asset_record(path, frontier="database")
        self.assertEqual("", route.owner)
        self.assertIn("unknown design asset frontier: database", route.gaps)

    def test_invalid_asset_keeps_validation_gaps(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.asset.md"
            path.write_text(
                "# Broken\n\n"
                "**Work Object:** `2026-08-22-017`\n"
                "**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`\n"
                "**Status:** tracer\n"
                "**Asset ID:** `asset.design.broken`\n"
                "**Asset kind:** component-family\n"
                "**Source of truth:** this asset record\n\n"
                "## Asset Summary\n\nBroken.\n"
                "## Lifecycle\n\n| Step | Owning skill | Evidence |\n"
                "|------|--------------|----------|\n"
                "| Intake | `design-manage-assets` | test |\n"
                "## Verification Notes\n\nNone.\n"
                "## Rollback\n\nDelete.\n",
                encoding="utf-8",
            )
            route = route_asset_record(path)
        self.assertEqual("design-manage-assets", route.owner)
        self.assertTrue(any("Projection status" in gap for gap in route.gaps))

    def test_component_governance_declares_design_domain(self):
        self.assertEqual("design", governance_domain_for_skill("design-manage-assets"))


if __name__ == "__main__":
    unittest.main()
