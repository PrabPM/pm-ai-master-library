"""Chapter 9: confusion matrix, curves, calibration and a threshold set by cost."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score

from ch00_payflow_data import PAYMENT_FEATURES, matrix, payments, split

# The hand example: 1,000 payments, 20 fraud, the model flags 50 and catches 15.
tp, fp, fn, tn = 15, 35, 5, 945
precision, recall = tp / (tp + fp), tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)
accuracy = (tp + tn) / 1000
print(f"precision {precision:.2f}  recall {recall:.2f}  F1 {f1:.3f}  "
      f"accuracy {accuracy:.2f}  flag-nothing accuracy {(tn + fp) / 1000:.2f}")
assert np.isclose(f1, 3 / 7) and np.isclose(accuracy, 0.96)
assert fn * 120 + fp * 4 == 740 and 20 * 120 == 2400      # the two costs by hand

# The payments table: fit on 15,000 rows, judge on the 5,000 held out.
t = payments()
X = matrix(t, PAYMENT_FEATURES)
X[:, 0] = np.log(X[:, 0])                      # amounts are skewed, so use the log
Xtr, Xte, ytr, yte = split(X, t["is_fraud"])
model = LogisticRegression(C=np.inf, max_iter=5000).fit(Xtr, ytr)
p = model.predict_proba(Xte)[:, 1]
print(f"held-out fraud rate {yte.mean():.3f}   ROC AUC {roc_auc_score(yte, p):.3f}   "
      f"PR AUC {average_precision_score(yte, p):.3f}   "
      f"Brier {brier_score_loss(yte, p):.4f}")

COST_MISSED, COST_BLOCKED = 120.0, 4.0         # USD per missed fraud, per good block
cost_threshold = COST_BLOCKED / (COST_BLOCKED + COST_MISSED)


def at(threshold):
    flag = p >= threshold
    tp, fp = np.sum(flag & (yte == 1)), np.sum(flag & (yte == 0))
    fn = np.sum(~flag & (yte == 1))
    cost = fn * COST_MISSED + fp * COST_BLOCKED
    prec = tp / max(tp + fp, 1)
    print(f"threshold {threshold:.3f}: caught {tp:>2}, blocked {fp:>3}, precision "
          f"{prec:.2f}, recall {tp / (tp + fn):.2f}, cost {cost:,.0f}")
    return cost


costs = [at(th) for th in (0.5, cost_threshold)]
assert costs[1] < costs[0] and np.isclose(cost_threshold, 0.032, atol=5e-4)

# Calibration: sort by score, cut into five equal groups, compare with reality.
groups = np.array_split(np.argsort(p), 5)
for name, v in (("predicted", p), ("observed ", yte)):
    rates = " ".join(f"{v[g].mean():.3f}" for g in groups)
    print(f"{name} rate by fifth: {rates}")

weighted = LogisticRegression(C=np.inf, max_iter=5000, class_weight="balanced")
pw = weighted.fit(Xtr, ytr).predict_proba(Xte)[:, 1]
print(f"with class weights: mean score {pw.mean():.3f}, fraud rate {yte.mean():.3f}, "
      f"ROC AUC {roc_auc_score(yte, pw):.3f}")
