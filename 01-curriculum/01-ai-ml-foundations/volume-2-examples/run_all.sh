#!/usr/bin/env bash
# Runs every script behind the numbers and figures in Volume 2. Exits non-zero on the first failure.
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg
if [ -n "${PYTHON:-}" ]; then PY="$PYTHON"
elif [ -x ../.venv/bin/python ]; then PY=../.venv/bin/python
else PY=python3; fi
echo "Using $("$PY" --version)"
count=0
for script in ch*.py; do
  echo "=== $script"
  "$PY" "$script" > /dev/null
  count=$((count + 1))
done
echo "All $count scripts ran and every check inside them passed."
