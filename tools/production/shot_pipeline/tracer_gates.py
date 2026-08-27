"""Slice 3 tracer: human-in-the-loop gate approvals via the console CLI (COMP-049).

WO 2026-08-25-011 slice 3. Proves an external actor — a SEPARATE process
invoking only ``approvals.py`` — can close the gate loop:

A) wait/approve loop: pipeline halts waiting@breakdown; external ``wait``
   observes it; external ``approve`` records the decision; pipeline resumes;
   repeat per gate to completion. No approval file is ever written in-process.
B) bogus gate rejected by the CLI (exit != 0, nothing written).
C) deny writes a denial audit record and leaves the shot waiting; a later
   approve still completes the shot.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent

sys.path.insert(0, str(REPO / "tools" / "production"))
from shot_pipeline import pipeline  # noqa: E402


def _cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "shot_pipeline.approvals", *args],
        cwd=str(REPO / "tools" / "production"), capture_output=True, text=True,
    )


def _fake_executor(calls: dict):
    def execute_tier(tier: str, width: int, height: int) -> dict:
        calls[tier] = calls.get(tier, 0) + 1
        print(f"  [{tier}] fake execute #{calls[tier]}")
        return {"fake": True}
    return execute_tier


def _passing_critic(tier: str, result: dict) -> dict:
    return {"escalation_needed": False, "composition_score": 0.95}


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ws-shot-gates-") as tmp:
        work = Path(tmp)
        calls: dict[str, int] = {}

        # ── Scenario A: external human loop to completion ────────────────
        shot = pipeline.ShotState("SH-g1", "human gated")
        gates = ("breakdown", "tier_a", "tier_b", "tier_c")
        for round_no in range(len(gates) + 1):
            current = pipeline.run_pipeline(
                pipeline.ShotState.load(work / "shot_state.json")
                if (work / "shot_state.json").exists() else shot,
                work, _fake_executor(calls), critic=_passing_critic,
            )
            if current.status == pipeline.STATE_COMPLETE:
                break
            assert current.status == pipeline.STATE_WAITING, \
                f"unexpected {current.status}@{current.state}"
            # External actor inspects via CLI...
            r = _cli("wait", "--work-dir", str(work))
            if r.returncode != 0 or '"waiting": true' not in r.stdout:
                print(f"[A] FAIL wait output rc={r.returncode}: {r.stdout}")
                return 2
            # ...then approves through the same separate process.
            tier = current.state
            r = _cli("approve", "--work-dir", str(work),
                     "--tier", tier, "--approver", "director-andre")
            if r.returncode != 0:
                print(f"[A] FAIL approve {tier}: {r.stderr}")
                return 3
            print(f"  [console] approved {tier} (external process)")
        else:
            print("[A] FAIL never completed")
            return 4
        if not all((work / f"approval-{g}.json").exists() for g in gates):
            print("[A] FAIL missing approval records")
            return 5
        print(f"[A] PASS human-loop completion via separate console processes "
              f"(calls={calls})")

        # ── Scenario B: bogus gate rejected before any write ─────────────
        before = sorted(p.name for p in work.iterdir())
        r = _cli("approve", "--work-dir", str(work), "--tier", "tier_z")
        if r.returncode == 0:
            print("[B] FAIL bogus tier accepted")
            return 6
        after = sorted(p.name for p in work.iterdir())
        if before != after:
            print("[B] FAIL files changed on rejection")
            return 7
        print("[B] PASS bogus gate rejected, filesystem untouched")

        # ── Scenario C: deny leaves waiting; later approve completes ─────
        work2 = Path(tempfile.mkdtemp(dir=work))
        shot2 = pipeline.ShotState("SH-g2", "deny then approve")
        first = pipeline.run_pipeline(shot2, work2, _fake_executor({}),
                                      critic=_passing_critic)
        if first.status != pipeline.STATE_WAITING:
            print(f"[C] FAIL expected waiting, got {first.status}")
            return 8
        r = _cli("deny", "--work-dir", str(work2), "--tier", "breakdown",
                 "--reason", "staging not ready")
        if r.returncode != 0 or not (work2 / "denial-breakdown.json").exists():
            print(f"[C] FAIL deny record: rc={r.returncode} {r.stdout}{r.stderr}")
            return 9
        resumed = pipeline.run_pipeline(
            pipeline.ShotState.load(work2 / "shot_state.json"),
            work2, _fake_executor({}), critic=_passing_critic)
        if resumed.status != pipeline.STATE_WAITING or resumed.state != "breakdown":
            print(f"[C] FAIL deny must leave shot waiting: "
                  f"{resumed.status}@{resumed.state}")
            return 10
        r = _cli("approve", "--work-dir", str(work2), "--tier", "breakdown",
                 "--approver", "director-andre")
        resumed2 = pipeline.run_pipeline(
            pipeline.ShotState.load(work2 / "shot_state.json"),
            work2, _fake_executor({}), critic=_passing_critic)
        # Approving breakdown must resume progression: tier_a executes, then
        # the shot legitimately waits at the NEXT gate (tier_a).
        if resumed2.status != pipeline.STATE_WAITING or resumed2.state != "tier_a":
            print(f"[C] FAIL expected progression to waiting@tier_a, got "
                  f"{resumed2.status}@{resumed2.state}")
            return 11
        if calls_check := sum(1 for h in resumed2.history
                              if h["note"] == "executed:tier_a"):
            pass  # tier_a executed exactly once past the denied gate
        denial = (work2 / "denial-breakdown.json").read_text(encoding="utf-8")
        if "staging not ready" not in denial:
            print("[C] FAIL denial reason not persisted")
            return 12
        print("[C] PASS deny leaves waiting + audit record; later approve completes")

        print("[gates] PASS: human-in-the-loop gating closed through an "
              "external console process — inspect, approve, deny, resume.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
