"""Focused tests for the COMP-041 GPU claim registry tracer."""

import sys
import tempfile
import threading
import unittest
from pathlib import Path

TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
sys.path.insert(0, str(TOOLS_PRODUCTION))

from gpu_orchestrator import registry  # noqa: E402


class TestGpuClaimRegistry(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.registry_dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_query_defaults_to_idle(self):
        state = registry.query(self.registry_dir)
        self.assertEqual(state["state"], "idle")
        self.assertIsNone(state["owner"])

    def test_claim_and_release_round_trip(self):
        claimed = registry.claim(
            self.registry_dir, "blender", "blender-1", stale_after_s=60, now_s=10
        )
        self.assertTrue(claimed.granted)
        self.assertEqual(claimed.state, "blender_loaded")

        current = registry.query(self.registry_dir)
        self.assertEqual(current["owner"], "blender")
        self.assertEqual(current["owner_id"], "blender-1")

        released = registry.release(
            self.registry_dir, "blender", "blender-1", now_s=20
        )
        self.assertTrue(released.granted)
        self.assertEqual(released.state, "idle")

    def test_competing_claim_is_rejected_while_owner_is_live(self):
        first = registry.claim(
            self.registry_dir, "comfyui_flux", "flux-1", stale_after_s=60, now_s=10
        )
        second = registry.claim(
            self.registry_dir, "blender", "blender-1", stale_after_s=60, now_s=20
        )

        self.assertTrue(first.granted)
        self.assertFalse(second.granted)
        self.assertEqual(second.reason, "occupied")
        self.assertEqual(registry.query(self.registry_dir)["state"], "comfyui_flux_loaded")

    def test_reclaim_by_same_owner_refreshes_heartbeat(self):
        registry.claim(
            self.registry_dir, "comfyui_hunyuan", "hunyuan-1",
            stale_after_s=60, now_s=10,
        )
        refreshed = registry.claim(
            self.registry_dir, "comfyui_hunyuan", "hunyuan-1",
            stale_after_s=60, now_s=30,
        )

        self.assertTrue(refreshed.granted)
        self.assertEqual(refreshed.reason, "refreshed")
        self.assertEqual(registry.query(self.registry_dir)["heartbeat_at_s"], 30.0)

    def test_stale_owner_can_be_recovered(self):
        registry.claim(
            self.registry_dir, "comfyui_flux", "flux-1", stale_after_s=60, now_s=10
        )
        recovered = registry.claim(
            self.registry_dir, "blender", "blender-1", stale_after_s=60, now_s=71
        )

        self.assertTrue(recovered.granted)
        self.assertEqual(recovered.state, "blender_loaded")
        self.assertEqual(recovered.recovered_from["owner"], "comfyui_flux")
        self.assertEqual(registry.query(self.registry_dir)["owner"], "blender")

    def test_wrong_owner_cannot_release_live_claim(self):
        registry.claim(
            self.registry_dir, "blender", "blender-1", stale_after_s=60, now_s=10
        )
        released = registry.release(
            self.registry_dir, "comfyui_flux", "flux-1", now_s=20
        )

        self.assertFalse(released.granted)
        self.assertEqual(released.reason, "owner_mismatch")
        self.assertEqual(registry.query(self.registry_dir)["state"], "blender_loaded")

    def test_parallel_claims_grant_at_most_one_owner(self):
        results = []
        start = threading.Barrier(3)

        def attempt(owner, owner_id):
            start.wait()
            results.append(
                registry.claim(
                    self.registry_dir, owner, owner_id,
                    stale_after_s=60, now_s=10,
                )
            )

        threads = [
            threading.Thread(target=attempt, args=("blender", "blender-1")),
            threading.Thread(target=attempt, args=("comfyui_flux", "flux-1")),
        ]
        for thread in threads:
            thread.start()
        start.wait()
        for thread in threads:
            thread.join()

        granted = [result for result in results if result.granted]
        rejected = [result for result in results if not result.granted]
        self.assertEqual(len(granted), 1)
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0].reason, "occupied")
        self.assertIn(
            registry.query(self.registry_dir)["state"],
            {"blender_loaded", "comfyui_flux_loaded"},
        )


if __name__ == "__main__":
    unittest.main()
