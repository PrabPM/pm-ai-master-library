"""Chapter 64: uplift modeling with two models (a T-learner) on a simulated
randomized retention experiment. Illustrative numbers.
"""
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

V, C = 1500.0, 90.0                     # value of a kept merchant, cost of an offer


def segment_value(n, stay_treated, stay_control):
    """Net value of sending the offer to n merchants of one kind."""
    return n * (stay_treated - stay_control) * V - n * C


hand = [round(segment_value(1000, a, b)) for a, b in
        [(0.80, 0.60), (0.95, 0.94), (0.30, 0.30)]]
print("hand table, net USD per 1,000 offers:", hand)

rng = np.random.default_rng(64)


def simulate(n):
    risk = rng.random(n)                # how close to leaving
    price = rng.random(n)               # how much fees matter to this merchant
    stay0 = 0.95 - 0.75 * risk ** 2     # chance of staying with no offer
    effect = np.where(risk > 0.8, 0.02, 0.9 * price * (1 - stay0))
    effect = np.where(risk < 0.2, -0.03, effect)       # sleeping dogs
    treated = rng.random(n) < 0.5                      # randomized offer
    stayed = rng.random(n) < stay0 + treated * effect
    return np.column_stack([risk, price]), treated, stayed, effect


X, T, Y, _ = simulate(20_000)           # the experiment
X_new, _, _, true_effect = simulate(20_000)            # merchants to target next


def fit(rows):
    return GradientBoostingClassifier(n_estimators=60, max_depth=3,
                                      random_state=0).fit(X[rows], Y[rows])


m_control, m_treated = fit(~T), fit(T)                 # the two models
stay_without = m_control.predict_proba(X_new)[:, 1]
uplift = m_treated.predict_proba(X_new)[:, 1] - stay_without
k = len(X_new) // 5                                    # budget: offers for the top 20%
targets = {"highest churn risk": np.argsort(stay_without)[:k],
           "highest predicted uplift": np.argsort(-uplift)[:k],
           "random": rng.choice(len(X_new), k, replace=False)}
print(f"average effect in the experiment: {Y[T].mean() - Y[~T].mean():+.3f}")
for name, idx in targets.items():
    saves = true_effect[idx].sum()                     # known only in a simulation
    print(f"{name:25s} merchants kept by the offer {saves:5.0f}"
          f"   net USD {saves * V - k * C:9,.0f}")

# ---- checks against the hand-worked numbers ----
assert hand == [210_000, -75_000, -90_000]
kept = {name: true_effect[idx].sum() for name, idx in targets.items()}
assert kept["highest predicted uplift"] > 1.5 * kept["highest churn risk"]
