"""Chapter 11: gradient boosting as residual fitting, and exact Shapley values."""
from itertools import permutations

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

# Boosting by hand: four payments, features (new_card, foreign_card), a risk score.
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([0.0, 2.0, 4.0, 6.0])


def best_stump(X, residual):
    """The one-question tree that leaves the smallest squared error."""
    best = None
    for j in range(X.shape[1]):
        yes = X[:, j] > 0.5
        left, right = residual[~yes].mean(), residual[yes].mean()
        sse = ((residual - np.where(yes, right, left)) ** 2).sum()
        if best is None or sse < best[0]:
            best = (sse, j, left, right)
    return best


def boost(rate, rounds):
    pred = np.full(len(y), y.mean())           # round 0: predict the average
    history = []
    for r in range(rounds):
        residual = y - pred                    # what is still unexplained
        sse, j, left, right = best_stump(X, residual)
        pred = pred + rate * np.where(X[:, j] > 0.5, right, left)
        history.append((j, pred))
    return history


for r, (j, pred) in enumerate(boost(rate=1.0, rounds=2), start=1):
    print(f"round {r}: split on feature {j}, predictions {pred.tolist()}")
errors = [((y - pred) ** 2).sum() for j, pred in boost(rate=0.3, rounds=6)]
print("learning rate 0.3, squared error by round:", np.round(errors, 2).tolist())
sk = GradientBoostingRegressor(n_estimators=2, learning_rate=1.0, max_depth=1)
assert all(a > b for a, b in zip(errors, errors[1:]))    # the error keeps falling
assert np.allclose(boost(1.0, 2)[-1][1], y)
assert np.allclose(sk.fit(X, y).predict(X), y)

# Exact Shapley values for a three-feature risk model with one interaction.
names = ["new_card", "foreign_card", "high_velocity"]


def model(v):
    return 10 * v[0] + 4 * v[1] + 8 * v[0] * v[2]


background = np.array([[a, b, c] for a in (0, 1) for b in (0, 1) for c in (0, 1)])
payment = np.array([1, 1, 1])


def value(known):
    """Average prediction when only the features in `known` are revealed."""
    rows = background.copy()
    rows[:, list(known)] = payment[list(known)]
    return np.mean([model(r) for r in rows])


shap = np.zeros(3)
orders = list(permutations(range(3)))
for order in orders:
    known = []
    for j in order:
        before = value(known)
        known.append(j)
        shap[j] += (value(known) - before) / len(orders)
base = value([])
print(f"base value {base:.1f}   prediction {model(payment):.1f}")
print("Shapley values:", dict(zip(names, np.round(shap, 2).tolist())))
assert np.allclose(shap, [8, 2, 3]) and np.isclose(base + shap.sum(), model(payment))
