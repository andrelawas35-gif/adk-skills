import unittest
from pathlib import Path

from tools.ws.design_assets import (
    VALID_ASSET_KINDS,
    asset_record_paths,
    parse_asset_fields,
    validate_asset_record,
)
from tools.ws.design_asset_routing import FRONTIER_OWNERS, route_asset_record


ROOT = Path(__file__).resolve().parents[1]

# The four real draft asset records produced by the ReviewBadge tracer and the
# real-use ingest slices. The live pipeline walk must see all of them.
EXPECTED_REAL_ASSETS = {
    "`asset.design.reviewbadge`",
    "`asset.design.studio-status-tokens`",
    "`asset.design.reviewbadge-themes`",
    "`asset.design.create-review-approve-pattern`",
}

# Asset kind -> the design-asset frontiers that kind naturally exercises.
KIND_FRONTIERS = {
    "foundation": ("foundation",),
    "token-set": ("tokens",),
    "theme": ("theme",),
    "component-family": ("component-family",),
    "ux-pattern": ("ux-pattern",),
    "flow": ("flow",),
    "projection": ("projection",),
}

# Asset kind -> the single accepted owning skill for that frontier.
KIND_OWNER = {
    "foundation": "design-compose-design-system",
    "token-set": "design-compose-design-system",
    "theme": "design-compose-design-system",
    "component-family": "design-compose-design-system",
    "ux-pattern": "design-steward-experience-patterns",
    "flow": "design-steward-experience-patterns",
    "projection": "design-project-asset-workbench",
}


class LivePipelineWalkTests(unittest.TestCase):
    def test_real_asset_records_are_valid_and_known(self):
        paths = asset_record_paths(ROOT)
        self.assertGreaterEqual(len(paths), len(EXPECTED_REAL_ASSETS))
        asset_ids = set()
        for path in paths:
            self.assertEqual([], validate_asset_record(path), msg=str(path))
            asset_ids.add(
                parse_asset_fields(path.read_text(encoding="utf-8")).get(
                    "Asset ID", ""
                )
            )
        for expected in EXPECTED_REAL_ASSETS:
            self.assertIn(expected, asset_ids)

    def test_every_real_asset_routes_to_one_owner(self):
        paths = asset_record_paths(ROOT)
        self.assertTrue(paths, "no real asset records found to walk")
        for path in paths:
            fields = parse_asset_fields(path.read_text(encoding="utf-8"))
            kind = fields.get("Asset kind", "")
            self.assertIn(kind, VALID_ASSET_KINDS, msg=str(path))
            for frontier in KIND_FRONTIERS[kind]:
                route = route_asset_record(path, frontier=frontier)
                self.assertEqual(frontier, route.frontier, msg=str(path))
                self.assertTrue(route.owner, f"{path}: no owner at {frontier}")
                self.assertEqual((), route.gaps, msg=str(path))
            identity = route_asset_record(path, frontier="identity")
            self.assertEqual("design-manage-assets", identity.owner, msg=str(path))

    def test_pipeline_ownership_map_holds_on_real_kinds(self):
        for kind, owner in KIND_OWNER.items():
            for frontier in KIND_FRONTIERS[kind]:
                self.assertEqual(owner, FRONTIER_OWNERS[frontier])


if __name__ == "__main__":
    unittest.main()
