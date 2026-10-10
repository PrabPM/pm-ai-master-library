"""Chapter 13: a survival table, churn by reason, and one leading indicator."""
from collections import Counter

import numpy as np

from payflow import COHORTS, simulate, survival_table

rows = simulate()
table = survival_table(rows)
MAX_AGE = len(COHORTS) - 1


def naive_churn(rows):
    """WRONG on purpose: everyone who ever left / everyone who ever activated."""
    return sum(1 for _, _, churned, _ in rows if churned) / len(rows)


def leading_indicator(rows, seed=13):
    """Did payment volume fall by half or more versus the month before?

    The flag is simulated: it fires in 58% of final months before a merchant
    leaves and in 6% of ordinary months.
    """
    rng = np.random.default_rng(seed)
    counts = Counter()
    for cohort, last, churned, _ in rows:
        for month in range(1, last + 1):
            if month + 1 > MAX_AGE - cohort:
                continue                      # next month not observed yet
            leaves_next = churned and last == month
            flagged = rng.random() < (0.58 if leaves_next else 0.06)
            counts[(flagged, leaves_next)] += 1
    return counts


if __name__ == "__main__":
    print("age  at risk   left  hazard  survival")
    for age, at_risk, left, h, surv in table:
        print(f"{age:>3}{at_risk:>9,}{left:>7}{h:>8.1%}{surv:>10.1%}")
    print(f"Naive 'churn rate' (ever left / ever activated): "
          f"{naive_churn(rows):.1%}")

    print()
    reasons = Counter(reason for _, _, churned, reason in rows if churned)
    total = sum(reasons.values())
    for reason, n in reasons.most_common():
        print(f"{reason:<24}{n:>6,}{n / total:>7.0%}")

    print()
    c = leading_indicator(rows)
    for flagged, label in [(True, "volume fell 50%+"), (False, "no such fall")]:
        left, stayed = c[(flagged, True)], c[(flagged, False)]
        print(f"{label:<18} merchant-months {left + stayed:>6,}   "
              f"left next month {left / (left + stayed):.1%}")
    caught = c[(True, True)] / (c[(True, True)] + c[(False, True)])
    print(f"Share of leavers the flag caught: {caught:.0%}")
