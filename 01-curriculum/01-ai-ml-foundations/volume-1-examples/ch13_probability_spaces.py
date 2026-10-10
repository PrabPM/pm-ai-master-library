"""Chapter 13. Probability spaces: events as sets of PayFlow payments.

Run: python ch13_probability_spaces.py
"""
import numpy as np

# [listing]
rng = np.random.default_rng(13)

# 1,000 payments: 20 are fraud, 100 are over USD 500, 8 are both
n = 1000
fraud = np.zeros(n, dtype=bool)
large = np.zeros(n, dtype=bool)
fraud[:20] = True
large[12:112] = True          # rows 12-19 are both
order = rng.permutation(n)    # shuffle the rows
fraud, large = fraud[order], large[order]


def prob(event):
    """Share of the equally likely outcomes that fall inside the event."""
    return event.mean()


print(f"P(fraud)           = {prob(fraud):.3f}")
print(f"P(large)           = {prob(large):.3f}")
print(f"P(fraud and large) = {prob(fraud & large):.3f}")
print(f"P(fraud or large)  = {prob(fraud | large):.3f}")
print(f"P(neither)         = {prob(~(fraud | large)):.3f}")
print(f"union bound        = {prob(fraud) + prob(large):.3f}")

# Five independent payout attempts, each failing 0.8% of the time
exact = 1 - 0.992**5
simulated = (rng.random((200_000, 5)) < 0.008).any(axis=1).mean()
print(f"P(at least one of 5 fails) = {exact:.4f} exact, {simulated:.4f} simulated")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(prob(fraud), 20 / 1000)
assert np.isclose(prob(large), 100 / 1000)
assert np.isclose(prob(fraud & large), 8 / 1000)
# inclusion-exclusion: 0.020 + 0.100 - 0.008 = 0.112
assert np.isclose(prob(fraud | large), 0.020 + 0.100 - 0.008)
assert np.isclose(prob(~(fraud | large)), 1 - 0.112)
assert prob(fraud | large) <= prob(fraud) + prob(large)
assert np.isclose(exact, 0.0394, atol=5e-5)
assert abs(simulated - exact) < 0.002
# Q13.1: fraud but not large = 12, exactly one of the two = 104
assert (fraud & ~large).sum() == 12 and (fraud ^ large).sum() == 104
# Q13.2: ten independent attempts
assert np.isclose(1 - 0.992**10, 0.0772, atol=5e-5)
