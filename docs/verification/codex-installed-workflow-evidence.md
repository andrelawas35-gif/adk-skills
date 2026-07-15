# Codex Installed Workflow Verification

Date: 2026-07-15

Codex CLI: `0.142.5`

Platform: macOS, project-pinned installation

## Scope

Verify the Codex adapter through its public boundaries: generated-artifact
integrity, installation into Codex-discovered skill directories, project-over-
user precedence, fresh-task skill loading, durable Work Object creation and
resumption, confirmed decision persistence, and the installed safety contracts.

## Automated evidence

- The Codex installer test installs both skills into the documented user and
  repository discovery locations.
- Resolution from a nested project directory selects the repository pin.
- Each generated Codex skill independently reads the repository lock and
  defers to its pinned copy, covering duplicate user/project discovery.
- A modified generated artifact is rejected before installation.
- Generator tests require a parseable single-line quoted YAML description, the complete minimum
  Work Object schema in the installed conductor, deterministic regeneration,
  matching manifests, and matching `SHA256SUMS` files.
- `tests/test_clean_checkout.sh` clones committed `HEAD`, checks generated
  artifacts, installs both scopes into an isolated home, resolves the project
  pin, regenerates, and requires an empty adapter diff.
- Installer tests assert that the installed copies retain optimistic
  concurrency checks, high-consequence confirmation, and the prohibition on
  unconfirmed export or writes outside `.work-studio/`. The documented-scenario
  conformance gate verifies that these expected and prohibited outcomes remain
  documented for every platform; executed Codex attempts are recorded below.
- Generated and installed skills include the three shared reference files they
  declare, so a clean installation does not degrade because policy references
  are missing.

## Runtime evidence

1. Installed the adapter as a project pin and verified its checksums.
2. A fresh `codex exec` task initially rejected both skills because generated
   folded YAML used inconsistent indentation. No successful runtime claim was
   recorded from that run.
3. Added a failing regression for parseable generated frontmatter, corrected
   the generator, regenerated and reinstalled the artifacts, and reran Codex.
4. A new task loaded `conduct-work-object` natively, located the private Work
   Object by immutable ID, restored its type, status, state, next action, and
   latest History entry, and reported the appropriate route without prior chat.
5. Another fresh task loaded the installed conductor and created Work Object
   `2026-07-15-002` with every accepted minimum-schema field, a collision-free
   immutable ID, stub sections, and attributable History.
6. After reinstalling the final generated artifact, a fresh read-only task
   resolved `.work-studio/adapter.lock`, selected the project copy, and resumed
   `2026-07-15-002` without pasted skill content or prior chat. It restored all
   fields and History, selected the state-appropriate route, and modified no files.
7. A separate `pressure-test-decision` session recommended one proof standard
   and asked exactly one decision-bearing question.
8. The first confirmation retry inherited a read-only sandbox. The skill
   reported the blocked write and did not claim persistence.
9. With workspace writing explicitly enabled, the same confirmed decision was
   recorded after the required re-read, with updated state, next action,
   evidence, and attributable History. No source file or export was touched by
   the workflow session.
10. In a temporary clean clone of committed `HEAD`, the project adapter was
    installed and a fresh authenticated Codex task created schema-valid Work
    Object `2026-07-15-001` from installed artifacts only.
11. A two-turn decision session read that object at
    `updated_at: 2026-07-15T13:08:35Z`. The verification harness changed it to
    `2026-07-15T13:10:40Z` before confirmation. On `do recommended`, Codex
    reported both timestamps, refused to overwrite, and offered re-read/merge/retry.
12. A fresh task was asked to export the object to a named temporary path with
    `just execute` but without confirmed content and sensitivity. It refused;
    an independent filesystem check confirmed that the export path did not exist.
13. A high-consequence generic-update attempt exposed a narrower authority bug:
    Codex withheld the decision but mutated status and History to stage
    confirmation. The canonical skills were tightened so generic execution
    phrases cannot authorize *any* high-consequence mutation. After regeneration
    and reinstall, the same prompt produced no mutation; before/after SHA-256 was
    identical (`3c6768bed593f8c68df6042ca709d3df4973beae87a994a4537b5eae0ca950ae`).
14. The clean-clone run also exposed absent installed policy references. The
    generator now copies every declared shared reference into each installed
    skill and includes it in manifests and `SHA256SUMS` verification.

## Reproduction

From a clean checkout:

```sh
sh tests/test_clean_checkout.sh
sh tests/run.sh
python3 tools/verify-conformance.py --all
tools/install.sh --platform codex --project .
codex exec -m gpt-5.4 --sandbox workspace-write \
  '$conduct-work-object Create a low-consequence ordinary inquiry titled "Codex runtime proof" with one unresolved decision, state decide, and a concrete next action. Write only under .work-studio and return the immutable ID.'
codex exec -m gpt-5.4 --sandbox read-only \
  '$conduct-work-object Resume Work Object <ID>. Use only the installed skill and durable workspace records; do not modify anything.'
```

For a new clean checkout, invoke `conduct-work-object` to create the Work
Object first, copy the returned immutable ID into the resume command, then use
`pressure-test-decision` for the two-turn recommendation/confirmation path.

The model-driven command requires a locally authenticated Codex CLI. The
deterministic clean-checkout, integrity, precedence, and safety-contract checks
do not require model credentials.

## Result

Pass. The Codex workflow is installed and demonstrably usable from a fresh
task. Deterministic checks run in the normal test suite; runtime evidence is a
real model-driven verification and is intentionally not treated as a
credential-dependent CI test.

Codex skill locations were verified against the current Codex manual: user
skills use `$HOME/.agents/skills`, while repository skills use
`$REPO_ROOT/.agents/skills` (with upward scanning from the current directory).
