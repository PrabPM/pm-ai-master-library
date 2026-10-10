# Companion code for Growth Strategy and Experimentation (Version 2)

Every Python listing in the handbook is an excerpt of a file in this folder, and
every `Output:` block in the handbook is the complete output of one of these
scripts. PayFlow is fictional, and so is every number here.

## What you need

- Python 3.13 (the listings were executed on Python 3.13.2).
- The libraries pinned in `requirements.txt`: NumPy, SciPy, pandas, statsmodels.
  No network access and no data files. Random numbers are seeded, so the output
  is the same on every run.

## Set up and run

```bash
# from the folder that contains volume-8-examples/
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r volume-8-examples/requirements.txt

# without uv:
# python3 -m venv .venv && .venv/bin/pip install -r volume-8-examples/requirements.txt

./volume-8-examples/run_all.sh                          # every script
.venv/bin/python volume-8-examples/ch19_sample_size.py  # or one at a time
```

`run_all.sh` uses `../.venv/bin/python` if it exists. To use another interpreter,
set `PYTHON=/path/to/python` first. It exits non-zero on the first failure.

## Files

| File | Where | What it computes |
|---|---|---|
| `ch01_growth_model.py` | Ch. 1 | Twelve-month growth model and a sensitivity table |
| `ch05_channel_saturation.py` | Ch. 5 | Average and marginal CAC on a saturating channel |
| `ch07_virality.py` | Ch. 7 | Viral factor K, its ceiling, and the effect of cycle time |
| `ch10_activation.py` | Ch. 10 | Retention with and without four candidate activation events |
| `ch11_mix_shift.py` | Ch. 11 | A rate drop split into real change and mix shift |
| `ch14_retention.py` | Ch. 14 | Cohort table, pooled retention curve, expected active months, LTV |
| `ch15_winback.py` | Ch. 15 | Lift against a holdout, with interval and p-value |
| `ch16_price_test.py` | Ch. 16 | A price test read at one month and at twelve |
| `ch17_dunning.py` | Ch. 17 | Involuntary churn before and after a recovery sequence |
| `ch18_ice.py` | Ch. 18 | ICE scores for an experiment backlog |
| `ch19_sample_size.py` | Ch. 19 | Sample size for a two-proportion test at several effect sizes |
| `ch20a_assignment.py` | Ch. 20 | Deterministic assignment by hashing |
| `ch20b_srm.py` | Ch. 20 | Sample ratio mismatch chi-square check |
| `ch21_readout.py` | Ch. 21 | Difference, 95% interval, and p-value for two proportions |
| `ch22a_peeking.py` | Ch. 22 | Simulation: false positives against number of looks (seed 21) |
| `ch22b_cuped.py` | Ch. 22 | CUPED variance reduction on synthetic data (seed 2026) |
| `ch23_did.py` | Ch. 23 | Difference-in-differences with a regression interval |
| `lab1_terminal.py` | Lab 1 | Growth model for three options |
| `lab2_allocation.py` | Lab 2 | Greedy budget allocation across three channels |
| `lab3_assist_activation.py` | Lab 3 | Candidate activation events for Assist |
| `lab5_trial_test.py` | Lab 5 | Sample size and calendar for a trial test |
| `lab6_readout_review.py` | Lab 6 | Split check and the multiple-segment arithmetic |
| `lab7_pql.py` | Lab 7 | Value per sales call by tier |
| `case3_flat_result.py` | Case 3 | Interval for a flat result |

## Notes on method

- Two-proportion tests use the normal approximation: an unpooled standard error
  for the confidence interval and a pooled one for the z-test.
- The sample size formula is the standard two-sided one for two proportions.
- The peeking simulation draws 20,000 A/A tests per row, so each rate is good to
  about a quarter of a percentage point.
- `ch14_retention.py` extends each curve at its average monthly ratio over the
  last three observed months. That is an assumption, stated in the chapter.
