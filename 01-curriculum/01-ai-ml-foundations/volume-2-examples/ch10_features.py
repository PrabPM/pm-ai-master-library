"""Chapter 10: building features, catching leakage, and two kinds of importance."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from ch00_payflow_data import PAYMENT_FEATURES, matrix, payments, split

# Two features by hand.
velocity_ratio = 5 / 0.5                       # 5 payments this hour, usual rate 0.5
frauds, rows, overall, m = 2, 8, 0.02, 20      # a category with 8 payments, 2 fraud
encoded = (frauds + m * overall) / (rows + m)
print(f"velocity ratio {velocity_ratio:.0f}   raw category rate {frauds / rows:.2f}   "
      f"smoothed target encoding {encoded:.4f}")
assert np.isclose(encoded, 2.4 / 28)

# The payments table plus two columns that should not help on new payments.
t = payments()
rng = np.random.default_rng(10)
y = t["is_fraud"]
card_hash = rng.integers(0, 10**6, len(y))     # a random number per row: pure noise
dispute_opened = np.where(rng.random(len(y)) < 0.9, y, 0)   # known weeks later
names = PAYMENT_FEATURES + ["card_hash", "dispute_opened"]
X = np.column_stack([matrix(t, PAYMENT_FEATURES), card_hash, dispute_opened])
X[:, 0] = np.log(X[:, 0])
Xtr, Xte, ytr, yte = split(X, y, test_share=0.5)

for label, cols in [("honest features", [0, 1, 2, 3, 4]),
                    ("plus dispute_opened", [0, 1, 2, 3, 4, 6])]:
    model = LogisticRegression(C=np.inf, max_iter=5000).fit(Xtr[:, cols], ytr)
    auc = roc_auc_score(yte, model.predict_proba(Xte[:, cols])[:, 1])
    print(f"{label:<20} held-out ROC AUC {auc:.3f}")

# Importance two ways, for a forest given the five honest features and card_hash.
cols = [0, 1, 2, 3, 4, 5]
forest = RandomForestClassifier(n_estimators=50, random_state=0)
forest.fit(Xtr[:, cols], ytr)
perm = permutation_importance(forest, Xte[:, cols], yte, scoring="roc_auc",
                              n_repeats=5, random_state=0)
print(f"{'feature':<14}{'impurity':>10}{'permutation':>13}")
for j in np.argsort(forest.feature_importances_)[::-1]:
    print(f"{names[cols[j]]:<14}{forest.feature_importances_[j]:>10.3f}"
          f"{perm.importances_mean[j]:>13.3f}")
assert np.argsort(forest.feature_importances_)[::-1].tolist().index(5) <= 1
assert abs(perm.importances_mean[5]) < 0.02
