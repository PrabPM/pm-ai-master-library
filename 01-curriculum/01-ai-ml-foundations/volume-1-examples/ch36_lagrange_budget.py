"""Chapter 36: splitting a fixed budget with a Lagrange multiplier.

PayFlow has USD 40 thousand a month to win new merchants through two channels:
paid search (x1) and partner referrals (x2), both in USD thousands.
New merchants won: f(x1, x2) = 10 sqrt(x1) + 30 sqrt(x2).
Writes volume-1-assets/ch36-budget-tangent.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)
A1, A2 = 10.0, 30.0


def merchants(x):
    return A1 * np.sqrt(x[0]) + A2 * np.sqrt(x[1])


def solve_by_lagrange(budget):
    """Stationarity gives x_i = (a_i / (2 lam))^2; the budget fixes lam."""
    lam = np.sqrt((A1**2 + A2**2) / (4 * budget))
    x = np.array([(A1 / (2 * lam)) ** 2, (A2 / (2 * lam)) ** 2])
    return x, lam


def solve_numerically(budget):
    result = minimize(lambda x: -merchants(x), x0=[budget / 2, budget / 2],
                      constraints=[{"type": "eq",
                                    "fun": lambda x: x[0] + x[1] - budget}],
                      bounds=[(1e-9, None)] * 2, method="SLSQP")
    return result.x


x_star, lam = solve_by_lagrange(40.0)
print(f"best split: paid search {x_star[0]:.1f}, referrals {x_star[1]:.1f}")
print(f"merchants won: {merchants(x_star):.1f}")
print(f"shadow price lambda: {lam:.2f} merchants per extra USD thousand")
marginal = [A1 / (2 * np.sqrt(x_star[0])), A2 / (2 * np.sqrt(x_star[1]))]
print(f"marginal return of each channel at the optimum: {marginal[0]:.2f}, "
      f"{marginal[1]:.2f}")
print(f"an even 20/20 split wins {merchants([20.0, 20.0]):.1f}")

x_num = solve_numerically(40.0)
print("numerical solver agrees:", np.round(x_num, 2))
assert np.allclose(x_star, [4.0, 36.0]) and np.isclose(lam, 2.5)
assert np.isclose(merchants(x_star), 200.0)
assert np.allclose(x_num, x_star, atol=1e-2)
assert np.allclose(marginal, lam)

# the multiplier predicts what one more thousand dollars is worth
gain = merchants(solve_by_lagrange(41.0)[0]) - merchants(x_star)
print(f"actual gain from budget 40 -> 41: {gain:.3f} merchants")
assert abs(gain - lam) < 0.02

# ... but only at the margin: the shadow price falls as the budget grows
for budget in (40, 90, 160):
    xb, lam_b = solve_by_lagrange(float(budget))
    print(f"budget {budget:3d}: lambda = {lam_b:.3f}, merchants = {merchants(xb):.0f}")
assert np.isclose(solve_by_lagrange(90.0)[1], 5 / 3)


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch36", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, ax = plt.subplots(figsize=(5.6, 3.6), dpi=100)
    g1, g2 = np.meshgrid(np.linspace(0.001, 46, 400), np.linspace(0.001, 46, 400))
    f = A1 * np.sqrt(g1) + A2 * np.sqrt(g2)
    levels = [140, 170, 200, 230]
    ax.contour(g1, g2, f, levels=levels, colors="#cbd5e1", linewidths=1.2)
    for level in levels:                      # label each contour at x1 = 40
        y_at = ((level - A1 * np.sqrt(40.0)) / A2) ** 2
        ax.text(40.5, y_at + 0.8, str(level), color="#6b7280", fontsize=9)
    ax.plot([0, 40], [40, 0], color="#1f2937", linewidth=1.8)
    ax.text(23.0, 18.3, "budget line x₁ + x₂ = 40", color="#1f2937", fontsize=10,
            rotation=-45, rotation_mode="anchor", transform_rotates_text=True)
    ax.plot(4, 36, "o", color="#4f46e5", markersize=8)
    ax.annotate("optimum (4, 36): the line just\ntouches the 200-merchant contour",
                (4, 36), xytext=(9, 40.5), color="#4f46e5", fontsize=10,
                arrowprops={"arrowstyle": "-", "color": "#4f46e5"})
    ax.plot(20, 20, "o", color="#b45309", markersize=6)
    ax.annotate("even split:\n179 merchants", (20, 20), xytext=(3, 6),
                color="#b45309", fontsize=10,
                arrowprops={"arrowstyle": "-", "color": "#b45309"})
    ax.set_xlim(0, 46)
    ax.set_ylim(0, 46)
    ax.set_xlabel("x₁: paid search (USD thousands)")
    ax.set_ylabel("x₂: partner referrals (USD thousands)")
    fig.tight_layout()
    fig.savefig(ASSETS / "ch36-budget-tangent.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
