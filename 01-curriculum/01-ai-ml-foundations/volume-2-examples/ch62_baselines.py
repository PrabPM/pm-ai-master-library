"""Chapter 62: three baselines and a fitted model for PayFlow's daily payout
volume. Synthetic series; every number is illustrative.
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

rng = np.random.default_rng(62)
days = 182                                            # 26 weeks, starting on a Monday
t = np.arange(days)
weekday = np.array([0, 2, 3, 4, 9, -12, -16], dtype=float)[t % 7]
promo = (rng.random(days) < 0.08) * 6.0               # marketing pushes, known ahead
volume = 50 + 0.02 * t + weekday + promo + rng.normal(0, 1.8, days)   # USD million
test = np.arange(days - 28, days)                     # the last four weeks


def mae(forecast):
    return float(np.mean(np.abs(volume[test] - forecast)))


def features(idx):
    """Trend, weekday dummies, the promo flag, and the value a week earlier."""
    return np.column_stack([np.ones(len(idx)), idx, np.eye(7)[idx % 7][:, 1:],
                            promo[idx], volume[idx - 7]])


train = np.arange(7, days - 28)
coef, *_ = np.linalg.lstsq(features(train), volume[train], rcond=None)
forecasts = {
    "mean of history": np.full(28, volume[:days - 28].mean()),
    "yesterday": volume[test - 1],
    "same weekday last week": volume[test - 7],
    "fitted model": features(test) @ coef,
}
errors = {name: mae(f) for name, f in forecasts.items()}
hand = np.mean(np.abs(np.array([100, 120, 90, 110]) - np.array([95, 125, 100, 105])))
print("hand MAE:", hand)
for name, e in errors.items():
    print(f"{name:24s} MAE USD {e:.2f} million")
gap_total = errors["mean of history"] - errors["fitted model"]
share = (errors["mean of history"] - errors["same weekday last week"]) / gap_total
buffer_saving = 2 * (errors["same weekday last week"] - errors["fitted model"]) \
    * 1e6 * 0.08                                      # buffer = 2 x MAE, 8% a year
print(f"the weekly baseline captures {share:.0%} of the model's improvement")
RUN_COST = 150_000                                    # USD a year to own the model
print(f"model's extra value: USD {buffer_saving:,.0f} a year, against "
      f"USD {RUN_COST:,} a year to run it")

# ---- checks ----
assert hand == 6.25
assert errors["fitted model"] < errors["same weekday last week"] < errors["yesterday"]
assert 0.5 < share < 1.0

# ---- figure ----
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
x = np.arange(1, 29)
ax.plot(x, volume[test], color="#1f2937", lw=2, label="actual")
ax.plot(x, forecasts["same weekday last week"], color="#b45309", lw=1.5, ls="--",
        label="same weekday last week")
ax.plot(x, forecasts["fitted model"], color="#4f46e5", lw=1.5, label="fitted model")
ax.axhline(forecasts["mean of history"][0], color="#6b7280", ls=":", lw=1.5,
           label="mean of history")
ax.set_xlabel("day of the four-week test window")
ax.set_ylabel("payout volume, USD million")
ax.grid(axis="y")
ax.legend(frameon=False, ncol=4, loc="lower center", bbox_to_anchor=(0.5, 1.0),
          fontsize=10, columnspacing=1.2, handlelength=1.6)
fig.savefig(ASSETS / "ch62-baseline-forecasts.svg", bbox_inches="tight",
            metadata={"Date": None})
