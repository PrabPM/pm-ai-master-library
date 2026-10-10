# Volume 7 examples

The scripts behind every computed number in *User Research and Product Discovery*
(Version 2). Each listing in the book is an excerpt of one of these files, and each
`Output:` block is the complete output of one of them.

PayFlow is a fictional company. All data here is made up for teaching.

## Run everything

```bash
uv venv --python 3.13 .venv
uv pip install --python .venv/bin/python -r requirements.txt
PYTHON=.venv/bin/python ./run_all.sh
```

`run_all.sh` runs each script in turn and stops with a non-zero exit code at the first
failure. Nothing is random and nothing reads the clock, so the output is the same on
every run. Only `ch09_sus.py` needs a third-party package (SciPy, for one t-value).

## What each script shows

| Script | Book | What it computes |
|---|---|---|
| `ch04_how_many_participants.py` | Chapter 4 | Chance that n participants reveal a problem, for three problem rates |
| `ch09_task_success_interval.py` | Chapter 9 | Adjusted Wald interval for small-sample task success |
| `ch09_sus.py` | Chapter 9 | System Usability Scale scores, their mean, and its interval |
| `ch10_funnel.py` | Chapter 10, Figure 0.1 | The onboarding funnel and where merchants are lost |
| `ch11_margin_of_error.py` | Chapter 11 | Survey shares with margins of error; sample sizes needed |
| `ch12_nps.py` | Chapter 12, Figure 12.1 | NPS with its 95% interval at several sample sizes |
| `ch12_nps_compare.py` | Chapter 12 | Interval for a change in NPS; NPS by segment |
| `ch12_csat.py` | Case 1 | CSAT as a top-two-box share with a Wilson interval |
| `ch13_tickets.py` | Chapter 13 | Support tickets by tag, share, and rate per 1,000 starts |
| `ch14_segments.py` | Chapter 14, Figure 16.1 | Finish rate by segment, for two ways of segmenting |
| `ch15_kappa.py` | Chapter 15 | Cohen's kappa for two coders |
| `ch21_validation.py` | Chapter 21 | Wilson intervals for a fake door, a Wizard of Oz test, and a beta |
| `lab4_weighting.py` | Lab 4 | Survey shares reweighted by device |
| `lab5_sus.py` | Lab 5 | SUS scores for five sessions |
| `check_numbers.py` | — | Asserts that the numbers shared across scripts agree |
| `check_answers.py` | Answers, Chapters 11 and 20 | Asserts the arithmetic quoted in prose and in the answers |

The figures in `volume-7-assets/` that show data (the funnel, the NPS chart, and the
persona card's funnel line) are drawn from the same constants.
