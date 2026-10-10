#!/usr/bin/env bash
# Runs every script behind the book's numbers. Stops at the first failure.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
for script in \
    ch04_how_many_participants.py \
    ch09_task_success_interval.py \
    ch09_sus.py \
    ch10_funnel.py \
    ch11_margin_of_error.py \
    ch12_nps.py \
    ch12_nps_compare.py \
    ch12_csat.py \
    ch13_tickets.py \
    ch14_segments.py \
    ch15_kappa.py \
    ch21_validation.py \
    lab4_weighting.py \
    lab5_sus.py \
    check_numbers.py \
    check_answers.py
do
    echo "=== $script"
    "$PY" "$script"
    echo
done
echo "All scripts ran."
