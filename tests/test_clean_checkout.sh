#!/bin/sh
# Prove committed Codex artifacts regenerate and install from a clean checkout.

set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
CHECKOUT="$WORK/checkout"

git clone -q --no-hardlinks "$REPO_ROOT" "$CHECKOUT"
cd "$CHECKOUT"

python3 tools/generate-adapters.py --check >/dev/null
HOME="$WORK/home" tools/install.sh --platform codex --global >/dev/null
HOME="$WORK/home" tools/install.sh --platform codex --project . >/dev/null

resolved=$(HOME="$WORK/home" tools/install.sh --platform codex --resolve .)
case "$resolved" in
  project:"$CHECKOUT/.agents/skills") ;;
  *) echo "FAIL: clean checkout did not resolve its project pin" >&2; exit 1 ;;
esac

python3 tools/generate-adapters.py >/dev/null
git diff --exit-code -- adapters >/dev/null

echo "clean-checkout regeneration and Codex install: passed"
