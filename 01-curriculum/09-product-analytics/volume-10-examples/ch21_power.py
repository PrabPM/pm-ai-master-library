"""Chapter 21: sample size before the test, and reading the result after it."""
from math import asin, sin, sqrt

from scipy.stats import chisquare
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportion_effectsize,
                                          proportions_ztest)

BASELINE = 0.51            # approved merchants who take a payment within 30 days
PER_WEEK = 232             # merchants approved each week (1,005 a month)
ALPHA, POWER = 0.05, 0.80


def sample_size(lift, baseline=BASELINE):
    """Merchants needed in EACH arm to detect baseline -> baseline + lift."""
    effect = proportion_effectsize(baseline + lift, baseline)
    return NormalIndPower().solve_power(effect, alpha=ALPHA, power=POWER, ratio=1)


def detectable_rate(n, baseline):
    """The treatment rate a test with n per arm can detect with 80% power."""
    effect = NormalIndPower().solve_power(nobs1=n, alpha=ALPHA, power=POWER, ratio=1)
    return sin(asin(sqrt(baseline)) + effect / 2) ** 2


def read(label, control, treatment):
    """control and treatment are (successes, merchants)."""
    (x0, n0), (x1, n1) = control, treatment
    _, p = proportions_ztest([x1, x0], [n1, n0])
    low, high = confint_proportions_2indep(x1, n1, x0, n0, method="wald")
    print(f"{label}: control {x0}/{n0} = {x0 / n0:.1%}, "
          f"treatment {x1}/{n1} = {x1 / n1:.1%}")
    print(f"  difference {x1 / n1 - x0 / n0:+.1%}, 95% CI {low:+.1%} to {high:+.1%}, "
          f"p = {p:.4f}")


if __name__ == "__main__":
    print(f"{'detect a lift of':<18}{'per arm':>9}{'weeks to enroll':>17}")
    for lift in (0.03, 0.05, 0.07, 0.10):
        n = sample_size(lift)
        print(f"{'+' + format(lift * 100, '.0f') + ' points':<18}{n:>9,.0f}"
              f"{2 * n / PER_WEEK:>17.1f}")

    print()
    read("Practice database, checkout_v2", (24, 31), (25, 27))
    print(f"  with 29 per arm, 80% power needs the treatment to reach "
          f"{detectable_rate(29, 24 / 31):.0%}")
    read("Quickstart pilot", (822, 1_612), (897, 1_588))
    _, srm_p = chisquare([1_612, 1_588])
    print(f"  split check: 1,612 vs 1,588, p = {srm_p:.2f} "
          f"({'looks fine' if srm_p > 0.001 else 'sample ratio mismatch'})")
