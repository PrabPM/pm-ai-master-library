"""Chapter 57, Lab 3: why most fraud flags are wrong (base rates)."""
import numpy as np


def precision(base_rate, recall, false_positive_rate):
    """P(fraud | flagged) by Bayes' theorem."""
    hit = recall * base_rate
    false_alarm = false_positive_rate * (1 - base_rate)
    return hit / (hit + false_alarm)


print(f"P(fraud | flag) at 2% false positives:   {precision(0.005, 0.90, 0.02):.4f}")
print(f"P(fraud | flag) at 0.5% false positives: {precision(0.005, 0.90, 0.005):.4f}")

# The same answer by counting, on one million simulated payments.
rng = np.random.default_rng(57)
fraud = rng.random(1_000_000) < 0.005
flag = np.where(fraud, rng.random(fraud.size) < 0.90, rng.random(fraud.size) < 0.02)
print(f"simulated: {fraud.sum()} fraud, {flag.sum()} flags, "
      f"{(flag & fraud).sum()} true; precision {(flag & fraud).sum() / flag.sum():.4f}")

# ---- checks against the hand results ----
assert np.isclose(precision(0.005, 0.90, 0.02), 450 / 2440)
assert np.isclose(precision(0.005, 0.90, 0.005), 450 / 947.5)
assert abs((flag & fraud).sum() / flag.sum() - 450 / 2440) < 0.01
