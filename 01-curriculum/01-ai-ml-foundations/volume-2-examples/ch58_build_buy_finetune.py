"""Chapter 58: a weighted scoring matrix for the support assistant, its
sensitivity to the weights, and three-year cost. Illustrative numbers.
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

criteria = ["answer quality", "time to launch", "three-year cost", "data control",
            "differentiation"]
weights = np.array([0.25, 0.25, 0.20, 0.15, 0.15])
scores = {                                   # 1 (poor) to 5 (excellent)
    "buy a product": np.array([3, 5, 3, 2, 1]),
    "build on a model API": np.array([4, 4, 4, 3, 3]),
    "fine-tune and host": np.array([4, 2, 2, 5, 4]),
}


def total(option, w=weights):
    return float(w @ scores[option])


def shifted(x):
    """Move x of weight from 'time to launch' to 'data control'."""
    w = weights.copy()
    w[1] -= x
    w[3] += x
    return w


assert np.isclose(weights.sum(), 1.0)
for option in scores:
    print(f"{option:22s} weighted score {total(option):.2f}")
a, b = scores["build on a model API"], scores["fine-tune and host"]
flip = (total("build on a model API") - total("fine-tune and host")) / (
    (b[3] - b[1]) - (a[3] - a[1]))
print(f"fine-tune overtakes when {flip:.4f} of weight moves from launch time "
      f"to data control")

months = 36
cost = {
    "buy a product": 40_000 + 60 * 150 * months,          # setup + 150 agent seats
    "build on a model API": 180_000 + 4_000 * months,     # build + inference and upkeep
    "fine-tune and host": 320_000 + 9_000 * months + 30_000 * 3,   # + yearly retrain
}
for option, usd in cost.items():
    print(f"{option:22s} three-year cost USD {usd:,}")

# ---- checks against the hand-worked numbers ----
assert np.isclose(total("buy a product"), 3.05)
assert np.isclose(total("build on a model API"), 3.70)
assert np.isclose(total("fine-tune and host"), 3.25)
assert np.isclose(flip, 0.1125)
assert np.isclose(total("build on a model API", shifted(flip)),
                  total("fine-tune and host", shifted(flip)))
assert cost["buy a product"] == 364_000 and cost["fine-tune and host"] == 734_000

# ---- figure ----
x = np.linspace(0, 0.25, 50)
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
style = {"buy a product": ("#6b7280", "--"), "build on a model API": ("#4f46e5", "-"),
         "fine-tune and host": ("#b45309", "-")}
for option, (color, ls) in style.items():
    ax.plot(x, [total(option, shifted(v)) for v in x], color=color, ls=ls, lw=2,
            label=option)
ax.plot([flip, flip], [2.6, 3.95], color="#1f2937", ls=":", lw=1.5)
ax.text(flip + 0.004, 2.72, f"decision flips at {flip:.4f}", color="#1f2937")
ax.set_xlabel("weight moved from 'time to launch' to 'data control'")
ax.set_ylabel("weighted score")
ax.set_ylim(2.6, 4.35)
ax.grid(axis="y")
ax.legend(frameon=False, loc="upper left", ncol=3, fontsize=10)
fig.savefig(ASSETS / "ch58-weight-sensitivity.svg", bbox_inches="tight",
            metadata={"Date": None})
