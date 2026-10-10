"""Chapter 122: would a nightly evaluation catch a silent quality drop?

A golden set of n answers is scored every night. The score is a proportion, so
its noise is the standard error sqrt(p * (1 - p) / n).
"""
from math import erf, sqrt

import numpy as np


def standard_error(p, n):
    return sqrt(p * (1 - p) / n)


def normal_cdf(z):
    return 0.5 * (1 + erf(z / sqrt(2)))


def chance_caught(p_before, p_after, n, z=3.0):
    """Chance that one night at p_after falls more than z standard errors
    below p_before (normal approximation)."""
    alarm_line = p_before - z * standard_error(p_before, n)
    return normal_cdf((alarm_line - p_after) / standard_error(p_after, n))


def nightly_alerts(true_rates, n, rng, z=3.0, window=7):
    scores = [rng.binomial(n, p) / n for p in true_rates]
    alerts = []
    for i, s in enumerate(scores):
        if i < window:
            alerts.append(False)
            continue
        base = np.mean(scores[i - window:i])
        alerts.append(s < base - z * standard_error(base, n))
    return scores, alerts


if __name__ == "__main__":
    for n in (1000, 50):
        se = standard_error(0.92, n)
        print(f"n = {n:>4}: standard error {se:.4f}; a 4-point drop is "
              f"{0.04 / se:.1f} standard errors;")
        print(f"          caught on the first night "
              f"{chance_caught(0.92, 0.88, n):.0%} of the time")

    rng = np.random.default_rng(21)
    rates = [0.92] * 14 + [0.88] * 4          # the model alias changes on night 15
    scores, alerts = nightly_alerts(rates, 1000, rng)
    for night in range(12, 18):
        flag = "  ALERT" if alerts[night] else ""
        print(f"night {night + 1:>2}: faithfulness {scores[night]:.3f}{flag}")

    # The fictional incident in the chapter.
    retries, fee = 212, 1.50
    print(f"incident: {retries} doomed retries x USD {fee:.2f} = "
          f"USD {retries * fee:.0f}")

    assert np.isclose(standard_error(0.92, 1000), 0.00858, atol=1e-5)
    assert np.isclose(0.04 / standard_error(0.92, 1000), 4.66, atol=0.01)
    assert np.isclose(standard_error(0.92, 50), 0.0384, atol=1e-4)
    assert np.isclose(chance_caught(0.92, 0.88, 1000), 0.92, atol=0.01)
    assert chance_caught(0.92, 0.88, 50) < 0.06
    assert alerts[14] and not any(alerts[:14])
    assert retries * fee == 318
