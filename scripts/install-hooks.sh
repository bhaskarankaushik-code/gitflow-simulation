#!/usr/bin/env bash
# Git does not version .git/hooks, so install the hook from scripts/.
set -e
root="$(git rev-parse --show-toplevel)"
cp "$root/scripts/pre-commit" "$root/.git/hooks/pre-commit"
chmod +x "$root/.git/hooks/pre-commit"
echo "Installed pre-commit hook."
