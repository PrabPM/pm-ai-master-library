"""Chapter 11: a cohort retention table from activation month and activity."""
from payflow import COHORTS, simulate

rows = simulate()
n_months = len(COHORTS)

retention = []     # retention[c][k]: share of cohort c still paying in month k
for c in range(n_months):
    cohort = [last for cc, last, _, _ in rows if cc == c]
    max_age = n_months - 1 - c
    retention.append([sum(last >= k for last in cohort) / len(cohort)
                      for k in range(max_age + 1)])

if __name__ == "__main__":
    print("Share of each activation cohort still paying, by months since "
          "activation (%)")
    print("cohort     n " + "".join(f"{'M' + str(k):>5}" for k in range(n_months)))
    for c, row in enumerate(retention):
        size = sum(1 for cc, *_ in rows if cc == c)
        print(f"{COHORTS[c]} {size:>4} " + "".join(f"{r * 100:5.0f}" for r in row))

    print()
    print("Month-3 retention, by cohort quarter")
    for label, cs in [("Oct-Dec 2025", (0, 1, 2)), ("Jan-Mar 2026", (3, 4, 5)),
                      ("Apr-Jun 2026", (6, 7, 8))]:
        kept = sum(1 for c, last, _, _ in rows if c in cs and last >= 3)
        size = sum(1 for c, *_ in rows if c in cs)
        print(f"  {label}: {kept:,} of {size:,} = {kept / size:.1%}")

    print()
    months = [(8, "Jun"), (9, "Jul"), (10, "Aug"), (11, "Sep")]
    active = [sum(1 for c, last, _, _ in rows if c <= t and last >= t - c)
              for t, _ in months]
    print("Merchants from these cohorts active in 2026: "
          + "  ".join(f"{name} {n:,}" for (_, name), n in zip(months, active)))
