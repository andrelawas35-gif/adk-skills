"""Tracer: Tier-A render timing + artifact durability (WO 2026-08-25-019).

Constructs a fresh minimal Blender scene, executes a Tier-A render with
wall-clock timing, persists artifact paths in ShotState, and verifies
artifacts on disk after reload.
"""

import sys
import time
from pathlib import Path

# Ensure shot_pipeline is importable from Blender's Python
_TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent
if str(_TOOLS_PRODUCTION) not in sys.path:
    sys.path.insert(0, str(_TOOLS_PRODUCTION))

import json

from shot_pipeline.pipeline import ShotState, record_artifact, TIERS, TIER_HEIGHT

WORK_DIR = Path(__file__).resolve().parent.parent.parent.parent / "runtime" / "tier_a_timing_test"
OUTPUTS_DIR = WORK_DIR / "outputs"


def _build_minimal_scene():
    """Construct a minimal Blender scene: cube + camera + light."""
    import bpy

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.name = "TestCube"
    cube.scale = (1, 1, 1)

    bpy.ops.object.camera_add(location=(3, -3, 2.5))
    cam = bpy.context.active_object
    cam.name = "TestCamera"
    cam.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type="POINT", location=(2, -2, 3))
    light = bpy.context.active_object
    light.name = "TestLight"
    light.data.energy = 500

    return cube, cam, light


def _execute_tier(tier: str, width: int, height: int) -> dict:
    """Execute a Tier-A render through the bounded operator surface."""
    import bpy

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    filepath = str(OUTPUTS_DIR / f"{tier}_render.png")

    scene = bpy.context.scene
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

    return {
        "tier": tier,
        "filepath": filepath,
        "resolution": [width, height],
        "rendered": True,
    }


def run_tracer():
    """Run the Tier-A timing + artifact durability tracer."""
    print("=" * 60)
    print("WO 2026-08-25-019: Tier-A Timing + Artifact Durability Tracer")
    print("=" * 60)

    WORK_DIR.mkdir(parents=True, exist_ok=True)

    shot = ShotState(shot_id="SH001-TIER-A-TEST", prompt="Minimal test scene for Tier-A timing")
    shot.save(WORK_DIR / "shot_state.json")

    print("\n[1/5] Building minimal Blender scene...")
    _build_minimal_scene()
    print("  Scene: cube + camera + light")

    tier = "tier_a"
    width, height = TIERS[tier], TIER_HEIGHT[tier]
    print(f"\n[2/5] Executing Tier-A render ({width}x{height})...")

    start = time.monotonic()
    result = _execute_tier(tier, width, height)
    elapsed_s = time.monotonic() - start

    print(f"  Render completed in {elapsed_s:.2f}s")
    print(f"  Output: {result['filepath']}")

    record_artifact(shot, tier, result["filepath"], kind="render")
    shot.history.append({
        "from": tier, "to": tier, "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": f"executed:{tier} wall_clock={elapsed_s:.2f}s",
    })
    shot.save(WORK_DIR / "shot_state.json")
    print(f"  Artifact recorded in ShotState")

    print("\n[3/5] Reloading ShotState from disk...")
    reloaded = ShotState.load(WORK_DIR / "shot_state.json")
    print(f"  shot_id: {reloaded.shot_id}")
    print(f"  artifacts count: {len(reloaded.artifacts)}")

    print("\n[4/5] Verifying artifacts on disk...")
    for art in reloaded.artifacts:
        art_path = Path(art["path"])
        exists = art_path.exists()
        size = art_path.stat().st_size if exists else 0
        status = "OK" if exists and size > 0 else "FAIL"
        print(f"  [{status}] {art['path']} (exists={exists}, size={size} bytes)")
        if not exists or size == 0:
            print("  FAIL: Artifact not verified on disk")
            return False

    print("\n[5/5] Summary")
    print(f"  Wall-clock timing: {elapsed_s:.2f}s")
    print(f"  Tier-A render: {width}x{height}")
    print(f"  Artifact path: {result['filepath']}")
    print(f"  Artifact persisted: {'artifacts' in json.loads((WORK_DIR / 'shot_state.json').read_text())}")
    print(f"  Artifact verified on disk: True")

    evidence = {
        "wall_clock_s": round(elapsed_s, 2),
        "tier": tier,
        "resolution": [width, height],
        "artifact_path": result["filepath"],
        "artifact_verified": True,
    }
    print(f"\n  [system] evidence: {json.dumps(evidence)}")

    print("\n" + "=" * 60)
    print("TRACER RESULT: PASS")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_tracer()
    exit(0 if success else 1)
