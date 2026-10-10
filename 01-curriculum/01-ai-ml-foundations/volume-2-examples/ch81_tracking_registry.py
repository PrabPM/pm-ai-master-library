"""Chapter 81. A run record, a data version and a model registry in forty lines:
enough to answer "what exactly is running, and how was it made?"."""
import hashlib
import inspect

import numpy as np
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score


def make_data(seed, shift=0.0):
    """Synthetic fraud data. `shift` moves the amount feature, as a new month might."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(6_000, 3)) * [40.0, 1.0, 1.0] + [60.0 + shift, 0.0, 0.0]
    logit = -3.0 + 0.03 * (X[:, 0] - 60.0 - shift) + 0.9 * X[:, 1]
    y = (rng.random(6_000) < 1 / (1 + np.exp(-logit))).astype(int)
    return X, y


def train_v1(X, y, C):
    Z = (X - X[:4_000].mean(axis=0)) / X[:4_000].std(axis=0)   # standardize
    model = LogisticRegression(C=C, max_iter=200).fit(Z[:4_000], y[:4_000])
    return roc_auc_score(y[4_000:], model.predict_proba(Z[4_000:])[:, 1])


def train_v2(X, y, C):
    Z = X / 1_000.0                                    # the scaling was "simplified"
    model = LogisticRegression(C=C, max_iter=200).fit(Z[:4_000], y[:4_000])
    return roc_auc_score(y[4_000:], model.predict_proba(Z[4_000:])[:, 1])


def digest(*parts):
    h = hashlib.sha256()
    for part in parts:
        h.update(part if isinstance(part, bytes) else str(part).encode())
    return h.hexdigest()[:10]


RUNS, REGISTRY = {}, {"versions": {}, "aliases": {}}


def tracked_run(train_fn, data, params):
    """Train, and record everything needed to do it again."""
    X, y = data
    record = {
        "code": digest(inspect.getsource(train_fn)),
        "data": digest(X.tobytes(), y.tobytes()),
        "env": f"numpy {np.__version__}, scikit-learn {sklearn.__version__}",
        "params": params,
        "auc": round(train_fn(X, y, **params), 4),
    }
    run_id = digest(sorted(record.items()))
    RUNS[run_id] = record
    return run_id


def register(run_id, alias=None):
    version = len(REGISTRY["versions"]) + 1
    REGISTRY["versions"][version] = run_id
    if alias:
        REGISTRY["aliases"][alias] = version
    return version


march, april = make_data(seed=81), make_data(seed=82, shift=25.0)
run_a = tracked_run(train_v1, march, {"C": 1.0})
register(run_a, alias="production")
run_b = tracked_run(train_v2, april, {"C": 1.0})
register(run_b, alias="production")

live = REGISTRY["aliases"]["production"]
print(f"production -> version {live} -> run {REGISTRY['versions'][live]}")
for run_id in (run_a, run_b):
    r = RUNS[run_id]
    print(f"run {run_id}: code {r['code']} data {r['data']} auc {r['auc']}")
print("env:", RUNS[run_b]["env"])

# Reproduce: same code, data and parameters give the same run id and metric.
assert tracked_run(train_v1, make_data(seed=81), {"C": 1.0}) == run_a

# What changed between the two versions? Retrain the two mixed combinations.
months = (("march", march), ("april", april))
grid = {(c.__name__, name): round(c(*d, C=1.0), 4)
        for c in (train_v1, train_v2) for name, d in months}
print("\n           march data  april data")
for c in ("train_v1", "train_v2"):
    print(f"{c:9s}  {grid[c, 'march']:10.4f}  {grid[c, 'april']:10.4f}")
code_effect = grid["train_v2", "march"] - grid["train_v1", "march"]
data_effect = grid["train_v1", "april"] - grid["train_v1", "march"]
print(f"code change alone {code_effect:+.4f}, data change alone {data_effect:+.4f}")
assert grid["train_v1", "march"] == RUNS[run_a]["auc"]
assert grid["train_v2", "april"] == RUNS[run_b]["auc"]
assert code_effect < data_effect

# Roll back: move the alias. Nothing is retrained and nothing is deleted.
REGISTRY["aliases"]["production"] = 1
print(f"after rollback: production -> version {REGISTRY['aliases']['production']}")
