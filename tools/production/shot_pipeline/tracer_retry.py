"""Slice 1 tracer: critic-gated retries with persisted counters (COMP-049).

WO 2026-08-25-011 Decision 2. Proves, in durable reloaded state:
A) fail-fail-pass — two critic rejections of tier_a then a pass; retries["tier_a"]
   survives gate-wait reloads; every tier ends executed exactly once.
B) max-retry halt — three consecutive rejections halt status=failed with
   retries["tier_a"]==3, state unchanged at tier_a.
C) live composition — tier_c runs through real Blender and passes the REAL
   (simulated-keyword) critic adapter on its actual PNG.
"""

import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(REPO / "tools" / "production"))
from shot_pipeline import pipeline  # noqa: E402


def _critic_script(rejections_left: dict[str, int]):
    """Critic that rejects a tier while its rejection budget lasts."""
    def critic(tier: str, result: dict) -> dict:
        if rejections_left.get(tier, 0) > 0:
            rejections_left[tier] -= 1
            return {"escalation_needed": True,
                    "composition_score": 0.2,
                    "note": f"scripted reject ({rejections_left.get(tier, 0)} left)"}
        return {"escalation_needed": False, "composition_score": 0.9}
    return critic


def _fake_executor(calls: dict[str, int]):
    def execute_tier(tier: str, width: int, height: int) -> dict:
        calls[tier] = calls.get(tier, 0) + 1
        print(f"  [{tier}] fake execute #{calls[tier]} at {width}x{height}")
        return {"fake": True}
    return execute_tier


def _drive(shot, work_dir, executor, critic):
    """Progressive approvals until terminal state (complete or failed)."""
    gates = ("breakdown", "tier_a", "tier_b", "tier_c")
    while True:
        try:
            current = pipeline.run_pipeline(
                pipeline.ShotState.load(work_dir / "shot_state.json")
                if (work_dir / "shot_state.json").exists() else shot,
                work_dir, executor, critic=critic,
            )
        except RuntimeError:
            # Max-retry halt: reload durable failed state for inspection.
            return pipeline.ShotState.load(work_dir / "shot_state.json")
        if current.status != pipeline.STATE_WAITING:
            return current
        # Approve the next missing gate and resume.
        for g in gates:
            if not (work_dir / f"approval-{g}.json").exists():
                pipeline.record_approval(work_dir, g)
                break
        else:
            return current  # all approved but still waiting — abnormal


def scenario_retry_then_pass() -> int:
    work = Path(tempfile.mkdtemp(prefix="ws-retry-pass-"))
    rejections = {"tier_a": 2}
    calls: dict[str, int] = {}
    shot = _drive(pipeline.ShotState("SH-r1", "retry then pass"),
                  work, _fake_executor(calls), _critic_script(dict(rejections)))
    if shot.status != pipeline.STATE_COMPLETE or shot.state != "final":
        print(f"[A] FAIL end {shot.status}@{shot.state}")
        return 2
    loaded = pipeline.ShotState.load(work / "shot_state.json")
    if loaded.retries.get("tier_a") != 2:
        print(f"[A] FAIL persisted retries {loaded.retries}")
        return 3
    rejects = [h for h in loaded.history
               if h["note"].startswith("critic-rejected:tier_a")]
    if len(rejects) != 2:
        print(f"[A] FAIL rejection notes {len(rejects)}")
        return 4
    for t in ("tier_a", "tier_b", "tier_c"):
        n = sum(1 for h in loaded.history if h["note"] == f"executed:{t}")
        if n != 1 or calls.get(t, 0) < 1:
            print(f"[A] FAIL tier {t}: marker x{n}, calls {calls.get(t)}")
            return 5
    if calls["tier_a"] != 3:
        print(f"[A] FAIL tier_a executions {calls['tier_a']} != 3")
        return 6
    print(f"[A] PASS fail-fail-pass: retries={loaded.retries}, "
          f"tier_a executed once after 3 attempts, complete@final")
    return 0


def scenario_max_retry_halt() -> int:
    work = Path(tempfile.mkdtemp(prefix="ws-retry-max-"))
    always_reject = _critic_script({"tier_a": 99})
    shot = _drive(pipeline.ShotState("SH-r2", "always rejected"),
                  work, _fake_executor({}), always_reject)
    if shot.status != pipeline.STATE_FAILED or shot.state != "tier_a":
        print(f"[B] FAIL expected failed@tier_a, got {shot.status}@{shot.state}")
        return 7
    loaded = pipeline.ShotState.load(work / "shot_state.json")
    if loaded.retries.get("tier_a") != 3:
        print(f"[B] FAIL retry count {loaded.retries}")
        return 8
    if any(h["note"].startswith("executed:") for h in loaded.history):
        print("[B] FAIL executed marker present despite rejection")
        return 9
    print(f"[B] PASS max-retry halt: status=failed, "
          f"retries={loaded.retries}, no executed markers, saved durably")
    return 0


def scenario_live_critic() -> int:
    from shot_pipeline.tracer_ws import _live_blender_tier

    import importlib.util
    critic_file = (REPO / "skills" / "core" / "production-operate-visual-critic"
                   / "tracer_bullet.py")
    spec = importlib.util.spec_from_file_location("vc", critic_file)
    vc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vc)

    def critic(tier: str, result: dict) -> dict:
        if "image" not in result:  # fake tiers carry no render to critique
            return {"escalation_needed": False, "composition_score": 1.0,
                    "note": "no image (fake tier)"}
        verdict = vc.visual_critique_for_image(
            result["image"], "A lone hero stands in a vast desert at dusk")
        print(f"  [critic/{tier}] score={verdict['composition_score']} "
              f"escalation={verdict['escalation_needed']}")
        return verdict

    calls: dict[str, int] = {}
    work = Path(tempfile.mkdtemp(prefix="ws-retry-live-"))
    rejections: dict[str, int] = {}

    def executor(tier: str, width: int, height: int) -> dict:
        if tier == "tier_c":
            return _live_blender_tier(tier, width, height)
        return _fake_executor(calls)(tier, width, height)

    shot = _drive(pipeline.ShotState("SH-r3", "live tier c"), work, executor, critic)
    if shot.status != pipeline.STATE_COMPLETE or shot.state != "final":
        print(f"[C] FAIL end {shot.status}@{shot.state}")
        return 10
    loaded = pipeline.ShotState.load(work / "shot_state.json")
    if loaded.retries:
        print(f"[C] FAIL unexpected retries {loaded.retries}")
        return 11
    print("[C] PASS live composition: Blender-rendered tier_c passed the real "
          "critic adapter on first attempt, complete@final")
    return 0


if __name__ == "__main__":
    rc = scenario_retry_then_pass()
    if rc:
        sys.exit(rc)
    rc = scenario_max_retry_halt()
    if rc:
        sys.exit(rc)
    rc = scenario_live_critic()
    sys.exit(rc)
