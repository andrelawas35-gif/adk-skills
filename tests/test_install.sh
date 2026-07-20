#!/bin/sh
# Behavioral tests for tools/install.sh — the dependency-free installer.
# No test framework: plain POSIX sh with a tiny assert helper.

set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
INSTALL="$REPO_ROOT/tools/install.sh"
PLATFORM=claude-code

PASS=0
FAIL=0
ok()   { PASS=$((PASS+1)); echo "  ok    $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  FAIL  $1"; }
check() { if [ "$1" = "$2" ]; then ok "$3"; else bad "$3 (want '$2', got '$1')"; fi; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

echo "test: verify source artifacts"
if "$INSTALL" --platform "$PLATFORM" --verify >/dev/null 2>&1; then
  ok "verify passes on committed artifacts"
else
  bad "verify passes on committed artifacts"
fi

echo "test: global install"
CLAUDE_HOME="$WORK/home/.claude" "$INSTALL" --platform "$PLATFORM" --global >/dev/null
n=$(find "$WORK/home" -name SKILL.md | wc -l | tr -d ' ')
expected=$(find "$REPO_ROOT/skills/core" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')
check "$n" "$expected" "global install places every generated skill"

echo "test: project pin writes lock and skills"
mkdir -p "$WORK/proj/.git"
"$INSTALL" --platform "$PLATFORM" --project "$WORK/proj" >/dev/null
[ -f "$WORK/proj/.claude/skills/alawas-conduct-work-object/SKILL.md" ] \
  && ok "project skill installed" || bad "project skill installed"
[ -f "$WORK/proj/.work-studio/adapter.$PLATFORM.lock" ] \
  && ok "project lock written" || bad "project lock written"
grep -q "^platform=$PLATFORM$" "$WORK/proj/.work-studio/adapter.$PLATFORM.lock" \
  && ok "lock records platform" || bad "lock records platform"

echo "test: project pins coexist across platforms"
"$INSTALL" --platform codex --project "$WORK/proj" >/dev/null
[ -f "$WORK/proj/.work-studio/adapter.$PLATFORM.lock" ] \
  && [ -f "$WORK/proj/.work-studio/adapter.codex.lock" ] \
  && ok "platform-specific locks coexist" || bad "platform-specific locks coexist"

echo "test: precedence resolution"
res=$("$INSTALL" --platform "$PLATFORM" --resolve "$WORK/proj")
case "$res" in
  project:*) ok "pinned project resolves to project adapter" ;;
  *) bad "pinned project resolves to project adapter (got '$res')" ;;
esac
res=$("$INSTALL" --platform "$PLATFORM" --resolve "$WORK")
case "$res" in
  global:*) ok "unpinned dir resolves to global adapter" ;;
  *) bad "unpinned dir resolves to global adapter (got '$res')" ;;
esac

echo "test: precedence resolves upward from a subdirectory"
mkdir -p "$WORK/proj/src/deep"
res=$("$INSTALL" --platform "$PLATFORM" --resolve "$WORK/proj/src/deep")
case "$res" in
  project:*) ok "nested dir inherits project pin" ;;
  *) bad "nested dir inherits project pin (got '$res')" ;;
esac

echo "test: lock uses relative dest path"
lock_dest=$(sed -n 's/^dest=//p' "$WORK/proj/.work-studio/adapter.$PLATFORM.lock")
case "$lock_dest" in
  /*) bad "lock dest is relative (got absolute: '$lock_dest')" ;;
  .claude/skills|.agents/skills|.github/skills) ok "lock dest is relative" ;;
  *) bad "lock dest is relative (got '$lock_dest')" ;;
esac

echo "test: relative lock resolves to correct absolute path"
res=$("$INSTALL" --platform "$PLATFORM" --resolve "$WORK/proj")
case "$res" in
  project:*"$WORK/proj/.claude/skills"*) ok "relative lock resolves to absolute" ;;
  project:*"$WORK/proj/.agents/skills"*) ok "relative lock resolves to absolute" ;;
  project:*"$WORK/proj/.github/skills"*) ok "relative lock resolves to absolute" ;;
  *) bad "relative lock resolves to absolute (got '$res')" ;;
esac

echo "test: tamper detection on installed copy"
tampered="$WORK/proj/.claude/skills/alawas-conduct-work-object/SKILL.md"
echo "corruption" >> "$tampered"
adapter_dir="$REPO_ROOT/adapters/$PLATFORM"
if command -v sha256sum >/dev/null 2>&1; then SUM="sha256sum -c"; else SUM="shasum -a 256 -c"; fi
# Rewrite sums to the installed layout and confirm the tampered file fails.
sed 's#  skills/#  #' "$adapter_dir/SHA256SUMS" > "$WORK/proj/.claude/skills/.sums"
if ( cd "$WORK/proj/.claude/skills" && $SUM .sums >/dev/null 2>&1 ); then
  bad "tampered install fails checksum"
else
  ok "tampered install fails checksum"
fi

echo "test: unknown platform is rejected"
if "$INSTALL" --platform bogus --verify >/dev/null 2>&1; then
  bad "unknown platform rejected"
else
  ok "unknown platform rejected"
fi

echo ""
echo "install tests: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
