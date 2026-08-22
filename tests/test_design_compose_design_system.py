import unittest
from pathlib import Path

from tools.ws.component_governance import governance_domain_for_skill
from tools.ws.design_asset_routing import FRONTIER_OWNERS, route_asset_record


ROOT = Path(__file__).resolve().parents[1]


class DesignComposeDesignSystemTests(unittest.TestCase):
    def test_skill_contract_names_boundaries_and_routes(self):
        text = (
            ROOT / "skills" / "core" / "design-compose-design-system" / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(text.lower().split())
        self.assertIn("name: design-compose-design-system", text)
        self.assertIn("## Governing principle", text)
        self.assertIn("## Design asset pipeline", text)
        self.assertIn("references/DESIGN-ASSET-PIPELINE.md", text)
        self.assertIn("references/DESIGN-ASSET-REGISTRY.md", text)
        self.assertIn("does not:", normalized)
        self.assertIn("silently choose a creative direction", normalized)
        self.assertIn("mutate canonical asset records", normalized)
        self.assertIn("implement code or verify browser parity", normalized)
        self.assertIn("route to exactly one owner or preserve ambiguity", normalized)

    def test_compose_frontiers_route_to_compose_skill(self):
        expected = {
            "foundation": "design-compose-design-system",
            "tokens": "design-compose-design-system",
            "theme": "design-compose-design-system",
            "variant": "design-compose-design-system",
            "component-family": "design-compose-design-system",
        }
        for frontier, owner in expected.items():
            self.assertEqual(owner, FRONTIER_OWNERS[frontier])

    def test_reviewbadge_routes_to_compose_at_compose_frontier(self):
        path = ROOT / ".work-studio" / "design-assets" / "reviewbadge.asset.md"
        for frontier in ("theme", "component-family"):
            route = route_asset_record(path, frontier=frontier)
            self.assertEqual("`asset.design.reviewbadge`", route.asset_id)
            self.assertEqual(frontier, route.frontier)
            self.assertEqual("design-compose-design-system", route.owner)
            self.assertEqual((), route.gaps)

    def test_compose_does_not_own_adjacent_frontiers(self):
        adjacent = {
            "identity": "design-manage-assets",
            "ux-pattern": "design-steward-experience-patterns",
            "flow": "design-steward-experience-patterns",
            "creative-direction": "design-apply-design-direction",
            "implementation": "alawas-engineering-implement-bounded-change",
            "verification": "design-verify-design-implementation",
            "component-registration": "design-track-components",
            "projection": "design-project-asset-workbench",
        }
        for frontier, owner in adjacent.items():
            self.assertNotEqual(
                "design-compose-design-system", FRONTIER_OWNERS[frontier]
            )
            self.assertEqual(owner, FRONTIER_OWNERS[frontier])

    def test_component_governance_declares_design_domain(self):
        self.assertEqual(
            "design", governance_domain_for_skill("design-compose-design-system")
        )


if __name__ == "__main__":
    unittest.main()
