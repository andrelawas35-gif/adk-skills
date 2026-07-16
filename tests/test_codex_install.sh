#!/bin/sh
# End-to-end installer checks at Codex's public skill-discovery boundary.

set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
INSTALL="$REPO_ROOT/tools/install.sh"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

mkdir -p "$WORK/project/.git"

HOME="$WORK/home" "$INSTALL" --platform codex --global >/dev/null
[ -f "$WORK/home/.agents/skills/alawas-conduct-work-object/SKILL.md" ] \
  || fail "global install did not use the Codex user skill directory"
[ -f "$WORK/home/.agents/skills/alawas-pressure-test-decision/SKILL.md" ] \
  || fail "global install did not install both Codex skills"

HOME="$WORK/home" "$INSTALL" --platform codex --project "$WORK/project" >/dev/null
[ -f "$WORK/project/.agents/skills/alawas-conduct-work-object/SKILL.md" ] \
  || fail "project install did not use the Codex repository skill directory"
[ -f "$WORK/project/.agents/skills/alawas-pressure-test-decision/SKILL.md" ] \
  || fail "project install did not install both Codex skills"
[ -f "$WORK/project/.agents/skills/alawas-conduct-work-object/references/CONSEQUENCE-AUTHORITY.md" ] \
  || fail "project install omitted declared shared references"

CONDUCTOR="$WORK/project/.agents/skills/alawas-conduct-work-object/SKILL.md"
DECIDER="$WORK/project/.agents/skills/alawas-pressure-test-decision/SKILL.md"
grep -Fq 'If `updated_at` changed since step 1, report the conflict' "$CONDUCTOR" \
  || fail "installed conductor lost concurrent-write protection"
grep -Fq 'Creating or updating a Work Object of **high** consequence: ask first.' "$CONDUCTOR" \
  || fail "installed conductor lost its high-consequence authority gate"
grep -Fq 'Never export, share, deploy, or write outside `.work-studio/` without' "$CONDUCTOR" \
  || fail "installed conductor lost its export authority gate"
grep -Fq 'Compare `updated_at` with the value from the initial read.' "$DECIDER" \
  || fail "installed decision skill lost its concurrent-write protection"
grep -Fq 'Export requires explicit confirmation showing destination, content, affected files, and sensitivity.' "$DECIDER" \
  || fail "installed decision skill lost its export boundary"

mkdir -p "$WORK/project/src/deep"
resolved=$(HOME="$WORK/home" "$INSTALL" --platform codex --resolve \
  "$WORK/project/src/deep")
case "$resolved" in
  project:"$WORK/project/.agents/skills") ;;
  *) fail "nested project did not resolve the project-pinned Codex adapter" ;;
esac

COPY="$WORK/repository-copy"
mkdir -p "$COPY/tools" "$COPY/adapters"
cp "$INSTALL" "$COPY/tools/install.sh"
cp "$REPO_ROOT/VERSION" "$COPY/VERSION"
cp -R "$REPO_ROOT/adapters/codex" "$COPY/adapters/codex"
printf '\ncorruption\n' >> \
  "$COPY/adapters/codex/skills/alawas-conduct-work-object/SKILL.md"
if HOME="$WORK/tampered-home" "$COPY/tools/install.sh" \
  --platform codex --global >/dev/null 2>&1; then
  fail "tampered Codex source artifacts were installed"
fi

echo "codex install, precedence, integrity, and safety contracts: passed"
