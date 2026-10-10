"""Chapter 3: one Gini split by hand, then a tree against a forest."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier

from ch00_payflow_data import PAYMENT_FEATURES, matrix, payments, split

# Ten payments worked by hand: amount in USD, new card (1 = yes), fraud (1 = yes).
amount = np.array([20, 35, 50, 60, 80, 120, 250, 300, 400, 500])
new_card = np.array([0, 0, 1, 0, 1, 0, 1, 1, 1, 0])
fraud = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 0])


def gini(labels):
    p = labels.mean()
    return 1 - p ** 2 - (1 - p) ** 2


def gain(mask):
    """Impurity removed by sending the rows where mask is True to one side."""
    share = mask.mean()
    children = share * gini(fraud[mask]) + (1 - share) * gini(fraud[~mask])
    return gini(fraud) - children


print(f"parent Gini {gini(fraud):.2f}")
print(f"split on new_card      gain {gain(new_card == 1):.2f}")
print(f"split on amount > 100  gain {gain(amount > 100):.2f}")
stump = DecisionTreeClassifier(max_depth=1).fit(np.column_stack([amount, new_card]),
                                                fraud)
print(f"scikit-learn splits on feature {stump.tree_.feature[0]} "
      f"at {stump.tree_.threshold[0]:.0f}")
assert np.isclose(gini(fraud), 0.48) and np.isclose(gain(new_card == 1), 0.08)
assert np.isclose(gain(amount > 100), 0.32) and stump.tree_.threshold[0] == 100

# The payments table: one deep tree, one shallow tree, one forest.
t = payments()
Xtr, Xte, ytr, yte = split(matrix(t, PAYMENT_FEATURES), t["is_fraud"])
models = {
    "tree, no depth limit": DecisionTreeClassifier(random_state=0),
    "tree, depth 4": DecisionTreeClassifier(max_depth=4, random_state=0),
    "forest, 100 trees": RandomForestClassifier(
        n_estimators=100, min_samples_leaf=20, oob_score=True, random_state=0),
}
for name, model in models.items():
    model.fit(Xtr, ytr)
    auc_tr = roc_auc_score(ytr, model.predict_proba(Xtr)[:, 1])
    auc_te = roc_auc_score(yte, model.predict_proba(Xte)[:, 1])
    print(f"{name:<21} train AUC {auc_tr:.3f}   test AUC {auc_te:.3f}")
forest = models["forest, 100 trees"]
oob = roc_auc_score(ytr, forest.oob_decision_function_[:, 1])
print(f"forest out-of-bag AUC {oob:.3f}")
