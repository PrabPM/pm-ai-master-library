#!/usr/bin/env bash
# Rebuild the practice database and run every example. Exits non-zero on the
# first failure.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1

PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
  if [ -x "../.venv/bin/python" ]; then PYTHON="../.venv/bin/python"
  elif [ -x ".venv/bin/python" ]; then PYTHON=".venv/bin/python"
  else PYTHON="python3"; fi
fi
echo "Using $("$PYTHON" --version) at $PYTHON"

echo
echo "=============== seed.py"
"$PYTHON" seed.py

count=1
for script in ch[0-9][0-9]_*.py labs.py; do
  echo
  echo "=============== $script"
  "$PYTHON" "$script"
  count=$((count + 1))
done

echo
echo "ALL GOOD: $count scripts ran."
