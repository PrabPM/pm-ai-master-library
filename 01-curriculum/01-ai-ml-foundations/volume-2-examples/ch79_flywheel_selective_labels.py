"""Chapter 79. Label channels, and the selective-labels trap: a fraud model that
only sees outcomes for payments it approved forgets why it was declining."""
import numpy as np
from sklearn.linear_model import LogisticRegression

# ---- 1. Label channels: volume times fidelity ------------------------------------
channels = {                     # labels per day, share of those labels that are right
    "dispute outcome": (150, 0.99),
    "analyst review": (350, 0.95),
    "customer prompt": (1_500, 0.90),
    "no dispute by day 120": (18_000, 0.98),
}
total = sum(n for n, _ in channels.values())
correct = sum(n * f for n, f in channels.values())
print(f"labels per day {total:,}, expected share correct {correct / total:.4f}")
assert total == 20_000 and np.isclose(correct / total, 19_471 / 20_000)

# ---- 2. By hand: 1,000 payments, one risky segment -------------------------------
n_new, n_old, p_new, p_old = 100, 900, 0.30, 0.01    # brand-new vs known merchants
fraud_new, fraud_old = n_new * p_new, n_old * p_old
true_rate = (fraud_new + fraud_old) / (n_new + n_old)
seen_rate = fraud_old / n_old                        # the rule declines every new one
explore = 0.10                                       # approve 1 in 10 of them anyway
let_in, let_in_fraud = explore * n_new, explore * fraud_new
w = 1 / explore                                      # each one stands for 10
weighted = (fraud_old + w * let_in_fraud) / (n_old + w * let_in)
print(f"true fraud rate {true_rate:.3f}, rate in the labels {seen_rate:.3f}, "
      f"with weighted exploration {weighted:.3f}")
print(f"exploration lets through {let_in:.0f} payments, "
      f"about {let_in_fraud:.0f} of them fraud")
assert np.isclose(true_rate, 0.039) and np.isclose(seen_rate, 0.010)
assert np.isclose(weighted, true_rate)

# ---- 3. The loop, simulated ------------------------------------------------------
def payments(n, rng):
    new = (rng.random(n) < 0.10).astype(float)       # payment at a brand-new merchant
    amount_z = rng.normal(size=n)
    logit = -4.6 + 3.75 * new + 0.5 * amount_z
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return np.column_stack([new, amount_z]), y


rng = np.random.default_rng(79)
X, y = payments(40_000, rng)                         # last quarter
X_next, y_next = payments(40_000, rng)               # next quarter
is_new = X[:, 0] == 1


def retrain_and_deploy(explore_rate):
    """Rule declines new-merchant payments, except a random share it lets through."""
    let_through = rng.random(len(y)) < explore_rate
    approved = ~is_new | let_through                 # only these ever get a label
    weight = np.where(is_new, 1 / max(explore_rate, 1e-9), 1.0)[approved]
    model = LogisticRegression(C=100.0).fit(X[approved], y[approved],
                                            sample_weight=weight)
    score = model.predict_proba(X_next)[:, 1]
    ok = score < 0.10                                # rule retired: the model decides
    return (model.coef_[0][0], y[approved].mean(), ok.mean(),
            y_next[ok].sum(), (is_new & let_through & (y == 1)).sum())


print(f"\ntrue fraud rate {y.mean():.3f}; at new merchants {y[is_new].mean():.3f}")
print("explore  labeled rate  weight on 'new'  approved next  fraud approved  cost")
rows = {}
for rate in (0.0, 0.10):
    coef, seen, share, fraud_ok, cost = retrain_and_deploy(rate)
    rows[rate] = (coef, fraud_ok)
    print(f"{rate:6.0%}  {seen:12.3f}  {coef:15.2f}  {share:13.1%}  {fraud_ok:14d}  "
          f"{cost:4d}")
assert abs(rows[0.0][0]) < 0.01                      # no evidence, no weight
assert rows[0.10][0] > 3 and rows[0.10][1] < rows[0.0][1] / 2
