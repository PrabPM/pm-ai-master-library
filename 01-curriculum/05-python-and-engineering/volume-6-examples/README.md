# Companion code for the Python Handbook for Payment Systems (Version 2)

Every Python listing in the handbook is taken from a file in this folder, and
every `Output:` block in the handbook was pasted from running that file.

## What you need

- Python 3.13 or later. The listings were executed on Python 3.13.2 and the whole
  folder also passes on Python 3.14.4.
- The libraries pinned in `requirements.txt` (Pydantic, SQLAlchemy, Hypothesis,
  Polars, pytest). Nothing else: no database server, no network access, no payment
  provider account. Databases are SQLite; the bank is `fake_provider.py`.

## Set up and run

```bash
# from the folder that contains volume-6-examples/
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r volume-6-examples/requirements.txt

# without uv:
# python3 -m venv .venv && .venv/bin/pip install -r volume-6-examples/requirements.txt

./volume-6-examples/run_all.sh                  # every example, then the tests
.venv/bin/python volume-6-examples/ch03_money.py   # or one chapter at a time
```

`run_all.sh` uses `../.venv/bin/python` if it exists. To use a different
interpreter, set `PYTHON=/path/to/python` first. It exits non-zero on any failure.

## Files

| File | Chapter | What it shows |
|---|---|---|
| `fake_provider.py` | all | NorthBank, an in-memory bank with scripted failures |
| `ch00_primer.py` | primer | Type hints, enums, dataclasses, exceptions, `with`, decorators, `async` |
| `ch01_environment.py` | 1 | Checks your Python and library versions |
| `ch02_domain.py` | 2 | A payment state machine that refuses illegal moves |
| `ch03_money.py` | 3 | Float losing a cent; `Decimal`, minor units, rounding, splitting |
| `ch04_time_ids.py` | 4 | Naive vs aware time, the 23-hour day, cutoffs, what IDs leak |
| `ch05_boundaries.py` | 5 | Pydantic at the edge; four error families; one public error shape |
| `ch06_config.py` | 6 | Fail-fast settings and masked secrets |
| `ch07_logging.py` | 7 | A log line that leaks a card number, and one that cannot |
| `ch08_transactions.py` | 8 | The check-then-insert race; a lock held across a network call |
| `ch09_api.py` | 9 | Offset vs cursor pagination; authentication vs authorization |
| `ch10_idempotency.py` | 10 | The double charge, then the idempotency key |
| `ch11_webhooks.py` | 11 | Signatures over the raw body; duplicates and ordering |
| `ch12_retries.py` | 12 | A retry storm; backoff with jitter; what is safe to retry |
| `ch13_outbox_saga.py` | 13 | The lost event; the outbox; a saga with compensation |
| `ch14_workers.py` | 14 | Visibility timeout, dead letters, a job that runs twice |
| `ch15_ledger.py` | 15 | A double-entry ledger that refuses an unbalanced journal |
| `ch16_reconciliation.py` | 16 | Classifying planted differences against a bank file |
| `ch17_concurrency.py` | 17 | asyncio, threads and processes timed on the same work |
| `ch18_polars.py` | 18 | Lazy Parquet scans, pushdown, control totals |
| `ch19_find_bug.py` | 19 | Hypothesis finds the payment nobody tested |
| `ch20_observability.py` | 20 | RED, an SLI, an error budget, a trace |
| `ch21_security.py` | 21 | SQL injection, SSRF through webhook URLs, tokenization |
| `ch22_ai_tools.py` | 22 | A tool boundary that blocks what a model proposes |
| `ch23_deploy.py` | 23 | A rename that breaks a rollout; counting round trips |
| `labs.py` | 24 | Model answers for the code labs |
| `cases.py` | 25 | The worked cases, built from the chapter modules |
| `test_ch19_properties.py` | 19 | Property-based tests |
| `test_failure_cases.py` | 19 | One test per production failure |
| `test_labs.py` | 24 | Tests for the lab answers |
| `extra_py314_notes.py` | notes | Python 3.14+ features; skips itself on 3.13 |

Timing lines in `ch17_concurrency.py` vary a little from run to run. Everything
else is deterministic: randomness is seeded and clocks are fixed.
