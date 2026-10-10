#!/usr/bin/env bash
# Runs every script behind the numbers in Volume 9. Exits non-zero on any failure.
set -euo pipefail
cd "$(dirname "$0")"

if [ -n "${PYTHON:-}" ]; then
  PY="$PYTHON"
elif [ -x ../.venv/bin/python ]; then
  PY=../.venv/bin/python
else
  PY=python3
fi

for script in payflow ch02_segments ch04_message_test ch05_brand_tracker \
              ch08_pricing ch09_launch_tiers ch13_channels ch17_paid_chain \
              ch21_attribution lab4_discount lab5_paid_trades lab6_geo_holdout \
              prose_checks verify_stats; do
  echo "=== $script.py"
  "$PY" "$script.py"
  echo
done
echo "All scripts ran."
