"""Slice 1 tracer: gate decisions through the Director Console bridge (COMP-049).

WO 2026-08-25-018 slice 1. Proves the riskiest assumption: a decision
originating in DirectorConsoleBridge — not the CLI — produces a record a
SEPARATE pipeline process observes and acts on:

A) subprocess run_pipeline halts waiting@breakdown; bridge.approve_gate
   writes the record; a SECOND subprocess resumes into tier_a's own
   legitimate gate; console-written record is structurally identical to one
   written directly by pipeline.record_approval.
B) bridge.deny_gate writes the denial audit record and leaves the shot
   untouched at waiting@breakdown.
C) bridge.approve_gate on a wrong tier returns ok:false with zero
   filesystem change; gate_status on an empty dir returns a structured
   error rather than raising.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent
PROD = REPO / "tools" / "production"

sys.path.insert(0, str(PROD))
from shot_pipeline import pipeline  # noqa: E402

sys.path.insert(0, str(REPO))
from director_console.bridge import DirectorConsoleBridge  # noqa: E402

RUNNER = """
import sys
from pathlib import Path
prod = Path(sys.argv[1])
work = Path(sys.argv[2])
sys.path.insert(0, str(prod))
from shot_pipeline import pipeline


def execute(tier, width, height):
    return {"fake": True}


def critic(tier, result):
    return {"escalation_needed": False, "composition_score": 0.95}


state_path = work / "shot_state.json"
shot = (pipeline.ShotState.load(state_path) if state_path.exists()
        else pipeline.ShotState("SH-cg", "console gated"))
result = pipeline.run_pipeline(shot, work, execute, critic=critic)
print(f"{result.status}@{result.state}")
"""


def _pipeline_process(work: Path) -> str:
    r = subprocess.run(
        [sys.executable, "-c", RUNNER, str(PROD), str(work)],
        capture_output=True, text=True, cwd=str(REPO),
    )
    if r.returncode != 0:
        raise AssertionError(f"pipeline process failed: {r.stderr}")
    return r.stdout.strip().splitlines()[-1]


def main() -> int:
    bridge = DirectorConsoleBridge()

    with tempfile.TemporaryDirectory(prefix="ws-console-gate-") as tmp:
        # ── Scenario A: bridge approve observed by external process ──────
        work_a = Path(tmp) / "A"
        work_a.mkdir()
        first = _pipeline_process(work_a)
        if first != "waiting_for_approval@breakdown":
            print(f"[A] FAIL expected waiting@breakdown, got {first}")
            return 2
        response = bridge.approve_gate(str(work_a), "breakdown",
                                       approver="director-andre")
        if not response["ok"]:
            print(f"[A] FAIL approve_gate rejected: {response['error']}")
            return 3
        second = _pipeline_process(work_a)
        if second != "waiting_for_approval@tier_a":
            print(f"[A] FAIL expected progression to tier_a gate, got {second}")
            return 4

        # Structural byte-compatibility vs direct record_approval output.
        reference_dir = work_a / "_reference"
        reference_dir.mkdir()
        pipeline.record_approval(reference_dir, "breakdown",
                                 approver="director-andre")
        console_rec = json.loads(
            (work_a / "approval-breakdown.json").read_text(encoding="utf-8"))
        reference_rec = json.loads(
            (reference_dir / "approval-breakdown.json").read_text(encoding="utf-8"))
        for rec in (console_rec, reference_rec):
            rec.pop("at")  # timestamp necessarily differs between writes
        if set(console_rec) != {"tier", "approved_by"} or console_rec != reference_rec:
            print(f"[A] FAIL record contract mismatch: {console_rec} vs {reference_rec}")
            return 5
        raw_console = (work_a / "approval-breakdown.json").read_text(encoding="utf-8")
        if '  "approved_by"' not in raw_console:
            print("[A] FAIL formatting diverges from record_approval output")
            return 6
        print("[A] PASS bridge approve resumed external pipeline "
              "(breakdown -> tier_a gate); records contract-compatible")

        # ── Scenario B: bridge deny leaves shot untouched ─────────────────
        work_b = Path(tmp) / "B"
        work_b.mkdir()
        halted = _pipeline_process(work_b)
        if halted != "waiting_for_approval@breakdown":
            print(f"[B] FAIL setup: got {halted}")
            return 7
        before_state = (work_b / "shot_state.json").read_text(encoding="utf-8")
        response = bridge.deny_gate(str(work_b), "breakdown",
                                    reason="staging not ready",
                                    approver="director-andre")
        if not response["ok"] or not (work_b / "denial-breakdown.json").exists():
            print(f"[B] FAIL denial record missing: {response}")
            return 8
        denial = json.loads(
            (work_b / "denial-breakdown.json").read_text(encoding="utf-8"))
        if (denial["reason"] != "staging not ready" or denial["tier"] != "breakdown"):
            print(f"[B] FAIL denial payload wrong: {denial}")
            return 9
        if (work_b / "shot_state.json").read_text(encoding="utf-8") != before_state:
            print("[B] FAIL deny mutated shot state")
            return 10
        after = _pipeline_process(work_b)
        if after != "waiting_for_approval@breakdown":
            print(f"[B] FAIL denied shot must stay waiting: {after}")
            return 11
        print("[B] PASS bridge deny wrote audit record, left shot waiting")

        # ── Scenario C: wrong-tier rejection pre-write + clean status error ─
        snapshot = sorted(p.name for p in work_b.iterdir())
        response = bridge.approve_gate(str(work_b), "tier_c")
        if response["ok"] or "not waiting at" not in response["error"]["message"]:
            print(f"[C] FAIL wrong-tier approve accepted: {response}")
            return 12
        if sorted(p.name for p in work_b.iterdir()) != snapshot:
            print("[C] FAIL filesystem changed on rejection")
            return 13
        probe = bridge.gate_status(str(Path(tmp) / "does-not-exist"))
        if probe["ok"] or probe["error"]["code"] != "FileNotFoundError":
            print(f"[C] FAIL missing-dir status not structured: {probe}")
            return 14
        print("[C] PASS wrong-tier rejected pre-write; "
              "missing dir returns structured error")

    print("[console-gate] PASS: Director Console bridge closes a live gate "
          "across a process boundary with contract-identical records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
