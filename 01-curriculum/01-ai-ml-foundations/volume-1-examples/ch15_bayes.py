"""Chapter 15. Bayes' theorem and the base-rate trap for a fraud model.

Run: python ch15_bayes.py
"""
import numpy as np

# [listing]
base_rate = 0.002     # P(fraud): 2 payments in 1,000
tpr = 0.90            # P(flag | fraud), the true-positive rate
fpr = 0.02            # P(flag | legitimate), the false-positive rate

n = 100_000
fraud, legit = n * base_rate, n * (1 - base_rate)
true_flags, false_flags = tpr * fraud, fpr * legit
print(f"fraud {fraud:,.0f} -> flagged {true_flags:,.0f}")
print(f"legit {legit:,.0f} -> flagged {false_flags:,.0f}")
print(f"P(fraud | flag) by counting = {true_flags / (true_flags + false_flags):.4f}")


def posterior(prior, p_e_given_h, p_e_given_not_h):
    evidence = p_e_given_h * prior + p_e_given_not_h * (1 - prior)
    return p_e_given_h * prior / evidence


print(f"P(fraud | flag) by Bayes    = {posterior(base_rate, tpr, fpr):.4f}")

# Odds form
odds = base_rate / (1 - base_rate) * (tpr / fpr)
print(f"likelihood ratio {tpr / fpr:.0f}, posterior odds {odds:.4f}")
odds2 = odds * 6      # second signal, likelihood ratio 6
print(f"after the second signal     = {odds2 / (1 + odds2):.4f}")
for b in (0.0005, 0.002, 0.01, 0.05):
    print(f"base rate {b:.2%} -> precision {posterior(b, tpr, fpr):.3f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(fraud, 200) and np.isclose(legit, 99_800)
assert np.isclose(true_flags, 180) and np.isclose(false_flags, 1996)
assert np.isclose(true_flags / (true_flags + false_flags), 180 / 2176)
assert np.isclose(posterior(base_rate, tpr, fpr), 180 / 2176)
assert np.isclose(odds, 0.002 / 0.998 * 45)
assert np.isclose(odds / (1 + odds), 180 / 2176)
assert np.isclose(odds2 / (1 + odds2), 0.3511, atol=5e-5)

# Simulation check with a fixed seed
rng = np.random.default_rng(15)
is_fraud = rng.random(2_000_000) < base_rate
flag = np.where(is_fraud, rng.random(2_000_000) < tpr, rng.random(2_000_000) < fpr)
assert abs(is_fraud[flag].mean() - 180 / 2176) < 0.005

# Q15.1: false-positive rate cut to 0.5% -> 180 / (180 + 499)
assert np.isclose(posterior(base_rate, tpr, 0.005), 180 / 679)
assert np.isclose(180 / 679, 0.265, atol=5e-4)
# Q15.2: flags that are not fraud out of 2,176
assert np.isclose(1996 / 2176, 0.9173, atol=5e-5)
