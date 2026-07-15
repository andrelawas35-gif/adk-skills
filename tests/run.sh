#!/bin/sh
# Run the full Work Studio test suite: generator contract + installer behavior.
set -eu
REPO_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$REPO_ROOT"

echo "== generator contract (python unittest) =="
python3 -m unittest discover -s tests -p 'test_*.py' -v

echo ""
echo "== installer behavior (sh) =="
sh tests/test_install.sh

echo ""
echo "== Codex installation and precedence (sh) =="
sh tests/test_codex_install.sh

echo ""
echo "== clean-checkout Codex reproducibility (sh) =="
sh tests/test_clean_checkout.sh

echo ""
echo "== drift gate (generator --check) =="
python3 tools/generate-adapters.py --check >/dev/null && echo "no drift"
