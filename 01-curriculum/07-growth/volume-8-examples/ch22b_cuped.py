"""Chapter 22: CUPED on synthetic data (an experiment on existing merchants)."""
import numpy as np

rng = np.random.default_rng(2026)
n = 4_000  # merchants per group
before = rng.gamma(shape=2.0, scale=75, size=2 * n)  # payments, 4 weeks before
during = 0.9 * before + rng.normal(0, 70, 2 * n)     # payments, 4 test weeks
treated = np.arange(2 * n) < n
during[treated] += 5                                 # the true effect we planted


def readout(metric, label):
    lift = metric[treated].mean() - metric[~treated].mean()
    se = np.sqrt(metric[treated].var(ddof=1) / n + metric[~treated].var(ddof=1) / n)
    print(f"{label:<6} lift {lift:5.2f} payments, "
          f"95% CI {lift - 1.96 * se:5.2f} to {lift + 1.96 * se:5.2f}")
    return se


theta = np.cov(before, during)[0, 1] / before.var(ddof=1)
adjusted = during - theta * (before - before.mean())
se_plain = readout(during, "Plain")
se_cuped = readout(adjusted, "CUPED")
print(f"Correlation of before and during: {np.corrcoef(before, during)[0, 1]:.2f}")
print(f"Variance removed: {1 - (se_cuped / se_plain) ** 2:.0%}")
