#!/usr/bin/env python3
"""Figwright MCP capability probe.

Checks MCP connectivity, enumerates available Figwright tools, and classifies
capabilities against the design skill architecture's expectations.

This is a utility, not a skill. It runs before the tracer bullet (Phase 2)
to verify that Figwright's actual interface matches the assumptions in
ADR 0025 (Work Studio wraps Figwright).

Usage:
    python3 tools/figwright-probe.py [--json]

Without --json, prints a human-readable report.
With --json, outputs a machine-readable JSON summary.

Exit codes:
    0  All expected capabilities found
    1  Some capabilities missing or unavailable
    2  Figwright MCP not reachable
"""

import json
import sys


EXPECTED_CAPABILITIES = {
    "figma-build": {
        "description": "Create Figma pages from specifications",
        "required_by": ["render-to-figma"],
        "criticality": "required",
    },
    "figma-codegen": {
        "description": "Generate code from Figma designs",
        "required_by": ["connect-design-to-code"],
        "criticality": "required",
    },
    "component_map": {
        "description": "Map code components to Figma components",
        "required_by": ["connect-design-to-code"],
        "criticality": "required",
    },
    "token_map": {
        "description": "Map code tokens to Figma tokens",
        "required_by": ["render-to-figma"],
        "criticality": "required",
    },
    "design_diff": {
        "description": "Compare Figma output against specification",
        "required_by": ["verify-design-implementation"],
        "criticality": "optional",
    },
}

UNDOCUMENTED_BEHAVIORS = [
    "Branch creation — does Figwright support creating Figma branches?",
    "Node deletion — what happens when Figwright targets a deleted node?",
    "Node ID return — does figma-build return created node IDs?",
    "Content preservation — does updating a frame preserve child content?",
    "Section creation — can Figwright create sections within a page?",
]


def probe_figwright():
    """Probe Figwright MCP availability and capabilities.

    Returns a dict with:
        reachable: bool
        capabilities: dict of capability -> {found: bool, details: str}
        undocumented: list of behaviors to verify manually
    """
    result = {
        "reachable": False,
        "capabilities": {},
        "undocumented": UNDOCUMENTED_BEHAVIORS,
        "probe_method": "static",
    }

    for cap_name, cap_info in EXPECTED_CAPABILITIES.items():
        result["capabilities"][cap_name] = {
            "expected": True,
            "found": False,
            "criticality": cap_info["criticality"],
            "required_by": cap_info["required_by"],
            "description": cap_info["description"],
            "note": "Static probe — live verification requires MCP connection",
        }

    return result


def print_report(result):
    """Print a human-readable probe report."""
    print("Figwright MCP Capability Probe")
    print("=" * 50)
    print()

    if result["reachable"]:
        print("Status: CONNECTED")
    else:
        print("Status: NOT CONNECTED (static probe only)")
        print("  Connect Figwright MCP and re-run for live verification.")
    print()

    print("Expected Capabilities:")
    print("-" * 50)
    for cap_name, cap_info in result["capabilities"].items():
        status = "FOUND" if cap_info["found"] else "NOT VERIFIED"
        criticality = cap_info["criticality"].upper()
        print(f"  [{status}] {cap_name} ({criticality})")
        print(f"    {cap_info['description']}")
        print(f"    Required by: {', '.join(cap_info['required_by'])}")
    print()

    print("Undocumented Behaviors (verify in tracer bullet):")
    print("-" * 50)
    for behavior in result["undocumented"]:
        print(f"  [ ] {behavior}")
    print()

    found = sum(1 for c in result["capabilities"].values() if c["found"])
    total = len(result["capabilities"])
    print(f"Summary: {found}/{total} capabilities verified")
    if not result["reachable"]:
        print("Note: Live MCP connection required for full verification.")


def main():
    use_json = "--json" in sys.argv

    result = probe_figwright()

    if use_json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)

    if not result["reachable"]:
        sys.exit(2)

    all_found = all(
        c["found"]
        for c in result["capabilities"].values()
        if c["criticality"] == "required"
    )
    sys.exit(0 if all_found else 1)


if __name__ == "__main__":
    main()
