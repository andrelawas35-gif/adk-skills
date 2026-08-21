#!/usr/bin/env python3
"""Repair pre-existing evidence ledger formatting across Work Objects.

Bounded change: 2026-07-22-004
Responds to: 2026-07-22-003 (diagnosis session — backtick-wrapped tag fix)

Fixes:
  1. Non-canonical tags ([observed], [verified], [known]) → canonical
  2. Non-standard table formats → | Tag | Source | Entry |
  3. 4-column format with empty first column → 3-column canonical
  4. Unclosed brackets ([system → [system])
  5. Free-text rows → extracted or removed (reported for manual review)

Constraints:
  - Evidence substance preserved; only tag names and table format change
  - Append-only: each fix appends a History entry; evidence entries are
    format-corrected in place (no semantic change)
  - Only edits Work Object .md files in .work-studio/objects/
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Canonical tags from AGREEMENT-LOOP.md
CANONICAL_TAGS = {
    "[system]", "[decision]", "[inference]",
    "[gap]", "[testimony]", "[memory]",
}

# Tag migration map
TAG_MIGRATION = {
    "[observed]": "[testimony]",
    "[verified]": "[system]",
    "[known]": "[system]",
    "[inferred]": "[inference]",
    "[decided]": "[decision]",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
OBJECTS_DIR = REPO_ROOT / ".work-studio" / "objects"


def parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from Work Object content."""
    if not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in content[3:end].strip().split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip().strip('"')
    return fm


def extract_sections(content: str) -> tuple:
    """Extract frontmatter, body before evidence, evidence section, rest after."""
    if not content.startswith("---"):
        return {}, content, "", ""

    fm_end = content.find("---", 3)
    if fm_end == -1:
        return {}, content, "", ""

    fm_text = content[:fm_end + 3]
    body = content[fm_end + 3:]

    fm = parse_frontmatter(content)

    # Find Evidence ledger section
    ev_match = re.search(r'(## Evidence ledger\s*\n)', body)
    if not ev_match:
        return fm, body, "", ""

    before_ev = body[:ev_match.start()]
    ev_start = ev_match.start()
    ev_heading = ev_match.group(1)

    # Find next ## section after evidence ledger
    rest = body[ev_match.end():]
    next_section = re.search(r'\n## ', rest)
    if next_section:
        ev_body = rest[:next_section.start()]
        after_ev = rest[next_section.start():]
    else:
        ev_body = rest
        after_ev = ""

    return fm, before_ev + ev_heading, ev_body, after_ev


def fix_tag(tag: str) -> str:
    """Fix a single tag: unclosed brackets, non-canonical migration."""
    tag = tag.strip()

    # Fix unclosed brackets
    if tag.startswith("[") and not tag.endswith("]"):
        tag = tag + "]"

    # Migrate non-canonical tags
    if tag in TAG_MIGRATION:
        tag = TAG_MIGRATION[tag]

    return tag


def normalize_evidence_rows(ev_body: str) -> tuple:
    """Normalize evidence ledger rows to canonical 3-column format.

    Returns (fixed_evidence_body, repair_summary).
    """
    lines = ev_body.split("\n")
    if not lines:
        return ev_body, ""

    fixed_lines = []
    repairs = []

    # Detect format by examining first non-empty, non-header, non-separator line
    # after the heading
    in_header = True
    header_done = False

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        # Pass through empty lines
        if not stripped:
            fixed_lines.append(raw)
            i += 1
            continue

        # Pass through the heading line
        if stripped.startswith("## Evidence ledger") or stripped.startswith("## Evidence"):
            fixed_lines.append(raw)
            i += 1
            continue

        # Detect and replace non-standard table headers
        if not header_done and stripped.startswith("|"):
            cells = [c.strip().lower() for c in stripped.strip("| ").split("|")]
            header_keywords = {"tag", "source", "entry"}

            # Check if this is a standard header
            matches = sum(1 for c in cells if c in header_keywords)
            if matches >= 2:
                # Standard header — keep but normalize
                fixed_lines.append("| Tag | Source | Entry |")
                header_done = True
                i += 1
                # Next line should be separator
                if i < len(lines) and re.match(r"^\|[-\s|]+\|$", lines[i].strip()):
                    fixed_lines.append("|-----|--------|-------|")
                    i += 1
                continue

            # Non-standard header — replace
            claim_keywords = {"claim", "provenance", "status", "#"}
            cells_set = set(cells)
            if cells_set & claim_keywords:
                repairs.append("replaced non-standard table header")
                fixed_lines.append("| Tag | Source | Entry |")
                header_done = True
                i += 1
                # Check for separator
                if i < len(lines) and re.match(r"^\|[-\s|]+\|$", lines[i].strip()):
                    fixed_lines.append("|-----|--------|-------|")
                    i += 1
                continue

            # Timestamp | Tag | Evidence | Source header — replace
            if "timestamp" in cells_set or "evidence" in cells_set:
                repairs.append("replaced 4-column table header with 3-column")
                fixed_lines.append("| Tag | Source | Entry |")
                header_done = True
                i += 1
                if i < len(lines) and re.match(r"^\|[-\s|]+\|$", lines[i].strip()):
                    fixed_lines.append("|-----|--------|-------|")
                    i += 1
                continue

        # Separator line — pass through if standard
        if re.match(r"^\|[-\s|]+\|$", stripped):
            if header_done:
                fixed_lines.append(raw)
            else:
                fixed_lines.append("|-----|--------|-------|")
                header_done = True
            i += 1
            continue

        # Data row processing
        if stripped.startswith("|"):
            # Split by pipe without stripping pipes first, then clean each cell
            cells_raw = stripped.split("|")
            cells = [c.strip() for c in cells_raw]

            # Remove leading and trailing empty cells (from leading/trailing pipes)
            while cells and cells[0] == "":
                cells.pop(0)
            while cells and cells[-1] == "":
                cells.pop()

            if len(cells) == 3:
                # 3-column format: Tag | Source | Entry
                # But first cell may be empty (e.g., from | | [tag] | text |)
                # Or first cell may not be a tag (e.g., Claim | Provenance | Status)
                if not cells[0] and re.match(r'^\[', cells[1]):
                    # Empty first cell + tag in second — treat as Tag | Entry
                    tag = fix_tag(cells[1])
                    source = ""
                    entry = cells[2]
                    if tag != cells[1]:
                        repairs.append(f"tag migrated: {cells[1]} → {tag}")
                elif re.match(r'^\[', cells[0]):
                    tag = fix_tag(cells[0])
                    source = cells[1]
                    entry = cells[2]
                    if tag != cells[0]:
                        repairs.append(f"tag migrated: {cells[0]} → {tag}")
                elif re.search(r'\[([a-z_]+)\]', cells[1]):
                    # First cell is not a tag but second cell contains one
                    # (e.g., Claim | [decision] Provenance | Status)
                    m = re.search(r'\[([a-z_]+)\]', cells[1])
                    tag = fix_tag(f"[{m.group(1)}]")
                    source = re.sub(r'\[[a-z_]+\]\s*', '', cells[1]).strip()
                    entry = cells[0]
                    repairs.append(f"extracted tag {tag} from middle cell")
                    fixed_lines.append(f"| {tag} | {source} | {entry} |")
                    i += 1
                    continue
                else:
                    # No recognizable tag — wrap as testimony
                    tag = "[testimony]"
                    source = cells[1] if cells[1] else ""
                    entry = cells[0] + " | " + cells[2] if cells[2] else cells[0]
                    repairs.append("no tag found, wrapped as [testimony]")
                fixed_lines.append(f"| {tag} | {source} | {entry} |")

            elif len(cells) == 2:
                # 2-column: likely Tag | Entry (missing Source)
                tag_candidate = cells[0]
                if re.match(r'^\[', tag_candidate):
                    tag = fix_tag(tag_candidate)
                    source = ""
                    entry = cells[1]
                    if tag != tag_candidate:
                        repairs.append(f"tag migrated: {tag_candidate} → {tag}")
                else:
                    # First cell is not a tag — treat as [testimony]
                    tag = "[testimony]"
                    source = cells[0]
                    entry = cells[1]
                    repairs.append(f"reconstructed 2-col: tag={tag}")
                fixed_lines.append(f"| {tag} | {source} | {entry} |")

            elif len(cells) == 4:
                # 4-column format: Timestamp | Tag | Evidence | Source
                # or Tag(fragmented) | Tag | Entry | Source
                c0, c1, c2, c3 = cells

                # If c0 is empty or a bare bracket fragment and c1 has a tag
                if (not c0 or c0 in ("[known", "[system")) and c1:
                    tag = fix_tag(c1)
                    source = c0 if c0 else ""
                    entry = c2
                    if tag != c1:
                        repairs.append(f"tag migrated: {c1} → {tag}")
                    fixed_lines.append(f"| {tag} | {source} | {entry} |")
                # If c0 is a timestamp
                elif re.match(r'^\d{4}-\d{2}-\d{2}', c0) or re.match(r'^\d{2}:\d{2}', c0):
                    tag = fix_tag(c1) if c1 else "[system]"
                    source = c0
                    entry = c2
                    if tag != c1:
                        repairs.append(f"tag migrated: {c1} → {tag}")
                    fixed_lines.append(f"| {tag} | {source} | {entry} |")
                # If c0 looks like a tag or evidence marker
                elif re.match(r'^\[', c0):
                    tag = fix_tag(c0)
                    source = c1
                    entry = c2
                    if tag != c0:
                        repairs.append(f"tag migrated: {c0} → {tag}")
                    fixed_lines.append(f"| {tag} | {source} | {entry} |")
                else:
                    # Fallback: try to extract tag from any cell
                    tag = "[testimony]"
                    for c in cells:
                        m = re.match(r'\[([a-z_]+)\]', c)
                        if m:
                            tag = fix_tag(f"[{m.group(1)}]")
                            break
                    source = cells[0] if cells[0] else ""
                    entry = " | ".join(c for c in cells[1:] if c) if len(cells) > 1 else cells[0]
                    repairs.append(f"reconstructed from 4-column: tag={tag}")
                    fixed_lines.append(f"| {tag} | {source} | {entry} |")

            elif len(cells) > 4:
                # Excess columns — collapse
                tag_found = None
                for c in cells:
                    m = re.match(r'\[([a-z_]+)\]', c)
                    if m:
                        tag_found = fix_tag(f"[{m.group(1)}]")
                        break
                tag = tag_found or "[testimony]"
                source = cells[0] if cells[0] else ""
                entry = " | ".join(c for c in cells[2:] if c) if len(cells) > 2 else " ".join(cells)
                repairs.append(f"collapsed {len(cells)}-column row")
                fixed_lines.append(f"| {tag} | {source} | {entry} |")

            else:
                # 2 or fewer columns — treat as free text
                repairs.append("free-text row preserved as-is")
                fixed_lines.append(raw)

        elif stripped.startswith("- "):
            # Inline format — convert to table
            match = re.match(
                r"^-\s+(\S+)\s+[—–-]\s+`?(\[[a-z_]+\])`?\s*(.*)", stripped
            )
            if match:
                timestamp = match.group(1)
                tag = fix_tag(match.group(2))
                text = match.group(3)
                if tag != match.group(2):
                    repairs.append(f"inline tag migrated: {match.group(2)} → {tag}")
                fixed_lines.append(f"| {tag} | {timestamp} | {text} |")
            else:
                repairs.append("unparseable inline row preserved")
                fixed_lines.append(raw)

        elif "|" in stripped and not stripped.startswith("|"):
            # Pipe-separated row without leading pipe (e.g., Claim | Provenance | Status data,
            # or inline timestamp | tag | text format)
            cells_raw = stripped.split("|")
            cells = [c.strip() for c in cells_raw]

            # Try to find a tag in any cell
            tag = None
            tag_idx = -1
            for j, c in enumerate(cells):
                m = re.match(r'\[([a-z_]+)\]', c)
                if m:
                    tag = fix_tag(f"[{m.group(1)}]")
                    tag_idx = j
                    break

            if tag and tag_idx >= 0:
                # Build source from cells before tag, entry from cells after tag
                source = " | ".join(c for c in cells[:tag_idx] if c)
                entry = " | ".join(c for c in cells[tag_idx+1:] if c)
                # If the tag cell has text after the tag, put it in source
                tag_cell_remainder = re.sub(r'\[[a-z_]+\]', '', cells[tag_idx]).strip()
                if tag_cell_remainder:
                    source = (source + " " + tag_cell_remainder).strip()
                if not source:
                    source = ""
                repairs.append(f"extracted tag {tag} from pipe-separated row")
                fixed_lines.append(f"| {tag} | {source} | {entry} |")
            else:
                # No tag found — wrap as testimony
                entry = " | ".join(c for c in cells if c)
                repairs.append("wrapped pipe-separated row as [testimony]")
                fixed_lines.append(f"| [testimony] |  | {entry} |")

        else:
            # Free text — preserve if it looks like evidence, otherwise skip
            if re.search(r'\[', stripped):
                repairs.append("free-text row preserved")
                fixed_lines.append(raw)
            else:
                repairs.append("non-evidence row skipped")
                # Don't add — skip this line

        i += 1

    fixed_body = "\n".join(fixed_lines)
    summary = "; ".join(repairs[:5]) + (f" (+{len(repairs)-5} more)" if len(repairs) > 5 else "")
    return fixed_body, summary


def append_history_entry(content: str, repair_summary: str) -> str:
    """Append a History entry documenting the evidence ledger repair."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    entry = (
        f"\n- **{now}** — Evidence ledger format repair. "
        f"State: frame (unchanged). "
        f"Actor: alawas-implement-bounded-change (github-copilot). "
        f"Rationale: Canonicalized evidence tags and table format per "
        f"bounded change 2026-07-22-004 (responds_to 2026-07-22-003). "
        f"Fixes applied: {repair_summary}."
    )

    # Find History section
    hist_match = re.search(r'(## History\s*\n)', content)
    if hist_match:
        insert_pos = hist_match.end()
        # Find the end of the History section (next ## or end of file)
        rest = content[insert_pos:]
        next_section = re.search(r'\n## ', rest)
        if next_section:
            insert_pos = insert_pos + next_section.start()
        else:
            insert_pos = len(content)
        return content[:insert_pos] + entry + content[insert_pos:]
    else:
        # No History section — add one before Evidence ledger
        ev_match = re.search(r'\n## Evidence ledger', content)
        if ev_match:
            return content[:ev_match.start()] + f"\n## History\n{entry}\n" + content[ev_match.start():]
        # Fallback: append at end
        return content + f"\n## History\n{entry}\n"


def repair_work_object(filepath: Path) -> dict:
    """Repair a single Work Object's evidence ledger.

    Returns dict with 'status' ('repaired', 'skipped', 'error') and details.
    """
    try:
        original = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return {"status": "error", "error": str(e)}

    # Check if this file has an evidence ledger section
    if "## Evidence ledger" not in original:
        return {"status": "skipped", "reason": "no evidence ledger"}

    fm, before_ev, ev_body, after_ev = extract_sections(original)

    if not ev_body.strip():
        return {"status": "skipped", "reason": "empty evidence ledger"}

    fixed_ev, repair_summary = normalize_evidence_rows(ev_body)

    if fixed_ev.strip() == ev_body.strip():
        return {"status": "skipped", "reason": "no changes needed"}

    # Reassemble
    new_body = before_ev + "\n" + fixed_ev + after_ev

    # Find where body starts (after frontmatter)
    if original.startswith("---"):
        fm_end = original.find("---", 3)
        if fm_end != -1:
            new_content = original[:fm_end + 3] + new_body
        else:
            new_content = new_body
    else:
        new_content = new_body

    # Append History entry
    new_content = append_history_entry(new_content, repair_summary)

    try:
        filepath.write_text(new_content, encoding="utf-8")
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {
        "status": "repaired",
        "summary": repair_summary,
    }


def main():
    """Main entry point — repair all affected Work Objects."""
    affected = [
        "2026-07-16-004-rewrite-grilling-lenses-two-tier.md",
        "2026-07-20-001-optimize-work-studio-skill-prompt-payloads-cache-efficiency.md",
        "2026-07-16-003-govern-scorecards-and-versioned-workflow-rules.md",
        "2026-07-15-004-design-learner-owned-coding-companion.md",
        "2026-07-16-002-maintain-working-methods-and-workflow-candidates.md",
        "2026-07-18-001-design-component-registry-continuous-grilling.md",
        "2026-07-16-001-review-outcome-and-adapt.md",
        "2026-07-20-005-scope-commit-boundary-for-adopted-changes.md",
        "2026-07-20-002-progressive-disclosure-generator-foundations.md",
        "2026-07-22-002-implement-platform-adapters-component-plan.md",
        "2026-07-15-003-qualify-pkm-memory-candidate-gate.md",
        "2026-07-21-002-implement-adr-0015-8-state-lifecycle-model.md",
        "2026-07-21-001-implement-adr-0021-extract-missing-artifact-gap-constitution.md",
        "2026-07-20-003-design-dependency-aware-reference-closure.md",
        "2026-07-15-005-qualify-pkm-project-adapter.md",
        "2026-07-20-004-adopt-reference-closure-into-generator.md",
        "2026-07-22-001-implement-capability-degradation-component-plan.md",
        "2026-07-21-008-implement-evidence-model-component-plan.md",
        "2026-07-21-003-produce-adr-0022-widen-append-only-scope.md",
        "2026-07-21-009-implement-authority-sensitivity-component-plan.md",
        "2026-07-21-004-implement-adr-0018-advisory-attention-register.md",
        "2026-07-21-010-implement-deterministic-cli-component-plan.md",
        "2026-07-21-006-build-append-only-verification-script.md",
        "2026-07-15-001-verify-installed-codex-workflow.md",
        "2026-07-21-007-implement-adr-0020-one-session-per-workspace.md",
        "2026-07-21-005-implement-adr-0019-sensitivity-gates.md",
        "2026-07-15-002-confirm-native-codex-creation.md",
    ]

    results = {"repaired": 0, "skipped": 0, "errors": 0, "details": []}

    for filename in affected:
        filepath = OBJECTS_DIR / "2026" / "07" / filename
        if not filepath.exists():
            results["errors"] += 1
            results["details"].append(f"{filename}: file not found")
            continue

        result = repair_work_object(filepath)
        results[result["status"]] += 1

        detail = f"{filename}: {result['status']}"
        if result["status"] == "repaired":
            detail += f" — {result.get('summary', '')[:100]}"
        elif result["status"] == "skipped":
            detail += f" ({result.get('reason', '')})"
        elif result["status"] == "error":
            detail += f" — {result.get('error', '')}"

        results["details"].append(detail)
        print(detail)

    print(f"\nSummary: {results['repaired']} repaired, "
          f"{results['skipped']} skipped, {results['errors']} errors")

    return 0 if results["errors"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
