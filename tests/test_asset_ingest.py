import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.ws.asset_ingest import ingest_asset
from tools.ws.design_assets import compose_draft_asset_record, validate_asset_record


ROOT = Path(__file__).resolve().parents[1]


class AssetIngestTests(unittest.TestCase):
    def test_compose_draft_asset_record_marks_proposal_not_canonical(self):
        text = compose_draft_asset_record(
            asset_id="asset.design.test.tokens",
            asset_kind="token-set",
            work_object="2026-08-22-017",
            summary="Draft status token set for ingest testing.",
            source_note="unit test explicit input",
            frontier="tokens",
        )

        self.assertIn("**Status:** draft", text)
        self.assertIn("**Asset ID:** `asset.design.test.tokens`", text)
        self.assertIn("draft ingest proposal from explicit input", text)
        self.assertIn("not an accepted canonical asset", text)
        self.assertIn("`design-manage-assets`", text)

    def test_ingest_asset_creates_valid_draft_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = ingest_asset(
                root,
                asset_id="asset.design.test.tokens",
                asset_kind="token-set",
                work_object="2026-08-22-017",
                summary="Draft status token set for ingest testing.",
                source_note="unit test explicit input",
                frontier="tokens",
            )

            path = root / ".work-studio" / "design-assets" / "test-tokens.asset.md"
            self.assertEqual(path, result["path"])
            self.assertEqual([], result["errors"])
            self.assertEqual([], validate_asset_record(path))
            self.assertIn("**Status:** draft", path.read_text(encoding="utf-8"))

    def test_ingest_asset_refuses_duplicate_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            kwargs = {
                "asset_id": "asset.design.duplicate",
                "asset_kind": "component-family",
                "work_object": "2026-08-22-017",
                "summary": "Duplicate ingest test.",
                "source_note": "unit test explicit input",
            }
            ingest_asset(root, **kwargs)

            with self.assertRaises(FileExistsError):
                ingest_asset(root, **kwargs)

    def test_cli_command_creates_valid_draft_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".work-studio").mkdir()
            env = dict(os.environ)
            env["PYTHONPATH"] = str(ROOT)
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "tools.ws",
                    "asset-ingest",
                    "--asset-id",
                    "asset.design.cli.tokens",
                    "--asset-kind",
                    "token-set",
                    "--work-object",
                    "2026-08-22-017",
                    "--summary",
                    "CLI-created draft token set for ingest testing.",
                    "--source-note",
                    "unit test CLI explicit input",
                    "--frontier",
                    "tokens",
                ],
                cwd=str(root),
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

            path = root / ".work-studio" / "design-assets" / "cli-tokens.asset.md"
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("Validation: passed", result.stdout)
            self.assertTrue(path.exists())
            self.assertEqual([], validate_asset_record(path))


if __name__ == "__main__":
    unittest.main()
