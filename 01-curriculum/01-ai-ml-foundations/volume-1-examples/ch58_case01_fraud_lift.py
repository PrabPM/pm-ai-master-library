"""Chapter 58, Case 1: is the new fraud model's lift real?"""
import numpy as np

rng = np.random.default_rng(58)

# Two weeks of payments. Week 2 contains a sale: more volume and more fraud.
n1, n2 = 95_000, 105_000
week = np.r_[np.ones(n1, int), np.full(n2, 2)]
fraud = rng.random(n1 + n2) < np.where(week == 1, 0.0048, 0.0052)

# Both models score every payment. They share most of their evidence.
shared = rng.normal(0, 1, fraud.size)
score_a = 2.6 * fraud + shared
score_b = 2.75 * fraud + 0.8 * shared + 0.6 * rng.normal(0, 1, fraud.size)


def flags(score, share=0.02):
    """Flag the top `share` of payments: a fixed review budget."""
    return score >= np.quantile(score, 1 - share)


flag_a, flag_b = flags(score_a), flags(score_b)

# 1. The claim as made: A's catches in week 1 against B's in week 2.
a_w1 = int((flag_a & fraud & (week == 1)).sum())
b_w2 = int((flag_b & fraud & (week == 2)).sum())
a_w2 = int((flag_a & fraud & (week == 2)).sum())
print(f"fraud cases: week 1 {fraud[week == 1].sum()}, week 2 {fraud[week == 2].sum()}")
print(f"A in week 1 caught {a_w1}; B in week 2 caught {b_w2} "
      f"({100 * (b_w2 / a_w1 - 1):+.0f}%); A in week 2 caught {a_w2}")

# 2. The fair comparison: the same payments, the same number of flags.
n_fraud = int(fraud.sum())
caught_a, caught_b = int((flag_a & fraud).sum()), int((flag_b & fraud).sum())
print(f"same {fraud.size:,} payments, {flag_a.sum()} flags each: "
      f"recall A {caught_a / n_fraud:.3f}, B {caught_b / n_fraud:.3f}")

# 3. Is the difference more than chance? Paired test on the fraud cases.
only_b = int((flag_b & ~flag_a & fraud).sum())
only_a = int((flag_a & ~flag_b & fraud).sum())
z = (only_b - only_a) / np.sqrt(only_b + only_a)
diff = (only_b - only_a) / n_fraud
se = np.sqrt(only_b + only_a - (only_b - only_a) ** 2 / n_fraud) / n_fraud
print(f"caught by B only {only_b}, by A only {only_a}: z {z:.2f}")
print(f"recall lift {100 * diff:.1f} points, 95% interval "
      f"{100 * (diff - 1.96 * se):.1f} to {100 * (diff + 1.96 * se):.1f}")

# 4. What a reviewer sees: precision at this base rate.
print(f"precision: A {caught_a / flag_a.sum():.3f}, B {caught_b / flag_b.sum():.3f}"
      f"   (base rate {n_fraud / fraud.size:.4f})")

# ---- checks ----
assert b_w2 / a_w1 - 1 > 2 * (caught_b / caught_a - 1)   # the naive claim overstates
assert z > 1.96 and diff - 1.96 * se > 0
assert flag_a.sum() == flag_b.sum()
assert caught_b - caught_a == only_b - only_a
assert (only_b, only_a, n_fraud) == (118, 55, 1018)
assert np.isclose(z, 63 / np.sqrt(173))
