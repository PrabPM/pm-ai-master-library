"""Chapter 37: KKT conditions and the support vectors of a maximum-margin line.

Part 1 adds a cap to the budget problem of chapter 36 and reads the multipliers.
Part 2 fits a hard-margin classifier to six PayFlow payments.
Features: x1 = amount in USD hundreds, x2 = payments from the same device in
the last hour. Label +1 = fraud, -1 = legitimate.
Writes volume-1-assets/ch37-max-margin.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)

# ---- Part 1: the budget of chapter 36 with a cap on referrals --------------
# maximize 10 sqrt(x1) + 30 sqrt(x2)  subject to  x1 + x2 <= 40  and  x2 <= cap
for cap in (24.0, 38.0):
    x2 = min(cap, 36.0)                 # 36 is the uncapped optimum
    x1 = 40.0 - x2
    mu_budget = 5 / np.sqrt(x1)         # stationarity in x1
    mu_cap = 15 / np.sqrt(x2) - mu_budget          # stationarity in x2
    slack = cap - x2
    print(f"cap {cap:.0f}: x = ({x1:.0f}, {x2:.0f}), cap slack = {slack:.0f}, "
          f"mu_budget = {mu_budget:.3f}, mu_cap = {mu_cap:.3f}")
    assert mu_cap >= -1e-12 and np.isclose(mu_cap * slack, 0.0)   # KKT 3 and 4

# ---- Part 2: six payments, maximum-margin line ------------------------------
X = np.array([[3, 5], [5, 3], [6, 5], [2, 2], [1, 1], [3, 0]], dtype=float)
y = np.array([1, 1, 1, -1, -1, -1], dtype=float)


def fit(X, y):
    """Hard-margin SVM: the smallest ||w|| with every margin at least 1."""
    cons = [{"type": "ineq", "fun": lambda p, i=i: y[i] * (X[i] @ p[:2] + p[2]) - 1}
            for i in range(len(y))]
    res = minimize(lambda p: 0.5 * p[:2] @ p[:2], x0=np.zeros(3), constraints=cons,
                   method="SLSQP", options={"ftol": 1e-12, "maxiter": 500})
    return res.x[:2], res.x[2]


def multipliers(X, y, w, b):
    """Solve w = sum_i alpha_i y_i x_i on the points whose margin is 1."""
    margins = y * (X @ w + b)
    on = np.isclose(margins, 1.0, atol=1e-5)
    A = np.vstack([(y[on, None] * X[on]).T, y[on]])   # also sum_i alpha_i y_i = 0
    alpha_on = np.linalg.lstsq(A, np.append(w, 0.0), rcond=None)[0]
    alpha = np.zeros(len(y))
    alpha[on] = alpha_on
    return margins, alpha


w, b = fit(X, y)
margins, alpha = multipliers(X, y, w, b)
print(f"w = {np.round(w, 4)}, b = {b:.1f}, margin width = {2 / np.linalg.norm(w):.3f}")
print("y(w.x+b):", margins.round(3))
print("alpha:   ", alpha.round(3))

# hand result
assert np.allclose(w, [0.5, 0.5], atol=1e-5) and np.isclose(b, -3.0, atol=1e-5)
assert np.allclose(margins, [1, 1, 2.5, 1, 2, 1.5], atol=1e-4)
assert np.allclose(alpha, [0.125, 0.125, 0, 0.25, 0, 0], atol=1e-4)
# the four KKT conditions
assert np.allclose((alpha * y) @ X, w, atol=1e-4)            # stationarity in w
assert np.isclose(alpha @ y, 0.0, atol=1e-6)                 # stationarity in b
assert np.all(margins >= 1 - 1e-6) and np.all(alpha >= -1e-9)
assert np.allclose(alpha * (margins - 1), 0.0, atol=1e-6)    # complementary slack

keep = np.array([0, 1, 3])                                   # support vectors only
w_sv, b_sv = fit(X[keep], y[keep])
print(f"refit on payments 1, 2, 4 only: w = {np.round(w_sv, 4)}, b = {b_sv:.4f}")
drop = np.array([0, 1, 2, 4, 5])                             # remove payment 4
w_d, b_d = fit(X[drop], y[drop])
print(f"refit without payment 4:        w = {np.round(w_d, 4)}, b = {b_d:.4f}")
assert np.allclose(w_sv, w, atol=1e-5) and np.isclose(b_sv, b, atol=1e-5)
assert not np.allclose(w_d, w, atol=1e-2)


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch37", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=100)
    xs = np.array([-0.5, 7.5])
    ax.plot(xs, (0 - b - w[0] * xs) / w[1], "-", color="#1f2937", linewidth=1.5,
            label="decision line")
    ax.plot(xs, (1 - b - w[0] * xs) / w[1], "--", color="#6b7280", linewidth=1.3,
            label="margin edges")
    ax.plot(xs, (-1 - b - w[0] * xs) / w[1], "--", color="#6b7280", linewidth=1.3)
    fraud = y > 0
    ax.scatter(X[fraud, 0], X[fraud, 1], s=55, color="#b91c1c", marker="s",
               label="fraud (+1)", zorder=3)
    ax.scatter(X[~fraud, 0], X[~fraud, 1], s=55, color="#15803d", marker="o",
               label="legitimate (−1)", zorder=3)
    sv = alpha > 1e-6
    ax.scatter(X[sv, 0], X[sv, 1], s=230, facecolors="none", edgecolors="#4f46e5",
               linewidths=1.6, label="support vector")
    for i, (px, py) in enumerate(X):
        ax.annotate(str(i + 1), (px, py), textcoords="offset points", xytext=(11, 7),
                    fontsize=10, color="#1f2937")
    ax.set_xlim(-0.3, 7.3)
    ax.set_ylim(-0.6, 6.8)
    ax.set_xlabel("x₁: amount (USD hundreds)")
    ax.set_ylabel("x₂: device payments, last hour")
    ax.legend(frameon=False, fontsize=10, loc="center left",
              bbox_to_anchor=(1.02, 0.5), labelspacing=0.9)
    fig.tight_layout()
    fig.savefig(ASSETS / "ch37-max-margin.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
