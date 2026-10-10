"""Chapter 78. Uncertainty sampling against random sampling on a seeded toy fraud
problem, then weak supervision: three labeling functions and a majority vote."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

FRAUD, CLEAN, ABSTAIN = 1, 0, -1


def auc(y, score):
    """Area under the ROC curve from ranks (same value as scikit-learn, faster)."""
    ranks = np.empty(len(score))
    ranks[np.argsort(score)] = np.arange(1, len(score) + 1)
    n_pos = y.sum()
    return (ranks[y == 1].sum() - n_pos * (n_pos + 1) / 2) / (n_pos * (len(y) - n_pos))


def fit_logistic(X, y, l2=1.0, steps=25):
    """Logistic regression with an L2 penalty, fitted by Newton's method."""
    Xb = np.column_stack([np.ones(len(X)), X])
    penalty = l2 * np.eye(Xb.shape[1])
    penalty[0, 0] = 0.0                                   # do not shrink the intercept
    w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-Xb @ w))
        grad = Xb.T @ (p - y) + penalty @ w
        hess = (Xb * (p * (1 - p))[:, None]).T @ Xb + penalty
        w -= np.linalg.solve(hess, grad)
    return w


def predict(w, X):
    return 1 / (1 + np.exp(-(w[0] + X @ w[1:])))


def make_payments(n, rng):
    """Flagged payments: four real signals and six columns of noise."""
    d = {"amount": rng.lognormal(3.6, 0.9, n),             # USD
         "age_days": rng.exponential(400, n),              # merchant age
         "mismatch": (rng.random(n) < 0.12).astype(float),  # card vs IP country
         "velocity": rng.poisson(1.2, n).astype(float)}    # card uses, last hour
    logit = (-2.5 + 0.9 * np.log(d["amount"] / 40) - 0.9 * np.log1p(d["age_days"] / 100)
             + 2.0 * d["mismatch"] + 0.55 * d["velocity"])
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    X = np.column_stack([np.log(d["amount"]), np.log1p(d["age_days"]), d["mismatch"],
                         d["velocity"], rng.normal(size=(n, 6))])
    return X, y, d


# ---- 1. By hand: which payments to label next ------------------------------------
def entropy_bits(p):
    return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))


scores = np.array([0.03, 0.48, 0.91, 0.62, 0.20])
H = entropy_bits(scores)
print("score  ", scores)
print("entropy", np.round(H, 3))
assert np.isclose(H[4], 0.722, atol=5e-4)
assert list(np.argsort(-H)[:2]) == [1, 3]
assert list(np.argsort(np.abs(scores - 0.5))) == list(np.argsort(-H))   # same order

# ---- 2. Seeded comparison: random against uncertainty sampling -------------------
rng = np.random.default_rng(78)
X_pool, y_pool, d_pool = make_payments(2_000, rng)
X_test, y_test, _ = make_payments(4_000, rng)
mu, sd = X_pool.mean(axis=0), X_pool.std(axis=0)
Z_pool, Z_test = (X_pool - mu) / sd, (X_test - mu) / sd


def learning_run(strategy, seed, rounds=15, batch=10, start=20):
    rng = np.random.default_rng(seed)
    while True:                                   # a seed set with both classes
        first = rng.choice(len(y_pool), start, replace=False)
        if 0 < y_pool[first].sum() < start:
            break
    labeled = np.zeros(len(y_pool), bool)
    labeled[first] = True
    curve = []
    for _ in range(rounds + 1):
        w = fit_logistic(Z_pool[labeled], y_pool[labeled])
        curve.append(auc(y_test, predict(w, Z_test)))
        rest = np.flatnonzero(~labeled)
        if strategy == "random":
            pick = rng.choice(rest, batch, replace=False)
        else:                                     # label the scores nearest 0.5
            p = predict(w, Z_pool[rest])
            pick = rest[np.argsort(np.abs(p - 0.5))[:batch]]
        labeled[pick] = True
    return curve


curves = {s: np.array([learning_run(s, seed) for seed in range(20)])
          for s in ("random", "uncertainty")}
label_counts = 20 + 10 * np.arange(16)
print(f"\nfraud rate in the pool {y_pool.mean():.3f}; mean test AUC over 20 seeds")
print("labels       " + "".join(f"{n:7d}" for n in label_counts[::3]))
for s, c in curves.items():
    print(f"{s:12s} " + "".join(f"{v:7.3f}" for v in c.mean(axis=0)[::3]))
mean_r, mean_u = curves["random"].mean(axis=0), curves["uncertainty"].mean(axis=0)
match = label_counts[np.argmax(mean_u >= mean_r[-1])]
print(f"uncertainty sampling passes random's 170-label AUC at {match} labels")
assert mean_u[-1] > mean_r[-1]

# ---- 3. Weak supervision: labeling functions and a majority vote -----------------
def lf_mismatch_large(d):
    return np.where((d["mismatch"] == 1) & (d["amount"] > 100), FRAUD, ABSTAIN)


def lf_new_merchant(d):
    return np.where((d["age_days"] < 30) & (d["amount"] > 80), FRAUD, ABSTAIN)


def lf_quiet_card(d):
    return np.where((d["mismatch"] == 0) & (d["velocity"] <= 1), CLEAN, ABSTAIN)


LFS = [lf_mismatch_large, lf_new_merchant, lf_quiet_card]


def majority_vote(votes):
    fraud = (votes == FRAUD).sum(axis=1)
    clean = (votes == CLEAN).sum(axis=1)
    return np.where(fraud > clean, FRAUD, np.where(clean > fraud, CLEAN, ABSTAIN))


hand = {"mismatch": np.array([1, 0, 0, 0]), "amount": np.array([250, 20, 300, 45]),
        "age_days": np.array([400, 900, 5, 200]), "velocity": np.array([3, 0, 1, 3])}
hand_votes = np.column_stack([lf(hand) for lf in LFS])
assert list(majority_vote(hand_votes)) == [FRAUD, CLEAN, ABSTAIN, ABSTAIN]

votes = np.column_stack([lf(d_pool) for lf in LFS])
print("\nlabeling function    coverage  accuracy")
for lf, v in zip(LFS, votes.T):
    fired = v != ABSTAIN
    accuracy = np.mean(v[fired] == y_pool[fired])
    print(f"{lf.__name__:20s} {fired.mean():8.3f} {accuracy:9.3f}")
weak = majority_vote(votes)
covered = weak != ABSTAIN
print(f"{'majority vote':20s} {covered.mean():8.3f} "
      f"{np.mean(weak[covered] == y_pool[covered]):9.3f}")

w_weak = fit_logistic(Z_pool[covered], weak[covered])
w_gold = fit_logistic(Z_pool, y_pool)
auc_weak = auc(y_test, predict(w_weak, Z_test))
auc_gold = auc(y_test, predict(w_gold, Z_test))
print(f"test AUC: trained on {covered.sum()} vote labels {auc_weak:.3f}, "
      f"on 2000 hand labels {auc_gold:.3f}")

# The from-scratch pieces agree with scikit-learn.
sk = LogisticRegression(C=1.0, tol=1e-10, max_iter=1000).fit(Z_pool, y_pool)
assert np.allclose(np.r_[sk.intercept_, sk.coef_[0]], w_gold, atol=1e-4)
assert np.isclose(auc_gold, roc_auc_score(y_test, predict(w_gold, Z_test)))
