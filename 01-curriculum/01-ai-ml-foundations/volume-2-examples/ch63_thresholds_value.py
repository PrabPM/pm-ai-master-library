"""Chapter 63: the expected-value threshold from a cost matrix, and a model's
metrics translated into yearly money. Synthetic calibrated scores.
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

C_FP, C_FN = 15.0, 135.0        # USD: blocking a good payment, missing a fraud
p_star = C_FP / (C_FP + C_FN)   # block when the fraud probability is above this


def yearly_value(n, base_rate, tpr, fpr):
    """Fraud loss avoided minus good payments blocked, against blocking nothing."""
    return n * (base_rate * tpr * C_FN - (1 - base_rate) * fpr * C_FP)


rng = np.random.default_rng(63)
n = 400_000
p = rng.beta(0.08, 7.0, n)                 # each payment's true fraud probability
fraud = rng.random(n) < p                  # so the score p is calibrated
scale = 50_000_000 / n                     # PayFlow processes 50 million a year


def at(threshold):
    block = p >= threshold
    tpr = (block & fraud).sum() / fraud.sum()
    fpr = (block & ~fraud).sum() / (~fraud).sum()
    return tpr, fpr, yearly_value(50_000_000, fraud.mean(), tpr, fpr)


print(f"p* = {p_star:.2f}; hand translation: "
      f"USD {yearly_value(1e6, 0.01, 0.6, 0.02):,.0f}")
print(f"fraud rate in the sample: {fraud.mean():.2%}")
print("threshold   recall   good blocked   yearly value")
for thr in (0.02, 0.05, 0.10, 0.20, 0.50):
    tpr, fpr, value = at(thr)
    print(f"   {thr:.2f}     {tpr:6.1%}     {fpr:6.2%}      "
          f"USD {value / 1e6:6.2f} million")
grid = np.linspace(0.01, 0.60, 60)
values = np.array([at(g)[2] for g in grid])
print(f"best threshold on the grid: {grid[values.argmax()]:.2f}")

# ---- checks against the hand-worked numbers ----
assert np.isclose(p_star, 0.10)
assert np.isclose(yearly_value(1e6, 0.01, 0.6, 0.02), 513_000.0)
assert abs(grid[values.argmax()] - p_star) <= 0.03
assert at(0.10)[2] > at(0.50)[2]

# ---- figure ----
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
ax.plot(grid, values / 1e6, color="#4f46e5", lw=2)
for thr, color, label in [(p_star, "#15803d", "p* = 0.10"),
                          (0.5, "#b91c1c", "default 0.50")]:
    ax.axvline(thr, color=color, ls="--", lw=1.5)
    ax.plot([thr], [at(thr)[2] / 1e6], "o", color=color)
    ax.annotate(f"{label}: {at(thr)[2] / 1e6:.1f}", (thr, at(thr)[2] / 1e6),
                textcoords="offset points", xytext=(14, -34 if thr < 0.3 else 8),
                color=color)
ax.set_xlabel("block when fraud probability is at or above")
ax.set_ylabel("yearly value, USD million")
ax.grid(axis="y")
fig.savefig(ASSETS / "ch63-value-by-threshold.svg", bbox_inches="tight",
            metadata={"Date": None})
