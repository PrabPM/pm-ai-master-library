"""Case 2 (chapter 124): sizing the evaluation and the canary for a support
assistant."""
from math import ceil, sqrt

import numpy as np


def golden_set_size(p0, p1, z_alarm=3.0, z_power=1.2816):
    """Cases needed so that one night at p1 falls below the alarm line
    (z_alarm standard errors under p0) with 90% probability."""
    need = (z_alarm * sqrt(p0 * (1 - p0)) + z_power * sqrt(p1 * (1 - p1))) / (p0 - p1)
    return ceil(need ** 2)


def ab_sample_size(sd, effect, z_alpha=1.96, z_beta=0.8416):
    """Tickets per arm to detect a difference in means (5% two-sided, 80% power)."""
    return ceil(2 * (z_alpha + z_beta) ** 2 * sd ** 2 / effect ** 2)


if __name__ == "__main__":
    n_gold = golden_set_size(0.92, 0.89)
    print(f"golden set to catch 0.92 -> 0.89 in one night: {n_gold:,} cases")
    print(f"judging cost at USD 0.004 a case: USD {n_gold * 0.004:.2f} a night")

    n_arm = ab_sample_size(sd=4.0, effect=0.5)
    canary_per_day = 20_000 * 0.05
    print(f"canary: {n_arm:,} tickets per arm to see a 0.5-minute change")
    print(f"at 5% of 20,000 tickets a day that is {n_arm / canary_per_day:.1f} days "
          f"of traffic")

    cost = 0.0288
    print(f"cost per ticket USD {cost:.4f} against a ceiling of USD 0.03: "
          f"{'pass' if cost <= 0.03 else 'fail'}")

    assert n_gold == 1640 and n_arm == 1005
    assert np.isclose(n_arm / canary_per_day, 1.005)
