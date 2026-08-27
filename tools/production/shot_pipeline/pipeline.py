"""Gated tier progression state machine for the shot pipeline (COMP-049).

WO 2026-08-25-008 slice 2 (Decision 2026-08-26T01:45:00Z). States:
breakdown -> tier_a -> tier_b -> tier_c -> final. Shot state persists as a
JSON file carrying the full transition history. Tier escalation is gated:
advancing from a tier requires an explicit director approval record on disk;
without it the machine halts in ``waiting_for_approval`` (not an error).
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Callable, Optional

STATES = ("breakdown", "tier_a", "tier_b", "tier_c", "final")
TIERS = {"tier_a": 640, "tier_b": 1280, "tier_c": 1920}
TIER_HEIGHT = {tier: round(width * 9 / 16) for tier, width in TIERS.items()}

STATE_RUNNING = "running"
STATE_WAITING = "waiting_for_approval"
STATE_FAILED = "failed"
STATE_COMPLETE = "complete"


class ShotState:
    """Durable shot state: current position, status, transition history."""

    MAX_RETRIES = 3

    def __init__(self, shot_id: str, prompt: str):
        self.shot_id = shot_id
        self.prompt = prompt
        self.state = STATES[0]
        self.status = STATE_RUNNING
        self.retries: dict[str, int] = {}
        self.history: list[dict] = [
            {"from": None, "to": self.state, "at": _now(), "note": "breakdown"}
        ]
        self.artifacts: list[dict] = []

    def save(self, path: Path) -> Path:
        payload = {
            "shot_id": self.shot_id,
            "prompt": self.prompt,
            "state": self.state,
            "status": self.status,
            "retries": self.retries,
            "history": self.history,
            "artifacts": self.artifacts,
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        tmp.replace(path)
        return path

    @classmethod
    def load(cls, path: Path) -> "ShotState":
        data = json.loads(path.read_text(encoding="utf-8"))
        shot = cls.__new__(cls)
        shot.shot_id = data["shot_id"]
        shot.prompt = data["prompt"]
        shot.state = data["state"]
        shot.status = data["status"]
        shot.retries = data.get("retries", {})
        shot.history = data["history"]
        shot.artifacts = data.get("artifacts", [])
        return shot


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


class GateBlocked(Exception):
    """Raised when escalation is attempted without a director approval."""


def record_artifact(shot: ShotState, tier: str, path: str, kind: str = "render") -> None:
    """Record a render output artifact path in the shot's artifact list."""
    shot.artifacts.append({
        "tier": tier,
        "path": path,
        "kind": kind,
        "at": _now(),
    })


def approval_path(work_dir: Path, tier: str) -> Path:
    return work_dir / f"approval-{tier}.json"


def record_approval(work_dir: Path, tier: str, approver: str = "director-scripted") -> Path:
    """Write an explicit director approval record for escalating past ``tier``."""
    path = approval_path(work_dir, tier)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(
            {"tier": tier, "approved_by": approver, "at": _now()}, indent=2
        ),
        encoding="utf-8",
    )
    tmp.replace(path)
    return path


def require_approval(work_dir: Path, tier: str) -> None:
    """Gate check: escalate past ``tier`` only with an approval record."""
    if not approval_path(work_dir, tier).exists():
        raise GateBlocked(f"no director approval for {tier}")


def advance(shot: ShotState, work_dir: Path) -> str:
    """Advance one gated step; returns the new state.

    Raises GateBlocked (shot left in waiting_for_approval) or RuntimeError
    (final already reached). Caller executes the tier's operator between
    entering a tier and escalating out of it.
    """
    idx = STATES.index(shot.state)
    if shot.state == "final":
        raise RuntimeError("shot already final")
    tier = shot.state
    try:
        require_approval(work_dir, tier)
    except GateBlocked:
        shot.status = STATE_WAITING
        raise
    nxt = STATES[idx + 1]
    shot.history.append({"from": tier, "to": nxt, "at": _now(), "note": f"gate:{tier} approved"})
    shot.state = nxt
    shot.status = STATE_RUNNING
    return nxt


def fail(shot: ShotState, note: str) -> None:
    shot.status = STATE_FAILED
    shot.history.append({"from": shot.state, "to": shot.state, "at": _now(),
                         "note": f"failed: {note}"})


def _tier_executed(shot: ShotState, tier: str) -> bool:
    return any(h["note"].startswith(f"executed:{tier}") for h in shot.history)


class TierRejected(Exception):
    """Critic rejected a tier's output (distinct from operator crashes)."""


def _critic_passed(verdict: dict, score_threshold: float) -> bool:
    if verdict.get("escalation_needed"):
        return False
    score = verdict.get("composition_score")
    return score is None or score >= score_threshold


def run_pipeline(
    shot: ShotState,
    work_dir: Path,
    execute_tier: Callable[[str, int, int], dict],
    critic: Optional[Callable[[str, dict], dict]] = None,
    critic_score_threshold: float = 0.5,
) -> ShotState:
    """Drive a shot as far toward final as the current approvals allow.

    ``execute_tier(tier, width, height)`` runs the live operators for one tier
    and returns its result dict. When ``critic`` is provided it receives
    ``(tier, result)`` and must return a critique dict; rejection withholds
    the executed marker, increments the persisted retry count, and re-executes
    only that tier. Operator exceptions count toward the same retry budget;
    the MAX_RETRIES-th failure halts the shot as ``failed`` (saved) and raises.
    """
    while True:
        if shot.state == "final":
            break
        tier = shot.state
        if tier in TIERS and not _tier_executed(shot, tier):
            width, height = TIERS[tier], TIER_HEIGHT[tier]
            try:
                result = execute_tier(tier, width, height)
            except Exception as exc:  # noqa: BLE001 — counted retry, not instant halt
                shot.retries[tier] = shot.retries.get(tier, 0) + 1
                note = f"operator-rejected:{tier} attempt {shot.retries[tier]}"
                shot.history.append({"from": tier, "to": tier, "at": _now(),
                                     "note": note})
                if shot.retries[tier] >= ShotState.MAX_RETRIES:
                    fail(shot, f"{tier}: max retries after operator error: {exc}")
                    shot.save(work_dir / "shot_state.json")
                    raise
                shot.save(work_dir / "shot_state.json")
                continue
            if critic is not None:
                try:
                    verdict = critic(tier, result)
                    passed = _critic_passed(verdict, critic_score_threshold)
                except Exception as exc:  # noqa: BLE001 — critic failure counts as retry
                    passed = False
                    verdict = {"error": str(exc)}
                if not passed:
                    shot.retries[tier] = shot.retries.get(tier, 0) + 1
                    note = (f"critic-rejected:{tier} "
                            f"attempt {shot.retries[tier]}")
                    if verdict.get("error"):
                        note += f" error={verdict['error']}"
                    shot.history.append({"from": tier, "to": tier,
                                         "at": _now(), "note": note})
                    if shot.retries[tier] >= ShotState.MAX_RETRIES:
                        fail(shot, f"{tier}: max retries after critic rejection")
                        shot.save(work_dir / "shot_state.json")
                        raise RuntimeError(
                            f"{tier}: max retries ({ShotState.MAX_RETRIES}) "
                            f"after critic rejection"
                        )
                    shot.save(work_dir / "shot_state.json")
                    continue
            shot.history.append({"from": tier, "to": tier, "at": _now(),
                                 "note": f"executed:{tier}"})
        try:
            advance(shot, work_dir)
        except GateBlocked:
            shot.save(work_dir / "shot_state.json")
            return shot
    shot.status = STATE_COMPLETE
    shot.history.append({"from": "final", "to": "final", "at": _now(),
                         "note": "pipeline complete"})
    shot.save(work_dir / "shot_state.json")
    return shot
