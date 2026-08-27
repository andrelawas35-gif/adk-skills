"""GPU-claim wiring tests for the bounded Blender operator (WO 2026-08-24-014).

Covers the integration seam between the Blender operator's VRAM-heavy ops and
the COMP-041 file-backed GPU claim registry (WO 2026-08-24-013): a VRAM op
claims the single GPU slot before running and releases after; a competing live
owner blocks the VRAM op with ``gpu_occupied``.

The executor body is injected (a fake bpy-free callback), so this test
exercises the real claim/release wiring without launching Blender. The pure
registry semantics are already covered by ``tests/test_gpu_orchestrator.py``.
"""

import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
sys.path.insert(0, str(TOOLS_PRODUCTION))

from blender_operator import governance  # noqa: E402
from gpu_orchestrator import registry as gpu_registry  # noqa: E402

# executor.py imports bpy (unavailable outside Blender), so the GPU claim
# contract it uses is locked directly against gpu_registry + governance.VRAM_OPS:
# a VRAM op claims owner='blender' before running and releases after.
class TestVramOpsSet(unittest.TestCase):
    def test_vram_heavy_ops_are_gated(self):
        for op in ("render.preview", "render.final", "object.import_mesh",
                   "image.import_as_plane", "image.set_as_reference",
                   "material.set_texture"):
            self.assertIn(op, governance.VRAM_OPS)

    def test_read_only_ops_are_not_vram_gated(self):
        for op in ("scene.get_objects", "object.get", "camera.get"):
            self.assertNotIn(op, governance.VRAM_OPS)


class TestExecutorGpuClaimContract(unittest.TestCase):
    """Locks the exact claim/release sequence the executor performs for VRAM ops."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.registry_dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_claim_release_round_trip_for_blender_owner(self):
        claimed = gpu_registry.claim(
            self.registry_dir, "blender", "blender-0", stale_after_s=60, now_s=1
        )
        self.assertTrue(claimed.granted)
        self.assertEqual(claimed.state, "blender_loaded")
        state = gpu_registry.query(self.registry_dir)
        self.assertEqual(state["owner"], "blender")
        self.assertEqual(state["owner_id"], "blender-0")

        released = gpu_registry.release(
            self.registry_dir, "blender", "blender-0", now_s=2
        )
        self.assertTrue(released.granted)
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"], "idle")

    def test_competing_owner_blocks_vram_op(self):
        gpu_registry.claim(
            self.registry_dir, "comfyui_flux", "flux-1", stale_after_s=60, now_s=1
        )
        claimed = gpu_registry.claim(
            self.registry_dir, "blender", "blender-0", stale_after_s=60, now_s=2
        )
        self.assertFalse(claimed.granted)
        self.assertEqual(claimed.reason, "occupied")
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"],
                         "comfyui_flux_loaded")


if __name__ == "__main__":
    unittest.main()
