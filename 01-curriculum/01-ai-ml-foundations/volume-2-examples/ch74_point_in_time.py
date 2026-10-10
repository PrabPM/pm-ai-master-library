"""Chapter 74. Point-in-time joins: the naive join leaks the future, the correct
join does not, and the leak shows up as an inflated offline AUC."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

# ---- 1. The hand example ---------------------------------------------------------
# Feature history for merchant m1: (entity, day the value became known, value).
features = [("m1", 1, 0), ("m1", 5, 1), ("m1", 9, 4)]
# Label rows: (entity, day of the payment, fraud label).
labels = [("m1", 4, 0), ("m1", 6, 1), ("m1", 13, 0)]


def pit_join(labels, features, ttl):
    """Latest feature value known at or before each label time, if fresh enough."""
    out = []
    for entity, t, _ in labels:
        known = [(t_f, v) for e, t_f, v in features if e == entity and t_f <= t]
        if not known:
            out.append(None)
            continue
        t_f, v = max(known)
        out.append(v if t - t_f <= ttl else None)
    return out


def naive_join(labels, features):
    """What a join on the key alone does: every row gets the newest value."""
    latest = {}
    for e, t_f, v in sorted(features, key=lambda r: r[1]):
        latest[e] = v
    return [latest.get(entity) for entity, _, _ in labels]


naive = naive_join(labels, features)
correct = pit_join(labels, features, ttl=3)
print("payment day  ", [t for _, t, _ in labels])
print("naive join   ", naive)
print("point in time", correct)
assert naive == [4, 4, 4]
assert correct == [0, 1, None]

# ---- 2. The same mistake at scale, seeded ----------------------------------------
rng = np.random.default_rng(74)
n_merchants, n_pay = 400, 20_000
risk = rng.beta(1.0, 25.0, n_merchants)             # each merchant's fraud rate
m = rng.integers(0, n_merchants, n_pay)             # merchant of each payment
day = rng.uniform(0, 60, n_pay)                     # when the payment happened
amount_z = rng.normal(0, 1, n_pay)
p = np.clip(risk[m] * np.exp(0.4 * amount_z), 0, 1)
y = (rng.random(n_pay) < p).astype(int)             # 1 = fraud
filed = day + rng.uniform(10, 40, n_pay)            # the chargeback arrives later

cb_pit = np.zeros(n_pay)        # chargebacks already filed when the payment happens
cb_naive = np.zeros(n_pay)      # the merchant's total in today's table
for k in range(n_merchants):
    idx = np.where(m == k)[0]
    f = np.sort(filed[idx][y[idx] == 1])
    cb_pit[idx] = np.searchsorted(f, day[idx], side="right")
    cb_naive[idx] = len(f)


def design(cb):
    return np.column_stack([np.log1p(cb), amount_z])


train, test = day < 40, day >= 40
leaky = LogisticRegression().fit(design(cb_naive)[train], y[train])
honest = LogisticRegression().fit(design(cb_pit)[train], y[train])


def auc(model, cb):
    return roc_auc_score(y[test], model.predict_proba(design(cb)[test])[:, 1])


auc_offline = auc(leaky, cb_naive)      # the number in the slide deck
auc_served = auc(leaky, cb_pit)         # the same model on features it gets live
auc_honest = auc(honest, cb_pit)
print(f"\nfraud rate {y.mean():.3f}, test payments {test.sum()}")
print(f"naive join, offline AUC      {auc_offline:.3f}")
print(f"same model, live features    {auc_served:.3f}")
print(f"point-in-time join, AUC      {auc_honest:.3f}")
assert auc_offline > auc_honest + 0.05
assert auc_served <= auc_honest + 0.01
