#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
INSTALLER="$ROOT/tools/install-mattpocock-skills.sh"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

SOURCE="$WORK/source"
TARGET="$WORK/project/.agents/skills"
LOCK="$WORK/project/.agents/mattpocock-skills.lock"

mkdir -p "$SOURCE/skills/engineering/example" "$SOURCE/skills/deprecated/legacy"
printf '%s\n' '---' 'name: example' 'description: Example skill' '---' > "$SOURCE/skills/engineering/example/SKILL.md"
printf '%s\n' '---' 'name: legacy' 'description: Deprecated skill' '---' > "$SOURCE/skills/deprecated/legacy/SKILL.md"

git -C "$SOURCE" init -q
git -C "$SOURCE" add .
git -C "$SOURCE" -c user.name=Test -c user.email=test@example.com commit -qm 'fixture skills'
COMMIT=$(git -C "$SOURCE" rev-parse HEAD)

mkdir -p "$(dirname -- "$LOCK")"
printf '%s\n' \
  'version=1' \
  'repository=https://example.invalid/mattpocock/skills.git' \
  "commit=$COMMIT" \
  'categories=engineering productivity' > "$LOCK"

sh "$INSTALLER" --source "$SOURCE" --target "$TARGET" --lock "$LOCK"
test -f "$TARGET/example/SKILL.md"
test ! -e "$TARGET/legacy"
sh "$INSTALLER" --verify --source "$SOURCE" --target "$TARGET" --lock "$LOCK"

printf '%s\n' 'tampered' > "$TARGET/example/SKILL.md"
if sh "$INSTALLER" --verify --source "$SOURCE" --target "$TARGET" --lock "$LOCK"; then
  echo 'verification accepted a tampered skill' >&2
  exit 1
fi
