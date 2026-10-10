#!/usr/bin/env bash
# Runs every example in chapter order. Exits non-zero if any script fails.
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
for script in ch02_expected_value ch03_precision_recall ch06_retrieval_metrics \
              ch10_breakeven ch11_latency_budget ch12_agreement \
              ch13_eval_sample_size ch17_canary_size ch18_unit_economics \
              ch18_cascade ch25_incident_timeline practice_calcs; do
  echo "=== ${script}.py ==="
  "$PY" "${script}.py"
  echo
done
