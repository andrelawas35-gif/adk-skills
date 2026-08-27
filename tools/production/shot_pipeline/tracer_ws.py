"""Slice 3 tracer: durable shot state in a real Shot Work Object (COMP-049).

WO 2026-08-25-008 slice 3. Drives the accepted gated tier progression while a
StateSync mirrors every step into Shot WO 2026-08-25-009 via the public
``ws`` CLI. Risk under test: pipeline <-> real WO frontmatter sync with
optimistic concurrency intact and ``ws validate`` never regressing.

Tiers A and B use a fast fake executor (operators proven twice in slices 1-2);
tier C runs LIVE through Blender to prove composition with the WO attached.
"""

import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(REPO / "tools" / "production"))
from gpu_orchestrator import registry as gpu_registry  # noqa: E402
from scene_planner.planner import plan_scene  # noqa: E402
from shot_pipeline import pipeline  # noqa: E402
from shot_pipeline.sync import StateSync, SyncError  # noqa: E402
from shot_pipeline.tracer import (  # noqa: E402
    _tiny_obj,
    _fixture_registry,
    scene_plan_to_commands,
)

SHOT_WO_ID = "2026-08-25-009"


def _fake_tier(tier: str, width: int, height: int) -> dict:
    print(f"  [{tier}] fake execute at {width}x{height}")
    return {"fake": True}


def main() -> int:
    prompt = "A lone hero stands in a vast desert at dusk"
    sync = StateSync(SHOT_WO_ID)

    # Baseline ws validate error count before any pipeline writes.
    # First call only MEASURES (huge ceiling); later calls regress-check.
    baseline = sync.validate(10**9)
    print(f"[ws-sync] validate baseline errors: {baseline}")

    # ── Negative 1: invalid enum rejected by the CLI ────────────────────
    try:
        sync._transition_status("not-a-status")
        print("[ws-sync] FAIL invalid status accepted")
        return 2
    except SyncError as exc:
        assert ("Invalid shot status" in str(exc)
                or "invalid choice" in str(exc)), exc
        print("[ws-sync] NEG1 PASS: invalid enum rejected")

    # ── Negative 2: stale expect-updated hits the concurrency guard ─────
    stale = sync._updated_at
    sync._updated_at = "2000-01-01T00:00:00Z"
    try:
        sync._transition_status("blocking")
        print("[ws-sync] FAIL stale timestamp accepted")
        return 3
    except SyncError as exc:
        assert "Concurrent write detected" in str(exc) or "Expected updated_at" in str(exc), exc
        print("[ws-sync] NEG2 PASS: stale updated_at rejected by guard")
    sync._updated_at = sync._read_updated_at()

    # ── Gated progression with real WO sync ─────────────────────────────
    work_dir = Path(tempfile.mkdtemp(prefix="ws-shot-ws-sync-"))
    shot = pipeline.ShotState("SH004", prompt)
    live_done = {"ran": False}

    def execute_tier(tier: str, width: int, height: int) -> dict:
        if tier == "tier_c":
            result = _live_blender_tier(tier, width, height)
            live_done["ran"] = True
            return result
        return _fake_tier(tier, width, height)

    approvals = ("breakdown", "tier_a", "tier_b", "tier_c")
    for gate in range(len(approvals) + 1):
        if gate > 0:
            pipeline.record_approval(work_dir, approvals[gate - 1])
        shot = pipeline.run_pipeline(
            pipeline.ShotState.load(work_dir / "shot_state.json")
            if (work_dir / "shot_state.json").exists() else shot,
            work_dir, execute_tier,
        )
        # Sync every executed tier into the WO as soon as it appears in history.
        for h in shot.history:
            if h["note"].startswith("executed:"):
                tier = h["note"].split(":", 1)[1]
                info = sync.on_tier_executed(tier)
                print(f"[ws-sync] {info}")
                sync.validate(baseline)
        if shot.status == pipeline.STATE_WAITING:
            continue
        break

    if not live_done["ran"]:
        print("[ws-sync] FAIL live tier never ran")
        return 4
    if shot.status != pipeline.STATE_COMPLETE or shot.state != "final":
        print(f"[ws-sync] FAIL end state {shot.status}@{shot.state}")
        return 5

    result = sync.on_complete()
    print(f"[ws-sync] {result}")
    sync.validate(baseline)

    # ── Exit evidence from the WO itself ────────────────────────────────
    content = sync._wo_path().read_text(encoding="utf-8")
    import re
    fm = dict(re.findall(r"(?m)^([a-z_]+):\s*(.+)$", content))
    print(f"[ws-sync] final frontmatter: shot_status={fm.get('shot_status')} "
          f"shot_tier={fm.get('shot_tier')}")
    if fm.get("shot_status") != "approved" or fm.get("shot_tier") != "final":
        print("[ws-sync] FAIL frontmatter did not reach approved/final")
        return 6
    history_hits = len(re.findall(r"(?m)^### .*Shot status:", content))
    print(f"[ws-sync] Shot status History entries: {history_hits}")
    if history_hits < 5:
        print("[ws-sync] FAIL expected >=5 status History entries "
              "(blocking, render, review, approved)")
        return 7

    print(f"[ws-sync] PASS: durable shot state — pipeline drove {SHOT_WO_ID} "
          f"to shot_status=approved / shot_tier=final via ws tooling; "
          f"validate never regressed; concurrency guard enforced.")
    return 0


def _live_blender_tier(tier: str, width: int, height: int) -> dict:
    import os
    import subprocess
    import time
    from blender_operator import queue
    from shot_pipeline.tracer import BLENDER_EXE, ADDON, _wait_for_result

    with tempfile.TemporaryDirectory(prefix=f"ws-tier-{tier}-") as tmp:
        tmp_dir = Path(tmp)
        obj_path = tmp_dir / "figure.obj"
        _tiny_obj(obj_path)
        registry_path = _fixture_registry(tmp_dir, obj_path)
        plan = plan_scene("A lone hero stands in a vast desert at dusk", registry_path)
        commands = scene_plan_to_commands(plan)

        queue_dir = tmp_dir / "queue"
        gpu_dir = tmp_dir / "gpu"
        queue_dir.mkdir()
        gpu_dir.mkdir()
        env = dict(os.environ)
        env["QUEUE_DIR"] = str(queue_dir)
        env["GPU_REGISTRY_DIR"] = str(gpu_dir)
        proc = subprocess.Popen(
            [str(BLENDER_EXE), "--background", "--factory-startup",
             "--python", str(ADDON),
             "--", "--queue-dir", str(queue_dir), "--session-id", f"sync-{tier}"],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(6.0)
        try:
            seq = 0
            image_path = tmp_dir / f"{tier}.png"
            ops = [
                (op, dict(params, width=width, height=height)
                 if op == "render.preview" else params)
                for op, params in commands
            ]
            ops.append(("render.final", {"filepath": str(image_path), "format": "PNG"}))
            for op, params in ops:
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
            if not image_path.exists():
                raise RuntimeError(f"{tier}: no capture on disk")
        finally:
            proc.kill()
            proc.wait(timeout=10)
    return {"live": True, "image": image_path}


if __name__ == "__main__":
    sys.exit(main())
