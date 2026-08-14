"""Read-only orchestration tracer (WO 2026-08-14-008, Decision 3).

Proves the shape named in docs/adr/0025-canonical-runtime-truth-boundary-and-single-writer-rule.md
without adopting any orchestrator: load one Work Object, validate it through
the real `python3 -m tools.ws validate` path, stream events, halt for a
human decision, resume from the answer. Writes nothing to `.work-studio/` --
the runtime is a non-writer of canonical state by construction (ADR 0025's
single-writer rule). Stdlib only; no new dependencies.

Usage:
    python3 -m tools.runtime.tracer <work-object-id>

Exit criteria (Decision 3): the target Work Object's `updated_at` must be
byte-identical before and after the run. Check with:
    git diff --stat -- .work-studio/objects   (tracked files only)
or by re-reading the file's `updated_at` field before and after the run --
this script prints both so the comparison needs no extra tooling.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _find_repo_root() -> Path:
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent."
    )


def _find_work_object(repo_root: Path, wo_id: str) -> Path:
    objects_dir = repo_root / ".work-studio" / "objects"
    matches = sorted(objects_dir.glob(f"*/*/{wo_id}-*.md"))
    if not matches:
        raise FileNotFoundError(f"No Work Object found for id {wo_id!r} under {objects_dir}")
    if len(matches) > 1:
        raise RuntimeError(f"Ambiguous id {wo_id!r}: {matches}")
    return matches[0]


def _read_updated_at(file_path: Path) -> str:
    text = file_path.read_text()
    match = re.search(r"^updated_at:\s*(\S+)", text, re.MULTILINE)
    return match.group(1) if match else "<not found>"


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


class EventLog:
    """Appends one JSON line per event to a gitignored trace file."""

    def __init__(self, trace_path: Path):
        self.trace_path = trace_path
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = open(self.trace_path, "a", encoding="utf-8")

    def emit(self, event: str, **fields) -> None:
        record = {"event": event, "ts": datetime.now(timezone.utc).isoformat()}
        record.update(fields)
        line = json.dumps(record, sort_keys=True)
        self._fh.write(line + "\n")
        self._fh.flush()
        print(line)

    def close(self) -> None:
        self._fh.close()


def run(wo_id: str) -> int:
    repo_root = _find_repo_root()
    trace_path = repo_root / "runtime" / "traces" / f"{_timestamp()}-{wo_id}.jsonl"
    log = EventLog(trace_path)

    try:
        # 1. Load -- read-only.
        try:
            wo_path = _find_work_object(repo_root, wo_id)
        except (FileNotFoundError, RuntimeError) as e:
            log.emit("failed", stage="load", error=str(e))
            return 1

        updated_at_before = _read_updated_at(wo_path)
        log.emit("load", work_object=wo_id, path=str(wo_path.relative_to(repo_root)),
                  updated_at_before=updated_at_before)

        # 2. Validate -- the real path: invoke `python3 -m tools.ws validate`.
        result = subprocess.run(
            [sys.executable, "-m", "tools.ws", "validate", "--files", str(wo_path)],
            cwd=repo_root, capture_output=True, text=True,
        )
        validate_passed = result.returncode == 0
        log.emit(
            "validate", work_object=wo_id, passed=validate_passed,
            returncode=result.returncode,
            stdout_tail=result.stdout.strip().splitlines()[-5:],
        )
        if not validate_passed:
            log.emit("failed", stage="validate", reason="ws validate reported errors")
            return 1

        # 3. Interrupt -- halt and surface the decision to a human. This
        # process makes no decision; it stops and waits.
        log.emit("interrupt", work_object=wo_id,
                  question=f"Envelope for {wo_id} validated. Continue the trace? [y/N]")
        print(f"\nEnvelope for {wo_id} validated. Continue the trace? [y/N]: ", end="", flush=True)
        answer = sys.stdin.readline().strip().lower()

        # 4. Resume.
        log.emit("resume", work_object=wo_id, answer=answer)
        if answer != "y":
            log.emit("done", work_object=wo_id, outcome="stopped_by_director")
            return 0

        # 5. Write nothing to .work-studio/. Confirm the invariant by
        # re-reading updated_at -- it must be unchanged.
        updated_at_after = _read_updated_at(wo_path)
        unchanged = updated_at_before == updated_at_after
        log.emit(
            "done", work_object=wo_id, outcome="completed",
            updated_at_before=updated_at_before, updated_at_after=updated_at_after,
            canonical_state_unchanged=unchanged,
        )
        return 0 if unchanged else 1
    finally:
        log.close()
        print(f"Trace log: {trace_path.relative_to(repo_root)}")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 -m tools.runtime.tracer <work-object-id>", file=sys.stderr)
        return 2
    return run(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
