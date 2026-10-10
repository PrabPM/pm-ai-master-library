"""Chapter 85. Population stability index by hand and in code, its noise floor,
and the different signatures of data drift, label drift and concept drift."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def psi_from_shares(e, a):
    """PSI from two arrays of bin shares, baseline e and current a."""
    return float(np.sum((a - e) * np.log(a / e)))


def psi(baseline, current, bins=10):
    """PSI of one numeric feature. Bin edges are the baseline's quantiles."""
    edges = np.quantile(baseline, np.linspace(0, 1, bins + 1))[1:-1]
    e = np.bincount(np.searchsorted(edges, baseline), minlength=bins) / len(baseline)
    a = np.bincount(np.searchsorted(edges, current), minlength=bins) / len(current)
    e, a = np.clip(e, 1e-4, None), np.clip(a, 1e-4, None)   # no empty bins in the log
    return psi_from_shares(e, a)


# ---- 1. By hand: the velocity feature, normal week against incident week ---------
normal_week = np.array([0.50, 0.30, 0.15, 0.05])     # share of payments per bin
incident_week = np.array([0.75, 0.17, 0.06, 0.02])
terms = [(a - e) * np.log(a / e) for e, a in zip(normal_week, incident_week)]
print("terms", np.round(terms, 4), "PSI", round(sum(terms), 3))
assert np.isclose(sum(terms), 0.2852, atol=5e-5)
assert np.isclose(psi_from_shares(normal_week, incident_week), sum(terms))

# ---- 2. The noise floor: PSI between two samples of the SAME distribution --------
rng = np.random.default_rng(85)
print("\nrows per period   mean PSI with no drift   (bins - 1) * (1/N + 1/M)")
for n in (200, 20_000):
    sims = [psi(rng.normal(size=n), rng.normal(size=n)) for _ in range(300)]
    theory = 9 * (1 / n + 1 / n)
    print(f"{n:15,d}   {np.mean(sims):22.4f}   {theory:24.4f}")
    assert np.isclose(np.mean(sims), theory, rtol=0.15)

# ---- 3. Three kinds of drift leave three different signatures --------------------
def world(n, new_share=0.10, base=-4.0, amount_weight=0.8):
    """Fraud depends on a new-merchant flag and on the payment amount."""
    new = (rng.random(n) < new_share).astype(float)
    amount = rng.normal(size=n)                     # standardized log amount
    logit = base + 2.0 * new + amount_weight * amount
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return np.column_stack([new, amount]), y


def prior_shift(X, y, new_rate):
    """Resample so fraud is more common but looks exactly as it did."""
    pos, neg = np.flatnonzero(y == 1), np.flatnonzero(y == 0)
    k = int(len(y) * new_rate)
    idx = np.r_[rng.choice(pos, k), rng.choice(neg, len(y) - k)]
    return X[idx], y[idx]


X0, y0 = world(60_000)
model = LogisticRegression().fit(X0, y0)
scenarios = {
    "no drift": world(60_000),
    "data drift": world(60_000, new_share=0.40),         # P(x) moves
    "label drift": prior_shift(*world(60_000), 2 * y0.mean()),   # P(y) doubles
    "concept drift": world(60_000, amount_weight=-0.8),  # P(y | x) changes
}
def route(psi_value, rate_ratio, auc_drop):
    """Which signal goes to which owner."""
    if psi_value >= 0.25:
        return "data owner: inputs moved"
    if auc_drop >= 0.05:
        return "model owner: retrain ticket"
    if rate_ratio >= 1.5:
        return "model owner: recalibrate"
    return "none"


score0 = model.predict_proba(X0)[:, 1]
print("\nscenario       score PSI  fraud rate  mean score    AUC  page")
out = {}
for name, (X, y) in scenarios.items():
    score = model.predict_proba(X)[:, 1]
    out[name] = (psi(score0, score), y.mean(), score.mean(), roc_auc_score(y, score))
    p, rate, mean_score, auc = out[name]
    action = route(p, rate / mean_score, out["no drift"][3] - auc)
    print(f"{name:14s} {p:9.3f} {rate:11.3f} {mean_score:11.3f} {auc:6.3f}  {action}")
assert out["data drift"][0] > 0.25 > out["label drift"][0] > out["concept drift"][0]
assert out["concept drift"][3] < out["no drift"][3] - 0.1
assert out["label drift"][1] > 1.5 * out["label drift"][2]
assert abs(out["label drift"][3] - out["no drift"][3]) < 0.02   # AUC ignores P(y)
