"""Lab 5: sample size and calendar for the PayFlow Plus free-trial test."""
from math import ceil, sqrt

from scipy.stats import norm


def sample_size(baseline, lift, alpha=0.05, power=0.80):
    p1, p2 = baseline, baseline + lift
    pooled = (p1 + p2) / 2
    z_alpha, z_power = norm.ppf(1 - alpha / 2), norm.ppf(power)
    spread = (z_alpha * sqrt(2 * pooled * (1 - pooled))
              + z_power * sqrt(p1 * (1 - p1) + p2 * (1 - p2)))
    return ceil((spread / lift) ** 2)


WEEKLY, WINDOW_DAYS = 3_000, 45
n = sample_size(0.060, 0.015)
weeks = ceil(2 * n / WEEKLY)
print(f"Per group: {n:,}. Both groups: {2 * n:,}.")
print(f"Enrollment: {weeks} weeks at {WEEKLY:,} merchants a week.")
print(f"Earliest readout: day {weeks * 7 + WINDOW_DAYS} "
      f"({weeks * 7} days to enroll + {WINDOW_DAYS} days to mature).")
