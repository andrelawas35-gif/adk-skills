#!/bin/sh
# Andrelawas Work Studio — one-line global installer.
#
# Convenience wrapper around `tools/install.sh --platform <platform> --global`.
# tools/install.sh copies committed adapter artifacts out of THIS repo, so a
# standalone script fetched over curl has to bring its own copy of the repo
# with it. This wrapper delegates directly when it's already running from
# inside a checkout, and otherwise fetches a throwaway clone first — so both
# of these work:
#
#   tools/install-global.sh [claude-code|codex|github-copilot]
#
#   curl -fsSL https://raw.githubusercontent.com/andrelawas35-gif/adk-skills/master/tools/install-global.sh \
#     | sh -s -- claude-code
#
# Platform defaults to claude-code when omitted.
#
# Env:
#   WORK_STUDIO_REPO   override the git remote to clone from
set -eu

REPO_URL="${WORK_STUDIO_REPO:-https://github.com/andrelawas35-gif/adk-skills}"
PLATFORM="${1:-claude-code}"

case "$PLATFORM" in
  codex|claude-code|github-copilot) ;;
  *) echo "install-global.sh: unknown platform '$PLATFORM' (want codex|claude-code|github-copilot)" >&2; exit 1 ;;
esac

# Already inside a checkout of this repo (the normal case when cloned and run
# as tools/install-global.sh) — delegate directly, no clone needed.
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" 2>/dev/null && pwd) || SCRIPT_DIR=""
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/install.sh" ] && [ -d "$SCRIPT_DIR/../adapters" ]; then
  exec "$SCRIPT_DIR/install.sh" --platform "$PLATFORM" --global
fi

# Piped from curl (or otherwise run without an adjacent checkout) — fetch a
# throwaway clone and install from that.
command -v git >/dev/null 2>&1 || { echo "install-global.sh: git is required" >&2; exit 1; }

WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
git clone --depth 1 "$REPO_URL" "$WORK/adk-skills" >&2
"$WORK/adk-skills/tools/install.sh" --platform "$PLATFORM" --global
