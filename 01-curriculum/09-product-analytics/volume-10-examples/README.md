# Companion code for Product Analytics and Financial Analysis (Version 2)

Every Python listing in the handbook is an excerpt of a file in this folder, and
every `Output:` block in the handbook is part of what one of these scripts prints.
PayFlow is fictional, and so is every number here.

## What you need

- Python 3.13.
- The libraries pinned in `requirements.txt`: NumPy, pandas, SciPy, statsmodels.
- No network access and no data files. Random numbers are seeded, so the output is
  the same on every run.

## Set up and run

```bash
# from the folder that contains volume-10-examples/
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r volume-10-examples/requirements.txt

# without uv:
# python3 -m venv .venv && .venv/bin/pip install -r volume-10-examples/requirements.txt

./volume-10-examples/run_all.sh                       # every script, in chapter order
.venv/bin/python volume-10-examples/ch17_ltv.py       # or one at a time
```

`run_all.sh` uses `../.venv/bin/python` if it exists. To use another interpreter, set
`PYTHON=/path/to/python` first. It exits non-zero on the first failure.

## Files

| File | Where | What it computes |
|---|---|---|
| `payflow.py` | Shared | Unit-economics constants, the seeded merchant simulation, the survival table |
| `ch03_metric_tree.py` | Ch. 3, 27 | Each input's share of a change in weekly volume |
| `ch08_consent.py` | Ch. 8 | Measured traffic before and after a consent banner change |
| `ch10_funnel.py` | Ch. 10 | Step and overall conversion for the August funnel |
| `ch11_cohorts.py` | Ch. 11 | Cohort retention table and month-3 retention by quarter |
| `ch12_engagement.py` | Ch. 12 | DAU, WAU, MAU, stickiness and the L28 histogram (seed 12) |
| `ch13_churn.py` | Ch. 13 | Survival table, churn by reason, a leading indicator (seed 13) |
| `ch14_correlation.py` | Ch. 14 | Simpson's paradox and a confounded correlation (seed 14) |
| `ch15_liquidity.py` | Ch. 15 | Fill rate, time to match, balance and quality by category |
| `ch16_unit_economics.py` | Ch. 16 | One merchant-month, three payment sizes, the segment's quarter |
| `ch17_ltv.py` | Ch. 17 | LTV by formula, by cohort, discounted, and by cohort group |
| `ch18_cac.py` | Ch. 18 | Four CACs, payback, LTV:CAC, ROAS at four levels, ROI |
| `ch19_projection.py` | Ch. 19 | Driver-based Quickstart model, three scenarios, NPV, IRR, payback |
| `ch20_decision.py` | Ch. 20 | Expected value, sensitivity table, Monte Carlo (seed 20), value of information |
| `ch21_power.py` | Ch. 21 | Sample sizes, and two test results read with intervals |
| `ch22_did.py` | Ch. 22 | Geo holdout read with difference-in-differences (seed 223) |
| `ch23_attribution.py` | Ch. 23 | Four attribution rules next to holdout results |
| `ch24_ai_eval.py` | Ch. 24 | Evaluation-set scores, online signals, cost, latency (seed 24), review sample size |
| `labs.py` | Ch. 25 | Numbers behind the model answers of Labs 1 and 3 to 7 |
| `cases.py` | Ch. 26 | Numbers behind Cases 2 and 3 (seed 26) |
| `interview.py` | Ch. 27, 28 | The dollar cost of the drop, and the coffee-shop estimate |

## Notes on method

- The merchant simulation in `payflow.py` activates twelve monthly cohorts and removes
  merchants with a monthly hazard that falls with age. Cohorts from April 2026 on leave
  faster in their first three months. The analysis scripts are not told this.
- Survival is estimated the Kaplan-Meier way: a merchant counts as at risk only at
  ages its cohort has reached.
- LTV beyond the observed eleven months assumes the pooled hazard of months 7 to 11
  continues. That is an assumption, stated in the chapter.
- Two-proportion tests use statsmodels: a z-test with a pooled standard error and a
  Wald interval for the difference. Sample sizes use the arcsine effect size.
- The difference-in-differences regression clusters standard errors by region. With
  twelve regions the interval is approximate.
- IRR is found by bisection on a monthly rate and reported as an annual rate.

## The SQL in the book

The SQL examples do not live here. They run against `payflow_practice.sql`, the
PostgreSQL practice database that ships with Volume 5, with `search_path` set to
`payflow` and the session time zone set to UTC.
