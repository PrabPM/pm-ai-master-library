"""Chapter 53: recommending PayFlow add-on products with matrix factorization.
Synthetic merchants; every number is illustrative.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-2-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})

products = ["Invoicing", "Payment links", "Subscriptions", "Tax tool", "Fraud tools",
            "Card reader", "Tap to pay", "Tips", "Staff logins", "Instant payouts"]
# Taste of each product on two hidden axes: online selling, in-person selling.
Q_true = np.array([[1.0, 0.1], [0.9, 0.2], [1.0, 0.0], [0.8, 0.3], [0.7, 0.4],
                   [0.1, 1.0], [0.2, 0.9], [0.0, 1.0], [0.2, 0.8], [0.6, 0.6]])
rng = np.random.default_rng(53)
n = 800
online = rng.random(n) < 0.5
P_true = np.where(online[:, None], [1.0, 0.15], [0.15, 1.0])
P_true = P_true + rng.normal(0, 0.15, (n, 2))
popularity = np.array([0.0, 1.2, -0.6, -0.4, 0.2, 0.6, -0.2, -0.8, -0.6, 1.4])
adopt_prob = 1 / (1 + np.exp(-(4.5 * P_true @ Q_true.T - 3.6 + popularity)))
R = (rng.random((n, len(products))) < adopt_prob).astype(float)

# Hide one adopted product per merchant; the recommender must find it again.
train, hidden = R.copy(), np.full(n, -1)
for u in np.flatnonzero(R.sum(axis=1) >= 2):
    hidden[u] = rng.choice(np.flatnonzero(R[u]))
    train[u, hidden[u]] = 0.0
users = np.flatnonzero(hidden >= 0)

U, S, Vt = np.linalg.svd(train, full_matrices=False)   # matrix factorization
k = 2
scores_mf = (U[:, :k] * S[:k]) @ Vt[:k]                # p_u . q_i for every pair
scores_pop = np.tile(train.mean(axis=0), (n, 1))       # baseline: most adopted


def hit_rate(scores, top=3):
    """Share of merchants whose hidden product is in their top-3 new suggestions."""
    s = np.where(train > 0, -np.inf, scores)           # never suggest what they have
    best = np.argsort(-s, axis=1)[:, :top]
    return float(np.mean([hidden[u] in best[u] for u in users])), best


hit_pop, best_pop = hit_rate(scores_pop)
hit_mf, best_mf = hit_rate(scores_mf)
print("hand check, dot products:", np.dot([0.9, 0.2], [1.0, 0.1]).round(2),
      np.dot([0.9, 0.2], [0.1, 1.0]).round(2))
print(f"hit rate at 3   popularity {hit_pop:.3f}   matrix factorization {hit_mf:.3f}")
print("distinct products in first slot:  popularity", len(set(best_pop[users, 0])),
      "  matrix factorization", len(set(best_mf[users, 0])))
extra = 20_000 * (hit_mf - hit_pop) * 0.10 * 300.0   # 10% act, USD 300 a year each
print(f"extra yearly revenue across 20,000 merchants: USD {extra:,.0f}")

# ---- checks ----
assert np.isclose(np.dot([0.9, 0.2], [1.0, 0.1]), 0.92)
assert np.isclose(np.dot([0.9, 0.2], [0.1, 1.0]), 0.29)
assert hit_mf > hit_pop + 0.05

# ---- figure: the learned product and merchant positions ----
item = Vt[:k].T * S[:k] ** 0.5
user = U[:, :k] * S[:k] ** 0.5
fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=100)
show = rng.choice(n, 160, replace=False)
ax.scatter(user[show, 0] * 6, user[show, 1] * 6, s=10, color="#cbd5e1",
           label="merchants (scaled)")
ax.scatter(item[:, 0], item[:, 1], s=36, color="#4f46e5", label="products")
offsets = {"Subscriptions": (8, -14), "Tax tool": (8, 6), "Staff logins": (8, -13),
           "Tips": (8, 6), "Payment links": (8, 6), "Invoicing": (-8, -14),
           "Tap to pay": (-8, 6), "Card reader": (8, -4)}
for name, (x, y) in zip(products, item):
    dx, dy = offsets.get(name, (8, 6))
    ax.annotate(name, (x, y), textcoords="offset points", xytext=(dx, dy),
                ha="right" if dx < 0 else "left", color="#1f2937")
ax.set_xlabel("learned dimension 1")
ax.set_ylabel("learned dimension 2")
ax.grid(True)
ax.legend(frameon=False, loc="best")
fig.savefig(ASSETS / "ch53-embedding-map.svg", bbox_inches="tight",
            metadata={"Date": None})
