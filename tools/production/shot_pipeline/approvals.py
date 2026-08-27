"""Human approval console for gated shot escalations (COMP-049).

WO 2026-08-25-011 slice 3. A terminal surface a director uses from any shell:
inspect shots waiting on a gate decision, approve escalation past a tier
(writes exactly the same durable approval record ``pipeline.record_approval``
writes), or deny with a reason (writes a denial audit record and leaves the
shot waiting). Deliberately process-local: the console never touches pipeline
memory, only files — the same boundary a web console would sit behind.

WO 2026-08-25-018 slice 1: the ``status_payload`` / ``approve_gate`` /
``deny_gate`` helpers are extracted so the Director Console bridge can import
the exact same logic instead of copying it — byte-compatible records become a
structural property, not a promise.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from shot_pipeline import pipeline

GATES = ("breakdown", "tier_a", "tier_b", "tier_c")


class ApprovalError(Exception):
    """Invalid gate operation (unknown gate, tier/state mismatch, bad status)."""


def status_payload(work_dir: Path) -> dict:
    """Inspect a shot's gate position. Raises FileNotFoundError if absent."""
    path = work_dir / "shot_state.json"
    if not path.exists():
        raise FileNotFoundError(f"no shot_state.json under {work_dir}")
    shot = pipeline.ShotState.load(path)
    waiting = shot.status == pipeline.STATE_WAITING
    records = sorted(p.name for p in work_dir.iterdir()
                     if p.suffix == ".json"
                     and p.name.startswith(("approval-", "denial-")))
    return {
        "shot_id": shot.shot_id,
        "state": shot.state,
        "status": shot.status,
        "waiting": waiting,
        "retries": shot.retries,
        "pending_gate": shot.state if waiting else None,
        "records": records,
    }


def approve_gate(work_dir: Path, tier: str, approver: str = "director") -> Path:
    """Record an approval past ``tier`` via pipeline.record_approval."""
    if tier not in GATES:
        raise ApprovalError(
            f"unknown gate {tier!r}; valid gates: {', '.join(GATES)}")
    path = work_dir / "shot_state.json"
    if not path.exists():
        raise FileNotFoundError(f"no shot_state.json under {work_dir}")
    shot = pipeline.ShotState.load(path)
    if tier != shot.state:
        raise ApprovalError(
            f"shot {shot.shot_id} is at {shot.state}, not waiting at {tier}")
    if shot.status != pipeline.STATE_WAITING:
        raise ApprovalError(
            f"shot {shot.shot_id} is {shot.status}, not waiting_for_approval")
    return pipeline.record_approval(work_dir, tier, approver=approver)


def deny_gate(work_dir: Path, tier: str, reason: str = "unspecified",
              approver: str = "director") -> Path:
    """Write a denial audit record; leaves shot state untouched by design."""
    if tier not in GATES:
        raise ApprovalError(
            f"unknown gate {tier!r}; valid gates: {', '.join(GATES)}")
    path = work_dir / "shot_state.json"
    if not path.exists():
        raise FileNotFoundError(f"no shot_state.json under {work_dir}")
    shot = pipeline.ShotState.load(path)
    out = work_dir / f"denial-{tier}.json"
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps({
        "tier": tier,
        "shot_id": shot.shot_id,
        "denied_by": approver,
        "reason": reason,
    }, indent=2), encoding="utf-8")
    tmp.replace(out)
    # Denial leaves the shot waiting by design: no state mutation.
    return out


def _load_state(work_dir: Path) -> pipeline.ShotState:
    path = work_dir / "shot_state.json"
    if not path.exists():
        raise SystemExit(f"error: no shot_state.json under {work_dir}")
    return pipeline.ShotState.load(path)


def cmd_wait(args: argparse.Namespace) -> int:
    try:
        payload = status_payload(args.work_dir)
    except FileNotFoundError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(json.dumps(payload, indent=2))
    return 0


def cmd_approve(args: argparse.Namespace) -> int:
    try:
        path = approve_gate(args.work_dir, args.tier, approver=args.approver)
    except FileNotFoundError as exc:
        raise SystemExit(f"error: {exc}") from exc
    except ApprovalError as exc:
        raise SystemExit(f"error: {exc}") from exc
    shot = _load_state(args.work_dir)
    print(f"approved {args.tier} for {shot.shot_id} -> {path.name}")
    return 0


def cmd_deny(args: argparse.Namespace) -> int:
    try:
        out = deny_gate(args.work_dir, args.tier, reason=args.reason,
                        approver=args.approver)
    except FileNotFoundError as exc:
        raise SystemExit(f"error: {exc}") from exc
    except ApprovalError as exc:
        raise SystemExit(f"error: {exc}") from exc
    shot = _load_state(args.work_dir)
    print(f"denied {args.tier} for {shot.shot_id} -> {out.name} "
          f"(shot remains {shot.status})")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="shot-approvals")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("wait", "approve", "deny"):
        p = sub.add_parser(name)
        p.add_argument("--work-dir", required=True, type=Path)

    sub.choices["approve"].add_argument("--tier", required=True)
    sub.choices["approve"].add_argument("--approver", default="director")

    sub.choices["deny"].add_argument("--tier", required=True)
    sub.choices["deny"].add_argument("--approver", default="director")
    sub.choices["deny"].add_argument("--reason", default="unspecified")

    args = parser.parse_args(argv)
    return {"wait": cmd_wait, "approve": cmd_approve, "deny": cmd_deny}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
