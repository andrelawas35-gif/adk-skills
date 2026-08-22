"""ws engineering-handoff: inspect / approve / reject proposed engineering handoffs.

Successor tracer for Work Object ``2026-08-22-025``. Reads the verified Phase 6
engineering dispatch payloads (``engineering_handoff_envelope`` /
``engineering_route_result``) through ``runtime.graph.inspect_phase6`` and
records the director's approve/reject decision via the governance append path
(History + Evidence ledger). No dispatch or schema changes; ``runtime`` is
imported lazily so this module (and ``tools/ws``) stays importable without it.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from .atomic import atomic_write_text
from .concurrency import check_concurrency
from .schema import parse_frontmatter
from .sections import (
    append_to_section,
    compose_object_text,
    generate_evidence_entry,
    generate_history_entry,
)


def _find_work_studio_root() -> Path:
    """Walk upward from CWD to find .work-studio/ (mirrors __main__)."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent. "
        "Run 'ws init' first to bootstrap the workspace."
    )


def _resolve_object_file(objects_dir: Path, obj_id: str) -> Path:
    """Find a Work Object file by its ID anywhere under objects_dir."""
    for year_dir in objects_dir.iterdir():
        if not year_dir.is_dir():
            continue
        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            for obj_file in month_dir.iterdir():
                if obj_file.name.startswith(obj_id) and obj_file.suffix == ".md":
                    return obj_file
    raise FileNotFoundError(f"Work Object not found for ID: {obj_id}")


def _read_object(ws_root: Path, obj_id: str):
    objects_dir = ws_root / ".work-studio" / "objects"
    obj_file = _resolve_object_file(objects_dir, obj_id)
    content = obj_file.read_text(encoding="utf-8")
    return obj_file, content, parse_frontmatter(content)


def _body_text(content: str) -> str:
    """Return the body text after the frontmatter block."""
    if not content.startswith("---"):
        return content.strip()
    end = content.find("---", 3)
    return content[end + 3:].strip() if end != -1 else content.strip()


def _update_updated_at(content: str, new_value: str) -> str:
    """Replace the updated_at line inside the YAML frontmatter block."""
    if not content.startswith("---"):
        return content
    end = content.find("---", 3)
    if end == -1:
        return content
    fm_text = content[4:end]
    new_lines = []
    for line in fm_text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("updated_at:"):
            new_lines.append(f"updated_at: {new_value}")
        else:
            new_lines.append(line)
    return content[:4] + "\n".join(new_lines) + content[end:]


def _phase6_summary(thread_id: str, checkpoint_db: Path) -> dict:
    """Read the Phase 6 checkpoint through the verified runtime helper."""
    try:
        from runtime.graph import inspect_phase6  # lazy: runtime not always present
    except ImportError as e:  # pragma: no cover - depends on environment
        raise FileNotFoundError(
            f"runtime module is not importable here ({e}); "
            "engineering-handoff needs the Work Studio runtime present."
        ) from e
    return inspect_phase6(thread_id, checkpoint_db)


def _is_engineering_scoped(fm: dict) -> bool:
    """Explicit engineering_scope metadata only (mirrors runtime dispatch)."""
    return bool(fm.get("engineering_scope", False))


def cmd_engineering_handoff(args) -> int:
    """Dispatch ws engineering-handoff inspect|approve|reject."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    try:
        obj_file, content, fm = _read_object(ws_root, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    checkpoint_db = Path(args.checkpoint_db) if args.checkpoint_db else (
        ws_root / "runtime" / "checkpoints" / "tracer.sqlite"
    )
    thread_id = args.thread_id or args.id

    if args.handoff_command == "inspect":
        return _do_inspect(obj_file, fm, thread_id, checkpoint_db)
    if args.handoff_command in ("approve", "reject"):
        return _do_decision(
            obj_file, content, fm, thread_id, checkpoint_db, args.handoff_command
        )
    print(f"Error: unknown engineering-handoff command '{args.handoff_command}'",
          file=sys.stderr)
    return 1


def _do_inspect(obj_file: Path, fm: dict, thread_id: str, checkpoint_db: Path) -> int:
    """Read-only print of the proposed engineering handoff, if any."""
    wo_stem = obj_file.stem
    if not _is_engineering_scoped(fm):
        print(f"{wo_stem}: not engineering-scoped (engineering_scope absent/false).")
        return 0
    try:
        summary = _phase6_summary(thread_id, checkpoint_db)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    print(f"Work Object: {wo_stem}")
    print(f"thread_id: {thread_id}")
    print(f"checkpoint_db: {checkpoint_db}")
    if not summary.get("has_engineering_handoff_envelope"):
        print("no proposed engineering handoff "
              "(engineering_handoff_envelope absent in checkpoint)")
        return 0
    route = summary.get("engineering_route_result") or {}
    print("engineering handoff proposed:")
    print(f"  owning_skill: {route.get('owning_skill')}")
    if route.get("route_step"):
        print(f"  route_step: {route.get('route_step')}")
    print(f"  has_engineering_handoff_envelope: "
          f"{summary.get('has_engineering_handoff_envelope')}")
    print(f"  has_dispatch_envelope: {summary.get('has_envelope')}")
    return 0


def _do_decision(
    obj_file: Path,
    content: str,
    fm: dict,
    thread_id: str,
    checkpoint_db: Path,
    decision: str,
) -> int:
    """Approve or reject the proposed engineering handoff (governance record)."""
    wo_stem = obj_file.stem
    past = {"approve": "approved", "reject": "rejected"}.get(decision, decision)
    if not _is_engineering_scoped(fm):
        print(f"Error: {wo_stem} is not engineering-scoped; nothing to {decision}.",
              file=sys.stderr)
        return 1
    try:
        summary = _phase6_summary(thread_id, checkpoint_db)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    if not summary.get("has_engineering_handoff_envelope"):
        print(f"Error: no proposed engineering handoff to {decision} for "
              f"{wo_stem} (thread {thread_id}).", file=sys.stderr)
        return 1
    route = summary.get("engineering_route_result") or {}
    owning_skill = route.get("owning_skill") or "unknown"

    # Governance append: current updated_at read fresh, concurrency-checked.
    current_updated = str(fm.get("updated_at", ""))
    err = check_concurrency(obj_file, current_updated)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    history = generate_history_entry(
        action=f"Engineering handoff {past} (to {owning_skill})",
        state=str(fm.get("state", "")),
        status=str(fm.get("status", "")),
        actor="director",
        rationale=(
            f"Director {past} the proposed engineering handoff for "
            f"thread {thread_id}, routed to {owning_skill}."
        ),
    )
    evidence = generate_evidence_entry(
        tag="[decision]",
        source=f"ws engineering-handoff {decision}",
        text=f"Engineering handoff {past} (thread {thread_id}, "
             f"routed to {owning_skill}) on {now}.",
    )

    body = _body_text(content)
    new_body = append_to_section(body, "history", history)
    new_body = append_to_section(new_body, "evidence ledger", evidence)
    new_fm = _update_updated_at(content, now)
    atomic_write_text(obj_file, compose_object_text(new_fm, new_body))
    print(f"Engineering handoff {past} for {wo_stem} (to {owning_skill}).")
    return 0
