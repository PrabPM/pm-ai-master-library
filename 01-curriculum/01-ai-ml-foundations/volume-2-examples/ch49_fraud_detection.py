"""Chapter 49: payment fraud detection with boosted trees, a graph feature and
exact Shapley reason codes. Synthetic payments; every number is illustrative.
"""
import os
from itertools import combinations
from math import factorial

os.environ.setdefault("OMP_NUM_THREADS", "1")    # one thread: light and repeatable

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

rng = np.random.default_rng(49)
n = 120_000
fraud = rng.random(n) < 0.005
ring = fraud & (rng.random(n) < 0.35)          # fraud run from shared devices
loud = fraud & ~ring                           # stolen cards that look unusual
amount = rng.lognormal(3.6, 0.8, n) * np.where(loud, 3.0, 1.0)
velocity = rng.poisson(np.where(loud, 5.0, 0.6))            # payments in last hour
new_device = rng.random(n) < np.where(loud, 0.7, 0.08)
mismatch = rng.random(n) < np.where(loud, 0.6, 0.03)        # card vs IP country
kiosk = ~fraud & (rng.random(n) < 0.01)        # honest shared devices
shared = 1 + rng.poisson(np.where(ring, 7.0, np.where(kiosk, 2.5, 0.2)))
names = ["amount", "velocity_1h", "new_device", "country_mismatch",
         "accounts_on_device"]
X = np.column_stack([amount, velocity, new_device, mismatch, shared]).astype(float)
half = n // 2
X_tr, X_te, y_tr, y_te, ring_te = X[:half], X[half:], fraud[:half], fraud[half:], \
    ring[half:]


def fit(cols):
    m = HistGradientBoostingClassifier(max_depth=3, max_iter=60, learning_rate=0.1,
                                       early_stopping=False, random_state=0)
    return m.fit(X_tr[:, cols], y_tr)


def flag_at_fpr(score, y, fpr=0.005):
    """Flag payments scoring above the top 0.5% of good payments."""
    return score > np.quantile(score[~y], 1 - fpr)


def money(caught, false_alarms, loss=135.0, friction=12.0):
    """Fraud loss avoided minus the cost of stopping good payments, in USD."""
    return caught * loss - false_alarms * friction


def shapley(f, x, background):
    """Exact Shapley values: a feature's marginal effect, averaged over orders."""
    d = len(x)

    cache = {}

    def value(S):                      # features in S take this payment's values
        if S not in cache:
            Z = background.copy()
            Z[:, list(S)] = x[list(S)]
            cache[S] = f(Z).mean()
        return cache[S]

    phi = np.zeros(d)
    for j in range(d):
        others = [k for k in range(d) if k != j]
        for r in range(d):
            for S in combinations(others, r):
                w = factorial(r) * factorial(d - r - 1) / factorial(d)
                phi[j] += w * (value(tuple(sorted(S + (j,)))) - value(S))
    return phi


results = {}
for label, cols in [("tabular only", [0, 1, 2, 3]),
                    ("plus graph feature", [0, 1, 2, 3, 4])]:
    model = fit(cols)
    score = model.predict_proba(X_te[:, cols])[:, 1]
    flagged = flag_at_fpr(score, y_te)
    caught, fa = int((flagged & y_te).sum()), int((flagged & ~y_te).sum())
    ring_caught = int((flagged & ring_te).sum())
    results[label] = (caught, fa, ring_caught)
    print(f"{label:18s} caught {caught:3d} of {int(y_te.sum())} "
          f"(ring {ring_caught:3d} of {int(ring_te.sum())})  false alarms {fa:3d}  "
          f"USD {money(caught, fa):6,.0f}")

# Reason codes for one blocked stolen-card payment, from the second model.
f = lambda Z: model.predict_proba(Z)[:, 1]
i = int(np.flatnonzero(flagged & y_te & ~ring_te)[0])
background = X_te[~y_te][:200]
phi = shapley(f, X_te[i], background)
base, pred = f(background).mean(), f(X_te[i:i + 1])[0]
print(f"payment {i}: score {pred:.3f}, average good payment {base:.3f}")
for j in np.argsort(-np.abs(phi))[:3]:
    print(f"  {names[j]:18s} = {X_te[i, j]:7.2f}   contribution {phi[j]:+.3f}")

# ---- checks ----
assert np.isclose(money(150, 200), 17_850.0)             # the hand example
assert np.isclose(phi.sum(), pred - base, atol=1e-9)     # Shapley values add up
assert results["plus graph feature"][2] > results["tabular only"][2]
