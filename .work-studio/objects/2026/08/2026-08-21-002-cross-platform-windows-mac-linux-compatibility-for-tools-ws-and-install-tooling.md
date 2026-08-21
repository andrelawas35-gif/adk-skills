---
schema_version: 1
id: 2026-08-21-002
title: Cross-platform (Windows/Mac/Linux) compatibility for tools/ws and install tooling
type: inquiry
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-21T08:32:44Z
updated_at: 2026-08-21T09:11:49Z
next_action: Director review and commit; nothing pushed or committed yet






---
## Intent

Make the studio's tooling (`tools/ws` CLI, `tools/install.sh`, `tests/run.sh`)
behave correctly and identically on Windows and on Mac/Linux, so the director
does not have to work around platform-specific breakage (encoding corruption,
console crashes, POSIX-only scripts, line-ending drift) to use the system.

## Success evidence

- [x] Direction 1: encoding=utf-8 on every open()/read_text()/write_text() in tools/ws/*.py, runtime/projection.py, and their tests; ws CLI stdout/stderr reconfigured to UTF-8. Full suite: 21 pre-existing failures newly pass, zero new failures.
- [x] Direction 2: install.ps1, test_install.ps1, test_clean_checkout.ps1, run.ps1 -- native Windows tooling parity, no Git Bash/WSL required. Also fixed the same encoding bug in tools/generate-adapters.py (was crashing with "unclassified required capability: *.tsx" -- actually em-dash misparsed due to missing encoding=utf-8) and a path-separator bug (manifest.json/SHA256SUMS emitted backslashes on Windows instead of the committed forward-slash format). generate-adapters.py --check now passes clean on Windows.
- [x] Direction 3: .gitattributes (forces LF regardless of contributor autocrlf) + conformance-windows CI job (windows-latest, native PowerShell for the installer/test gate). Verified locally: no test regressions, Gate 5 passes; Gate 3 hits one pre-existing unrelated bug (missing fixture, flagged separately).

## Constraints and non-goals

**Constraints:**
<!-- Boundaries the implementation must respect. -->

**Non-goals:**
<!-- Explicitly excluded work. -->

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Selected all three directions, sequenced: encoding-safety pass, then native Windows tooling parity, then repo-level determinism

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | All three directions accepted for implementation, in order: (1) encoding-safety pass, (2) native Windows tooling parity, (3) .gitattributes + CI matrix |
| **Authorization** | Director: "Do all three, starting with direction 1" |
| **Confidence** | high — direction 1 is a demonstrated, actively-recurring bug; 2 and 3 are additive scope the director has now explicitly accepted rather than left optional |
| **Actor** | director |
| **Revisit trigger** | If direction 1's fix does not eliminate the crash/corruption observed this session, treat directions 2-3 as premature and return to Open questions |
| **Rationale** | Director chose breadth over picking one; sequencing by direction 1 first follows its own dependency — 2 and 3 are easier to verify once the CLI's I/O is no longer silently corrupting text |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | grep across tools/ws/*.py, this session | Dozens of Path.read_text()/open() calls in tools/ws/*.py (epistemic.py, validate.py, __main__.py, attention.py, claim.py, conflict.py, etc.) omit encoding=utf-8; on Windows this defaults to the locale codepage (cp1252), which misdecodes UTF-8 multibyte characters. Reproduced this session: em dashes and curly quotes in this repo's own Work Object bodies were corrupted into mojibake after every ws create/append-evidence/transition call. |
| [system] | this session, live crash | tools/ws/__main__.py line 461 prints a literal Unicode arrow character straight to stdout with no encoding guard. The transition command on this same Work Object crashed with UnicodeEncodeError (cp1252) immediately after writing the file successfully — the mutation itself succeeded, only the CLI's confirmation print crashed. |
| [system] | this session, live crash | A follow-up append-evidence call then failed to even read this file: UnicodeDecodeError, byte 0x9d undefined in cp1252. Prior mojibake write had produced a byte sequence cp1252 cannot decode at all, escalating a cosmetic corruption into a hard read failure that blocks every further ws command against this file until repaired by hand. |
| [system] | grep for install.sh / tests/run.sh shebangs | tools/install.sh and tests/run.sh are `#!/bin/sh` scripts with no native Windows entry point; installing this session only worked because Git Bash was present. |
| [system] | ls .gitattributes (absent) | No .gitattributes exists, so checked-out line endings depend on each contributor's global core.autocrlf. This session hit exactly that gap: a global autocrlf=true corrupted the checksum file on checkout, and install.sh --verify failed until autocrlf was disabled locally for this repo. |
| [system] | this session, post-fix verification | Verification: after adding encoding=utf-8 to every read_text()/open() call in tools/ws/*.py and reconfiguring stdout/stderr to UTF-8 in __main__.py:main(), the exact command that crashed earlier (a transition with a unicode arrow in its confirmation message) now runs clean with no PYTHONUTF8 or PYTHONIOENCODING env override needed. |
| [system] | this session, tests/ full run before and after | Direction 1 complete: encoding=utf-8 added to every open()/read_text()/write_text() across tools/ws/*.py, runtime/projection.py, and their test suites; ws CLI reconfigures stdout/stderr to UTF-8 at entry. Full test suite: baseline (unmodified repo, this Windows machine) was 30 failures/13 errors/1 skipped out of 414; after the fix, 17 failures/4 errors/1 skipped -- 21 pre-existing failures newly passing, zero new failures introduced (confirmed by diffing failing-test-name sets before/after). |
| [system] | this session | Direction 2 complete: added tools/install.ps1 (native Windows counterpart to install.sh -- Verify/Global/Project/Resolve modes, SHA-256 via Get-FileHash, no external tools needed), tests/test_install.ps1 (13/13 passing, ports test_install.sh), tests/test_clean_checkout.ps1 (ports test_clean_checkout.sh), and tests/run.ps1 (native runner, no Git Bash/WSL needed). tests/test_codex_install.sh was not ported -- it asserts against pre-namespace-prefix skill names that no longer exist in this repo, so it is already broken independent of platform. |
| [system] | this session | Direction 3 complete: added .gitattributes (forces LF for all text files regardless of contributor autocrlf -- fixes the exact checkout corruption hit earlier this session) and a conformance-windows job in .github/workflows/ci.yml running on windows-latest. Gates 1/3/4/5 reuse the existing bash scripts via Git Bash (bundled on windows-latest runners, no OS-specific behavior to exercise there); Gate 2 runs tests/run.ps1 via native PowerShell specifically, to exercise the no-Git-Bash path a real Windows user would take. Verified locally: full unittest suite unaffected (439 tests, same 2 failures/3 errors as before -- pre-existing and unrelated), Gate 5's file-existence checks pass, Gate 3 (verify-conformance.py --all) hits one pre-existing unrelated bug (missing fixtures/personal-institution-work-studio-contract.md, reproduces on a bare clone) -- flagged as a separate task, not fixed here since it's a content/documentation gap unrelated to platform compatibility. |
## Open questions

- Do the actual Mac/Linux code paths already work cleanly as-is, or do they have their own untested gaps? (no CI or native Mac/Linux run has been observed this session — only Windows via Git Bash and native PowerShell)
- Is a GitHub Actions Windows CI job (needed to prevent regression of any fix, per Direction 3 below) acceptable on cost/quota grounds? (external, not discoverable locally)

## Next move

All three directions implemented and locally verified. Nothing has been
committed yet -- director review and commit is the next step. Two unrelated
pre-existing bugs were found and flagged as separate tasks rather than fixed
here: (1) fixtures/personal-institution-work-studio-contract.md is missing
from the repo though referenced by verify-conformance.py and README.md, (2)
tests/test_codex_install.sh asserts against stale pre-namespace skill names.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-21T08:32:56Z — activate-for-exploration

- **State:** explore
- **Status:** active
- **Actor:** director
- **Rationale:** Signal from director: make the system Windows-compatible while staying Mac/Unix-compatible
### 2026-08-21T08:35:29Z — select-all-three-directions

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director selected all three directions, starting with direction 1 (encoding-safety pass)
### 2026-08-21T09:11:49Z — all-three-directions-implemented

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Encoding-safety, native Windows tooling, and repo-level determinism (gitattributes + Windows CI) all implemented and locally verified; two unrelated pre-existing bugs found along the way were flagged as separate tasks rather than folded in
