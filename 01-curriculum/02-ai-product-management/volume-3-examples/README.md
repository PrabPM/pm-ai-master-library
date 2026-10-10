# Volume 3 examples

Every number the *Practical AI Product Manager Field Guide* computes comes from
one of these scripts. PayFlow and PayFlow Assist are fictional, and every input
is made up for teaching. The token prices in `payflow.py` are illustrative and
are not any provider's price list.

## Run

```bash
./run_all.sh                 # uses python3 on your PATH
PYTHON=../.venv/bin/python ./run_all.sh
```

Python 3.13, standard library only. Nothing to install. The latency simulation
is seeded, and the incident uses fixed dates, so every run prints the same text.

## Files

| File | Chapter | What it computes |
|---|---|---|
| `payflow.py` | all | Shared inputs: ticket volumes, token counts, prices |
| `ch02_expected_value.py` | 2 | Expected monthly value and break-even accuracy of four options |
| `ch03_precision_recall.py` | 3 | Precision, recall, F1, accuracy and cost at three thresholds |
| `ch06_retrieval_metrics.py` | 6 | Recall@3, MRR and nDCG@3 for keyword and hybrid retrieval |
| `ch10_breakeven.py` | 10 | Hosted API versus self-hosting break-even |
| `ch11_latency_budget.py` | 11 | Per-stage and end-to-end P50 and P95 latency |
| `ch12_agreement.py` | 12 | Reviewer agreement and Cohen's kappa |
| `ch13_eval_sample_size.py` | 13 | Wilson intervals and cases needed to tell 92% from 95% |
| `ch17_canary_size.py` | 17 | Canary size needed to see a rare failure |
| `ch18_unit_economics.py` | 18 | Cost per answer, ticket and resolved ticket, with sensitivities |
| `ch18_cascade.py` | 18 | Cheap-model-first cascade economics |
| `ch25_incident_timeline.py` | 25 | Incident durations from an event log |
| `practice_calcs.py` | 22, 27, Templates | Chapter 22's packaging numbers, the lab answers and the vendor matrix |

Listings in the book are the lines between `# [listing]` and `# [end listing]`
in each file. Each `Output:` block in the book is that script's printed output.
