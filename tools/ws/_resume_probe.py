"""Throwaway read-only resume-work ranking probe (WO 2026-08-10-001, Decision 10).

Tests the riskiest assumption of the resume-work skill: a frontmatter reader
that treats quoted and bare values identically ranks the live object tree
correctly — yielding the same single candidate a director would pick by hand,
plus accurate standing lines.

Read-only. Writes nothing, to any path, under any condition. Deleted after
verification.
"""

from __future__ import annotations

import glob
from collections import Counter
from pathlib import Path

from tools.ws.schema import parse_frontmatter

OBJECTS_DIR = Path(".work-studio/objects")
ACTIVE_MD = Path(".work-studio/active.md")
FORWARD_MOTION_STATES = ("notice", "explore", "design", "build")
NON_FORWARD_STATES = ("verify", "observe", "release")


def iter_object_files():
    for f in sorted(OBJECTS_DIR.glob("**/*.md")):
        yield f


def read_object(f: Path):
    """Return (obj_id, frontmatter dict, parse_error-or-None)."""
    try:
        text = f.read_text(encoding="utf-8")
        if not text.startswith("---"):
            return None, {}, "no frontmatter"
        fm = parse_frontmatter(text)
        return str(fm.get("id", "")), fm, None
    except Exception as exc:  # noqa: BLE001 - probe reports and continues
        return None, {}, str(exc)


def main():
    records = []
    parse_gaps = []
    for f in iter_object_files():
        obj_id, fm, err = read_object(f)
        if err:
            parse_gaps.append((f.name, err))
            continue
        records.append((obj_id, fm))

    status = {i: str(fm.get("status", "")).strip() for i, fm in records}
    state = {i: str(fm.get("state", "")).strip() for i, fm in records}
    next_action = {i: str(fm.get("next_action", "") or "").strip() for i, fm in records}
    updated = {i: str(fm.get("updated_at", "") or "").strip() for i, fm in records}
    created = {i: str(fm.get("created_at", "") or "").strip() for i, fm in records}

    active = [i for i, s in status.items() if s == "active"]
    unclosed_count = len(active)

    # Standing line 1: unclosed count (active objects).
    print(f"unclosed count: {unclosed_count}")

    # Standing line 2: oldest untouched (earliest updated_at among active).
    dated_active = [(i, updated[i]) for i in active if updated[i]]
    if dated_active:
        oldest = min(dated_active, key=lambda kv: kv[1])
        print(f"oldest untouched: {oldest[0]} (updated {oldest[1]})")
    else:
        print("oldest untouched: none (no active object has updated_at)")

    # Standing line 3: active.md drift (active objects absent from the register).
    register_ids = set()
    if ACTIVE_MD.exists():
        for line in ACTIVE_MD.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if "`20" in line and "-" in line:
                # e.g. - `2026-08-09-009` — title
                start = line.find("`") + 1
                end = line.find("`", start)
                if start > 0 and end > start:
                    register_ids.add(line[start:end])
    absent = sorted(set(active) - register_ids)
    print(f"active.md drift: {len(absent)} active objects absent from register")

    # Forward-motion candidates.
    forward = [i for i in active if state.get(i) in FORWARD_MOTION_STATES]
    disqualified = [i for i in forward if not next_action.get(i)]
    eligible = [i for i in forward if next_action.get(i)]
    eligible_sorted = sorted(eligible, key=lambda i: updated.get(i, ""), reverse=True)

    # Rank order (all forward-motion, most recently touched first).
    print("forward-motion (ranked by updated_at):")
    for i in sorted(forward, key=lambda i: updated.get(i, ""), reverse=True):
        tag = "DISQUALIFIED" if not next_action.get(i) else "eligible"
        print(f"  {tag:<12} {i:<16} {state.get(i):<8} updated={updated.get(i)}")

    # Candidate.
    print("candidate:")
    if eligible_sorted:
        c = eligible_sorted[0]
        print(f"  {c}  state={state.get(c)}  next_action={next_action.get(c)[:60]}")
    else:
        print("  no candidate — all forward-motion objects are disqualified")
        for i in sorted(forward, key=lambda i: updated.get(i, ""), reverse=True):
            print(f"    disqualified: {i} (state={state.get(i)}, empty next_action)")

    # Disqualification detail.
    if disqualified:
        print("disqualified (empty next_action, reported by name):")
        for i in sorted(disqualified, key=lambda i: updated.get(i, ""), reverse=True):
            print(f"  {i}  state={state.get(i)}")

    if parse_gaps:
        print("parse gaps (reported by name):")
        for name, err in parse_gaps:
            print(f"  {name}: {err}")

    # Active-by-state summary for cross-check.
    print("active by state:", dict(Counter(state.get(i, "") for i in active)))


if __name__ == "__main__":
    main()
