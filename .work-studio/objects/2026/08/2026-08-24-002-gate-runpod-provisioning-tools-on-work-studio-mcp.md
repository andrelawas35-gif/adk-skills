---
schema_version: 1
id: 2026-08-24-002
title: Gate RunPod provisioning tools on Work Studio's MCP server
type: change
status: active
state: design
consequence: high
sensitivity: ordinary
domain: [engineering]
relates_to: [2026-08-24-001, 2026-08-21-010]
created_at: 2026-08-24T09:45:00Z
updated_at: 2026-08-24T17:39:04Z
next_action: Awaiting director decision: keep retrying different RunPod data centers/GPU types for a working Community Cloud host, try Secure Cloud instead (costs more per hour but likely different host pool), or pause 2026-08-24-001 pending RunPod support contact.












---
## Intent

`work-studio-mcp` (`mcp_server/src/mcp_server/server.py`) is Work Studio's own
MCP server — it exposes `tools/ws` operations (currently only the read-only
`ws_validate`) to external MCP clients. Its own docstring explicitly warns
against adding a mutating tool "without that decision first," referring to an
unresolved authority/consequence-gating design named in this server's own
originating deliverable (`.work-studio/deliverables/2026-08-21-010-mcp-server-report.md`).

The director wants to extend this same server with tools that can provision
and manage RunPod GPU pods (to execute `2026-08-24-001`'s accepted rental
tracer bullet and future rentals) — a capability category the server has
never had: calling an external, billed, third-party API rather than governing
local Work Object state. The director explicitly chose full provisioning
capability (create/start/stop pods), not a read-only status tool, which means
this Work Object must design the authority gate before any provisioning code
is written.

## Success evidence

- [ ] A bounded first tracer-bullet slice of the authority gate is designed
      and accepted before any provisioning tool is implemented.
- [ ] The gate design makes explicit: what a calling MCP client can trigger
      unattended vs. what requires a human-confirmed step, how spend is
      bounded (max pod runtime, max hourly rate, auto-termination), and what
      happens on failure (e.g. a stuck/forgotten running pod).
- [ ] The design is proven against `2026-08-24-001`'s actual first use case
      (one A6000 pod, both ComfyUI models, then terminate) before being
      generalized to arbitrary provisioning.

## Constraints and non-goals

**Constraints:**
- Must not weaken or bypass the existing `ws_validate`-only mutating-tool
  gate in `server.py` — RunPod tools are a new, separate authority category,
  not an extension of the Work Object mutation gate.
- Any tool that can incur cost or leave a pod running must have an explicit,
  human-visible bound (cannot silently run indefinitely).
- RunPod credentials/OAuth session belong to the already-installed
  `runpod@runpod` plugin's own auth flow — this Work Object does not invent a
  separate credential path.

**Non-goals:**
- Building a general-purpose cloud-infrastructure abstraction layer for
  providers beyond RunPod.
- Automating the full studio pipeline (image → 3D → Blender → video) end to
  end — this is scoped to pod lifecycle only.
- Deciding here whether `tools/ws`'s other mutating subcommands (`create`,
  `transition`, etc.) get exposed — that remains the separate unresolved
  question from `2026-08-21-010`.

## Decisions and revisit triggers

### Decision 1 — Accepted layered-mitigation design for `runpod_start_pod`/`runpod_stop_pod`

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Build exactly two new tools on `work-studio-mcp`: `runpod_start_pod(gpu_type, max_runtime_minutes)` and `runpod_stop_pod(pod_id)`. `start` must implement all three mitigation layers as one non-optional unit: (1) an in-pod Docker Command timeout that self-terminates the container at `max_runtime_minutes`, (2) a `work-studio-mcp`-side watchdog that independently polls elapsed time and calls `podStop` at the same bound, (3) a response payload that always includes pod ID, GPU type, price/hr, elapsed time, and projected cost so far. No provisioning tool ships with fewer than all three layers. |
| **Authorization** | Director explicitly accepted with "accept the revised design" after the design was corrected to remove the false server-side-auto-terminate assumption and the weaker, layered trade-off was stated plainly. This Work Object is `consequence: high`; this message is the required explicit confirmation naming the exact design-record mutation described immediately prior. |
| **Confidence** | high that the three layers are independently real and buildable (each verified against RunPod's actual documentation or Work Studio's own existing code); medium on whether the layered guarantee is strong enough in practice — that remains untested until the first real pod runs against it. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a real rental run shows the watchdog or in-pod timeout failing to fire, if RunPod later adds real server-side scheduled termination (which would let this design be simplified/strengthened), or if the director decides the residual "all three layers fail at once" risk is unacceptable for larger/longer future rentals. |
| **Rationale** | RunPod's API has no server-side enforced auto-terminate — confirmed directly against its documentation. Three independently-failing mitigations, none of them alone sufficient, together reduce (without eliminating) the risk of an unattended pod billing indefinitely. This is accepted as a weaker guarantee than originally proposed, not a corrected version of the original claim. |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | `mcp_server/src/mcp_server/server.py`, read 2026-08-24 | Server currently exposes exactly one tool, `ws_validate` (read-only). Its docstring explicitly states: "Do not add a mutating tool without that decision first," referring to an authority/consequence-gating design named in its own deliverable. |
| [system] | `.work-studio/deliverables/2026-08-21-010-mcp-server-report.md`, read 2026-08-24 | This server was built as one-directional: exposing Work Studio's own capabilities to MCP clients, not consuming or proxying external services. The report's own "what this does not resolve" section names authority/consequence gating for mutating tools as future design work, not yet done. |
| [decision] | director, 2026-08-24 | Chose "full provisioning tools, gated like ws mutations" over a read-only-status-only option or leaving RunPod entirely outside work-studio-mcp — explicit authority to design (not yet implement) a provisioning capability. |
| [testimony] | this session, 2026-08-24 | `runpod@runpod` Claude Code plugin is installed and enabled (v1.2.0), but OAuth sign-in via `/mcp` has not yet completed — `runpod` does not yet appear in the live MCP server list. Provisioning tools designed here will depend on that plugin's auth completing, or an equivalent credential path. |
| [system] | docs.runpod.io/sdks/graphql/manage-pods, fetched 2026-08-24 | Confirmed directly against RunPod's own GraphQL documentation: pod creation has no field for scheduling automatic termination at a future timestamp or after a maximum duration. The only termination mechanism is the `podStop` mutation, called manually by ID — there is no server-side enforced timeout. A web-search snippet had suggested a `terminateAfter` field existed; this was checked against the actual API spec and documentation and does not hold up — no such field is documented. |
| [system] | RunPod documentation, fetched 2026-08-24 | The one real (but weaker) mitigation RunPod does document: an on-demand pod's Docker Command field can run a shell command that sleeps for N hours then self-terminates. This executes *inside* the pod's own container — it is not infrastructure-enforced. If the container hangs, crashes, or the process is killed for any reason, the timeout dies with it and the pod keeps billing with no backstop from RunPod's side. |
| [system] | this session, 2026-08-24, mcp__runpod__list-pods and mcp__runpod__get-billing tool calls | runpod MCP server tools (list-pods, get-billing) are connected and functional in this session, authenticated with a RunPod API key the client is already configured with (Bearer auth; no separate credential search needed). Resolves the open question of whether work-studio-mcp should invent its own credential path: it should not -- a RunPod API key is already live and usable. |
| [decision] | director, this session, 2026-08-24 | Director confirmed 'Option A, go ahead with that': work-studio-mcp generates and uses its own RUNPOD_API_KEY rather than reusing a locally-available key, since the runpod MCP server proved to be a hosted OAuth-authenticated proxy (mcp.getrunpod.io) with no local key file to reuse. This is a deviation from this WO's own prior resolution of the credential-path open question, which had assumed a reusable local key existed. |
| [system] | mcp_server/src/mcp_server/server.py, implemented and imported 2026-08-24 | runpod_start_pod and runpod_stop_pod implemented in server.py using stdlib urllib only (no new dependency), calling RunPod's REST v1 API (rest.runpod.io/v1, confirmed via docs.runpod.io/api-reference) directly. All three mitigation layers present: (1) dockerStartCmd sleeps for max_runtime_minutes then exits, self-terminating the container; (2) a daemon watchdog thread per pod independently polls and calls POST /pods/{id}/stop at the same bound; (3) both tools' responses always include pod_id, gpu_type, cost_per_hr, elapsed_minutes, projected_cost. Verified: module imports cleanly under the project .venv; both tools fail with a clear, non-crashing error message when RUNPOD_API_KEY is unset; git status confirms only server.py changed, no unrelated files touched. Gap: no real RunPod API call has been executed yet -- untested against the live endpoint, deferred to avoid incurring cost before a key existed. |
| [testimony] | director, this session, 2026-08-24 | Director generated a RunPod API key and saved it as the RUNPOD_API_KEY Windows User environment variable via setx. Confirmed present in the registry (Environment]::GetEnvironmentVariable('RUNPOD_API_KEY','User') returns non-empty), but not yet visible to this session's already-running shells/processes -- setx only affects newly-started processes. A fresh terminal/process is needed before work-studio-mcp can read it. |
| [system] | real runpod_start_pod/runpod_stop_pod run against pod 6g53mv2qfpbrkk, 2026-08-24 | First real end-to-end run (RTX 6000 Ada, since A6000 had zero Community Cloud stock; director approved substitution). Found two real defects: (1) dockerStartCmd's sleep-then-exit script replaces the base image's CMD entirely (official RunPod images have CMD ["/start.sh"], no separate ENTRYPOINT -- confirmed against github.com/runpod/containers), so /start.sh's own PUBLIC_KEY/sshd bootstrap never ran and SSH access failed with Permission denied even after updating the pod's PUBLIC_KEY env and restarting. (2) runpod_stop_pod crashed on the untracked/API-lookup path because GET /pods/{id}'s lastStartedAt is returned as Go's default time string ("2026-08-24 16:39:43.36 +0000 UTC"), not strict ISO 8601 -- datetime.fromisoformat rejected it. Pod was stopped via the direct RunPod tool instead (billed ~5 minutes, ~/usr/bin/bash.06) while the crash was diagnosed. Both fixed in server.py: dockerStartCmd now backgrounds /start.sh before applying the timeout; a new _parse_runpod_timestamp handles both timestamp formats. Re-verified: module imports cleanly, parser handles both real formats correctly. |
| [system] | real ssh test against pod hulsd7tkoib0w2 (L40S), 2026-08-24 | Traced the earlier SSH permission-denied failures to a second, separate cause beyond the /start.sh fix: RunPod's ssh.runpod.io PROXY path authenticates against SSH keys registered in the RunPod account console (Settings > SSH Public Keys), not the pod's PUBLIC_KEY env var -- confirmed against docs.runpod.io/pods/configuration/use-ssh. Direct SSH to a pod's own public IP (when the host assigns one) does use PUBLIC_KEY/authorized_keys via /start.sh, which is what the earlier fix restores. Director registered the ephemeral key in account settings; separately, this pod (L40S, Community Cloud) was assigned a direct public IP. Direct SSH succeeded on first attempt: GPU visible (NVIDIA L40S, 46068 MiB), confirming the /start.sh backgrounding fix works correctly end-to-end. Both the account-level proxy path and the direct-IP path are now understood and available as alternatives depending on whether a given pod gets a direct public IP. |
| [system] | real attempts across 4 pods (hulsd7tkoib0w2, 7oehjdcymqwprz, 4ysz7i7l4qrhse), 2026-08-24 | Discovered RunPod's ssh.runpod.io PROXY path requires a genuine interactive PTY -- rejects non-interactive command execution entirely ('Your SSH client doesn't support PTY') unless the client both forces -tt AND has a real or emulated local terminal; piping commands as stdin keystrokes into a forced -tt session does work as a scripted workaround, but it is fragile (parses the remote shell prompt/banner as if typed). More significant: 3 separate Community Cloud L40S pods in a row, across what were assumed to be different physical hosts, all landed on the identical public IP (60.249.37.148) with the identical /dev/nvidia0-missing CUDA failure -- the mknod/symlink workaround from the earlier pod also failed to fix it on retry. This is not proven to be one bad host vs. a broader Community Cloud L40S capacity-pool issue in this session's default data center/region; not resolved. All test pods stopped; no pod left running. Approx cumulative real spend across all attempts today: ~/usr/bin/bash.15-0.20. |
| [system] | pod 86qluwzc8uw7ui (A100 SXM 40GB), 2026-08-24 | Switching GPU type (away from L40S) landed on genuinely different host hardware and resolved the broken-GPU-passthrough blocker: /dev/nvidia0 present with correct permissions, torch.cuda.is_available() returns True, torch 2.1.0+cu118. Confirms the earlier failures were specific to whichever single physical host Community Cloud was routing all L40S requests to, not a general work-studio-mcp or account-level problem. Also confirms the ssh.runpod.io proxy PTY workaround (piping commands as stdin keystrokes into a forced -tt session) is usable for scripted verification when a pod has no direct public IP. |
## Revised tracer-bullet design (post-verification)

The originally proposed design assumed RunPod could enforce a server-side
auto-terminate — confirmed false. No single mechanism gives a "cannot
silently run forever" guarantee. The revised design layers three independent
mitigations, each of which can fail without the others failing simultaneously:

1. **In-pod Docker Command timeout** — the pod's own container runs a sleep-
   then-self-terminate command at the requested `max_runtime_minutes`. Fails
   if the container hangs or the process is killed.
2. **`work-studio-mcp`-side watchdog** — the server that started the pod
   polls elapsed time and calls `podStop` at the same bound, independently of
   layer 1. Fails if the `work-studio-mcp` process itself dies or loses
   network access.
3. **Human-visible cost surfacing** — every tool response (`start`, and any
   status check) includes pod ID, GPU type, price/hr, elapsed time, and
   projected cost so far, so a human glancing at the transcript or RunPod's
   own billing dashboard is the final backstop if both automated layers fail.

Tool shape stays the same as originally proposed —
`runpod_start_pod(gpu_type, max_runtime_minutes)` and
`runpod_stop_pod(pod_id)` — but `start` now also sets the Docker Command
timeout (layer 1) and begins the watchdog poll (layer 2) as part of the same
call, and its return payload always includes the cost-surfacing fields
(layer 3). No layer is optional; a design that ships only one of the three
is not this design.

**Accepted trade-off:** this cannot promise a pod will *never* run longer
than intended — it promises three independent, differently-failing paths
have to fail at once for that to happen, and even then it's visible in
billing within the hour. That is a materially weaker guarantee than the
original "cannot silently run forever" claim, and the director should accept
it as such, not as a corrected version of the original guarantee.

## Open questions (resolved)

- **Credential path** — RESOLVED. `work-studio-mcp`'s tools must implement
  the watchdog and Docker Command timeout themselves, which requires them to
  call RunPod's API directly from `work-studio-mcp`'s own process — a second
  MCP server cannot be "wrapped" from inside another server's tool
  implementation. Directly confirmed this session that a RunPod API key is
  already live and authenticating successfully (`mcp__runpod__list-pods`,
  `mcp__runpod__get-billing` both succeeded, Bearer auth, no separate
  credential search). `work-studio-mcp` reuses that same already-configured
  key rather than inventing a new credential or OAuth path — satisfying the
  Constraints section's requirement without needing to delegate to the
  `runpod@runpod` plugin's own tool surface.
- **Spend/runtime bound for the first tracer bullet** — RESOLVED as a
  parameter, not a fixed number. `max_runtime_minutes` is caller-supplied on
  every `runpod_start_pod` call, so there is no single value to bake into the
  design. For `2026-08-24-001`'s specific tracer bullet (provision, install
  both ComfyUI custom nodes, run one image through TRELLIS.2 and
  Hunyuan3D-2.1, verify Blender import, terminate), a recommended starting
  bound is **120 minutes** — covers node install plus model downloads plus
  two generation passes with margin, bounding worst-case spend at ~$0.33/hr
  to well under $1. The director can raise or lower this per call; it is not
  fixed by this design.
- **"Gated like ws mutations" — literal mechanism or equivalent standard of
  care** — RESOLVED as equivalent standard of care, not the same mechanism.
  Already implied by this Work Object's own Constraints section ("RunPod
  tools are a new, separate authority category, not an extension of the
  Work Object mutation gate") but not stated as an explicit answer until now.
  The standard being matched is: no spend-incurring action proceeds without
  an explicit, human-visible confirmation step and a visible bound on
  exposure — not literal reuse of `ws_validate`'s code path or schema.

## Next move

Route to `alawas-engineering-implement-bounded-change` to build
`runpod_start_pod` and `runpod_stop_pod` on `work-studio-mcp` exactly as
specified in Decision 1 — all three mitigation layers as one non-optional
unit, no broader provisioning surface than this.

## History

### 2026-08-24T09:45:00Z — Created change record for RunPod authority gate

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** Director asked to connect RunPod capability into Work Studio's own MCP server and, when asked to clarify, chose full provisioning tools gated like existing Work Object mutations. The server's own code explicitly warns against adding a mutating tool without a prior authority/consequence decision, and this is a new capability category (external billed API) beyond what that warning originally covered — so it gets a proper Work Object rather than being freehanded into `server.py`.

### 2026-08-24T10:15:00Z — Revised design after verifying RunPod has no server-side auto-terminate

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** The original tracer-bullet design assumed RunPod's API could schedule server-side auto-termination — director asked to verify this before accepting. Checked directly against RunPod's GraphQL documentation: no such field exists; `podStop` is manual-only. Revised the design from a single enforced guarantee to three independently-failing layered mitigations (in-pod Docker Command timeout, `work-studio-mcp`-side watchdog polling, and human-visible cost surfacing in every tool response), with the trade-off made explicit: this reduces but cannot eliminate the risk of a forgotten/stuck pod continuing to bill. Awaiting director acceptance of this revised, weaker-than-originally-claimed guarantee before any implementation.

### 2026-08-24T10:25:00Z — Accepted revised design; ready for bounded implementation

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director explicitly accepted the revised layered-mitigation design with "accept the revised design," satisfying the explicit-confirmation requirement this `consequence: high` Work Object needs before any design-record mutation. Recorded as Decision 1. No code has been written yet — routing to implement-bounded-change to build `runpod_start_pod`/`runpod_stop_pod` exactly as specified, with all three mitigation layers as one non-optional unit.
### 2026-08-24T16:26:43Z — Resolved all three open questions

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** Resolved all three open questions before implementation. (1) Credential path: work-studio-mcp must call RunPod's API directly to implement the watchdog/timeout itself -- confirmed live this session that a RunPod API key is already authenticating successfully via the connected runpod MCP tools, so work-studio-mcp reuses that key rather than inventing a new credential path or delegating to the runpod@runpod plugin. (2) Spend/runtime bound: resolved as a caller-supplied max_runtime_minutes parameter rather than a fixed design value; recommended starting bound of 120 minutes for -001's specific tracer bullet. (3) 'Gated like ws mutations': resolved as equivalent standard of care (explicit human confirmation plus visible exposure bound before any spend-incurring action), not literal reuse of the ws_validate mechanism -- consistent with this WO's own Constraints section. No design change to Decision 1; ready to route to implementation.
### 2026-08-24T16:35:01Z — Implemented runpod_start_pod/runpod_stop_pod; recorded credential-path deviation; RUNPOD_API_KEY saved

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** Routed to implement-bounded-change against Decision 1. Discovered before writing code that the runpod MCP server is a hosted OAuth proxy (mcp.getrunpod.io), not a local key-holding process -- the prior resolution assuming a reusable local key did not hold. Stopped and asked the director, who confirmed Option A: work-studio-mcp generates and uses its own RUNPOD_API_KEY. Implemented both tools in server.py (stdlib urllib only, no new dependency) with all three mitigation layers as one unit; verified the module imports cleanly and both tools fail cleanly (not crash) when the key is unset; confirmed no unrelated files touched. Director then generated a key and saved it via setx -- confirmed present in the Windows User environment registry, but not yet visible to any already-running process in this session. Real API call against RunPod remains unexecuted; that is the one open gap before -001's tracer bullet can actually run.
### 2026-08-24T16:42:44Z — Ran first real pod, found and fixed two live defects, stopped pod cleanly

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** Director approved running the first real test on RTX 6000 Ada (A6000 had zero Community Cloud stock) and separately approved generating an ephemeral SSH keypair for pod access when the base pod had no SSH configured. The real run surfaced two defects invisible to unit-level verification: dockerStartCmd overwriting the base image's own CMD (breaking SSH/Jupyter bootstrap), and a timestamp-format mismatch crashing runpod_stop_pod's untracked path. Director had the pod stopped rather than working around the SSH gap live; pod was stopped via the direct RunPod tool after runpod_stop_pod itself crashed on the timestamp bug, confirming the bug's real-world severity. Both fixed in server.py and re-verified at the unit level (import, parser against both real formats). Total real spend from this run: ~/usr/bin/bash.06 (5 minutes on RTX 6000 Ada). Neither fix required a design change to Decision 1's scope or authorization -- both are correctness fixes to the accepted design's implementation, not new decisions.
### 2026-08-24T17:36:43Z — Confirmed SSH fix works via direct IP; blocked on repeated broken-host CUDA failure, escalating to director

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** The /start.sh backgrounding fix (server.py) is confirmed correct: direct SSH to pod hulsd7tkoib0w2's public IP succeeded on first try after the fix, with the GPU visible to nvidia-smi. However, torch.cuda could not initialize on that pod (missing /dev/nvidia0 device node, only /dev/nvidia1 present) -- a host-level GPU passthrough defect, not a work-studio-mcp or ComfyUI issue. Retried pod creation twice more; all 3 Community Cloud L40S pods landed on the same public IP (60.249.37.148) with the identical failure, which the mknod/symlink workaround could not fix from inside the container (no CAP_MKNOD). This blocks 2026-08-24-001's tracer bullet before any ComfyUI install work could begin -- stopped before the checkpoint the director asked for since there was nothing installable on a pod without working CUDA. All pods stopped; no pod left running. Also discovered ssh.runpod.io's proxy path requires a real interactive PTY and is unsuitable for scripted automation without a workaround, separate from the CUDA blocker.
