"""MCP server exposing Work Studio's tools/ws operations to MCP clients.

WO 2026-08-21-010, Decision 1: a new sibling package depending on tools.ws
as an ordinary library import, plus mcp as its only new dependency -- not
inside tools/ws (would break its dependencies=[] contract), not folded into
runtime/ (wrong conceptual surface).

Exposes ws_validate -- the safe, read-only operation this Work Object's
tracer bullets already proved works end-to-end -- plus, per WO
2026-08-24-002 Decision 1, exactly two RunPod pod-lifecycle tools
(runpod_start_pod, runpod_stop_pod). Those two are a new, separate
authority category (an external, billed, third-party API), not an
extension of the ws_validate-only mutating-tool gate. Which further
tools/ws subcommands should be exposed, and how authority/consequence
gating should work for an external MCP client invoking a mutating one
(create, transition, close, append-*), remains the separate unresolved
decision named in this Work Object's own deliverable report,
.work-studio/deliverables/2026-08-21-010-mcp-server-report.md -- not
silently decided here. Do not add a mutating ws tool without that decision
first.
"""
import contextlib
import glob
import io
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from mcp.server.mcpserver import MCPServer

from tools.ws.__main__ import main as ws_main

server = MCPServer("work-studio-mcp")

RUNPOD_API_BASE = "https://rest.runpod.io/v1"
RUNPOD_DEFAULT_IMAGE = "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04"

# In-memory only (WO 2026-08-24-002 Decision 1, layer 2): tracks pods this
# process started, so its watchdog and the cost-surfacing fields on
# runpod_stop_pod know each pod's requested bound and starting price
# without a second API round-trip. Lost on process restart -- the in-pod
# timeout (layer 1) is what still fires if this process is not running.
_started_pods: dict[str, dict] = {}


def _runpod_api_key() -> str:
    key = os.environ.get("RUNPOD_API_KEY")
    if not key:
        raise RuntimeError(
            "RUNPOD_API_KEY is not set. WO 2026-08-24-002: work-studio-mcp "
            "calls RunPod's API directly and needs its own key (generate "
            "one at runpod.io/console/user/settings and set it as the "
            "RUNPOD_API_KEY environment variable for this process)."
        )
    return key


def _runpod_request(method: str, path: str, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        f"{RUNPOD_API_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {_runpod_api_key()}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"RunPod API {method} {path} failed: {exc.code} {detail}") from exc


def _watchdog_stop(pod_id: str, max_runtime_minutes: int) -> None:
    """Layer 2: independent of the in-pod timeout (layer 1) -- polls
    elapsed wall-clock time from this process and calls podStop at the
    same bound. Fails only if this process itself dies or loses network,
    which is why layer 1 exists as an independent backstop for that case.
    """
    time.sleep(max_runtime_minutes * 60)
    pod = _started_pods.get(pod_id)
    if pod is None or pod.get("stopped"):
        return
    try:
        _runpod_request("POST", f"/pods/{pod_id}/stop")
    finally:
        pod["stopped"] = True


def _parse_runpod_timestamp(raw: str) -> datetime:
    """RunPod's REST API is inconsistent about timestamp format: pod-creation
    responses return strict ISO 8601 ("...Z"), but GET /pods/{id} has been
    observed returning Go's default time.Time string form instead
    ("2026-08-24 16:39:43.36 +0000 UTC") -- confirmed against a real
    runpod_stop_pod call during 2026-08-24-001's tracer bullet, which crashed
    on this exact input before this fix. Handle both.
    """
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        pass
    cleaned = raw.replace(" UTC", "").strip()
    cleaned = cleaned.replace(" +0000", "+00:00").replace(" -0000", "+00:00")
    return datetime.fromisoformat(cleaned)


def _elapsed_and_cost(started_at_iso: str, cost_per_hr: float) -> tuple[float, float]:
    started_at = _parse_runpod_timestamp(started_at_iso)
    elapsed_minutes = (datetime.now(timezone.utc) - started_at).total_seconds() / 60.0
    projected_cost = (elapsed_minutes / 60.0) * cost_per_hr
    return elapsed_minutes, projected_cost


@server.tool()
def runpod_start_pod(gpu_type: str, max_runtime_minutes: int) -> str:
    """Start a RunPod on-demand GPU pod with a bounded runtime (WO 2026-08-24-002 Decision 1).

    Implements all three mitigation layers as one non-optional unit:
    (1) an in-pod Docker start command that sleeps for max_runtime_minutes
    then exits, self-terminating the container; (2) a work-studio-mcp-side
    watchdog thread that independently polls elapsed time and calls
    podStop at the same bound; (3) a response that always includes pod
    ID, GPU type, price/hr, elapsed time, and projected cost so far.

    This cannot guarantee the pod never runs longer than requested -- it
    guarantees three independently-failing paths must all fail at once for
    that to happen, and even then it is visible in RunPod's own billing
    within the hour (WO 2026-08-24-002, accepted trade-off).
    """
    if max_runtime_minutes <= 0:
        return "error: max_runtime_minutes must be a positive number of minutes"

    sleep_seconds = max_runtime_minutes * 60
    pod_name = f"work-studio-mcp-{int(time.time())}"
    body = {
        "name": pod_name,
        "imageName": RUNPOD_DEFAULT_IMAGE,
        "cloudType": "COMMUNITY",
        "computeType": "GPU",
        "gpuCount": 1,
        "gpuTypeIds": [gpu_type],
        "dockerStartCmd": [
            "/bin/bash",
            "-c",
            (
                "/start.sh & "
                f"sleep {sleep_seconds}; "
                "echo 'work-studio-mcp: max_runtime_minutes reached, self-terminating'; "
                "exit 0"
            ),
        ],
    }
    try:
        pod = _runpod_request("POST", "/pods", body)
    except RuntimeError as exc:
        return f"error: {exc}"

    pod_id = pod.get("id")
    cost_per_hr = pod.get("costPerHr", 0.0)
    started_at = pod.get("lastStartedAt") or datetime.now(timezone.utc).isoformat()

    _started_pods[pod_id] = {
        "gpu_type": gpu_type,
        "cost_per_hr": cost_per_hr,
        "max_runtime_minutes": max_runtime_minutes,
        "started_at": started_at,
        "stopped": False,
    }
    threading.Thread(
        target=_watchdog_stop, args=(pod_id, max_runtime_minutes), daemon=True
    ).start()

    return json.dumps(
        {
            "pod_id": pod_id,
            "gpu_type": gpu_type,
            "cost_per_hr": cost_per_hr,
            "max_runtime_minutes": max_runtime_minutes,
            "elapsed_minutes": 0.0,
            "projected_cost": 0.0,
            "mitigation_layers": [
                "in_pod_docker_timeout",
                "work_studio_mcp_watchdog",
                "cost_surfacing",
            ],
        }
    )


@server.tool()
def runpod_stop_pod(pod_id: str) -> str:
    """Stop a RunPod pod by ID (WO 2026-08-24-002 Decision 1).

    Response always includes the same cost-surfacing fields as
    runpod_start_pod: GPU type, price/hr, elapsed time, and projected
    cost, computed from this process's own record if this pod was
    started via runpod_start_pod, else best-effort from RunPod's API.
    """
    tracked = _started_pods.get(pod_id)
    if tracked is not None:
        gpu_type = tracked["gpu_type"]
        cost_per_hr = tracked["cost_per_hr"]
        elapsed_minutes, projected_cost = _elapsed_and_cost(
            tracked["started_at"], cost_per_hr
        )
    else:
        try:
            pod = _runpod_request("GET", f"/pods/{pod_id}")
        except RuntimeError as exc:
            return f"error: {exc}"
        gpu_type = ",".join(pod.get("gpuTypeIds", []) or []) or "unknown"
        cost_per_hr = pod.get("costPerHr", 0.0)
        started_at = pod.get("lastStartedAt")
        if started_at:
            elapsed_minutes, projected_cost = _elapsed_and_cost(started_at, cost_per_hr)
        else:
            elapsed_minutes, projected_cost = 0.0, 0.0

    try:
        _runpod_request("POST", f"/pods/{pod_id}/stop")
    except RuntimeError as exc:
        return f"error: {exc}"

    if tracked is not None:
        tracked["stopped"] = True

    return json.dumps(
        {
            "pod_id": pod_id,
            "gpu_type": gpu_type,
            "cost_per_hr": cost_per_hr,
            "elapsed_minutes": round(elapsed_minutes, 2),
            "projected_cost": round(projected_cost, 4),
            "status": "stopped",
        }
    )


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
