import unittest
from pathlib import Path

from tools.ws.component_governance import governance_domain_for_skill
from tools.ws.design_asset_routing import FRONTIER_OWNERS, route_asset_record


ROOT = Path(__file__).resolve().parents[1]


class DesignProjectAssetWorkbenchTests(unittest.TestCase):
    def test_skill_contract_names_boundaries_and_routes(self):
        text = (
            ROOT
            / "skills"
            / "core"
            / "design-project-asset-workbench"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(text.lower().split())
        self.assertIn("name: design-project-asset-workbench", text)
        self.assertIn("## Governing principle", text)
        self.assertIn("## Design asset pipeline", text)
        self.assertIn("references/DESIGN-ASSET-PIPELINE.md", text)
        self.assertIn("references/DESIGN-ASSET-REGISTRY.md", text)
        self.assertIn("does not:", normalized)
        self.assertIn("create or edit assets", normalized)
        self.assertIn("become the source of truth", normalized)
        self.assertIn("infer unrecorded relationships", normalized)
        self.assertIn("register durable components", normalized)
        self.assertIn("export, publish, or share a projection", normalized)
        self.assertIn("route back to the owning asset skill or conductor", normalized)

    def test_projection_frontier_routes_to_workbench_skill(self):
        self.assertEqual(
            "design-project-asset-workbench", FRONTIER_OWNERS["projection"]
        )

    def test_reviewbadge_routes_to_workbench_at_projection_frontier(self):
        path = ROOT / ".work-studio" / "design-assets" / "reviewbadge.asset.md"
        route = route_asset_record(path, frontier="projection")
        self.assertEqual("`asset.design.reviewbadge`", route.asset_id)
        self.assertEqual("projection", route.frontier)
        self.assertEqual("design-project-asset-workbench", route.owner)
        self.assertEqual((), route.gaps)

    def test_workbench_does_not_own_adjacent_frontiers(self):
        adjacent = {
            "identity": "design-manage-assets",
            "foundation": "design-compose-design-system",
            "tokens": "design-compose-design-system",
            "theme": "design-compose-design-system",
            "variant": "design-compose-design-system",
            "component-family": "design-compose-design-system",
            "ux-pattern": "design-steward-experience-patterns",
            "flow": "design-steward-experience-patterns",
            "creative-direction": "design-apply-design-direction",
            "implementation": "alawas-engineering-implement-bounded-change",
            "verification": "design-verify-design-implementation",
            "component-registration": "design-track-components",
        }
        for frontier, owner in adjacent.items():
            self.assertNotEqual(
                "design-project-asset-workbench", FRONTIER_OWNERS[frontier]
            )
            self.assertEqual(owner, FRONTIER_OWNERS[frontier])

    def test_component_governance_declares_design_domain(self):
        self.assertEqual(
            "design", governance_domain_for_skill("design-project-asset-workbench")
        )


if __name__ == "__main__":
    unittest.main()
