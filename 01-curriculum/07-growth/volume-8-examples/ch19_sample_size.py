"""Chapter 19: merchants needed per group for a two-proportion A/B test."""
from math import ceil, sqrt

from scipy.stats import norm


def sample_size(baseline, lift, alpha=0.05, power=0.80):
    """Merchants per group to detect baseline -> baseline + lift, two-sided."""
    p1, p2 = baseline, baseline + lift
    pooled = (p1 + p2) / 2
    z_alpha, z_power = norm.ppf(1 - alpha / 2), norm.ppf(power)
    spread = (z_alpha * sqrt(2 * pooled * (1 - pooled))
              + z_power * sqrt(p1 * (1 - p1) + p2 * (1 - p2)))
    return ceil((spread / lift) ** 2)


DAILY_SIGNUPS = 8_000 / 30
print(f"{'Lift to detect':<16}{'Per group':>11}{'Both groups':>13}"
      f"{'Days to enroll':>16}")
for lift in (0.01, 0.02, 0.03, 0.05):
    n = sample_size(0.55, lift)
    label = f"+{lift * 100:.0f} points"
    print(f"{label:<16}{n:>11,}{2 * n:>13,}{ceil(2 * n / DAILY_SIGNUPS):>16}")
