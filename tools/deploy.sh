#!/bin/bash
# Rebuild, run the test, commit and push to GitHub Pages. Run: bash tools/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build.py
node tests/score-test.js
git add -A
git diff --cached --quiet || git commit -qm "${1:-Update}"
git push -q origin main
echo "live at https://sathyacrisren-ui.github.io/compass/ within a minute"
