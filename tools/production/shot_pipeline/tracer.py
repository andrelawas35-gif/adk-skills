"""Tier A end-to-end tracer for the shot production pipeline (COMP-049).

WO 2026-08-25-008 Decision 2026-08-26T01:30:00Z (accepted tracer bullet).
Riskiest assumption under test: the scene planner's ``blender_command_plan``
can be consumed by the Blender operator's crash-durable file queue with only
a thin schema adapter.

Path:
1. ``plan_scene`` turns a prompt + a generated fixture registry into a scene
   spec whose ``blender_command_plan`` carries bounded ops.
2. The thin adapter validates every plan op against the known bounded surface
   and drops each one through ``blender_operator.queue`` as ``CMD-<id>.json``.
3. A real headless Blender 5.2 subprocess runs the COMP-042 add-on poller and
   executes the commands, returning durable result acks.
4. One appended ``render.final`` command captures the image artifact the exit
   criteria require (the planner's ``render.preview`` sets resolution only —
   discovered interface fact; ``render.final`` is in the same bounded §4.2
   surface and writes the file).
5. The visual critic evaluates the rendered image and returns its 5 bounded
   fields; presence + types are asserted (single pass, no loop).

Authorization: local test authority only; headless Blender subprocess;
no production access, no GPU-registry contention beyond the temp registry.
Rollback: TemporaryDirectory removes queue dir, artifacts, and registry.
"""

import importlib.util
import os
import subprocess
import sys
import tempfile
import time
import zlib
import struct
from pathlib import Path

BLENDER_EXE = Path(r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
REPO = Path(__file__).resolve().parent.parent.parent.parent
ADDON = REPO / "tools" / "production" / "blender_operator" / "addon.py"
CRITIC_FILE = (
    REPO / "skills" / "core" / "production-operate-visual-critic" / "tracer_bullet.py"
)

sys.path.insert(0, str(REPO / "tools" / "production"))
from blender_operator import queue  # noqa: E402
from gpu_orchestrator import registry as gpu_registry  # noqa: E402
from scene_planner.planner import plan_scene  # noqa: E402

_spec = importlib.util.spec_from_file_location("visual_critic_tracer", CRITIC_FILE)
visual_critic = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(visual_critic)

SESSION_ID = "shot-pipeline-tier-a"

# Ops the adapter will accept from a scene plan plus the capture command it
# appends itself. render.final is part of the accepted §4.2 bounded surface.
ADAPTER_OPS = frozenset(
    {"object.import_mesh", "camera.set", "light.set", "render.preview"}
)
CAPTURE_OP = "render.final"


def _tiny_obj(path: Path) -> None:
    obj = """# tier-a tracer figure stand-in
v -1 -1 -1
v  1 -1 -1
v  1  1 -1
v -1  1 -1
v -1 -1  1
v  1 -1  1
v  1  1  1
v -1  1  1
f 1 2 3 4
f 5 6 7 8
f 1 2 6 5
f 2 3 7 6
f 3 4 8 7
f 4 1 5 8
"""
    path.write_text(obj, encoding="utf-8")


def _fixture_registry(tmp_dir: Path, obj_path: Path) -> Path:
    registry_path = tmp_dir / "asset_registry.yaml"
    registry_path.write_text(
        "assets:\n"
        "  - asset_id: protagonist-hero\n"
        f"    path: {obj_path.as_posix()}\n"
        "    tags: [character, protagonist, hero]\n",
        encoding="utf-8",
    )
    return registry_path


def scene_plan_to_commands(scene_plan: dict) -> list[tuple[str, dict]]:
    """Thin schema adapter: scene plan -> ordered (op, params) queue commands."""
    commands = []
    for entry in scene_plan["blender_command_plan"]:
        op, params = entry["op"], dict(entry.get("params") or {})
        if op not in ADAPTER_OPS:
            raise ValueError(f"scene plan emitted op outside adapter surface: {op!r}")
        params.pop("asset_id", None)  # planner provenance tag, ignored by executor
        commands.append((op, params))
    return commands


def _wait_for_result(queue_dir: Path, cid: str, timeout_s: float = 90.0) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        result = queue.read_result(queue_dir, cid)
        if result is not None:
            return result
        time.sleep(0.5)
    raise TimeoutError(f"no result ack for {cid}")


def main() -> int:
    prompt = "A lone hero stands in a vast desert at dusk"

    with tempfile.TemporaryDirectory(prefix="ws-shot-pipeline-tracer-") as tmp:
        tmp_dir = Path(tmp)
        queue_dir = tmp_dir / "queue"
        gpu_dir = tmp_dir / "gpu"
        queue_dir.mkdir()
        gpu_dir.mkdir()
        obj_path = tmp_dir / "figure.obj"
        _tiny_obj(obj_path)
        registry_path = _fixture_registry(tmp_dir, obj_path)

        # ── Stage 1: scene planner ───────────────────────────────────────
        scene_plan = plan_scene(prompt, registry_path)
        plan_ops = [c["op"] for c in scene_plan["blender_command_plan"]]
        print(f"[tracer] scene plan ops: {plan_ops}")

        # ── Stage 2+3: adapter -> queue -> headless Blender ──────────────
        env = dict(os.environ)
        env["QUEUE_DIR"] = str(queue_dir)
        env["GPU_REGISTRY_DIR"] = str(gpu_dir)
        proc = subprocess.Popen(
            [str(BLENDER_EXE), "--background", "--factory-startup",
             "--python", str(ADDON),
             "--", "--queue-dir", str(queue_dir), "--session-id", SESSION_ID],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(6.0)

        try:
            seq = 0
            for op, params in scene_plan_to_commands(scene_plan):
                seq += 1
                cid = queue.write_command(
                    queue_dir, op, params,
                    command_id=queue.make_command_id(seq=seq),
                )
                r = _wait_for_result(queue_dir, cid)
                print(f"[tracer] {op} -> {r['status']}")
                if r["status"] != "ok":
                    print(f"[tracer] FAIL {op}: {r.get('error')}")
                    return 2

            # ── Capture: render.final writes the image artifact ──────────
            image_path = str(tmp_dir / "tier_a_render.png")
            seq += 1
            cid = queue.write_command(
                queue_dir, CAPTURE_OP,
                {"filepath": image_path, "format": "PNG"},
                command_id=queue.make_command_id(seq=seq),
            )
            r = _wait_for_result(queue_dir, cid)
            print(f"[tracer] {CAPTURE_OP} -> {r['status']}")
            if r["status"] != "ok":
                print(f"[tracer] FAIL {CAPTURE_OP}: {r.get('error')}")
                return 3
            if not Path(image_path).exists():
                print("[tracer] FAIL no rendered image on disk")
                return 4

            # ── GPU registry must be idle after all VRAM ops released ────
            state = gpu_registry.query(gpu_dir)
            if state["state"] != "idle":
                print(f"[tracer] FAIL GPU registry state: {state['state']}")
                return 5
        finally:
            proc.kill()
            proc.wait(timeout=10)

        # ── Stage 4: visual critic single pass ───────────────────────────
        critique = visual_critic.visual_critique_for_image(image_path, prompt)
        required = {
            "composition_score": float,
            "lighting_issues": list,
            "staging_recommendations": list,
            "subject_scale_feedback": str,
            "escalation_needed": bool,
        }
        for field, expected_type in required.items():
            if field not in critique or not isinstance(critique[field], expected_type):
                print(f"[tracer] FAIL critique field {field!r} missing/wrong type")
                return 6
        if not 0.0 <= critique["composition_score"] <= 1.0:
            print("[tracer] FAIL composition_score out of range")
            return 7

        print(f"[tracer] critique: score={critique['composition_score']} "
              f"escalation={critique['escalation_needed']}")
        print("[tracer] PASS: Tier A end-to-end — scene plan -> thin adapter -> "
              "file queue -> live Blender render -> visual critique (5 fields). "
              "Composition assumption HOLDS.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
