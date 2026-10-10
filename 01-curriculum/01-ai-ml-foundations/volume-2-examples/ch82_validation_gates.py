"""Chapter 82. Data-validation and model-validation gates as small runnable checks.
A release proceeds only if every blocking gate passes."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(82)

# ---- 1. Data gates on today's batch of payments ----------------------------------
history = rng.normal(48.20, 1.50, 30)                # the last 30 daily mean amounts
n = 5_000
batch = {
    "payment_id": np.arange(n),
    "merchant_id": np.where(rng.random(n) < 0.002, -1, rng.integers(0, 800, n)),
    "amount": rng.lognormal(3.45, 0.90, n),          # USD
}
bug = rng.random(n) < 0.002                          # an upstream job sent cents
batch["amount"][bug] *= 100


def gate_schema(b):
    missing = {"payment_id", "merchant_id", "amount"} - set(b)
    return not missing, f"missing columns: {sorted(missing) or 'none'}"


def gate_completeness(b, limit=0.005):
    share = np.mean(b["merchant_id"] == -1)
    return share <= limit, f"null merchant_id {share:.2%} (limit {limit:.1%})"


def gate_range(b, low=0.50, high=10_000):
    bad = np.mean((b["amount"] < low) | (b["amount"] > high))
    return bad == 0, f"{bad:.2%} of amounts outside USD {low} to {high:,}"


def gate_mean_shift(b, history, z_limit=3.0):
    z = (b["amount"].mean() - history.mean()) / history.std(ddof=1)
    return abs(z) <= z_limit, f"mean {b['amount'].mean():.2f}, z = {z:+.1f}"


def run_gates(gates):
    """Each gate is (name, blocking, (passed, detail)). Returns True if clear to go."""
    clear = True
    for name, blocking, (passed, detail) in gates:
        status = "pass" if passed else ("BLOCK" if blocking else "warn")
        clear = clear and (passed or not blocking)
        print(f"  {name:13s} {status:5s} {detail}")
    return clear


print(f"history: mean {history.mean():.2f}, sd {history.std(ddof=1):.2f}; "
      f"rows sent in cents today: {bug.sum()} of {n}")
data_ok = run_gates([
    ("schema", True, gate_schema(batch)),
    ("completeness", True, gate_completeness(batch)),
    ("range", False, gate_range(batch)),
    ("mean shift", True, gate_mean_shift(batch, history)),
])
print("data gates:", "train" if data_ok else "stop before training")
z_hand = (batch["amount"].mean() - history.mean()) / history.std(ddof=1)
assert not data_ok and z_hand > 3

# ---- 2. Model gates: candidate against the model in production -------------------
def make(n):
    small = (rng.random(n) < 0.15).astype(float)     # small-merchant segment
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    logit = -2.2 + 1.0 * x1 + np.where(small == 1, -0.8, 1.3) * x2
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
    return small, x1, x2, y


small, x1, x2, y = make(20_000)
s_t, x1_t, x2_t, y_t = make(20_000)
base = LogisticRegression().fit(np.column_stack([x1, small]), y)
cand = LogisticRegression().fit(np.column_stack([x1, small, x2]), y)   # new signal x2
p_base = base.predict_proba(np.column_stack([x1_t, s_t]))[:, 1]
p_cand = cand.predict_proba(np.column_stack([x1_t, s_t, x2_t]))[:, 1]


def ece(y, p, bins=10):
    """Expected calibration error: gap between confidence and outcome, by bin."""
    idx = np.minimum((p * bins).astype(int), bins - 1)
    return sum(np.mean(idx == b) * abs(y[idx == b].mean() - p[idx == b].mean())
               for b in range(bins) if np.any(idx == b))


def gate_not_worse(cand_value, base_value, slack, higher_is_better=True):
    """Pass unless the candidate is worse than production by more than `slack`."""
    worse_by = (base_value - cand_value) * (1 if higher_is_better else -1)
    detail = f"candidate {cand_value:.3f} vs production {base_value:.3f}"
    return worse_by <= slack, detail


seg, auc = s_t == 1, roc_auc_score
model_ok = run_gates([
    ("overall AUC", True, gate_not_worse(auc(y_t, p_cand), auc(y_t, p_base), 0.0)),
    ("small AUC", True, gate_not_worse(auc(y_t[seg], p_cand[seg]),
                                       auc(y_t[seg], p_base[seg]), 0.01)),
    ("large AUC", True, gate_not_worse(auc(y_t[~seg], p_cand[~seg]),
                                       auc(y_t[~seg], p_base[~seg]), 0.01)),
    ("calibration", True, gate_not_worse(ece(y_t, p_cand), ece(y_t, p_base), 0.01,
                                         higher_is_better=False)),
])
print("model gates:", "register the candidate" if model_ok else "do not release")
assert auc(y_t, p_cand) > auc(y_t, p_base) and not model_ok
