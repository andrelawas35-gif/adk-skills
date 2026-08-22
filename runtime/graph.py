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
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal, Optional, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, RetryPolicy, interrupt

from runtime.envelope import WorkObjectEnvelope
from runtime.handoff import (
    HandoffEnvelope,
    HandoffReceipt,
    derive_authority_scope,
    derive_proposal,
    derive_verification_gaps,
    merge_proposals,
)
from tools.ws.component_governance import governance_domain_for_skill
from runtime.research import ResearchReceipt, build_receipt, fetch_url

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


def _resolve_repo_root() -> Path:
    """Optional cross-repo override (WO 2026-08-21-001).

    Defaults to this repo's root -- unchanged behavior for every existing
    caller -- unless WS_REPO_ROOT is set, in which case Work Object lookups
    and node 2's `tools.ws validate` subprocess both redirect there instead.
    """
    override = os.environ.get("WS_REPO_ROOT")
    return Path(override) if override else _REPO_ROOT


def _default_checkpoint_db() -> Path:
    """Default --checkpoint-db location (WO 2026-08-21-003, Direction 1).

    Unset WS_REPO_ROOT: unchanged behavior, `runtime/checkpoints/tracer.sqlite`
    inside this repo. Set: a platform-appropriate user-data directory instead
    of the target repo's own tree, since the runtime's checkpoint state isn't
    canonical data that repo owns -- computed inline (no platformdirs
    dependency) to keep tools/ws and this override dependency-free.

    Known gap, not addressed here: this default doesn't key by which repo
    WS_REPO_ROOT pointed at, so switching targets without an explicit
    --checkpoint-db reuses the same file. Explicit --checkpoint-db avoids it;
    per-repo keying is left for a future revision if it proves necessary.
    """
    if not os.environ.get("WS_REPO_ROOT"):
        return _REPO_ROOT / "runtime" / "checkpoints" / "tracer.sqlite"
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", str(Path.home() / "AppData" / "Local")))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", str(Path.home() / ".local" / "share")))
    return base / "work-studio" / "checkpoints" / "tracer.sqlite"


def _repo_registry_path() -> Path:
    """Location of the optional cross-repo registry (WO 2026-08-21-005)."""
    return _REPO_ROOT / ".work-studio" / "repos.json"


def _load_repo_registry() -> dict:
    """Load the optional named-target registry (WO 2026-08-21-005, Direction 2).

    Schema: {"<name>": {"repo_root": "<path>", "checkpoint_db": "<path>"}, ...}.
    Read-path only so far -- only `checkpoint_db` is consumed here (by
    `inspect --repo`/`--repo-all`); `repo_root` is reserved for a future
    write-path (`run`/`resume`) revision, per the tracer bullet's Non-goals
    (WO 2026-08-21-005, Decision 2). Missing file returns an empty registry,
    not an error -- the registry is opt-in and does not change any existing
    caller's default behavior. JSON, not YAML, to add zero new dependencies
    (json is stdlib), consistent with tools/ws's dependency-free-by-design
    posture recorded in WO 2026-08-21-003's evidence ledger.
    """
    path = _repo_registry_path()
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _resolve_registry_entry(name: str) -> dict:
    registry = _load_repo_registry()
    if name not in registry:
        raise KeyError(
            f"'{name}' not found in registry ({_repo_registry_path()}); "
            f"known entries: {sorted(registry)}"
        )
    return registry[name]


def _resolve_registry_checkpoint_db(name: str) -> Path:
    entry = _resolve_registry_entry(name)
    if "checkpoint_db" not in entry:
        raise KeyError(f"registry entry '{name}' has no checkpoint_db")
    return Path(entry["checkpoint_db"])


def _resolve_registry_repo_root(name: str) -> Path:
    """Resolve a registry entry's repo_root (WO 2026-08-21-005, write path).

    Sets WS_REPO_ROOT for this process from the registry instead of
    requiring it pre-set in the environment. Safe for a single `run`/`resume`
    invocation targeting one named entry -- the tracer bullet (Decision 3)
    tested the harder case, mutating WS_REPO_ROOT *between* sequential
    iterations in one process, and confirmed no leakage; a single set before
    one graph execution is strictly simpler than what was tested.
    """
    entry = _resolve_registry_entry(name)
    if "repo_root" not in entry:
        raise KeyError(f"registry entry '{name}' has no repo_root")
    return Path(entry["repo_root"])


def _find_work_object(wo_id: str) -> Path:
    matches = sorted(_resolve_repo_root().glob(f".work-studio/objects/*/*/{wo_id}-*.md"))
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


def has_idempotency_receipt(
    idempotency_db: Path,
    *,
    thread_id: str,
    work_object_id: str,
    effect_name: str,
) -> bool:
    """Read-only check for an existing receipt, without claiming one.

    For an effect that can fail *after* being claimed (WO 2026-08-17-016
    Decision 6): claim-before-effect (`claim_idempotency_receipt`) assumes
    the effect always succeeds once claimed, which node1_load_envelope's
    effectively-infallible marker write satisfies but a real file append
    under simulated failure does not -- a claim burned by a failed attempt
    would block every subsequent retry from ever performing the effect.
    The correct order for a fallible effect is: check (this function,
    read-only) -> attempt the effect -> claim only after it succeeds.
    """
    if not idempotency_db.exists():
        return False
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
        row = conn.execute(
            """
            SELECT 1 FROM idempotency_receipts
            WHERE thread_id = ? AND work_object_id = ? AND effect_name = ?
            """,
            (thread_id, work_object_id, effect_name),
        ).fetchone()
        return row is not None


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
    resolved_root = _resolve_repo_root()
    # cwd drives tools/ws's own CWD-based root discovery (_find_work_studio_root),
    # so it must be the resolved root -- not always _REPO_ROOT -- or ambient
    # checks like `dashboard-signals` silently scan this repo's own
    # .work-studio/objects/ instead of the target repo's (WO 2026-08-21-001
    # Open questions). `tools.ws` still lives in this repo's code, though, so
    # PYTHONPATH is set explicitly rather than relying on cwd for the import --
    # `-m` normally adds cwd to sys.path, which would break once cwd moves.
    env = dict(os.environ)
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(_REPO_ROOT) if not existing_pythonpath
        else str(_REPO_ROOT) + os.pathsep + existing_pythonpath
    )
    result = subprocess.run(
        [sys.executable, "-m", "tools.ws", "validate", "--files", str(wo_path)],
        cwd=str(resolved_root), env=env, capture_output=True, text=True,
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


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 6 — bounded specialist concurrency and reliable handoff (WO 2026-08-17-008)
# ═══════════════════════════════════════════════════════════════════════════════

PHASE6_MAX_CONCURRENCY = 2  # explicit concurrency limit (build plan 362; open q1)


class Phase6Crash(Exception):
    """Test-only sentinel: simulates a crash at the start of a named Phase 6 node."""

    def __init__(self, node: str):
        super().__init__(f"simulated crash at Phase 6 node '{node}'")
        self.node = node


def _phase6_crash_hook(node: str) -> None:
    """Test-only crash hook: crash exactly once at a named node's first attempt.

    ``PHASE6_CRASH_NODE`` names the node to crash (dispatch|branch_a|branch_b|
    join); ``PHASE6_CRASH_MARKER`` is the marker path. On the first attempt the
    marker is written and a ``Phase6Crash`` sentinel is raised; a resume (marker
    already present) proceeds, proving the checkpoint recovered the completed
    supersteps without re-running them. The four superstep boundaries are the
    four-crash-point matrix (Decision 4).
    """
    if os.environ.get("PHASE6_CRASH_NODE") != node:
        return
    marker = os.environ.get("PHASE6_CRASH_MARKER")
    if marker and not Path(marker).exists():
        Path(marker).write_text(f"{node}-attempt-1\n")
        raise Phase6Crash(node)


class Phase6State(TypedDict, total=False):
    work_object_id: str
    thread_id: str
    handoff_envelope: dict
    business_route_result: dict
    business_handoff_envelope: dict
    engineering_route_result: dict
    engineering_handoff_envelope: dict
    branch_a_receipt: dict
    branch_b_receipt: dict
    branch_a_completed: bool
    branch_b_completed: bool
    join_fired: bool
    join_proposal: str
    direction_approved: bool


def _phase6_is_business_scoped(frontmatter: dict, body_text: str) -> bool:
    """Return whether Phase 6 dispatch should use business operating routing."""
    explicit_scope = frontmatter.get("business_scope")
    if isinstance(explicit_scope, bool):
        return explicit_scope
    if isinstance(explicit_scope, str):
        normalized_scope = explicit_scope.strip().lower()
        if normalized_scope in {"true", "yes", "business", "business-operating"}:
            return True
        if normalized_scope in {"false", "no", "none", "generic"}:
            return False
    open_questions = re.search(
        r"## Open questions\s*(.*?)(?:\n## |\Z)",
        body_text,
        flags=re.DOTALL,
    )
    scoped_text = " ".join(
        [
            str(frontmatter.get("title", "")),
            str(frontmatter.get("next_action", "")),
            open_questions.group(1) if open_questions else "",
        ]
    ).lower()
    explicit_markers = (
        "business",
        "pricing",
        "package",
        "pipeline",
        "market",
        "commercial",
        "customer success",
        "cash runway",
        "supplier",
        "workforce",
        "capacity",
    )
    return any(marker in scoped_text for marker in explicit_markers)


def _phase6_business_next_gap(frontmatter: dict, body_text: str) -> str:
    """Extract a deterministic business frontier for dispatch routing."""
    next_action = str(frontmatter.get("next_action", "")).strip()
    if next_action and "awaiting activation" not in next_action.lower():
        return next_action
    open_questions = re.search(
        r"## Open questions\s*(.*?)(?:\n## |\Z)",
        body_text,
        flags=re.DOTALL,
    )
    if open_questions:
        for raw in open_questions.group(1).splitlines():
            line = raw.strip()
            if line.startswith("- "):
                return line[2:].strip()
    return str(frontmatter.get("title", "")).strip()


def _phase6_is_engineering_scoped(frontmatter: dict, body_text: str) -> bool:
    """Return whether Phase 6 dispatch should use engineering routing.

    This first tracer intentionally honors only explicit metadata. It does not
    infer engineering scope from prose, so generic lifecycle routing remains
    the fallback unless a Work Object opts in with ``engineering_scope``.
    """
    explicit_scope = frontmatter.get("engineering_scope")
    if isinstance(explicit_scope, bool):
        return explicit_scope
    if isinstance(explicit_scope, str):
        normalized_scope = explicit_scope.strip().lower()
        if normalized_scope in {"true", "yes", "engineering", "engineering-operating"}:
            return True
        if normalized_scope in {"false", "no", "none", "generic"}:
            return False
    return False


def _phase6_engineering_next_gap(frontmatter: dict, body_text: str) -> str:
    """Extract a deterministic engineering frontier for dispatch routing."""
    next_action = str(frontmatter.get("next_action", "")).strip()
    if next_action and "awaiting activation" not in next_action.lower():
        return next_action
    open_questions = re.search(
        r"## Open questions\s*(.*?)(?:\n## |\Z)",
        body_text,
        flags=re.DOTALL,
    )
    if open_questions:
        for raw in open_questions.group(1).splitlines():
            line = raw.strip()
            if line.startswith("- "):
                return line[2:].strip()
    return str(frontmatter.get("title", "")).strip()


def _phase6_business_dispatch_payload(
    state: Phase6State,
    frontmatter: dict,
    wo_path: Path,
) -> dict:
    """Build runtime-only business routing payloads for Phase 6 dispatch."""
    from runtime.business import propose_business_handoff, route_business_frontier

    body_text = wo_path.read_text(encoding="utf-8")
    if not _phase6_is_business_scoped(frontmatter, body_text):
        return {}
    next_gap = _phase6_business_next_gap(frontmatter, body_text)
    route = route_business_frontier(next_gap)
    authority_scope = derive_authority_scope(frontmatter.get("consequence", ""))
    business_envelope = propose_business_handoff(
        handoff_id=f"BUSINESS-HANDOFF-{state['work_object_id']}-{state['thread_id']}",
        work_object_id=state["work_object_id"],
        lifecycle_state=str(frontmatter.get("state", "")),
        current_frontier=str(frontmatter.get("title", "")),
        from_skill="business-formulate-strategy",
        evidence_resolved=[],
        next_gap=next_gap,
        same_work_object=True,
        authority_boundary=authority_scope,
    )
    dispatch_envelope = HandoffEnvelope(
        handoff_id=f"HANDOFF-{state['work_object_id']}-{state['thread_id']}",
        from_role="runtime",
        to_skill=business_envelope.to_skill,
        component_kind="skill",
        governance_domain=governance_domain_for_skill(business_envelope.to_skill),
        task=f"route business frontier: {next_gap}",
        input_refs=[state["work_object_id"]],
        expected_output="business handoff proposal",
        authority_scope=authority_scope,
    )
    return {
        "business_route_result": route.model_dump(),
        "business_handoff_envelope": business_envelope.model_dump(),
        "handoff_envelope": dispatch_envelope.model_dump(),
    }


def _phase6_engineering_dispatch_payload(
    state: Phase6State,
    frontmatter: dict,
    wo_path: Path,
) -> dict:
    """Build runtime-only engineering routing payloads for Phase 6 dispatch."""
    from runtime.engineering import (
        propose_engineering_handoff,
        route_engineering_frontier,
    )

    body_text = wo_path.read_text(encoding="utf-8")
    if not _phase6_is_engineering_scoped(frontmatter, body_text):
        return {}
    next_gap = _phase6_engineering_next_gap(frontmatter, body_text)
    route = route_engineering_frontier(next_gap)
    authority_scope = derive_authority_scope(frontmatter.get("consequence", ""))
    engineering_envelope = propose_engineering_handoff(
        handoff_id=(
            f"ENGINEERING-HANDOFF-{state['work_object_id']}-{state['thread_id']}"
        ),
        work_object_id=state["work_object_id"],
        lifecycle_state=str(frontmatter.get("state", "")),
        current_frontier=str(frontmatter.get("title", "")),
        from_skill="engineering-implement-bounded-change",
        evidence_resolved=[],
        next_gap=next_gap,
        same_work_object=True,
        authority_boundary=authority_scope,
    )
    dispatch_envelope = HandoffEnvelope(
        handoff_id=f"HANDOFF-{state['work_object_id']}-{state['thread_id']}",
        from_role="runtime",
        to_skill=engineering_envelope.to_skill,
        component_kind="skill",
        governance_domain=governance_domain_for_skill(engineering_envelope.to_skill),
        task=f"route engineering frontier: {next_gap}",
        input_refs=[state["work_object_id"]],
        expected_output="engineering handoff proposal",
        authority_scope=authority_scope,
    )
    return {
        "engineering_route_result": route.model_dump(),
        "engineering_handoff_envelope": engineering_envelope.model_dump(),
        "handoff_envelope": dispatch_envelope.model_dump(),
    }


def phase6_dispatch(state: Phase6State) -> dict:
    """Record the HandoffEnvelope in runtime state before fan-out (build plan 362).

    ``to_skill`` is derived from the WO's canonical state via derive_proposal
    (routing audit WO 2026-08-22-009, G1) -- previously a hardcoded
    "specialist" placeholder that carried no routing meaning, since the real
    proposal was only ever computed later, per-branch, on the HandoffReceipt.
    """
    _phase6_crash_hook("dispatch")
    wo_path = _find_work_object(state["work_object_id"])
    frontmatter = _read_frontmatter(wo_path)  # read-only probe of canonical state
    business_payload = _phase6_business_dispatch_payload(state, frontmatter, wo_path)
    if business_payload:
        return business_payload
    engineering_payload = _phase6_engineering_dispatch_payload(
        state, frontmatter, wo_path
    )
    if engineering_payload:
        return engineering_payload
    routed_skill = derive_proposal(frontmatter.get("state", ""), role="dispatch")
    envelope = HandoffEnvelope(
        handoff_id=f"HANDOFF-{state['work_object_id']}-{state['thread_id']}",
        from_role="runtime",
        to_skill=routed_skill,
        component_kind="skill",
        governance_domain=governance_domain_for_skill(routed_skill),
        task="propose next step",
        input_refs=[state["work_object_id"]],
        expected_output="proposal",
        authority_scope=derive_authority_scope(
            frontmatter.get("consequence", "")
        ),
    )
    return {"handoff_envelope": envelope.model_dump()}


def _phase6_dispatch_routed_skill(state: Phase6State) -> Optional[str]:
    """Return a dispatch-level routed skill when Phase 6 has one."""
    business_envelope = state.get("business_handoff_envelope") or {}
    if business_envelope.get("to_skill"):
        return business_envelope.get("to_skill")
    engineering_envelope = state.get("engineering_handoff_envelope") or {}
    if engineering_envelope.get("to_skill"):
        return engineering_envelope.get("to_skill")
    envelope = state.get("handoff_envelope") or {}
    if envelope.get("governance_domain") in {"business", "engineering", "operations"}:
        return envelope.get("to_skill")
    return None


def _phase6_wo_verification_signals(wo_path: Path) -> tuple[bool, bool]:
    """Read-only scan of a WO body for verification signals (Decision 8).

    Returns (has_checked_success_evidence, has_evidence_ledger_entries) by
    scanning the canonical body text. Never writes canonical state.
    """
    text = wo_path.read_text(encoding="utf-8")
    has_checked = bool(re.search(r"^\s*-\s*\[[xX]\]", text, flags=re.MULTILINE))
    has_ledger = bool(
        re.search(
            r"^\|\s*\[(?:decision|system|inference|gap|testimony|memory)\]",
            text,
            flags=re.MULTILINE,
        )
    )
    return has_checked, has_ledger


def _phase6_branch(state: Phase6State, key: str, role: str, node: str) -> dict:
    """Read-only specialist: read the WO and record a HandoffReceipt (no writes).

    Read-only by construction (ADR 0025 / build plan 239): it reads canonical
    state but never mutates it. The proposal is derived from the WO's canonical
    ``state`` field via derive_proposal (Decision 5) rather than hardcoded; the
    verify role additionally derives real verification gaps from the WO body
    (Decision 8). ``PHASE6_BRANCH_MARKER`` is a test-only hook that appends a
    line per branch run so a test can prove a branch was not re-run after a
    crash/resume. ``_phase6_crash_hook`` simulates a crash at this branch for
    the four-crash-point matrix.
    """
    _phase6_crash_hook(node)
    wo_path = _find_work_object(state["work_object_id"])
    frontmatter = _read_frontmatter(wo_path)  # read-only probe of canonical state
    proposal = _phase6_dispatch_routed_skill(state) or derive_proposal(
        frontmatter.get("state", ""), role
    )
    gaps: list[str] = []
    if role == "verify":
        has_checked, has_ledger = _phase6_wo_verification_signals(wo_path)
        gaps = derive_verification_gaps(has_checked, has_ledger)
    marker = os.environ.get("PHASE6_BRANCH_MARKER")
    if marker:
        with Path(marker).open("a", encoding="utf-8") as fh:
            fh.write(f"{key}\n")
    now = datetime.now(timezone.utc)
    receipt = HandoffReceipt(
        status="completed",
        output_refs=[str(wo_path)],
        verification_gaps=gaps,
        proposed_next_skill=proposal,
        started_at=now,
        completed_at=now,
    )
    return {key: receipt.model_dump()}


def phase6_branch_a(state: Phase6State) -> dict:
    out = _phase6_branch(state, "branch_a_receipt", "implement", "branch_a")
    out["branch_a_completed"] = True
    return out


def phase6_branch_b(state: Phase6State) -> dict:
    out = _phase6_branch(state, "branch_b_receipt", "verify", "branch_b")
    out["branch_b_completed"] = True
    return out


def phase6_join(state: Phase6State) -> dict:
    """Crash hook, then merge the two normalized branch proposals.

    ``_phase6_crash_hook("join")`` simulates a crash before the join for the
    four-crash-point matrix: on the first attempt the marker is written and a
    ``Phase6Crash`` sentinel is raised, leaving the branches' superstep
    checkpointed; a resume then runs the join (marker already present) without
    re-running the completed branches.
    """
    _phase6_crash_hook("join")

    # Test-only pause hook (Decision 6): let a subprocess test SIGKILL the
    # process after the branches' superstep is committed but before the join
    # completes. On resume the signal file already exists, so the pause is
    # skipped. Mirrors the Phase 3 GRAPH_NODE2 kill-test hooks.
    join_signal = os.environ.get("PHASE6_JOIN_SIGNAL_FILE")
    if join_signal and not Path(join_signal).exists():
        Path(join_signal).write_text("join-signal\n")
        time.sleep(float(os.environ.get("PHASE6_JOIN_SLEEP_SECONDS", "60")))

    # Normalize the two unordered branch receipts into one deterministic
    # proposal (Decision 11): merge_proposals sorts and dedupes, so identical
    # branch proposals collapse to a single skill name.
    receipts = [
        state.get("branch_a_receipt"),
        state.get("branch_b_receipt"),
    ]
    proposal = merge_proposals([r for r in receipts if r])
    return {"join_fired": True, "join_proposal": proposal}


def phase6_direction_gate(state: Phase6State) -> dict:
    """Pause for explicit director approval of the joined proposal (WO 2026-08-17-016 Decision 11).

    The build plan's own reference architecture names a "Director direction
    interrupt" immediately after "Join proposals" -- this is that point,
    generalized via `authority_gate` rather than a hand-rolled `interrupt()`.
    Uses `direction_approved`, not `authority_gate`'s own `approved` key, to
    leave room for a second gate type on this graph later without collision.
    No differential routing on the outcome yet -- both approved and rejected
    directions simply complete, recording which one happened.
    """
    result = authority_gate(reason=f"approve direction: {state['join_proposal']}")
    return {"direction_approved": bool(result.get("approved"))}


def build_phase6_graph(checkpoint_db: Path):
    """Build the Phase 6 two-branch/join graph; returns (compiled_graph, conn)."""
    recover_checkpoint_db(checkpoint_db)
    builder = StateGraph(Phase6State)
    builder.add_node("dispatch", phase6_dispatch)
    builder.add_node("branch_a", phase6_branch_a)
    builder.add_node("branch_b", phase6_branch_b)
    builder.add_node("join", phase6_join)
    builder.add_node("direction_gate", phase6_direction_gate)
    builder.add_edge(START, "dispatch")
    builder.add_edge("dispatch", "branch_a")
    builder.add_edge("dispatch", "branch_b")
    builder.add_edge("branch_a", "join")
    builder.add_edge("branch_b", "join")
    builder.add_edge("join", "direction_gate")
    builder.add_edge("direction_gate", END)
    conn = sqlite3.connect(str(checkpoint_db), check_same_thread=False)
    saver = SqliteSaver(conn, serde=build_checkpoint_serializer())
    return builder.compile(checkpointer=saver), conn


def _phase6_config(thread_id: str) -> dict:
    return {
        "configurable": {"thread_id": thread_id},
        "max_concurrency": PHASE6_MAX_CONCURRENCY,
    }


def run_phase6(
    work_object_id: str,
    thread_id: str,
    checkpoint_db: Path,
    resume: bool = False,
    approve_direction: Optional[bool] = None,
) -> dict:
    """Run the Phase 6 graph once (used directly by tests).

    `resume` and `approve_direction` are distinct mechanisms that never
    share a code path (WO 2026-08-17-016 Decision 11): `resume` continues
    a run after an uncaught crash via LangGraph's checkpoint (`graph.invoke
    (None, ...)`); `approve_direction`, when not None, answers the
    `direction_gate` interrupt via `Command(resume=...)`. A crash always
    happens before `direction_gate` (at dispatch/branch_a/branch_b/join),
    so `resume=True` alone always gets a thread past a crash and up to the
    interrupt; a separate `approve_direction` call is then needed to pass it.
    """
    graph, conn = build_phase6_graph(checkpoint_db)
    try:
        if approve_direction is not None:
            return graph.invoke(
                Command(resume=approve_direction), config=_phase6_config(thread_id)
            )
        if resume:
            return graph.invoke(None, config=_phase6_config(thread_id))
        return graph.invoke(
            {
                "work_object_id": work_object_id,
                "thread_id": thread_id,
                "branch_a_completed": False,
                "branch_b_completed": False,
                "join_fired": False,
            },
            config=_phase6_config(thread_id),
        )
    finally:
        conn.close()


def inspect_phase6(thread_id: str, checkpoint_db: Path) -> dict:
    """Inspect the latest runtime checkpoint state for one Phase 6 thread."""
    recovery = recover_checkpoint_db(checkpoint_db)
    summary = {
        "checkpoint_db": str(checkpoint_db),
        "recovery": recovery.status,
    }
    if recovery.status != "usable" and not checkpoint_db.exists():
        return summary
    graph, conn = build_phase6_graph(checkpoint_db)
    try:
        snapshot = graph.get_state(_phase6_config(thread_id))
        values = snapshot.values or {}
        summary["thread_id"] = thread_id
        summary["branch_a_completed"] = values.get("branch_a_completed", False)
        summary["branch_b_completed"] = values.get("branch_b_completed", False)
        summary["join_fired"] = values.get("join_fired", False)
        summary["join_proposal"] = values.get("join_proposal")
        summary["has_envelope"] = bool(values.get("handoff_envelope"))
        summary["has_business_handoff_envelope"] = bool(
            values.get("business_handoff_envelope")
        )
        summary["business_route_result"] = values.get("business_route_result")
        summary["has_engineering_handoff_envelope"] = bool(
            values.get("engineering_handoff_envelope")
        )
        summary["engineering_route_result"] = values.get("engineering_route_result")
        summary["has_branch_a_receipt"] = bool(values.get("branch_a_receipt"))
        summary["has_branch_b_receipt"] = bool(values.get("branch_b_receipt"))
    finally:
        conn.close()
    return summary


def _fork_phase6_as_node(values: dict) -> Optional[str]:
    """Map the current Phase 6 graph state to the node that produced it."""
    if values.get("join_fired"):
        return "join"
    if values.get("branch_a_completed") or values.get("branch_b_completed"):
        # The branches superstep produced this state; the join is next.
        return "branch_a"
    return None


def fork_phase6_thread(
    source_thread_id: str,
    new_thread_id: str,
    checkpoint_db: Path,
    *,
    work_object_id: Optional[str] = None,
) -> dict:
    """Create a sibling checkpoint identity from the latest Phase 6 state.

    Mirrors the Phase 3 fork_thread for the parallel handoff graph (Decision 9):
    it copies inspectable runtime state into a new thread without invoking graph
    nodes, so completed source work is not repeated during fork creation, and the
    sibling can resume (e.g. a crash-before-join run forked and completed).
    """
    recovery = recover_checkpoint_db(checkpoint_db)
    if recovery.status != "usable":
        raise RuntimeError(
            f"cannot fork from checkpoint DB in {recovery.status!r} state"
        )

    graph, conn = build_phase6_graph(checkpoint_db)
    try:
        existing_target = graph.get_state(_phase6_config(new_thread_id))
        if existing_target.values:
            raise ValueError(
                f"target thread already has checkpoint state: {new_thread_id}"
            )

        source_snapshot = graph.get_state(_phase6_config(source_thread_id))
        if not source_snapshot.values:
            raise ValueError(
                f"source thread has no checkpoint state: {source_thread_id}"
            )

        forked_values = dict(source_snapshot.values)
        forked_values["thread_id"] = new_thread_id
        if work_object_id is not None:
            forked_values["work_object_id"] = work_object_id

        graph.update_state(
            _phase6_config(new_thread_id),
            forked_values,
            as_node=_fork_phase6_as_node(forked_values),
        )
        forked_snapshot = graph.get_state(_phase6_config(new_thread_id))
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


# ═══════════════════════════════════════════════════════════════════════════════
# Research — single-URL live fetch, human-approval-gated (WO 2026-08-17-011)
# ═══════════════════════════════════════════════════════════════════════════════

# Runtime's first external-effect node. Gated by langgraph's native
# `interrupt()` (Decision 2): the graph pauses at `gate_fetch` and performs
# no network call until explicitly resumed with `Command(resume=True)`,
# naming approval of the exact proposed URL. A read-only GET has no
# external state to compensate/undo -- only failure-as-gap applies.


class ResearchState(TypedDict, total=False):
    work_object_id: str
    thread_id: str
    url: str
    approved: bool
    research_receipt: dict
    note_recorded: bool


def research_propose_fetch(state: ResearchState) -> dict:
    """Name the exact URL to fetch. No network call happens here."""
    return {"url": state["url"]}


def authority_gate(reason: str) -> dict:
    """Pause for explicit human approval, named by `reason`.

    Performs no side effect itself. `interrupt()` checkpoints the pause; a
    resume without `Command(resume=True)` (approval) leaves `approved` False.
    Generalizes the research-only approval gate below (Direction 4, ADR 0026)
    for reuse across the four director-gate types (direction, restricted,
    high_consequence, release) -- WO 2026-08-17-016 Decision 2 wires only the
    research call site for now; the other three remain unimplemented.
    """
    approval = interrupt({"reason": reason, "ask": "approve this action?"})
    return {"approved": bool(approval)}


def research_gate_fetch(state: ResearchState) -> dict:
    """Pause for explicit human approval of the exact proposed URL.

    Wraps the generalized `authority_gate` with a research-specific reason.
    Performs no network call itself; the fetch node below performs no fetch
    without approval -- proving exit criterion 1 (no fetch without approval).
    """
    return authority_gate(reason=f"approve fetch: {state['url']}")


def research_fetch_source(state: ResearchState) -> dict:
    """Perform the approved single GET and record a ResearchReceipt.

    Only runs the network call if `approved` is True (set by
    `research_gate_fetch` after `interrupt()` resume). An unapproved state
    records a "failed" receipt with an explicit detail rather than silently
    skipping -- the receipt always reflects what happened.
    """
    now_start = datetime.now(timezone.utc)
    if not state.get("approved"):
        receipt = build_receipt(
            state["url"], now_start, datetime.now(timezone.utc),
            ok=False, body="", detail="fetch not approved",
        )
        return {"research_receipt": receipt.model_dump()}

    ok, body, detail = fetch_url(state["url"])
    receipt = build_receipt(
        state["url"], now_start, datetime.now(timezone.utc), ok, body, detail,
    )
    return {"research_receipt": receipt.model_dump()}


def _make_research_record_note(notes_dir: Path):
    """Build the record_note node, closed over a test-isolable notes directory.

    Runtime-local only (WO 2026-08-17-016 Decision 6) -- not a canonical
    Evidence Ledger entry; a human or `investigate-live-question` still owns
    promoting fetched content into `.work-studio/` (research.py's own
    constraint). `notes_dir` is derived from `checkpoint_db`'s directory by
    `build_research_graph` so tests using an isolated temp checkpoint dir get
    an isolated notes dir too, matching the existing test-isolation pattern
    (`claim_idempotency_receipt`'s db is likewise never a fixed shared path).
    """

    def research_record_note(state: ResearchState) -> dict:
        """Append the fetched receipt to a runtime-local, durable log.

        Check-then-write-then-claim, not claim-then-write: this effect can
        fail (a real file append, unlike node1_load_envelope's effectively-
        infallible marker write), so claiming before attempting it would
        burn the claim on a failed try and block every retry from ever
        completing. `has_idempotency_receipt` skips the append if a prior
        attempt already succeeded (the crash-resume case); `RetryableError`
        on a transient `OSError` lets the node's `retry_policy` retry the
        write itself (the in-process case); the claim is only recorded once
        the write actually succeeds.
        """
        thread_id = state["thread_id"]
        idempotency_db = notes_dir / "idempotency.sqlite"
        work_object_id = state["work_object_id"]

        if has_idempotency_receipt(
            idempotency_db,
            thread_id=thread_id,
            work_object_id=work_object_id,
            effect_name="record_note",
        ):
            return {"note_recorded": True}

        log_path = notes_dir / f"{thread_id}.jsonl"
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write(
                    json.dumps(state.get("research_receipt", {}), default=_json_default)
                    + "\n"
                )
        except OSError as exc:
            raise RetryableError(f"note append failed: {exc}") from exc

        claim_idempotency_receipt(
            idempotency_db,
            thread_id=thread_id,
            work_object_id=work_object_id,
            effect_name="record_note",
        )
        return {"note_recorded": True}

    return research_record_note


def _make_record_note_error_handler(notes_dir: Path):
    """Build record_note's error_handler, closed over the same notes_dir.

    Fires once `record_note`'s `retry_policy` exhausts all attempts (WO
    2026-08-17-016 Decision 8) -- proven pattern (`test_phase7_tracer.py`'s
    `risky_effect_error_handler`): journal a distinct `record_note:failed`
    identity, never the `record_note` success identity, so an exhausted note
    append is visible in the effect journal instead of crashing the run.
    """

    def record_note_error_handler(state: ResearchState) -> dict:
        idempotency_db = notes_dir / "idempotency.sqlite"
        claim_idempotency_receipt(
            idempotency_db,
            thread_id=state["thread_id"],
            work_object_id=state["work_object_id"],
            effect_name="record_note:failed",
        )
        return {"note_recorded": False}

    return record_note_error_handler


def build_research_graph(checkpoint_db: Path, notes_dir: Optional[Path] = None):
    """Build the propose -> gate -> fetch -> record research graph; returns (graph, conn).

    `notes_dir` defaults to a sibling of `checkpoint_db` so callers get an
    isolated research-notes directory for free; pass explicitly to share one
    across separate checkpoint DBs.
    """
    recover_checkpoint_db(checkpoint_db)
    if notes_dir is None:
        notes_dir = checkpoint_db.parent / "research_notes"
    builder = StateGraph(ResearchState)
    builder.add_node("propose_fetch", research_propose_fetch)
    builder.add_node("gate_fetch", research_gate_fetch)
    builder.add_node("fetch_source", research_fetch_source)
    builder.add_node(
        "record_note",
        _make_research_record_note(notes_dir),
        retry_policy=RetryPolicy(max_attempts=3, retry_on=RetryableError),
        error_handler=_make_record_note_error_handler(notes_dir),
    )
    builder.add_edge(START, "propose_fetch")
    builder.add_edge("propose_fetch", "gate_fetch")
    builder.add_edge("gate_fetch", "fetch_source")
    builder.add_edge("fetch_source", "record_note")
    builder.add_edge("record_note", END)
    conn = sqlite3.connect(str(checkpoint_db), check_same_thread=False)
    saver = SqliteSaver(conn, serde=build_checkpoint_serializer())
    return builder.compile(checkpointer=saver), conn


def _research_config(thread_id: str) -> dict:
    return {"configurable": {"thread_id": thread_id}}


def run_research(
    work_object_id: str,
    thread_id: str,
    url: str,
    checkpoint_db: Path,
    approve: bool = False,
) -> dict:
    """Run the research graph once.

    `approve=False` (default): starts a fresh run, which pauses at
    `interrupt()` and performs no fetch. `approve=True`: resumes an existing
    paused thread with `Command(resume=True)`, approving the exact URL
    already proposed and checkpointed -- never re-proposes or re-asks.
    """
    graph, conn = build_research_graph(checkpoint_db)
    try:
        if approve:
            return graph.invoke(Command(resume=True), config=_research_config(thread_id))
        return graph.invoke(
            {"work_object_id": work_object_id, "thread_id": thread_id, "url": url},
            config=_research_config(thread_id),
        )
    finally:
        conn.close()


def inspect_research(thread_id: str, checkpoint_db: Path) -> dict:
    """Inspect the latest runtime checkpoint state for one research thread."""
    recovery = recover_checkpoint_db(checkpoint_db)
    summary = {"checkpoint_db": str(checkpoint_db), "recovery": recovery.status}
    if recovery.status != "usable" and not checkpoint_db.exists():
        return summary
    graph, conn = build_research_graph(checkpoint_db)
    try:
        snapshot = graph.get_state(_research_config(thread_id))
        values = snapshot.values or {}
        summary["thread_id"] = thread_id
        summary["url"] = values.get("url")
        summary["approved"] = values.get("approved", False)
        summary["has_receipt"] = bool(values.get("research_receipt"))
        summary["awaiting_approval"] = bool(snapshot.interrupts)
    finally:
        conn.close()
    return summary


# ═══════════════════════════════════════════════════════════════════════════════
# Phase 7 — error classes (WO 2026-08-17-016 Decisions 3-4, ADR 0026)
# ═══════════════════════════════════════════════════════════════════════════════

# Not yet wired to any real node. Declared here as reusable Phase 7
# primitives; retry_on's isinstance-based matching (confirmed directly
# against langgraph.pregel._retry._should_retry_on) means RetryPolicy(
# retry_on=RetryableError) retries RetryableError and its subclasses only --
# TerminalError and AuthorityRequiredError are unrelated sibling classes, so
# they propagate immediately with zero retries.


class RetryableError(Exception):
    """A node effect failed in a way that may succeed if attempted again."""


class TerminalError(Exception):
    """A node effect failed in a way retrying cannot fix."""


class AuthorityRequiredError(Exception):
    """A node effect was blocked pending human authority; not a retry condition."""


def _add_runtime_db_options(parser: argparse.ArgumentParser) -> None:
    db_group = parser.add_mutually_exclusive_group()
    db_group.add_argument("--checkpoint-db", default=None)
    db_group.add_argument(
        "--repo",
        help="Registry entry name (WO 2026-08-21-005); sets WS_REPO_ROOT "
             "for this invocation and resolves --checkpoint-db from "
             ".work-studio/repos.json if not also given explicitly",
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
    if args.repo:
        os.environ["WS_REPO_ROOT"] = str(_resolve_registry_repo_root(args.repo))
    checkpoint_db = Path(
        args.checkpoint_db
        or (_resolve_registry_checkpoint_db(args.repo) if args.repo
            else _default_checkpoint_db())
    )
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


def _split_semicolon_list(raw: str) -> list[str]:
    return [part.strip() for part in raw.split(";") if part.strip()] if raw else []


def main(argv: Optional[list[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    commands = {
        "run", "inspect", "resume", "fork", "backup", "restore",
        "run-phase6", "inspect-phase6", "fork-phase6",
        "run-research", "inspect-research",
        "run-business-router", "inspect-business-router",
    }
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
    inspect_db_group = inspect_parser.add_mutually_exclusive_group()
    inspect_db_group.add_argument("--checkpoint-db", default=None)
    inspect_db_group.add_argument(
        "--repo",
        help="Registry entry name to inspect (WO 2026-08-21-005); "
             "resolves --checkpoint-db from .work-studio/repos.json",
    )
    inspect_db_group.add_argument(
        "--repo-all", action="store_true",
        help="Inspect this thread_id against every registry entry",
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
        default=str(_default_checkpoint_db()),
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

    run_phase6_parser = subparsers.add_parser(
        "run-phase6", help="Run the Phase 6 two-branch/join graph"
    )
    run_phase6_parser.add_argument("work_object_id")
    run_phase6_parser.add_argument("thread_id")
    run_phase6_direction_group = run_phase6_parser.add_mutually_exclusive_group()
    run_phase6_direction_group.add_argument(
        "--resume", action="store_true",
        help="Resume from the checkpoint without fresh input",
    )
    run_phase6_direction_group.add_argument(
        "--approve-direction", action="store_true",
        help="Answer the direction_gate interrupt with approval",
    )
    run_phase6_direction_group.add_argument(
        "--reject-direction", action="store_true",
        help="Answer the direction_gate interrupt with rejection",
    )
    run_phase6_parser.add_argument(
        "--checkpoint-db",
        default=str(_default_checkpoint_db()),
    )

    inspect_phase6_parser = subparsers.add_parser(
        "inspect-phase6",
        help="Inspect one Phase 6 thread's runtime checkpoint state",
    )
    inspect_phase6_parser.add_argument("thread_id")
    inspect_phase6_parser.add_argument(
        "--checkpoint-db",
        default=str(_default_checkpoint_db()),
    )

    fork_phase6_parser = subparsers.add_parser(
        "fork-phase6",
        help=(
            "Copy a Phase 6 thread's latest checkpoint state into a sibling "
            "thread"
        ),
    )
    fork_phase6_parser.add_argument("source_thread_id")
    fork_phase6_parser.add_argument("new_thread_id")
    fork_phase6_parser.add_argument(
        "--checkpoint-db",
        default=str(_default_checkpoint_db()),
    )
    fork_phase6_parser.add_argument("--work-object-id")

    run_research_parser = subparsers.add_parser(
        "run-research", help="Run the single-URL, approval-gated research graph"
    )
    run_research_parser.add_argument("work_object_id")
    run_research_parser.add_argument("thread_id")
    run_research_parser.add_argument("--url", default="")
    run_research_parser.add_argument(
        "--approve", action="store_true",
        help="Resume a paused thread, approving its already-proposed URL",
    )
    run_research_parser.add_argument(
        "--checkpoint-db",
        default=str(_default_checkpoint_db()),
    )

    inspect_research_parser = subparsers.add_parser(
        "inspect-research",
        help="Inspect one research thread's runtime checkpoint state",
    )
    inspect_research_parser.add_argument("thread_id")
    inspect_research_parser.add_argument(
        "--checkpoint-db",
        default=str(_default_checkpoint_db()),
    )

    run_business_router_parser = subparsers.add_parser(
        "run-business-router",
        help="Run the checkpointed business operating router",
    )
    run_business_router_parser.add_argument("--work-object-id", required=True)
    run_business_router_parser.add_argument("--thread-id", required=True)
    run_business_router_parser.add_argument("--checkpoint-db", required=True)
    run_business_router_parser.add_argument("--lifecycle-state", default="build")
    run_business_router_parser.add_argument("--current-frontier", default="")
    run_business_router_parser.add_argument(
        "--from-skill", default="business-formulate-strategy"
    )
    run_business_router_parser.add_argument(
        "--evidence-resolved",
        default="",
        help="Semicolon-separated evidence already resolved by the current skill",
    )
    run_business_router_parser.add_argument(
        "--next-gap",
        default="",
        help="Specific business frontier to route on a fresh run",
    )
    run_business_router_parser.add_argument(
        "--linked-work-object",
        action="store_true",
        help="Propose the handoff against a linked Work Object instead of same WO",
    )
    run_business_router_parser.add_argument(
        "--authority-boundary", default="read-only-propose"
    )
    business_approval_group = (
        run_business_router_parser.add_mutually_exclusive_group()
    )
    business_approval_group.add_argument(
        "--approve",
        action="store_true",
        help="Resume a paused router thread and approve its handoff proposal",
    )
    business_approval_group.add_argument(
        "--reject",
        action="store_true",
        help="Resume a paused router thread and reject its handoff proposal",
    )

    inspect_business_router_parser = subparsers.add_parser(
        "inspect-business-router",
        help="Inspect one business-router thread's runtime checkpoint state",
    )
    inspect_business_router_parser.add_argument("--thread-id", required=True)
    inspect_business_router_parser.add_argument("--checkpoint-db", required=True)

    args = parser.parse_args(argv)

    if args.command == "run-phase6":
        approve_direction = (
            True if args.approve_direction
            else False if args.reject_direction
            else None
        )
        _print_json(
            run_phase6(
                args.work_object_id,
                args.thread_id,
                Path(args.checkpoint_db),
                resume=args.resume,
                approve_direction=approve_direction,
            )
        )
        return 0

    if args.command == "inspect-phase6":
        _print_json(inspect_phase6(args.thread_id, Path(args.checkpoint_db)))
        return 0

    if args.command == "fork-phase6":
        _print_json(
            fork_phase6_thread(
                args.source_thread_id,
                args.new_thread_id,
                Path(args.checkpoint_db),
                work_object_id=args.work_object_id,
            )
        )
        return 0

    if args.command == "run-research":
        _print_json(
            run_research(
                args.work_object_id,
                args.thread_id,
                args.url,
                Path(args.checkpoint_db),
                approve=args.approve,
            )
        )
        return 0

    if args.command == "inspect-research":
        _print_json(inspect_research(args.thread_id, Path(args.checkpoint_db)))
        return 0

    if args.command == "run-business-router":
        from runtime.business import run_business_router

        approve = True if args.approve else False if args.reject else None
        if approve is None and not args.next_gap:
            print(
                "Error: --next-gap is required for a fresh business-router run",
                file=sys.stderr,
            )
            return 2
        try:
            result = run_business_router(
                work_object_id=args.work_object_id,
                thread_id=args.thread_id,
                lifecycle_state=args.lifecycle_state,
                current_frontier=args.current_frontier,
                from_skill=args.from_skill,
                evidence_resolved=_split_semicolon_list(args.evidence_resolved),
                next_gap=args.next_gap,
                same_work_object=not args.linked_work_object,
                authority_boundary=args.authority_boundary,
                checkpoint_db=Path(args.checkpoint_db),
                approve=approve,
            )
        except Exception as exc:
            print(f"Error: business router failed: {exc}", file=sys.stderr)
            return 1
        _print_json(result)
        return 0

    if args.command == "inspect-business-router":
        from runtime.business import inspect_business_router

        _print_json(inspect_business_router(args.thread_id, Path(args.checkpoint_db)))
        return 0

    if args.command == "inspect":
        if args.repo_all:
            registry = _load_repo_registry()
            if not registry:
                _print_json({
                    "error": f"registry empty or not found at {_repo_registry_path()}"
                })
                return 1
            for name in sorted(registry):
                result = inspect_thread(
                    args.thread_id, _resolve_registry_checkpoint_db(name)
                )
                result["repo"] = name
                _print_json(result)
            return 0
        if args.repo:
            checkpoint_db = _resolve_registry_checkpoint_db(args.repo)
        else:
            checkpoint_db = Path(args.checkpoint_db or _default_checkpoint_db())
        _print_json(inspect_thread(args.thread_id, checkpoint_db))
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

    if getattr(args, "repo", None):
        os.environ["WS_REPO_ROOT"] = str(_resolve_registry_repo_root(args.repo))
    checkpoint_db = Path(
        args.checkpoint_db
        or (_resolve_registry_checkpoint_db(args.repo) if getattr(args, "repo", None)
            else _default_checkpoint_db())
    )
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
