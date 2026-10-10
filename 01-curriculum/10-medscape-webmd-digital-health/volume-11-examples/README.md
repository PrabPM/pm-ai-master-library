# Volume 11 examples

Scripts and SQL behind every number in the *Medscape / WebMD Senior Technical PM
Field Guide*, Version 2. All data is fictional: the Wrenfield company, its clients,
its clinicians and their NPIs (which start with 9, a first digit real NPIs do not
use) are invented for teaching.

## Run everything

```bash
./run_all.sh
```

This rebuilds `wrenfield.db` (SQLite) from `seed.py`, runs each chapter script and
exits non-zero on the first failure. It needs only the Python standard library.
Tested on Python 3.9, 3.12 and 3.13 (SQLite 3.45 to 3.54), with identical output. The seed uses only
`random.Random.random()`, so the data is the same on every run and every version.

`wrenfield.db` is generated. Delete it whenever you like; the next run rebuilds it.

## Files

| File | Chapter | What it prints |
|---|---|---|
| `seed.py` | Meet Wrenfield | Builds the practice database and lists its tables |
| `common.py` | all | Opens the database, runs a `.sql` file, prints a table |
| `ch06_cpm.py` | 6 | CPM arithmetic and where an advertiser's dollar goes |
| `ch07_yield.py` | 7 | A first-price auction with floors; yield for three settings |
| `ch10_identity.py` | 10 | NPI check digit; the match-rate funnel |
| `ch12_pacing.py` | 12 | Delivery, pacing and frequency for the campaign |
| `ch13_lift.py` | 13 | Lift with a confidence interval, sample ratio check, holdout sizing |
| `ch14_unit_economics.py` | 14 | Contribution margin for one campaign |
| `ch15_workflow.py` | 15 | The cost of one extra minute per visit |
| `ch18_suppression.py` | 18 | Minimum cell size suppression |
| `ch21_data_quality.py` | 21 | Four data-quality rules as queries |
| `ch23_decisions.py` | 23 | Next-best-action decisions and no-action rate |
| `ch24_score.py` | 24, Lab 2 | A transparent clinician engagement score |
| `ch25_integration.py` | 25 | Partner API success, latency and rate limiting |
| `ch27_registration.py` | 27, 28 | Registration funnel by variant and device; retention |
| `ch30_opportunity.py` | 30 | Service-line opportunity with capacity |
| `ch31_closed_loop.py` | 31 | Campaign-to-encounter funnel; three ways to state ROI |
| `ch37_sql.py` | 37 | Decision-to-activation latency; weekly activation funnel |
| `labs.py` | 42, 43 | Latency budget, prescribing study, forecast range, deal funnel |
| `sql/*.sql` | as above | The queries the scripts run, one per file |

Each block of output in the book appears under a line such as `-- Match-rate funnel --`
in the script's output.

## Tables in `wrenfield.db`

`target_list`, `hcp_profile`, `journey_assignment`, `exposure`, `line_item`,
`engagement_event`, `decision_event`, `activation_event`, `integration_event`,
`registration_event`, `login_event`. Column lists are in Chapter 37 and in
`seed.py`.
