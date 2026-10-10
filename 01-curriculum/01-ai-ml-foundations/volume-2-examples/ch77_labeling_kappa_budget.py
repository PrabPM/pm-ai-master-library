"""Chapter 77. Cohen's kappa by hand and in code, a labeling throughput and budget
plan, and a learning curve that says how many labels a quality target costs."""
import math

import numpy as np
from sklearn.metrics import cohen_kappa_score


def from_table(both_fraud, a_only, b_only, both_clean):
    """Rebuild the two annotators' label lists from a 2x2 agreement table."""
    a = [1] * both_fraud + [1] * a_only + [0] * b_only + [0] * both_clean
    b = [1] * both_fraud + [0] * a_only + [1] * b_only + [0] * both_clean
    return a, b


def cohens_kappa(a, b):
    """Agreement between two annotators, corrected for chance agreement."""
    a, b = np.asarray(a), np.asarray(b)
    p_observed = np.mean(a == b)
    p_chance = sum(np.mean(a == k) * np.mean(b == k) for k in np.union1d(a, b))
    return (p_observed - p_chance) / (1 - p_chance), p_observed, p_chance


# ---- 1. Two analysts label the same 200 disputed payments ------------------------
a, b = from_table(both_fraud=20, a_only=10, b_only=14, both_clean=156)
kappa, p_o, p_e = cohens_kappa(a, b)
print(f"observed agreement {p_o:.3f}, chance agreement {p_e:.3f}, kappa {kappa:.3f}")
assert np.isclose(p_o, 0.88) and np.isclose(p_e, 0.731)
assert np.isclose(kappa, 0.149 / 0.269)
assert np.isclose(kappa, cohen_kappa_score(a, b))

# Rare class: 95% raw agreement, and they never agree on a single fraud case.
a2, b2 = from_table(both_fraud=0, a_only=5, b_only=5, both_clean=190)
kappa2, p_o2, p_e2 = cohens_kappa(a2, b2)
print(f"observed agreement {p_o2:.3f}, chance agreement {p_e2:.3f}, "
      f"kappa {kappa2:.3f}")
assert np.isclose(p_o2, 0.95) and kappa2 < 0

# ---- 2. Throughput and budget ----------------------------------------------------
labels_needed = 12_000
passes_per_item = 1 + 0.25 * 2              # 25% of items get two extra opinions
per_day = 6 * 50 * 6 * 0.8                  # annotators x items/hour x hours x use
total_passes = labels_needed * passes_per_item
cost = total_passes * 0.10 * 1.15           # USD 0.10 a pass, 15% review overhead
print(f"\n{total_passes:.0f} passes at {per_day:.0f} a day = "
      f"{total_passes / per_day:.1f} working days, USD {cost:,.0f}")
assert (total_passes, per_day) == (18_000, 1_440)
assert np.isclose(cost, 2_070)

# ---- 3. Learning curve: quality(n) = ceiling - A * n ** (-beta) ------------------
ceiling, A, beta = 0.95, 0.80, 0.5


def labels_for(target):
    return math.ceil((A / (ceiling - target)) ** (1 / beta) - 1e-9)


for n in (1_600, 6_400):
    print(f"n = {n:6,d}: quality {ceiling - A * n ** -beta:.3f}")
for target in (0.942, 0.946):
    n = labels_for(target)
    print(f"target {target}: {n:6,d} labels, USD {n * 1.5 * 0.10 * 1.15:,.0f}")
assert labels_for(0.942) == 10_000 and labels_for(0.946) == 40_000
