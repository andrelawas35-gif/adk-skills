#!/usr/bin/env python3
"""Deterministic CLI for Work Studio state file operations.

Entry point for python3 -m tools.ws <command>.
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from . import VERSION
from .attention import (
    check_attention_consistency,
    remove_active_entry,
    update_active_entry,
)
from .concurrency import check_concurrency
from .identity import ID_PATTERN, allocate_id, build_path
from .lifecycle import (
    check_gates_for_transition,
    get_close_route,
    validate_transition,
)
from .schema import (
    generate_frontmatter,
    parse_frontmatter,
    validate_campaign,
    validate_consequence,
    validate_sensitivity,
    validate_type,
)
from .sections import (
    append_to_section,
    check_append_only,
    generate_evidence_entry,
    generate_history_entry,
    get_section,
)
from .template import generate_body_template
from .validate import DEFAULT_CHECKS, CHECK_REGISTRY, run_checks


def _find_work_studio_root() -> Path:
    """Walk upward from CWD to find .work-studio/ directory."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent. "
        "Run 'ws init' first to bootstrap the workspace."
    )


def _resolve_object_file(objects_dir: Path, obj_id: str) -> Path:
    """Find a Work Object file by its ID anywhere under objects_dir.

    Raises FileNotFoundError if not found.
    """
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


def _write_object(file_path: Path, frontmatter: str, body: str) -> None:
    """Write frontmatter + body to a Work Object file."""
    file_path.write_text(frontmatter + "\n" + body)


def _get_updated_at(file_path: Path) -> str:
    """Extract updated_at from a Work Object's frontmatter."""
    content = file_path.read_text()
    fm = parse_frontmatter(content)
    return str(fm.get("updated_at", ""))


# ═══════════════════════════════════════════════════════════════════════════════
# ws create
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_create(args: argparse.Namespace) -> int:
    """Allocate ID, validate args, write Work Object file."""
    errors = []
    for validator, value, name in [
        (validate_type, args.type, "type"),
        (validate_consequence, args.consequence, "consequence"),
        (validate_sensitivity, args.sensitivity, "sensitivity"),
    ]:
        err = validator(value)
        if err:
            errors.append(err)

    if errors:
        for e in errors:
            print(f"Error: {e}", file=sys.stderr)
        return 1

    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    try:
        obj_id = allocate_id(objects_dir)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    target_path = build_path(objects_dir, obj_id, args.title)

    if target_path.exists():
        print(f"Error: Target file already exists: {target_path}", file=sys.stderr)
        return 1

    frontmatter = generate_frontmatter(
        obj_id=obj_id,
        title=args.title,
        obj_type=args.type,
        consequence=args.consequence,
        sensitivity=args.sensitivity,
    )
    body = generate_body_template(
        title=args.title,
        obj_type=args.type,
        consequence=args.consequence,
    )

    target_path.write_text(frontmatter + body)

    relative_path = target_path.relative_to(ws_root)
    print(f"Created: {relative_path}")
    print(f"ID: {obj_id}")

    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws members
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_members(args: argparse.Namespace) -> int:
    """List Work Objects sharing an exact campaign anchor."""
    err = validate_campaign(args.campaign)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"
    members = []
    if objects_dir.exists():
        for obj_file in sorted(objects_dir.rglob("*.md")):
            if not ID_PATTERN.match(obj_file.name):
                continue
            try:
                fm = parse_frontmatter(obj_file.read_text())
            except (OSError, ValueError) as e:
                print(
                    f"Error: Cannot inspect Work Object '{obj_file}': {e}",
                    file=sys.stderr,
                )
                return 1
            if fm.get("campaign") == args.campaign:
                members.append((
                    str(fm.get("id", obj_file.stem)),
                    str(fm.get("title", obj_file.stem)),
                ))

    for obj_id, title in sorted(members):
        print(f"{obj_id} — {title}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws set-campaign
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_set_campaign(args: argparse.Namespace) -> int:
    """Assign a campaign anchor to an existing Work Object."""
    err = validate_campaign(args.campaign)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"
    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    err = check_concurrency(obj_file, args.expect_updated)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()
    fm = parse_frontmatter(content)
    if fm.get("campaign") == args.campaign:
        print(f"Campaign unchanged for {args.id}: {args.campaign}")
        return 0

    body = (
        content[content.find("---", 3) + 3:].strip()
        if content.startswith("---")
        else content
    )
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {
        "campaign": args.campaign,
        "updated_at": now,
    })
    history_entry = generate_history_entry(
        action=f"Campaign set: {args.campaign}",
        state=str(fm.get("state", "")),
        status=str(fm.get("status", "")),
        actor=args.actor,
        rationale=args.rationale,
    )
    new_body = append_to_section(body, "history", history_entry)
    obj_file.write_text(new_fm + "\n" + new_body.rstrip("\n") + "\n")

    print(f"Campaign set for {args.id}: {args.campaign}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws transition
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_transition(args: argparse.Namespace) -> int:
    """Validate and execute a state/status transition."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Optimistic concurrency check
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()
    fm = parse_frontmatter(content)

    from_state = str(fm.get("state", ""))
    from_status = str(fm.get("status", ""))
    consequence = str(fm.get("consequence", "meaningful"))

    # Validate transition
    err = validate_transition(from_state, args.state, from_status, args.status)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    # Check gates
    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content
    gate_passed, gate_msg = check_gates_for_transition(body, args.state, consequence)
    if not gate_passed:
        print(f"Error: {gate_msg}", file=sys.stderr)
        return 1

    # Update frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {
        "state": args.state,
        "status": args.status,
        "updated_at": now,
    })

    # Append history entry
    history_entry = generate_history_entry(
        action=args.action,
        state=args.state,
        status=args.status,
        actor=args.actor,
        rationale=args.rationale,
    )
    new_body = append_to_section(body, "history", history_entry)

    obj_file.write_text(new_fm + "\n" + new_body)

    print(f"Transitioned {args.id}: {from_state}/{from_status} → {args.state}/{args.status}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws close
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_close(args: argparse.Namespace) -> int:
    """Consequence-scaled closure."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Optimistic concurrency
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()
    fm = parse_frontmatter(content)

    from_state = str(fm.get("state", ""))
    consequence = str(fm.get("consequence", "meaningful"))

    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content

    # Determine close route
    route = get_close_route(consequence, from_state)
    if route == "two-step":
        print(
            f"Error: High-consequence objects must first transition to 'close' state "
            f"before setting status: closed. Current state: '{from_state}'.",
            file=sys.stderr,
        )
        print("Run: ws transition <id> --state close --status active ...", file=sys.stderr)
        return 1

    # Check close gate (bypassed by --force for legacy grandfathering)
    gate_passed, gate_msg = check_gates_for_transition(body, "close", consequence)
    if not gate_passed:
        if args.force:
            print(
                f"Warning: Close gate bypassed (--force): {gate_msg}",
                file=sys.stderr,
            )
        else:
            print(f"Error: {gate_msg}", file=sys.stderr)
            return 1

    # Close: set status to closed
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {
        "status": "closed",
        "updated_at": now,
    })

    # Append history
    history_entry = generate_history_entry(
        action=f"Closed: {args.rationale}",
        state=from_state,
        status="closed",
        actor=args.actor if hasattr(args, "actor") else "system",
        rationale=args.rationale,
    )
    new_body = append_to_section(body, "history", history_entry)

    obj_file.write_text(new_fm + "\n" + new_body)

    # Remove from active.md
    active_md = ws_root / ".work-studio" / "active.md"
    if active_md.exists():
        updated_active = remove_active_entry(active_md, args.id)
        if updated_active is not None:
            active_md.write_text(updated_active)

    print(f"Closed {args.id}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws activate
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_activate(args: argparse.Namespace) -> int:
    """Update active.md entry for a Work Object."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    # Cross-check: object must exist
    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Cross-check: object must not be closed
    content = obj_file.read_text()
    fm = parse_frontmatter(content)
    if str(fm.get("status", "")) == "closed":
        print(
            f"Error: Cannot activate closed object {args.id}",
            file=sys.stderr,
        )
        return 1

    title = str(fm.get("title", args.id))

    # Optimistic concurrency on the object file
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    # Update active.md
    active_md = ws_root / ".work-studio" / "active.md"
    updated = update_active_entry(active_md, args.id, title, args.role)
    active_md.write_text(updated)

    print(f"Activated {args.id} as {args.role}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws append-evidence
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_append_evidence(args: argparse.Namespace) -> int:
    """Append a tagged evidence entry (Tier B)."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Optimistic concurrency
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()
    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content

    # Generate evidence entry
    try:
        entry = generate_evidence_entry(args.tag, args.source, args.text,
                                         sha=getattr(args, 'sha', None))
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Append-only check
    if not check_append_only(body, "evidence ledger", entry):
        print(
            f"Warning: Evidence entry may duplicate existing content. "
            f"Proceeding (append-only structural check passed).",
            file=sys.stderr,
        )

    # Append
    new_body = append_to_section(body, "evidence ledger", entry)

    # Update frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {"updated_at": now})

    obj_file.write_text(new_fm + "\n" + new_body)

    print(f"Evidence appended to {args.id}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws append-history
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_append_history(args: argparse.Namespace) -> int:
    """Append a history entry (Tier B)."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"

    try:
        obj_file = _resolve_object_file(objects_dir, args.id)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    # Optimistic concurrency
    err = check_concurrency(obj_file, args.expect_updated, force=args.force)
    if err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    content = obj_file.read_text()
    body = content[content.find("---", 3) + 3:].strip() if content.startswith("---") else content

    # Generate history entry
    entry = generate_history_entry(
        action=args.action,
        state=args.state,
        status=args.status,
        actor=args.actor,
        rationale=args.rationale,
        commit=getattr(args, 'commit', None),
    )

    # Append
    new_body = append_to_section(body, "history", entry)

    # Update frontmatter
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_fm = _update_frontmatter_fields(content, {"updated_at": now})

    obj_file.write_text(new_fm + "\n" + new_body)

    print(f"History appended to {args.id}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# ws validate
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_validate(args: argparse.Namespace) -> int:
    """Run composed validation checks."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    objects_dir = ws_root / ".work-studio" / "objects"
    active_md = ws_root / ".work-studio" / "active.md"

    # Determine file paths
    if args.files:
        file_paths = [Path(f).resolve() for f in args.files]
    else:
        file_paths = []
        if objects_dir.exists():
            for year_dir in objects_dir.iterdir():
                if not year_dir.is_dir():
                    continue
                for month_dir in year_dir.iterdir():
                    if not month_dir.is_dir():
                        continue
                    for obj_file in month_dir.iterdir():
                        if obj_file.suffix == ".md":
                            file_paths.append(obj_file)

    if not file_paths:
        print("No Work Objects found to validate.", file=sys.stderr)
        return 0

    # Determine checks
    check_names = args.checks if args.checks else None

    return run_checks(check_names, file_paths, active_md, objects_dir)


# ═══════════════════════════════════════════════════════════════════════════════
# ws init
# ═══════════════════════════════════════════════════════════════════════════════


def cmd_init(args: argparse.Namespace) -> int:
    """Idempotent workspace bootstrap."""
    cwd = Path.cwd().resolve()
    ws_root = cwd

    ws_dir = ws_root / ".work-studio"

    if ws_dir.exists() and (ws_dir / "config.md").exists():
        print(f"Workspace already initialized at {ws_dir}")
        return 0

    ws_dir.mkdir(parents=True, exist_ok=True)
    (ws_dir / "objects").mkdir(exist_ok=True)

    # Config
    config = (
        f"# Work Studio Configuration\n\n"
        f"workspace_name: {args.name}\n"
        f"created_at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"cli_version: {VERSION}\n"
    )
    (ws_dir / "config.md").write_text(config)

    # Active register
    (ws_dir / "active.md").write_text("# Active Work Objects\n\n")

    # Inbox
    (ws_dir / "inbox.md").write_text("# Inbox\n\n")

    print(f"Initialized workspace '{args.name}' at {ws_dir}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# Frontmatter helper
# ═══════════════════════════════════════════════════════════════════════════════


def _update_frontmatter_fields(content: str, updates: dict) -> str:
    """Update specific fields in the YAML frontmatter block.

    Args:
        content: Full file content including frontmatter.
        updates: Dict of field_name → new_value.

    Returns:
        Updated full content with modified frontmatter.
    """
    if not content.startswith("---"):
        return content

    end = content.find("---", 3)
    if end == -1:
        return content

    fm_text = content[4:end]

    lines = fm_text.split("\n")
    new_lines = []
    updated_keys = set()

    for line in lines:
        stripped = line.strip()
        if ":" in stripped and not stripped.startswith("#"):
            key = stripped.split(":", 1)[0].strip()
            if key in updates:
                new_lines.append(f"{key}: {updates[key]}")
                updated_keys.add(key)
                continue
        new_lines.append(line)

    # Add any new fields not found
    for key, val in updates.items():
        if key not in updated_keys:
            new_lines.append(f"{key}: {val}")

    new_fm = "\n".join(new_lines)
    return "---\n" + new_fm + "\n---"


# ═══════════════════════════════════════════════════════════════════════════════
# Parser and main
# ═══════════════════════════════════════════════════════════════════════════════


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the ws CLI."""
    parser = argparse.ArgumentParser(
        prog="ws",
        description="Deterministic CLI for Work Studio state file operations.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"ws {VERSION}",
    )

    subparsers = parser.add_subparsers(dest="command", title="commands")

    # ── ws init ───────────────────────────────────────────────────────────
    init_parser = subparsers.add_parser("init", help="Bootstrap a new workspace")
    init_parser.add_argument("--name", required=True, help="Workspace name")

    # ── ws create ─────────────────────────────────────────────────────────
    create_parser = subparsers.add_parser("create", help="Create a new Work Object")
    create_parser.add_argument("--title", required=True, help="Work Object title")
    create_parser.add_argument(
        "--type", required=True,
        choices=["change", "inquiry", "project", "incident"],
        help="Work Object type",
    )
    create_parser.add_argument(
        "--consequence", required=True,
        choices=["low", "meaningful", "high"],
        help="Consequence level (required, no default per Decision 58)",
    )
    create_parser.add_argument(
        "--sensitivity", required=True,
        choices=["ordinary", "restricted"],
        help="Sensitivity classification",
    )

    # ── ws members ────────────────────────────────────────────────────────
    members_parser = subparsers.add_parser(
        "members",
        help="List Work Objects sharing a campaign anchor",
    )
    members_parser.add_argument(
        "campaign",
        help="Repository-relative docs/design/*.md campaign anchor",
    )

    # ── ws set-campaign ───────────────────────────────────────────────────
    set_campaign_parser = subparsers.add_parser(
        "set-campaign",
        help="Assign a campaign anchor to an existing Work Object",
    )
    set_campaign_parser.add_argument("id", help="Work Object ID")
    set_campaign_parser.add_argument(
        "campaign",
        help="Repository-relative docs/design/*.md campaign anchor",
    )
    set_campaign_parser.add_argument(
        "--expect-updated",
        required=True,
        help="Expected updated_at timestamp",
    )
    set_campaign_parser.add_argument(
        "--actor",
        default="system",
        help="Actor identifier",
    )
    set_campaign_parser.add_argument(
        "--rationale",
        default="Campaign assigned through ws set-campaign.",
        help="History rationale",
    )

    # ── ws transition ─────────────────────────────────────────────────────
    trans_parser = subparsers.add_parser("transition", help="Transition state/status")
    trans_parser.add_argument("id", help="Work Object ID")
    trans_parser.add_argument(
        "--state", required=True,
        choices=["notice", "explore", "design", "build", "verify",
                 "release", "observe", "close"],
        help="Target state",
    )
    trans_parser.add_argument(
        "--status", required=True,
        choices=["active", "waiting", "paused", "closed"],
        help="Target status",
    )
    trans_parser.add_argument(
        "--expect-updated", required=True,
        help="Expected updated_at timestamp for optimistic concurrency",
    )
    trans_parser.add_argument("--action", required=True, help="Action description")
    trans_parser.add_argument("--actor", default="system", help="Actor identifier")
    trans_parser.add_argument("--rationale", required=True, help="Transition rationale")
    trans_parser.add_argument(
        "--force", action="store_true",
        help="Bypass optimistic concurrency check (with warning)",
    )

    # ── ws close ──────────────────────────────────────────────────────────
    close_parser = subparsers.add_parser("close", help="Close a Work Object")
    close_parser.add_argument("id", help="Work Object ID")
    close_parser.add_argument(
        "--expect-updated", required=True,
        help="Expected updated_at timestamp",
    )
    close_parser.add_argument("--rationale", required=True, help="Closure rationale")
    close_parser.add_argument("--actor", default="system", help="Actor identifier")
    close_parser.add_argument("--force", action="store_true",
                              help="Bypass optimistic concurrency and close gate (grandfathering)")

    # ── ws activate ───────────────────────────────────────────────────────
    activate_parser = subparsers.add_parser("activate", help="Update active.md entry")
    activate_parser.add_argument("id", help="Work Object ID")
    activate_parser.add_argument(
        "--role", required=True,
        choices=["primary", "supporting", "paused"],
        help="Active role",
    )
    activate_parser.add_argument(
        "--expect-updated", required=True,
        help="Expected updated_at timestamp",
    )
    activate_parser.add_argument("--force", action="store_true",
                                 help="Bypass optimistic concurrency check")

    # ── ws append-evidence ────────────────────────────────────────────────
    append_evidence_parser = subparsers.add_parser(
        "append-evidence", help="Append an evidence entry (Tier B)"
    )
    append_evidence_parser.add_argument("id", help="Work Object ID")
    append_evidence_parser.add_argument("--tag", required=True, help="Evidence tag")
    append_evidence_parser.add_argument("--text", required=True, help="Evidence text")
    append_evidence_parser.add_argument("--source", required=True, help="Evidence source")
    append_evidence_parser.add_argument("--sha", default=None, help="Git commit SHA (optional, [system] only per ADR 0023)")
    append_evidence_parser.add_argument(
        "--expect-updated", required=True,
        help="Expected updated_at timestamp",
    )
    append_evidence_parser.add_argument("--force", action="store_true",
                                        help="Bypass optimistic concurrency check")

    # ── ws append-history ─────────────────────────────────────────────────
    append_history_parser = subparsers.add_parser(
        "append-history", help="Append a history entry (Tier B)"
    )
    append_history_parser.add_argument("id", help="Work Object ID")
    append_history_parser.add_argument("--action", required=True, help="Action description")
    append_history_parser.add_argument(
        "--state", required=True,
        choices=["notice", "explore", "design", "build", "verify",
                 "release", "observe", "close"],
        help="Current state",
    )
    append_history_parser.add_argument(
        "--status", required=True,
        choices=["active", "waiting", "paused", "closed"],
        help="Current status",
    )
    append_history_parser.add_argument("--actor", default="system", help="Actor identifier")
    append_history_parser.add_argument("--rationale", required=True, help="Entry rationale")
    append_history_parser.add_argument("--commit", default=None, help="Git commit SHA (optional, per ADR 0023)")
    append_history_parser.add_argument(
        "--expect-updated", required=True,
        help="Expected updated_at timestamp",
    )
    append_history_parser.add_argument("--force", action="store_true",
                                       help="Bypass optimistic concurrency check")

    # ── ws validate ───────────────────────────────────────────────────────
    validate_parser = subparsers.add_parser("validate", help="Run validation checks")
    validate_parser.add_argument(
        "checks", nargs="*",
        help=f"Named checks to run (default: all — {' '.join(DEFAULT_CHECKS)})",
    )
    validate_parser.add_argument(
        "--files", nargs="*",
        help="File paths to validate (default: all objects)",
    )

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 1

    commands = {
        "init": cmd_init,
        "create": cmd_create,
        "members": cmd_members,
        "set-campaign": cmd_set_campaign,
        "transition": cmd_transition,
        "close": cmd_close,
        "activate": cmd_activate,
        "append-evidence": cmd_append_evidence,
        "append-history": cmd_append_history,
        "validate": cmd_validate,
    }

    if args.command in commands:
        return commands[args.command](args)

    print(f"Unknown command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
