"""Chapter 56: a seasonal baseline, Holt-Winters, a holiday, and how to score."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})


def mae(actual, forecast):
    return float(np.mean(np.abs(actual - forecast)))


def mape(actual, forecast):
    return float(100 * np.mean(np.abs(actual - forecast) / actual))


# ---- the hand example: one merchant's payments per day, Monday to Sunday ----
last_week = np.array([100, 104, 108, 110, 130, 90, 60], dtype=float)
this_week = np.array([103, 108, 110, 114, 180, 94, 50], dtype=float)
print(f"hand example: MAE {mae(this_week, last_week):.1f}  "
      f"MAPE {mape(this_week, last_week):.2f}%")

# ---- ten weeks of synthetic daily payments (thousands) ----
rng = np.random.default_rng(56)
m = 7
t = np.arange(70)
weekday = np.array([-6, -8, -4, 0, 6, 14, -2], dtype=float)   # Mon..Sun
y = 100 + 0.5 * t + weekday[t % m] + rng.normal(0, 2, t.size)
y[[25, 60]] += 40                       # two sale Fridays; the second lies ahead
train, test = y[:56], y[56:]


def holt_winters(y, m, alpha, beta, gamma, horizon):
    level = y[:m].mean()
    trend = (y[m:2 * m].mean() - y[:m].mean()) / m
    season = list(y[:m] - level)
    for i in range(m, len(y)):
        previous = level
        level = alpha * (y[i] - season[i - m]) + (1 - alpha) * (level + trend)
        trend = beta * (level - previous) + (1 - beta) * trend
        season.append(gamma * (y[i] - level) + (1 - gamma) * season[i - m])
    last = season[-m:]
    return np.array([level + (h + 1) * trend + last[h % m] for h in range(horizon)])


# Baseline: repeat the last observed week.
seasonal_naive = np.tile(train[-m:], 2)

# Measure the training sale day's lift, then replace it with a normal Friday.
clean = train.copy()
clean[25] = (train[18] + train[32]) / 2
lift = train[25] - clean[25]
hw = holt_winters(clean, m, alpha=0.3, beta=0.1, gamma=0.3, horizon=14)
hw_sale = hw.copy()
hw_sale[60 - 56] += lift                # the known sale date

print(f"\nsale-day lift measured in training: {lift:.1f}")
for name, f in [("seasonal naive", seasonal_naive), ("Holt-Winters", hw),
                ("Holt-Winters + sale", hw_sale)]:
    print(f"{name:20s} MAE {mae(test, f):5.2f}   MAPE {mape(test, f):5.2f}%")

# ---- from payments to revenue, and a price scenario ----
ticket = 50.0                            # average payment, USD
fee_now = 0.029 * ticket + 0.30
fee_cut = 0.027 * ticket + 0.30
revenue = hw_sale.sum() * 1000 * fee_now
print(f"\nfee per payment USD {fee_now:.2f}; two-week revenue forecast "
      f"USD {revenue / 1e6:.2f} million")
print(f"at 2.7% the fee is USD {fee_cut:.2f}; payments must grow "
      f"{100 * (fee_now / fee_cut - 1):.1f}% to pay for the cut")

# ---- checks: hand results against computed ones ----
assert np.allclose(this_week - last_week, [3, 4, 2, 4, 50, 4, -10])
assert np.isclose(mae(this_week, last_week), 77 / 7)
assert np.isclose(mape(this_week, last_week), 9.14, atol=0.005)
assert np.isclose(100 * 50 / 180, 27.8, atol=0.05) and np.isclose(100 * 10 / 50, 20)
assert mae(test, hw) < mae(test, seasonal_naive)
assert mae(test, hw_sale) < mae(test, hw)
assert 30 < lift < 50
assert np.isclose(fee_now, 1.75) and np.isclose(fee_cut, 1.65)
assert np.isclose(100 * (fee_now / fee_cut - 1), 6.06, atol=0.01)

# ---- checks for the Check-yourself answers ----
a, f = np.array([10.0, 200.0]), np.array([15.0, 190.0])
assert np.isclose(mae(a, f), 7.5) and np.isclose(mape(a, f), 27.5)
assert np.isclose(100 * 10 / 50, 20) and np.isclose(100 * 10 / 60, 16.7, atol=0.05)

# ---- Figure 56.1 ----
fig, ax = plt.subplots(figsize=(7.2, 3.3), dpi=100)
ax.plot(np.arange(35, 70), y[35:], color="#1f2937", lw=1.6, label="actual")
ax.plot(t[56:], seasonal_naive, color="#b45309", lw=1.3, ls="--",
        label="seasonal naive")
ax.plot(t[56:], hw_sale, color="#4f46e5", lw=1.6, label="Holt-Winters + sale")
ax.axvline(55.5, color="#6b7280", lw=1)
ax.text(55, y[35:].max() + 2, "known history ", ha="right", color="#6b7280")
ax.text(56, y[35:].max() + 2, " forecast", ha="left", color="#6b7280")
ax.annotate("sale day", xy=(60, y[60]), xytext=(62.5, y[60] - 6),
            color="#1f2937", arrowprops={"arrowstyle": "-", "color": "#6b7280"})
ax.set_xlabel("day")
ax.set_ylabel("payments (thousands)")
ax.set_ylim(top=y[35:].max() + 12)
ax.grid(True, axis="y")
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3)
fig.tight_layout()
fig.savefig(ASSETS / "ch56-forecast-holdout.svg", bbox_inches="tight")
