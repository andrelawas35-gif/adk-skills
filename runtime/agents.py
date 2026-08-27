"""Provider-neutral agent dispatch contracts (tracer bullet, WO 2026-08-25-001 Decision 3).

Sits BESIDE runtime/graph.py, not inside it: a grep of graph.py found no real
model/subprocess dispatch anywhere in the Phase 6 nodes (phase6_dispatch/
branch_a/branch_b build HandoffEnvelope *proposal* payloads only, per ADR
0025's non-writer rule). There is no existing execution call-site this module
needs to nest into.

This is a tracer bullet, not a production dispatch layer: one adapter
(CodexAgentAdapter), no registration with runtime/graph.py's routing, no real
Work Object task dispatched through it. Referenced-but-undefined types from
the originating proposal (AuthorityEnvelope, ObjectRef, EvidenceCandidate,
ActionProposal, ArtifactRef) are simplified to minimal stand-ins here -- see
each class's docstring for the simplification.
"""

from __future__ import annotations

import asyncio
import json
import shutil
import sys
from pathlib import Path
from typing import List, Literal, Optional, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field


class AuthorityEnvelope(BaseModel):
    """Simplified stand-in: the proposal left this type unspecified.

    Reduced to the three boolean flags the proposal's own example used
    (inspect/modify_code/deploy) rather than a fully general authority model.
    """

    model_config = ConfigDict(extra="forbid")

    inspect: bool = True
    modify_code: bool = False
    deploy: bool = False


class AgentRequest(BaseModel):
    """What Work Studio wants done -- says nothing about which model does it."""

    model_config = ConfigDict(extra="forbid")

    task: str
    role: Optional[str] = None
    skill: Optional[str] = None
    work_object_id: Optional[str] = None
    context_refs: List[str] = Field(default_factory=list)
    artifact_refs: List[str] = Field(default_factory=list)
    required_capabilities: List[str] = Field(default_factory=list)
    constraints: List[str] = Field(default_factory=list)
    protected: List[str] = Field(default_factory=list)
    authority: AuthorityEnvelope = Field(default_factory=AuthorityEnvelope)
    expected_output: str
    consequence: str = "low"


class AgentResult(BaseModel):
    """Normalized result -- the rest of Work Studio should not need to
    understand any given adapter's native output shape.

    outputs/evidence_candidates/proposed_actions/artifacts are simplified to
    List[str] (the proposal left ObjectRef/EvidenceCandidate/ActionProposal/
    ArtifactRef unspecified; a tracer bullet does not need a full type system
    for references it does not yet populate with real structured data).
    """

    model_config = ConfigDict(extra="forbid")

    status: Literal["completed", "blocked", "needs_approval", "failed"]
    summary: str
    outputs: List[str] = Field(default_factory=list)
    evidence_candidates: List[str] = Field(default_factory=list)
    proposed_actions: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)
    unresolved_questions: List[str] = Field(default_factory=list)
    tool_trace_ref: Optional[str] = None


@runtime_checkable
class AgentAdapter(Protocol):
    """Deliberately boring: one method, one normalized result."""

    name: str

    async def run(self, request: AgentRequest) -> AgentResult: ...


class CodexAgentAdapter:
    """Translates an AgentRequest into a `codex exec` subprocess call and
    normalizes its output back into an AgentResult.

    Tracer-bullet scope only: no sandboxing policy beyond `--sandbox
    read-only`, no repository context wiring, no real task ever dispatched
    through this adapter yet (WO 2026-08-25-001 Decision 2/3 non-goals).
    """

    name = "codex"
    type = "coding"
    capabilities = {"retrieve", "inspect_code", "hypothesize"}

    def __init__(self, codex_executable: str = "codex", cwd: Optional[Path] = None):
        self._codex_executable = codex_executable
        self._cwd = cwd

    async def run(self, request: AgentRequest) -> AgentResult:
        # --sandbox read-only only constrains model-generated shell commands,
        # NOT MCP tool calls (WO 2026-08-25-001 Decision 5) -- an enabled MCP
        # server (e.g. node_repl) can execute code unsandboxed regardless of
        # this flag. --ignore-user-config alone is also insufficient: it
        # skips $CODEX_HOME/config.toml but MCP servers can still be defined
        # elsewhere (a live rmcp connection attempt to mcp.cloudflare.com was
        # observed even with --ignore-user-config set). The explicit
        # `mcp_servers={}` override is what actually verified clean.
        cmd = [
            self._codex_executable,
            "exec",
            "--json",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
            "--ignore-user-config",
            "-c",
            "mcp_servers={}",
            request.task,
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(self._cwd) if self._cwd else None,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_bytes, stderr_bytes = await proc.communicate()
        stdout_text = stdout_bytes.decode("utf-8", errors="replace")
        stderr_text = stderr_bytes.decode("utf-8", errors="replace")

        if proc.returncode != 0:
            return AgentResult(
                status="failed",
                summary=f"codex exec exited {proc.returncode}",
                unresolved_questions=[stderr_text.strip()[:500]] if stderr_text.strip() else [],
                tool_trace_ref=stdout_text[:2000] if stdout_text else None,
            )

        final_message = None
        had_failed_command = False
        for line in stdout_text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict) or event.get("type") != "item.completed":
                continue
            item = event.get("item", {})
            if not isinstance(item, dict):
                continue
            if item.get("type") == "agent_message":
                final_message = item.get("text")
            elif item.get("type") == "command_execution" and item.get("status") == "failed":
                had_failed_command = True

        # A rejected patch/file-edit tool call does NOT surface as a
        # command_execution item in the --json stdout stream -- it's a
        # Rust-level error logged to stderr instead (WO 2026-08-25-001
        # Decision 6/7). Catch it the same way: prevented from completing,
        # not achieved, regardless of the final agent_message's tone.
        if "error=patch rejected" in stderr_text:
            had_failed_command = True

        if final_message is None:
            return AgentResult(
                status="failed",
                summary="codex exec completed but no agent_message event was found in --json output",
                tool_trace_ref=stdout_text[:2000],
            )

        if had_failed_command:
            # The process finished and Codex reported honestly, but at least
            # one command it needed failed -- the task itself was prevented
            # from completing, not achieved. This is a heuristic: a failed
            # command does not always mean the overall task failed (Codex
            # may have recovered by another path), but for a dispatch layer
            # feeding a governed system, erring toward "blocked" over a
            # silently-trusted "completed" is the safer direction.
            return AgentResult(
                status="blocked",
                summary=final_message,
                unresolved_questions=["one or more command_execution items reported status=failed during the run"],
                tool_trace_ref=stdout_text[:2000],
            )

        return AgentResult(
            status="completed",
            summary=final_message,
            tool_trace_ref=stdout_text[:2000],
        )


class OpenCodeAgentAdapter:
    """Translates an AgentRequest into an `opencode run` subprocess call and
    normalizes its JSON event output back into an AgentResult.

    Tracer-bullet scope: zero model-tier binding (model passed at invocation
    time via --model, never hardcoded), --auto for non-interactive dispatch,
    --format json for parseable event stream.  Mirrors CodexAgentAdapter's
    shape per WO 2026-08-25-001 Decision 15.
    """

    name = "opencode"
    type = "coding"
    capabilities = {"retrieve", "inspect_code", "hypothesize"}

    def __init__(
        self,
        opencode_executable: str = "opencode",
        model: Optional[str] = None,
        cwd: Optional[Path] = None,
    ):
        self._opencode_executable = opencode_executable
        self._model = model
        self._cwd = cwd

    async def run(self, request: AgentRequest) -> AgentResult:
        cmd = [
            self._opencode_executable,
            "run",
            "--format",
            "json",
            "--auto",
        ]
        if self._model:
            cmd.extend(["--model", self._model])
        cmd.append(request.task)

        # On Windows, .CMD wrappers (npm global installs) require shell=True
        # or wrapping via cmd /c for asyncio.create_subprocess_exec to find them.
        if sys.platform == "win32":
            proc = await asyncio.create_subprocess_shell(
                " ".join(cmd),
                cwd=str(self._cwd) if self._cwd else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        else:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self._cwd) if self._cwd else None,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        stdout_bytes, stderr_bytes = await proc.communicate()
        stdout_text = stdout_bytes.decode("utf-8", errors="replace")
        stderr_text = stderr_bytes.decode("utf-8", errors="replace")

        if proc.returncode != 0:
            return AgentResult(
                status="failed",
                summary=f"opencode run exited {proc.returncode}",
                unresolved_questions=[stderr_text.strip()[:500]] if stderr_text.strip() else [],
                tool_trace_ref=stdout_text[:2000] if stdout_text else None,
            )

        final_text: Optional[str] = None
        had_failed_tool = False
        for line in stdout_text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue

            event_type = event.get("type")
            part = event.get("part", {})

            if event_type == "text" and isinstance(part, dict):
                final_text = part.get("text")
            elif event_type == "tool_use" and isinstance(part, dict):
                state = part.get("state", {})
                if isinstance(state, dict) and state.get("status") != "completed":
                    had_failed_tool = True

        if final_text is None:
            return AgentResult(
                status="failed",
                summary="opencode run completed but no text event was found in --format json output",
                tool_trace_ref=stdout_text[:2000],
            )

        if had_failed_tool:
            return AgentResult(
                status="blocked",
                summary=final_text,
                unresolved_questions=["one or more tool_use events reported non-completed status during the run"],
                tool_trace_ref=stdout_text[:2000],
            )

        return AgentResult(
            status="completed",
            summary=final_text,
            tool_trace_ref=stdout_text[:2000],
        )


class AgentResolver:
    """Version one: iterate the registry, no scoring model, no AI routing."""

    def __init__(self, agents: List[AgentAdapter]):
        self._agents = agents

    def resolve(
        self, required_type: str, required_capabilities: set[str]
    ) -> Optional[AgentAdapter]:
        for agent in self._agents:
            if getattr(agent, "type", None) != required_type:
                continue
            if required_capabilities <= getattr(agent, "capabilities", set()):
                return agent
        return None


def codex_available() -> bool:
    """True when a `codex` executable is on PATH -- cheap pre-flight check."""
    return shutil.which("codex") is not None


def opencode_available() -> bool:
    """True when an `opencode` executable is on PATH -- cheap pre-flight check."""
    return shutil.which("opencode") is not None
