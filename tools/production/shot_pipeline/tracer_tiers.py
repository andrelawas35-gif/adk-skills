"""Slice 2 tracer: gated tier progression over live operators (COMP-049).

WO 2026-08-25-008 Decision 2026-08-26T01:45:00Z. Drives one shot through
breakdown -> tier_a -> tier_b -> tier_c -> final using pipeline.py:

1. NEGATIVE GATE CHECK — first run has zero approvals: the machine must halt
   in ``waiting_for_approval`` at breakdown without executing anything.
2. Progressive director approvals are recorded one gate at a time; after each
   halt the shot state is RELOADED FROM DISK before resuming, proving durable
   state across process boundaries and no re-execution of completed tiers.
3. Each tier executes the full scene plan through the proven adapter + queue
   into a FRESH headless Blender subprocess and queue dir at escalating
   resolution; render.final captures a per-tier PNG.
4. Exit evidence: complete transition history, four approval records, final
   PNG on disk, waiting-state negative check observed.
"""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(REPO / "tools" / "production"))
from blender_operator import queue  # noqa: E402
from gpu_orchestrator import registry as gpu_registry  # noqa: E402
from scene_planner.planner import plan_scene  # noqa: E402
from shot_pipeline import pipeline  # noqa: E402
from shot_pipeline.tracer import (  # noqa: E402
    BLENDER_EXE,
    ADDON,
    _tiny_obj,
    _fixture_registry,
    scene_plan_to_commands,
    _wait_for_result,
)


def _execute_tier_factory(plan_commands, tmp_dir: Path):
    """Build an execute_tier callback: fresh subprocess + queue dir per tier."""

    def execute_tier(tier: str, width: int, height: int) -> dict:
        tier_dir = tmp_dir / tier
        queue_dir = tier_dir / "queue"
        gpu_dir = tier_dir / "gpu"
        queue_dir.mkdir(parents=True)
        gpu_dir.mkdir()

        env = dict(os.environ)
        env["QUEUE_DIR"] = str(queue_dir)
        env["GPU_REGISTRY_DIR"] = str(gpu_dir)
        proc = subprocess.Popen(
            [str(BLENDER_EXE), "--background", "--factory-startup",
             "--python", str(ADDON),
             "--", "--queue-dir", str(queue_dir),
             "--session-id", f"shot-tier-{tier}"],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(6.0)
        try:
            seq = 0
            commands = list(plan_commands)
            image_path = str(tier_dir / f"{tier}.png")
            if tier == "tier_c":
                image_path = str(tmp_dir / "shot_final.png")
            commands.append(("render.final", {"filepath": image_path, "format": "PNG"}))
            for op, params in commands:
                if op == "render.preview":
                    params = dict(params, width=width, height=height)
                seq += 1
                cid = queue.write_command(
                    queue_dir, op, params,
                    command_id=queue.make_command_id(seq=seq),
                )
                r = _wait_for_result(queue_dir, cid)
                print(f"  [{tier}] {op} -> {r['status']}")
                if r["status"] != "ok":
                    raise RuntimeError(f"{tier}/{op}: {r.get('error')}")
            state = gpu_registry.query(gpu_dir)
            if state["state"] != "idle":
                raise RuntimeError(f"{tier}: GPU registry {state['state']}")
            if not Path(image_path).exists():
                raise RuntimeError(f"{tier}: no capture on disk")
        finally:
            proc.kill()
            proc.wait(timeout=10)
        return {"image": image_path}

    return execute_tier


def main() -> int:
    prompt = "A lone hero stands in a vast desert at dusk"

    with tempfile.TemporaryDirectory(prefix="ws-shot-pipeline-tiers-") as tmp:
        tmp_dir = Path(tmp)
        obj_path = tmp_dir / "figure.obj"
        _tiny_obj(obj_path)
        registry_path = _fixture_registry(tmp_dir, obj_path)
        plan = plan_scene(prompt, registry_path)
        plan_commands = scene_plan_to_commands(plan)
        execute_tier = _execute_tier_factory(plan_commands, tmp_dir)

        work_dir = tmp_dir / "work"
        work_dir.mkdir()
        shot = pipeline.ShotState("SH-tracer-01", prompt)

        # ── Negative gate check: zero approvals must block at breakdown ──
        shot.save(work_dir / "shot_state.json")
        shot = pipeline.run_pipeline(
            pipeline.ShotState.load(work_dir / "shot_state.json"),
            work_dir, execute_tier,
        )
        if shot.status != pipeline.STATE_WAITING or shot.state != "breakdown":
            print(f"[tiers] FAIL expected waiting@breakdown, got "
                  f"{shot.status}@{shot.state}")
            return 2
        if any((work_dir / f"approval-{t}.json").exists() for t in pipeline.STATES):
            print("[tiers] FAIL unexpected approval record present")
            return 3
        print(f"[tiers] GATE CHECK PASS: halted {shot.status}@{shot.state}, "
              f"nothing executed")

        # ── Progressive approvals: halt -> approve -> reload -> resume ───
        for gate in ("breakdown", "tier_a", "tier_b", "tier_c"):
            pipeline.record_approval(work_dir, gate)
            shot = pipeline.run_pipeline(
                pipeline.ShotState.load(work_dir / "shot_state.json"),
                work_dir, execute_tier,
            )
            print(f"[tiers] after approving {gate}: "
                  f"{shot.status}@{shot.state}")

        if shot.status != pipeline.STATE_COMPLETE or shot.state != "final":
            print(f"[tiers] FAIL expected complete@final, got "
                  f"{shot.status}@{shot.state}")
            return 4

        # ── Exit evidence ────────────────────────────────────────────────
        transitions = [(h["from"], h["to"]) for h in shot.history
                       if h["to"] != h["from"] and h["from"] is not None]
        expected_chain = [("breakdown", "tier_a"), ("tier_a", "tier_b"),
                          ("tier_b", "tier_c"), ("tier_c", "final")]
        if transitions != expected_chain:
            print(f"[tiers] FAIL transition chain {transitions}")
            return 5
        executed = [h["note"] for h in shot.history
                    if h["note"].startswith("executed:")]
        if sorted(executed) != ["executed:tier_a", "executed:tier_b",
                                "executed:tier_c"]:
            print(f"[tiers] FAIL executed set {executed}")
            return 6
        approvals = sorted(p.name for p in work_dir.glob("approval-*.json"))
        if len(approvals) != 4:
            print(f"[tiers] FAIL approval records {approvals}")
            return 7
        final_png = tmp_dir / "shot_final.png"
        if not final_png.exists():
            print("[tiers] FAIL no final PNG")
            return 8

        print(f"[tiers] approvals: {approvals}")
        print(f"[tiers] final artifact: {final_png.stat().st_size} bytes")
        print("[tiers] PASS: gated tier progression over live operators — "
              "gate blocks without approval, durable resume across reloads, "
              "full breakdown->final chain, three tiers executed exactly once.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
