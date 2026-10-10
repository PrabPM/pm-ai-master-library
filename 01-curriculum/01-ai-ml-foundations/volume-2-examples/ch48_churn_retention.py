"""Chapter 48: churn prediction and the retention-offer decision at PayFlow.

Synthetic merchants. Every number is illustrative.
"""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(48)
n = 6000
drop = rng.beta(2, 5, n)              # share of card volume lost vs last quarter
tickets = rng.poisson(1.2, n)         # support tickets in the last 30 days
delays = rng.poisson(0.4, n)          # delayed payouts in the last 30 days
tenure = rng.integers(1, 60, n)       # months on PayFlow
logit = -3.9 + 3.0 * drop + 0.5 * tickets + 0.9 * delays - 0.02 * tenure
churn = rng.random(n) < 1 / (1 + np.exp(-logit))     # left within 30 days
X = np.column_stack([drop, tickets, delays, tenure])
X_tr, X_te, y_tr, y_te = train_test_split(X, churn, test_size=0.5, random_state=0)

V, C, s = 1500.0, 90.0, 0.30     # fees kept per save, cost of one offer, save rate
p_star = C / (s * V)             # offer only above this churn probability


def ev(p):
    """Expected value of one offer to a merchant with churn probability p."""
    return p * s * V - C


model = GradientBoostingClassifier(max_depth=3, n_estimators=120,
                                   learning_rate=0.05, random_state=0)
p = model.fit(X_tr, y_tr).predict_proba(X_te)[:, 1]


def policy_value(offer):
    """Net value of a set of offers, scored on what really happened (y_te)."""
    return float(np.sum(offer * (y_te * s * V - C)))


policies = {"offer to nobody": np.zeros_like(y_te),
            "offer to everybody": np.ones_like(y_te),
            "rule: volume drop > 40%": X_te[:, 0] > 0.40,
            f"model: p >= {p_star:.2f}": p >= p_star}
print(f"p* = {p_star:.2f}   EV at p=0.62: {ev(0.62):.0f}   "
      f"EV at p=0.10: {ev(0.10):.0f}")
print(f"test merchants: {len(y_te)}, churned: {int(y_te.sum())}")
for name, offer in policies.items():
    reached = int((offer & y_te).sum())
    print(f"{name:24s} offers {int(offer.sum()):4d}  churners reached {reached:3d}"
          f"  net USD {policy_value(offer):8,.0f}")

# ---- checks against the hand-worked numbers ----
assert np.isclose(p_star, 0.20)
assert np.isclose(ev(0.62), 189.0) and np.isclose(ev(0.10), -45.0)
best = policy_value(policies[f"model: p >= {p_star:.2f}"])
assert best > 0 > policy_value(policies["rule: volume drop > 40%"])
assert policy_value(policies["offer to everybody"]) < 0
