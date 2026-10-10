"""Chapter 65: a data feasibility audit for a dispute-outcome model.
Synthetic table; every number is illustrative.
"""
import math

import numpy as np


def positives_needed(rate, margin, z=1.96):
    """Positives needed to measure a rate (such as recall) to within +/- margin."""
    return math.ceil(z ** 2 * rate * (1 - rate) / margin ** 2)


def measured_accuracy(true_accuracy, flip_rate):
    """What a test set with randomly flipped labels will report."""
    return true_accuracy * (1 - flip_rate) + (1 - true_accuracy) * flip_rate


rng = np.random.default_rng(65)
n = 60_000                                             # disputes in the warehouse
region = rng.choice(["US", "EU", "LATAM"], n, p=[0.70, 0.27, 0.03])
lost = rng.random(n) < 0.30                            # label: PayFlow lost the dispute
duplicate = rng.random(n) < 0.06                       # same dispute exported twice
opened = rng.integers(0, 365, n)                       # day the dispute was opened
evidence_day = opened + rng.integers(-2, 12, n)        # when 'evidence_count' was set

usable = ~duplicate
need = positives_needed(0.80, 0.05)
print("positives needed for recall 0.80 +/- 0.05:", need)
print(f"rows {n:,}  usable after removing duplicates {usable.sum():,}  "
      f"positives {int((usable & lost).sum()):,}")
for r in ("US", "EU", "LATAM"):
    pos = int((usable & lost & (region == r)).sum())
    test_pos = int(pos * 0.2)                          # a 20% test split
    print(f"  {r:6s} positives {pos:6,}  in a 20% test set {test_pos:5,}  "
          f"{'enough' if test_pos >= need else 'TOO FEW'}")
late = float(np.mean(evidence_day > opened))
print(f"'evidence_count' is filled in after the decision time for {late:.0%} of rows")
print("measured accuracy of a 95% model with 8% label noise:",
      round(measured_accuracy(0.95, 0.08), 3))
truth = rng.random(200_000) < 0.5
pred = np.where(rng.random(200_000) < 0.95, truth, ~truth)
noisy = np.where(rng.random(200_000) < 0.08, ~truth, truth)
print("simulated:", round(float(np.mean(pred == noisy)), 3))

# ---- checks against the hand-worked numbers ----
assert need == 246
assert math.isclose(measured_accuracy(0.95, 0.08), 0.878)
assert abs(np.mean(pred == noisy) - 0.878) < 0.003
assert math.ceil(need / 0.005) == 49_200
