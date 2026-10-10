# Volume 9 examples

The scripts that produced every computed number in *Product Marketing and
Go-to-Market*, Version 2. PayFlow is fictional and so is every input.

## Run

```bash
./run_all.sh
```

The chapter and lab scripts need only Python 3.13 and its standard library.
`verify_stats.py` cross-checks three formulas against statsmodels and skips
itself if statsmodels is missing. To install it in a private environment:

```bash
uv venv --python 3.13 ../.venv
uv pip install --python ../.venv/bin/python -r requirements.txt
```

`run_all.sh` uses `../.venv/bin/python` when it exists, or `$PYTHON`, or `python3`.
Nothing is random and no script reads the clock, so the output never changes.

## Files

| File | Used in | What it computes |
|---|---|---|
| `payflow.py` | Meet PayFlow | Fees, contribution, churn and payback helpers |
| `ch02_segments.py` | Chapter 2 | Beta results by segment; loss reasons |
| `ch04_message_test.py` | Chapter 4 | Wilson intervals for three headlines |
| `ch05_brand_tracker.py` | Chapter 5 | Interval for a change between tracker waves |
| `ch08_pricing.py` | Chapter 8 | Pay-as-you-go against a flat subscription |
| `ch09_launch_tiers.py` | Chapter 9 | Launch tier scores for five releases |
| `ch13_channels.py` | Chapter 13 | CAC by channel, blended CAC, marginal CAC |
| `ch17_paid_chain.py` | Chapter 17 | Impressions to payback; ROAS against margin |
| `ch21_attribution.py` | Chapter 21 | Three attribution models and a lift test |
| `lab4_discount.py` | Lab 4 | A flat discount against a volume tier |
| `lab5_paid_trades.py` | Lab 5 | Average and marginal payback for a campaign |
| `lab6_geo_holdout.py` | Lab 6 | Difference-in-differences for a geo test |
| `prose_checks.py` | Throughout | Asserts the small sums quoted in the text |
| `verify_stats.py` | Chapters 4, 5, 21 | Cross-check against statsmodels |
