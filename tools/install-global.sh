#!/bin/sh
# Andrelawas Work Studio — global skill installer for Claude Code on the web/mobile.
#
# Installs the checksummed Claude Code adapter skills into the global user
# skills directory (~/.claude/skills) so EVERY project opened in this
# environment inherits them — not just repos that pin .claude/skills.
#
# Claude Code on the web runs each session in an ephemeral container, so a
# global install does not persist between sessions. Run this from the
# environment's SETUP SCRIPT instead: it re-installs on every startup, which
# makes the ephemerality moot.
#
# Usage (from the environment setup script — one line, no checkout needed):
#   curl -fsSL https://raw.githubusercontent.com/andrelawas35-gif/adk-skills/master/tools/install-global.sh | sh
#
# Or, if this repo is already checked out:
#   tools/install-global.sh
#
# Environment overrides:
#   ADK_REF     git ref to install from (branch or tag). Default: master.
#   ADK_REPO    clone URL. Default: the public andrelawas35-gif/adk-skills repo.
#   CLAUDE_HOME Claude config home. Default: $HOME/.claude.

set -eu

ADK_REPO="${ADK_REPO:-https://github.com/andrelawas35-gif/adk-skills.git}"
ADK_REF="${ADK_REF:-master}"
CACHE_DIR="${ADK_CACHE:-$HOME/.cache/adk-skills}"

log() { echo "[install-global] $*"; }

# Prefer an existing checkout (script run from inside the repo); otherwise
# clone a fresh shallow copy so the wrapper works when curl-piped.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd || echo "")
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/install.sh" ]; then
  REPO_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
  log "using existing checkout: $REPO_ROOT"
else
  log "cloning $ADK_REPO@$ADK_REF into $CACHE_DIR"
  rm -rf "$CACHE_DIR"
  git clone --depth 1 --branch "$ADK_REF" "$ADK_REPO" "$CACHE_DIR" >/dev/null 2>&1 \
    || git clone --depth 1 "$ADK_REPO" "$CACHE_DIR" >/dev/null 2>&1
  REPO_ROOT="$CACHE_DIR"
fi

# Delegate to the checksum-verifying installer.
log "installing claude-code skills into ${CLAUDE_HOME:-$HOME/.claude}/skills"
sh "$REPO_ROOT/tools/install.sh" --platform claude-code --global

log "done — skills are available to every project in this environment"
