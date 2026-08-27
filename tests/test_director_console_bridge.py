import json
import tempfile
import unittest
from pathlib import Path

from director_console.bridge import DirectorConsoleBridge


class FakeWorkspace:
    def summary(self):
        return {"scene_count": 1}

    def get_scene(self, scene_id):
        return {"id": scene_id}

    def submit_direction(self, scene_id, text, expected_updated_at):
        return {
            "scene_id": scene_id,
            "text": text,
            "expected_updated_at": expected_updated_at,
        }

    def render_scene_board(self):
        return {"scenes": 1}

    def open_local_artifact(self, path):
        return {"path": path}


def _make_bridge():
    return DirectorConsoleBridge(FakeWorkspace())


class DirectorConsoleBridgeTests(unittest.TestCase):
    def test_bridge_wraps_success_response(self):
        bridge = _make_bridge()

        response = bridge.get_workspace_summary()

        self.assertEqual(
            response,
            {
                "ok": True,
                "data": {"scene_count": 1},
                "error": None,
            },
        )

    def test_bridge_keeps_api_surface_narrow(self):
        bridge = _make_bridge()

        public = {
            name for name in dir(bridge)
            if not name.startswith("_") and callable(getattr(bridge, name))
        }

        self.assertEqual(
            public,
            {
                "get_workspace_summary",
                "get_scene",
                "submit_direction",
                "render_scene_board",
                "open_local_artifact",
                "gate_status",
                "approve_gate",
                "deny_gate",
            },
        )


class GateBridgeTests(unittest.TestCase):
    def setUp(self):
        self.bridge = _make_bridge()
        self.tmp = tempfile.TemporaryDirectory(prefix="ws-gate-bridge-")
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)

    def _seed_waiting_shot(self):
        import sys

        prod = Path(__file__).resolve().parents[1] / "tools" / "production"
        sys.path.insert(0, str(prod))
        from shot_pipeline import pipeline

        pipeline.run_pipeline(
            pipeline.ShotState("SH-ui", "ui gate"),
            self.work,
            lambda tier, w, h: {"fake": True},
        )
        state = pipeline.ShotState.load(self.work / "shot_state.json")
        self.assertEqual(state.status, pipeline.STATE_WAITING)
        return prod

    def test_gate_status_reports_waiting_breakdown(self):
        self._seed_waiting_shot()

        response = self.bridge.gate_status(str(self.work))

        self.assertTrue(response["ok"])
        self.assertEqual(response["data"]["pending_gate"], "breakdown")
        self.assertTrue(response["data"]["waiting"])

    def test_approve_gate_writes_record_approval_contract(self):
        self._seed_waiting_shot()

        response = self.bridge.approve_gate(str(self.work), "breakdown")

        self.assertTrue(response["ok"])
        record = json.loads(
            (self.work / "approval-breakdown.json").read_text(encoding="utf-8"))
        self.assertEqual(set(record), {"tier", "approved_by", "at"})
        self.assertEqual(record["tier"], "breakdown")
        self.assertEqual(record["approved_by"], "director")

    def test_wrong_tier_rejected_before_write(self):
        self._seed_waiting_shot()
        before = sorted(p.name for p in self.work.iterdir())

        response = self.bridge.approve_gate(str(self.work), "tier_a")

        self.assertFalse(response["ok"])
        self.assertEqual(response["error"]["code"], "ApprovalError")
        self.assertEqual(sorted(p.name for p in self.work.iterdir()), before)

    def test_missing_work_dir_is_structured_error(self):
        response = self.bridge.gate_status(str(self.work / "nope"))

        self.assertFalse(response["ok"])
        self.assertEqual(response["error"]["code"], "FileNotFoundError")


if __name__ == "__main__":
    unittest.main()
