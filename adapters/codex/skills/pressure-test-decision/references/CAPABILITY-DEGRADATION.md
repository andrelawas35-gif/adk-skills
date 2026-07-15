# Capability Degradation

Every platform adapter must classify each required capability and degrade
explicitly when one is unavailable. No adapter may claim verification,
export, deployment, or any gated action succeeded when the required
capability was unavailable.

## Classification tiers

| Classification | Meaning | Required behavior |
|---------------|---------|-------------------|
| **native** | The platform supports this capability directly. | Use the native tool. No degradation needed. |
| **manual-fallback** | The platform lacks direct support, but a human can perform the step. | Pause the workflow. Give ONE concrete instruction for the human to perform. Record in the Work Object what was done manually and what remains unverified. Do NOT claim automated verification succeeded. |
| **unsupported** | The platform cannot perform this capability, and no safe manual fallback exists. | Stop the affected path immediately. Record the platform limitation in the Work Object with the capability name and the blocked action. Route to a platform that supports the capability, or ask the user how to proceed. Do NOT silently skip, fake, or substitute. |

## Rules

1. **No false verification**: An adapter must never mark a verification,
   export, deployment, or gated action as successful when the required
   capability was unavailable. If `verify-release-evidence` requires browser
   automation and the platform only has `manual-fallback`, the adapter
   reports "verification requires manual browser check" — never "verified."

2. **Stricter platform safety wins**: When a platform imposes a stricter
   constraint than the core (e.g., Claude Code requires explicit confirmation
   for actions Codex allows), the stricter rule takes precedence. The
   divergence from core behavior must be disclosed in the Platform Adapter
   section.

3. **One instruction at a time**: A `manual-fallback` pause gives exactly
   one concrete, actionable instruction. It does not dump a procedure.
   Example: "Open http://localhost:3000 in Chrome and confirm the login
   page renders. Type 'done' when ready." Not: "Check the UI."

4. **Record what remains unverified**: After a manual-fallback step, the
   Work Object History must record:
   - What capability was unavailable
   - What manual action was taken
   - What remains unverified (the gap)
   - Actor: `human` (the manual performer)

5. **Unsupported stops the path**: An `unsupported` capability does not
   just degrade — it stops. The affected workflow path cannot proceed.
   The adapter records the limitation and routes elsewhere. It does not
   attempt the action through a different capability or pretend.

## Capability catalog

The canonical set of capabilities a skill may require:

| Capability | Description | Typically native on |
|-----------|-------------|-------------------|
| `file_read` | Read files from the workspace | All platforms |
| `file_write` | Create or edit files in the workspace | All platforms |
| `directory_list` | List directory contents | All platforms |
| `glob_search` | Find files by glob pattern | All platforms |
| `content_search` | Search file contents (grep) | All platforms |
| `terminal_run` | Execute shell commands | All platforms |
| `git_operations` | Run git commands | All platforms |
| `web_fetch` | Fetch content from URLs | All platforms |
| `subagent_spawn` | Spawn sub-agents for parallel work | All platforms |
| `structured_output` | Produce structured (JSON, YAML) output | All platforms |
| `user_confirmation` | Receive an explicit, scoped user decision or authorization | All platforms |
| `browser_automation` | Automate browser interactions | Codex |
| `parallel_tool_execution` | Execute multiple tools simultaneously | Codex, Claude Code |
| `subagent_isolation` | Strong isolation between sub-agents | Codex |
| `web_search` | Search the live web | Varies |

## In the Platform Adapter

The generated Platform Adapter section includes a **Capability Degradation**
subsection that lists every capability with its classification and, for
non-native tiers, the exact degradation behavior.
