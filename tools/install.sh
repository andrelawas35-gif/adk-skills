#!/bin/sh
# Andrelawas Work Studio — dependency-free adapter installer.
#
# Installs committed, checksummed adapter artifacts into a platform's skills
# directory. Requires NO Python at runtime — only POSIX sh and a SHA-256 tool
# (sha256sum or shasum), both standard on macOS and Linux.
#
# Usage:
#   tools/install.sh --platform <name> --global            Install global bootstrap
#   tools/install.sh --platform <name> --project [DIR]     Pin adapter to a project (DIR default: .)
#   tools/install.sh --platform <name> --verify            Verify source artifacts only
#   tools/install.sh --platform <name> --resolve [DIR]     Print which install wins for DIR
#   tools/install.sh --platform <name> --dest DIR ...      Override the install directory
#
#   --dry-run   Show what would happen without writing.
#
# Platforms: codex, claude-code, github-copilot
#
# Precedence: a project-pinned adapter always takes precedence over the global
# bootstrap install. `--resolve` reports the effective adapter for a directory.

set -eu

PLATFORM=""
MODE=""
TARGET_DIR=""
DEST_OVERRIDE=""
DRY_RUN=0

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

die() { echo "install.sh: $*" >&2; exit 1; }

# ── SHA-256 tool detection ───────────────────────────────────────────────────
# Prints a command that, run as `$SHA_CHECK` inside a dir with SHA256SUMS,
# verifies every listed file.
sha_check_cmd() {
  if command -v sha256sum >/dev/null 2>&1; then
    echo "sha256sum -c SHA256SUMS"
  elif command -v shasum >/dev/null 2>&1; then
    echo "shasum -a 256 -c SHA256SUMS"
  else
    die "no SHA-256 tool found (need sha256sum or shasum)"
  fi
}

# ── Per-platform install directories ─────────────────────────────────────────
global_dir() {
  case "$1" in
    claude-code)    echo "${CLAUDE_HOME:-$HOME/.claude}/skills" ;;
    codex)          echo "$HOME/.agents/skills" ;;
    github-copilot) echo "${COPILOT_HOME:-$HOME/.copilot}/skills" ;;
    *) die "unknown platform: $1" ;;
  esac
}

project_subdir() {
  case "$1" in
    claude-code)    echo ".claude/skills" ;;
    codex)          echo ".agents/skills" ;;
    github-copilot) echo ".github/skills" ;;
    *) die "unknown platform: $1" ;;
  esac
}

# ── Argument parsing ─────────────────────────────────────────────────────────
while [ $# -gt 0 ]; do
  case "$1" in
    --platform) PLATFORM="${2:-}"; shift 2 ;;
    --global)   MODE="global"; shift ;;
    --project)  MODE="project"
                if [ $# -ge 2 ] && [ "${2#-}" = "$2" ]; then TARGET_DIR="$2"; shift 2; else TARGET_DIR="."; shift; fi ;;
    --verify)   MODE="verify"; shift ;;
    --resolve)  MODE="resolve"
                if [ $# -ge 2 ] && [ "${2#-}" = "$2" ]; then TARGET_DIR="$2"; shift 2; else TARGET_DIR="."; shift; fi ;;
    --dest)     DEST_OVERRIDE="${2:-}"; shift 2 ;;
    --dry-run)  DRY_RUN=1; shift ;;
    -h|--help)  sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) die "unknown argument: $1" ;;
  esac
done

[ -n "$PLATFORM" ] || die "missing --platform (codex|claude-code|github-copilot)"
[ -n "$MODE" ] || die "missing mode (--global | --project | --verify | --resolve)"

SRC="$REPO_ROOT/adapters/$PLATFORM"
[ -d "$SRC" ] || die "no adapter for platform '$PLATFORM' at $SRC"
[ -f "$SRC/SHA256SUMS" ] || die "missing $SRC/SHA256SUMS (run tools/generate-adapters.py)"

VERSION=$(cat "$REPO_ROOT/VERSION" 2>/dev/null || echo "0.0.0")

# ── verify: check source artifacts against their checksums ───────────────────
verify_source() {
  SHA_CHECK=$(sha_check_cmd)
  ( cd "$SRC" && eval "$SHA_CHECK" ) >/dev/null \
    || die "checksum verification FAILED for $PLATFORM adapter — refusing to install"
  echo "verified: $PLATFORM adapter artifacts match SHA256SUMS"
}

# ── resolve: report effective adapter (project pin beats global) ─────────────
resolve() {
  start=$(CDPATH= cd -- "$TARGET_DIR" && pwd)
  dir="$start"
  while :; do
    lock="$dir/.work-studio/adapter.$PLATFORM.lock"
    legacy_lock="$dir/.work-studio/adapter.lock"
    if [ -f "$lock" ]; then
      pinned=$(sed -n 's/^dest=//p' "$lock")
      echo "project:$pinned"
      return 0
    fi
    if [ -f "$legacy_lock" ] && grep -q "^platform=$PLATFORM$" "$legacy_lock" 2>/dev/null; then
      pinned=$(sed -n 's/^dest=//p' "$legacy_lock")
      echo "project:$pinned"
      return 0
    fi
    [ -d "$dir/.git" ] && break        # stop at repo boundary
    parent=$(dirname -- "$dir")
    [ "$parent" = "$dir" ] && break     # stop at filesystem boundary
    dir="$parent"
  done
  echo "global:$(global_dir "$PLATFORM")"
}

# ── install: verify, then copy skills into the destination ───────────────────
do_install() {
  verify_source

  if [ -n "$DEST_OVERRIDE" ]; then
    DEST="$DEST_OVERRIDE"
  elif [ "$MODE" = "global" ]; then
    DEST=$(global_dir "$PLATFORM")
  else
    DEST="$TARGET_DIR/$(project_subdir "$PLATFORM")"
  fi

  echo "installing $PLATFORM adapter v$VERSION → $DEST"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "(dry-run) would copy $SRC/skills/* to $DEST"
    [ "$MODE" = "project" ] && echo "(dry-run) would write $TARGET_DIR/.work-studio/adapter.$PLATFORM.lock"
    return 0
  fi

  mkdir -p "$DEST"
  # Copy each skill directory deterministically.
  for skill_dir in "$SRC"/skills/*/; do
    [ -d "$skill_dir" ] || continue
    name=$(basename "$skill_dir")
    rm -rf "$DEST/$name"
    cp -R "$skill_dir" "$DEST/$name"
  done

  # Verify the installed copy byte-for-byte against the source checksums.
  # SHA256SUMS paths are `skills/<name>/...`; installed paths drop the
  # `skills/` prefix, so rewrite the sums and check them inside DEST.
  SHA_CHECK=$(sha_check_cmd)
  sed 's#  skills/#  #' "$SRC/SHA256SUMS" > "$DEST/.work-studio-SHA256SUMS"
  ( cd "$DEST" && eval "${SHA_CHECK% *} .work-studio-SHA256SUMS" ) >/dev/null 2>&1 \
    || { rm -f "$DEST/.work-studio-SHA256SUMS"; die "installed copy failed verification at $DEST"; }
  rm -f "$DEST/.work-studio-SHA256SUMS"

  if [ "$MODE" = "project" ]; then
    lockdir="$TARGET_DIR/.work-studio"
    mkdir -p "$lockdir"
    dest_abs=$(CDPATH= cd -- "$DEST" && pwd)
    {
      echo "# Work Studio adapter pin — this project overrides the global install."
      echo "platform=$PLATFORM"
      echo "version=$VERSION"
      echo "dest=$dest_abs"
    } > "$lockdir/adapter.$PLATFORM.lock"
    legacy_lock="$lockdir/adapter.lock"
    if [ -f "$legacy_lock" ] && grep -q "^platform=$PLATFORM$" "$legacy_lock" 2>/dev/null; then
      rm -f "$legacy_lock"
    fi
    echo "pinned: $lockdir/adapter.$PLATFORM.lock (project overrides global for $PLATFORM)"
  fi

  echo "done."
}

case "$MODE" in
  verify)  verify_source ;;
  resolve) resolve ;;
  global|project) do_install ;;
  *) die "unhandled mode: $MODE" ;;
esac
