"""Minimal checkpointed 2-node graph (WO 2026-08-15-008, Decision 2).

Proves Phase 3's riskiest assumption: a killed run resumes from its SQLite
checkpoint without re-executing completed work, and never touches canonical
state. Node 1 `load_envelope` reads a Work Object through the Phase 2 Pydantic
envelope and appends a side-effect marker; node 2 `validate` runs the real
`python3 -m tools.ws validate --files <path>` subprocess.

Checkpointer: `SqliteSaver` (langgraph-checkpoint-sqlite) at a gitignored path
(default `runtime/checkpoints/tracer.sqlite`). The graph is a non-writer of
canonical state by construction (ADR 0025 single-writer rule): it reads
`.work-studio/` and writes only to its own gitignored marker file.

Run (from repo root, uv-managed Python 3.11):
    uv run --python 3.11 python -m runtime.graph \
        <work-object-id> <thread-id> <marker-file>
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, START, StateGraph

from runtime.envelope import WorkObjectEnvelope

_REPO_ROOT = Path(__file__).resolve().parents[1]


RecoveryStatus = Literal[
    "usable",
    "created_missing",
    "quarantined_corrupt",
    "unusable_checkpoint_payload",
]


@dataclass(frozen=True)
class CheckpointRecoveryResult:
    """Result of preparing the runtime-only checkpoint DB before graph use."""

    status: RecoveryStatus
    checkpoint_db: Path
    quarantine_path: Optional[Path] = None


@dataclass(frozen=True)
class CheckpointBackupResult:
    """Result of copying runtime-only checkpoint DB state."""

    source_checkpoint_db: Path
    backup_path: Path


@dataclass(frozen=True)
class CheckpointRestoreResult:
    """Result of restoring runtime-only checkpoint DB state."""

    backup_path: Path
    restored_checkpoint_db: Path


def _find_work_object(wo_id: str) -> Path:
    matches = sorted(_REPO_ROOT.glob(f".work-studio/objects/*/*/{wo_id}-*.md"))
    if not matches:
        raise FileNotFoundError(f"No Work Object found for id {wo_id!r}")
    return matches[0]


def _read_frontmatter(path: Path) -> dict:
    """Parse the flat frontmatter block (fields are scalars; safe for the CLI world)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{path} has no frontmatter block")
    fields: dict = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.startswith((" ", "\t")):
            continue
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        value = raw.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


def recover_checkpoint_db(checkpoint_db: Path) -> CheckpointRecoveryResult:
    """Prepare a SQLite checkpoint DB without touching canonical state.

    Missing DBs are allowed: the next graph run can create fresh runtime-only
    checkpoint state. Corrupted DBs are quarantined next to the original path so
    recovery never pretends old execution progress is still trustworthy.
    """
    checkpoint_db.parent.mkdir(parents=True, exist_ok=True)

    if not checkpoint_db.exists():
        return CheckpointRecoveryResult("created_missing", checkpoint_db)

    try:
        with sqlite3.connect(str(checkpoint_db)) as conn:
            row = conn.execute("PRAGMA quick_check").fetchone()
    except sqlite3.DatabaseError:
        row = None

    if row and row[0] == "ok":
        return CheckpointRecoveryResult("usable", checkpoint_db)

    quarantine_path = checkpoint_db.with_name(
        f"{checkpoint_db.name}.corrupt-{int(time.time() * 1000)}"
    )
    checkpoint_db.replace(quarantine_path)
    return CheckpointRecoveryResult(
        "quarantined_corrupt", checkpoint_db, quarantine_path
    )


def _sqlite_quick_check(db_path: Path) -> bool:
    try:
        with sqlite3.connect(str(db_path)) as conn:
            row = conn.execute("PRAGMA quick_check").fetchone()
    except sqlite3.DatabaseError:
        return False
    return bool(row and row[0] == "ok")


def backup_checkpoint_db(
    checkpoint_db: Path,
    backup_dir: Path,
) -> CheckpointBackupResult:
    """Copy a usable runtime-only checkpoint DB into a backup directory."""
    if not checkpoint_db.exists():
        raise FileNotFoundError(f"checkpoint DB not found: {checkpoint_db}")
    if not _sqlite_quick_check(checkpoint_db):
        raise sqlite3.DatabaseError(f"checkpoint DB is not usable: {checkpoint_db}")

    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_path = backup_dir / checkpoint_db.name
    if backup_path.exists():
        raise FileExistsError(f"backup already exists: {backup_path}")

    shutil.copy2(checkpoint_db, backup_path)
    return CheckpointBackupResult(checkpoint_db, backup_path)


def restore_checkpoint_db(
    backup_path: Path,
    checkpoint_db: Path,
) -> CheckpointRestoreResult:
    """Restore a runtime-only checkpoint DB copy into an isolated path."""
    if not backup_path.exists():
        raise FileNotFoundError(f"checkpoint backup not found: {backup_path}")
    if checkpoint_db.exists():
        raise FileExistsError(f"restore target already exists: {checkpoint_db}")
    if not _sqlite_quick_check(backup_path):
        raise sqlite3.DatabaseError(f"checkpoint backup is not usable: {backup_path}")

    checkpoint_db.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_path, checkpoint_db)
    return CheckpointRestoreResult(backup_path, checkpoint_db)


class GraphState(TypedDict):
    work_object_id: str
    thread_id: str
    marker_file: str
    idempotency_db: str
    node1_completed: bool
    node2_completed: bool


def _thread_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def _json_default(value):
    return str(value)


def build_checkpoint_serializer() -> JsonPlusSerializer:
    """Build the explicit checkpoint serializer for the runtime tracer.

    The local runtime never opts into pickle fallback. MessagePack extension
    loading is strict: only LangGraph's built-in safe types are allowed unless a
    later bounded decision records a specific allowlist.
    """
    return JsonPlusSerializer(
        pickle_fallback=False,
        allowed_msgpack_modules=None,
    )


def claim_idempotency_receipt(
    idempotency_db: Path,
    *,
    thread_id: str,
    work_object_id: str,
    effect_name: str,
) -> bool:
    """Claim a runtime-only receipt for one protected side effect.

    Returns True only for the first invocation of the stable identity. Duplicate
    invocations return False so callers can skip the protected effect without
    treating checkpoint state as canonical truth.
    """
    idempotency_db.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(idempotency_db)) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS idempotency_receipts (
                thread_id TEXT NOT NULL,
                work_object_id TEXT NOT NULL,
                effect_name TEXT NOT NULL,
                created_at REAL NOT NULL,
                PRIMARY KEY (thread_id, work_object_id, effect_name)
            )
            """
        )
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO idempotency_receipts
                (thread_id, work_object_id, effect_name, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (thread_id, work_object_id, effect_name, time.time()),
        )
        return cursor.rowcount == 1


def node1_load_envelope(state: GraphState) -> dict:
    """Read a Work Object through the strict envelope; record a side effect."""
    wo_path = _find_work_object(state["work_object_id"])
    frontmatter = _read_frontmatter(wo_path)
    WorkObjectEnvelope(**frontmatter)  # raises ValidationError on any drift
    claimed = claim_idempotency_receipt(
        Path(state["idempotency_db"]),
        thread_id=state["thread_id"],
        work_object_id=state["work_object_id"],
        effect_name="load_envelope_marker",
    )
    if not claimed:
        return {"node1_completed": True}
    marker = Path(state["marker_file"])
    marker.parent.mkdir(parents=True, exist_ok=True)
    with marker.open("a", encoding="utf-8") as fh:
        fh.write(f"load_envelope:{state['work_object_id']}\n")
    return {"node1_completed": True}


def node2_validate(state: GraphState) -> dict:
    """Validate through the real canonical CLI path (read-only).

    Two test-only hooks, driven by environment variables, make the kill/resume
    test deterministic without changing the node's meaning:
      - GRAPH_NODE2_SIGNAL_FILE: write this file (and flush) as soon as node 2
        starts, so a harness knows node 1's checkpoint is committed and can kill
        the process before node 2 finishes.
      - GRAPH_NODE2_SLEEP_SECONDS: sleep this long before validating, widening
        the kill window.
    """
    signal_file = os.environ.get("GRAPH_NODE2_SIGNAL_FILE")
    if signal_file:
        Path(signal_file).write_text("started\n", encoding="utf-8")
        Path(signal_file).touch()
    sleep_seconds = float(os.environ.get("GRAPH_NODE2_SLEEP_SECONDS", "0"))
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    wo_path = _find_work_object(state["work_object_id"])
    result = subprocess.run(
        [sys.executable, "-m", "tools.ws", "validate", "--files", str(wo_path)],
        cwd=str(_REPO_ROOT), capture_output=True, text=True,
    )
    return {"node2_completed": result.returncode == 0}


def build_graph(checkpoint_db: Path):
    """Build the 2-node graph; returns (compiled_graph, sqlite_connection).

    The sqlite3.Connection is held open for the lifetime of the invoke because
    `SqliteSaver` stores the connection directly (LangGraph 1.x signature:
    `SqliteSaver(conn: sqlite3.Connection)`). Caller closes it after invoking.
    """
    recover_checkpoint_db(checkpoint_db)

    builder = StateGraph(GraphState)
    builder.add_node("load_envelope", node1_load_envelope)
    builder.add_node("validate", node2_validate)
    builder.add_edge(START, "load_envelope")
    builder.add_edge("load_envelope", "validate")
    builder.add_edge("validate", END)
    conn = sqlite3.connect(str(checkpoint_db), check_same_thread=False)
    saver = SqliteSaver(conn, serde=build_checkpoint_serializer())
    return builder.compile(checkpointer=saver), conn


def run(
    work_object_id: str,
    thread_id: str,
    marker_file: str,
    checkpoint_db: Path,
    idempotency_db: Path,
    resume: bool = False,
) -> dict:
    """Run the graph once (used directly by tests and the CLI).

    When `resume` is True, invoke with no fresh input so the checkpointed state
    wins and completed nodes are skipped (LangGraph resume semantics). When
    False, start a fresh run from the given inputs.
    """
    graph, conn = build_graph(checkpoint_db)
    try:
        if resume:
            return graph.invoke(
                None, config={"configurable": {"thread_id": thread_id}}
            )
        return graph.invoke(
            {"work_object_id": work_object_id, "thread_id": thread_id,
             "marker_file": marker_file, "idempotency_db": str(idempotency_db),
             "node1_completed": False, "node2_completed": False},
            config={"configurable": {"thread_id": thread_id}},
        )
    finally:
        conn.close()


def inspect_thread(thread_id: str, checkpoint_db: Path) -> dict:
    """Inspect the latest runtime-only checkpoint state for one thread."""
    recovery = recover_checkpoint_db(checkpoint_db)
    summary = {
        "thread_id": thread_id,
        "checkpoint_db": str(checkpoint_db),
        "recovery_status": recovery.status,
        "quarantine_path": (
            str(recovery.quarantine_path) if recovery.quarantine_path else None
        ),
        "values": {},
        "next": [],
        "created_at": None,
        "error": None,
    }
    if recovery.status != "usable":
        return summary

    graph, conn = build_graph(checkpoint_db)
    try:
        try:
            snapshot = graph.get_state(_thread_config(thread_id))
        except Exception as exc:
            summary["recovery_status"] = "unusable_checkpoint_payload"
            summary["error"] = type(exc).__name__
            return summary
        summary.update(
            {
                "values": dict(snapshot.values),
                "next": list(snapshot.next),
                "created_at": snapshot.created_at,
            }
        )
        return summary
    finally:
        conn.close()


def _fork_as_node(values: dict) -> Optional[str]:
    """Map the current 2-node graph state to the node that produced it."""
    if values.get("node2_completed"):
        return "validate"
    if values.get("node1_completed"):
        return "load_envelope"
    return None


def fork_thread(
    source_thread_id: str,
    new_thread_id: str,
    checkpoint_db: Path,
    *,
    work_object_id: Optional[str] = None,
    marker_file: Optional[str] = None,
    idempotency_db: Optional[Path] = None,
) -> dict:
    """Create a sibling checkpoint identity from the latest source state.

    This is intentionally specific to the current 2-node tracer. It copies
    inspectable runtime state into a new thread without invoking graph nodes, so
    completed source work is not repeated during fork creation.
    """
    recovery = recover_checkpoint_db(checkpoint_db)
    if recovery.status != "usable":
        raise RuntimeError(
            f"cannot fork from checkpoint DB in {recovery.status!r} state"
        )

    graph, conn = build_graph(checkpoint_db)
    try:
        existing_target = graph.get_state(_thread_config(new_thread_id))
        if existing_target.values:
            raise ValueError(f"target thread already has checkpoint state: {new_thread_id}")

        source_snapshot = graph.get_state(_thread_config(source_thread_id))
        if not source_snapshot.values:
            raise ValueError(f"source thread has no checkpoint state: {source_thread_id}")

        forked_values = dict(source_snapshot.values)
        forked_values["thread_id"] = new_thread_id
        if work_object_id is not None:
            forked_values["work_object_id"] = work_object_id
        if marker_file is not None:
            forked_values["marker_file"] = marker_file
        if idempotency_db is not None:
            forked_values["idempotency_db"] = str(idempotency_db)

        graph.update_state(
            _thread_config(new_thread_id),
            forked_values,
            as_node=_fork_as_node(forked_values),
        )
        forked_snapshot = graph.get_state(_thread_config(new_thread_id))
        return {
            "source_thread_id": source_thread_id,
            "thread_id": new_thread_id,
            "checkpoint_db": str(checkpoint_db),
            "values": dict(forked_snapshot.values),
            "next": list(forked_snapshot.next),
            "created_at": forked_snapshot.created_at,
        }
    finally:
        conn.close()


def _add_runtime_db_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--checkpoint-db",
        default=str(_REPO_ROOT / "runtime" / "checkpoints" / "tracer.sqlite"),
    )
    parser.add_argument("--idempotency-db")


def _legacy_main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the 2-node checkpointed graph.")
    parser.add_argument("work_object_id")
    parser.add_argument("thread_id")
    parser.add_argument("marker_file")
    _add_runtime_db_options(parser)
    parser.add_argument("--resume", action="store_true",
                        help="Resume from the checkpoint (no fresh input; completed nodes skip)")
    args = parser.parse_args(argv)
    checkpoint_db = Path(args.checkpoint_db)
    idempotency_db = (
        Path(args.idempotency_db)
        if args.idempotency_db
        else checkpoint_db.with_name("idempotency.sqlite")
    )
    result = run(args.work_object_id, args.thread_id, args.marker_file,
                 checkpoint_db, idempotency_db, resume=args.resume)
    print(result)
    return 0


def _print_json(value: dict) -> None:
    print(json.dumps(value, sort_keys=True, default=_json_default))


def main(argv: Optional[list[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    commands = {"run", "inspect", "resume", "fork", "backup", "restore"}
    if argv and argv[0] not in {*commands, "-h", "--help"}:
        return _legacy_main(argv)

    parser = argparse.ArgumentParser(
        description="Operate the 2-node checkpointed graph."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a fresh graph execution")
    run_parser.add_argument("work_object_id")
    run_parser.add_argument("thread_id")
    run_parser.add_argument("marker_file")
    _add_runtime_db_options(run_parser)

    inspect_parser = subparsers.add_parser(
        "inspect", help="Inspect one thread's runtime checkpoint state"
    )
    inspect_parser.add_argument("thread_id")
    inspect_parser.add_argument(
        "--checkpoint-db",
        default=str(_REPO_ROOT / "runtime" / "checkpoints" / "tracer.sqlite"),
    )

    resume_parser = subparsers.add_parser(
        "resume", help="Resume from the checkpoint without fresh input"
    )
    resume_parser.add_argument("work_object_id")
    resume_parser.add_argument("thread_id")
    resume_parser.add_argument("marker_file")
    _add_runtime_db_options(resume_parser)

    fork_parser = subparsers.add_parser(
        "fork", help="Copy latest source checkpoint state into a sibling thread"
    )
    fork_parser.add_argument("source_thread_id")
    fork_parser.add_argument("new_thread_id")
    fork_parser.add_argument(
        "--checkpoint-db",
        default=str(_REPO_ROOT / "runtime" / "checkpoints" / "tracer.sqlite"),
    )
    fork_parser.add_argument("--work-object-id")
    fork_parser.add_argument("--marker-file")
    fork_parser.add_argument("--idempotency-db")

    backup_parser = subparsers.add_parser(
        "backup", help="Copy runtime checkpoint DB state into a backup directory"
    )
    backup_parser.add_argument("--checkpoint-db", required=True)
    backup_parser.add_argument("--backup-dir", required=True)

    restore_parser = subparsers.add_parser(
        "restore", help="Restore runtime checkpoint DB state into an isolated path"
    )
    restore_parser.add_argument("--backup", required=True)
    restore_parser.add_argument("--checkpoint-db", required=True)

    args = parser.parse_args(argv)

    if args.command == "inspect":
        _print_json(inspect_thread(args.thread_id, Path(args.checkpoint_db)))
        return 0

    if args.command == "backup":
        try:
            result = backup_checkpoint_db(
                Path(args.checkpoint_db),
                Path(args.backup_dir),
            )
        except (FileNotFoundError, FileExistsError, sqlite3.DatabaseError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        _print_json(
            {
                "source_checkpoint_db": str(result.source_checkpoint_db),
                "backup_path": str(result.backup_path),
            }
        )
        return 0

    if args.command == "restore":
        try:
            result = restore_checkpoint_db(
                Path(args.backup),
                Path(args.checkpoint_db),
            )
        except (FileNotFoundError, FileExistsError, sqlite3.DatabaseError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        _print_json(
            {
                "backup_path": str(result.backup_path),
                "restored_checkpoint_db": str(result.restored_checkpoint_db),
            }
        )
        return 0

    checkpoint_db = Path(args.checkpoint_db)
    idempotency_db = (
        Path(args.idempotency_db)
        if args.idempotency_db
        else checkpoint_db.with_name("idempotency.sqlite")
    )

    if args.command in {"run", "resume"}:
        try:
            result = run(args.work_object_id, args.thread_id, args.marker_file,
                         checkpoint_db, idempotency_db,
                         resume=args.command == "resume")
        except Exception as exc:
            print(f"Error: checkpoint execution failed: {exc}", file=sys.stderr)
            return 1
        _print_json(result)
        return 0

    if args.command == "fork":
        result = fork_thread(
            args.source_thread_id,
            args.new_thread_id,
            checkpoint_db,
            work_object_id=args.work_object_id,
            marker_file=args.marker_file,
            idempotency_db=Path(args.idempotency_db) if args.idempotency_db else None,
        )
        _print_json(result)
        return 0

    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    sys.exit(main())
