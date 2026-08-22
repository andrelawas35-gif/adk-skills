"""MCP server exposing Work Studio's tools/ws operations to MCP clients.

WO 2026-08-21-010, Decision 1: a new sibling package depending on tools.ws
as an ordinary library import, plus mcp as its only new dependency -- not
inside tools/ws (would break its dependencies=[] contract), not folded into
runtime/ (wrong conceptual surface).

Exposes exactly one tool -- ws_validate -- the safe, read-only operation
this Work Object's tracer bullets already proved works end-to-end. Which
further tools/ws subcommands should be exposed, and how authority/
consequence gating should work for an external MCP client invoking a
mutating one (create, transition, close, append-*), is an explicitly
unresolved decision (named in this WO's own deliverable report,
.work-studio/deliverables/2026-08-21-010-mcp-server-report.md) -- not
silently decided here. Do not add a mutating tool without that decision
first.
"""
import contextlib
import glob
import io
import sys

from mcp.server.mcpserver import MCPServer

from tools.ws.__main__ import main as ws_main

server = MCPServer("work-studio-mcp")


def _find_work_object_file(work_object_id: str) -> str | None:
    matches = glob.glob(f".work-studio/objects/*/*/{work_object_id}-*.md")
    return matches[0] if matches else None


@server.tool()
def ws_validate(work_object_id: str) -> str:
    """Validate one Work Object by ID via the real tools.ws validate command.

    Read-only. tools.ws's own main() reads sys.argv directly rather than
    accepting an argv parameter, so it must be patched around the call
    (confirmed necessary during this Work Object's second tracer bullet).
    """
    wo_path = _find_work_object_file(work_object_id)
    if wo_path is None:
        return f"error: no Work Object found for id {work_object_id}"

    buf = io.StringIO()
    argv_backup = sys.argv
    sys.argv = ["ws", "validate", "--files", wo_path]
    try:
        with contextlib.redirect_stdout(buf):
            exit_code = ws_main()
    finally:
        sys.argv = argv_backup
    return f"exit_code={exit_code}\n{buf.getvalue()}"


def run() -> None:
    """Console-script entry point (`work-studio-mcp`). Defaults to stdio transport."""
    server.run()


if __name__ == "__main__":
    run()
