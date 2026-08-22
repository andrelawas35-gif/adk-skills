import unittest
from pathlib import Path

from tools.ws.component_governance import governance_domain_for_skill
from tools.ws.design_asset_routing import FRONTIER_OWNERS, route_asset_record


ROOT = Path(__file__).resolve().parents[1]


class DesignStewardExperiencePatternsTests(unittest.TestCase):
    def test_skill_contract_names_boundaries_and_routes(self):
        text = (
            ROOT
            / "skills"
            / "core"
            / "design-steward-experience-patterns"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(text.lower().split())
        self.assertIn("name: design-steward-experience-patterns", text)
        self.assertIn("## Governing principle", text)
        self.assertIn("## Design asset pipeline", text)
        self.assertIn("references/DESIGN-ASSET-PIPELINE.md", text)
        self.assertIn("references/DESIGN-ASSET-REGISTRY.md", text)
        self.assertIn("does not:", normalized)
        self.assertIn("style the pattern or choose visual themes", normalized)
        self.assertIn("implement code or verify browser parity", normalized)
        self.assertIn("claim accessibility compliance", normalized)
        self.assertIn("register durable components", normalized)
        self.assertIn("mutate canonical asset records", normalized)
        self.assertIn("route to exactly one owner or preserve ambiguity", normalized)

    def test_steward_frontiers_route_to_steward_skill(self):
        expected = {
            "ux-pattern": "design-steward-experience-patterns",
            "flow": "design-steward-experience-patterns",
        }
        for frontier, owner in expected.items():
            self.assertEqual(owner, FRONTIER_OWNERS[frontier])

    def test_draft_ux_pattern_routes_to_steward_at_steward_frontier(self):
        path = (
            ROOT
            / ".work-studio"
            / "design-assets"
            / "create-review-approve-pattern.asset.md"
        )
        route = route_asset_record(path, frontier="ux-pattern")
        self.assertEqual("`asset.design.create-review-approve-pattern`", route.asset_id)
        self.assertEqual("ux-pattern", route.asset_kind)
        self.assertEqual("ux-pattern", route.frontier)
        self.assertEqual("design-steward-experience-patterns", route.owner)
        self.assertEqual((), route.gaps)

    def test_steward_does_not_own_adjacent_frontiers(self):
        adjacent = {
            "identity": "design-manage-assets",
            "foundation": "design-compose-design-system",
            "tokens": "design-compose-design-system",
            "theme": "design-compose-design-system",
            "variant": "design-compose-design-system",
            "component-family": "design-compose-design-system",
            "creative-direction": "design-apply-design-direction",
            "implementation": "alawas-engineering-implement-bounded-change",
            "verification": "design-verify-design-implementation",
            "component-registration": "design-track-components",
            "projection": "design-project-asset-workbench",
        }
        for frontier, owner in adjacent.items():
            self.assertNotEqual(
                "design-steward-experience-patterns", FRONTIER_OWNERS[frontier]
            )
            self.assertEqual(owner, FRONTIER_OWNERS[frontier])

    def test_component_governance_declares_design_domain(self):
        self.assertEqual(
            "design",
            governance_domain_for_skill("design-steward-experience-patterns"),
        )


if __name__ == "__main__":
    unittest.main()
