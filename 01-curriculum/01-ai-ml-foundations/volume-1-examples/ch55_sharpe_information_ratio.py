"""Chapter 55: Sharpe ratio, information ratio, and two ways they are gamed."""
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


def ratio(returns, yardstick, periods_per_year=12):
    """Annualized mean/sd of (returns - yardstick), and its t-statistic."""
    diff = np.asarray(returns, dtype=float) - yardstick
    per_period = diff.mean() / diff.std(ddof=1)
    return per_period * np.sqrt(periods_per_year), per_period * np.sqrt(len(diff))


# The hand example: six monthly returns, in percent.
fund = np.array([3.4, -1.6, 4.4, -2.6, 2.4, -0.6])
bench = np.array([2.9, -1.1, 3.4, -2.1, 1.9, -0.8])
print("Sharpe (annualized, t-stat):     %.3f, %.2f" % ratio(fund, 0.4))
print("information ratio (same pair):   %.3f, %.2f" % ratio(fund, bench))

# Gaming 1: report half of this month's move and half of last month's.
rng = np.random.default_rng(575)
honest = rng.normal(0.9, 3.0, 120)              # ten years, percent per month
smoothed = honest.copy()
smoothed[1:] = 0.5 * honest[1:] + 0.5 * honest[:-1]
d = smoothed - smoothed.mean()
lag1 = np.sum(d[:-1] * d[1:]) / np.sum(d * d)
print(f"\nhonest fund {ratio(honest, 0.3)[0]:.2f}   smoothed marks "
      f"{ratio(smoothed, 0.3)[0]:.2f}   (lag-1 autocorrelation {lag1:.2f})")

# Gaming 2: a steady premium, and a 25% loss about one month in fifty.
quiet = rng.normal(1.0, 0.3, 120)
crash = rng.random(120) < 0.02
seller = np.where(crash, -25.0, quiet)
first = int(np.flatnonzero(crash)[0])
print(f"tail-risk seller {ratio(seller[:first], 0.3)[0]:.2f} over the first "
      f"{first} months, {ratio(seller, 0.3)[0]:.2f} over all 120")

# ---- checks: hand results against computed ones ----
excess, active = fund - 0.4, fund - bench
assert np.allclose(excess, [3, -2, 4, -3, 2, -1]) and np.isclose(excess.mean(), 0.5)
assert np.isclose(excess.var(ddof=1), 8.3)
assert np.isclose(excess.mean() / excess.std(ddof=1), 0.1736, atol=1e-4)
assert np.isclose(ratio(fund, 0.4)[0], 0.601, atol=1e-3)
assert np.isclose(active.mean(), 0.2) and np.isclose(active.std(ddof=1), 0.6)
assert np.isclose(ratio(fund, bench)[0], 1.155, atol=1e-3)
assert np.allclose(np.round(100 * np.cumprod(1 + fund / 100), 2),
                   [103.4, 101.75, 106.22, 103.46, 105.94, 105.31])
assert ratio(smoothed, 0.3)[0] > 1.2 * ratio(honest, 0.3)[0] and lag1 > 0.3
assert ratio(seller[:first], 0.3)[0] > 5 > 1 > ratio(seller, 0.3)[0]

# ---- checks for the Check-yourself answers ----
assert np.isclose(1 / 4 * np.sqrt(12), 0.866, atol=5e-4)
assert np.isclose(1.0 * np.sqrt(2), 1.41, atol=0.005)
assert np.isclose((1.0 / np.sqrt(12)) * np.sqrt(24), np.sqrt(2))   # same t
assert np.isclose((2 / 1.0) ** 2, 4)                # years needed to reach t = 2

# ---- Figure 55.1 ----
fig, ax = plt.subplots(figsize=(7.0, 3.2), dpi=100)
x = np.arange(121)


def grow(r):
    return np.concatenate([[100], 100 * np.cumprod(1 + r / 100)])


ax.plot(x, grow(honest), color="#4f46e5", lw=1.6, label="honest, bumpy fund")
ax.plot(x, grow(seller), color="#b91c1c", lw=1.6, label="tail-risk seller")
ax.axvline(first, color="#6b7280", lw=1, ls="--")
ax.text(first - 2, 285, f"Sharpe {ratio(seller[:first], 0.3)[0]:.1f}\nup to here",
        ha="right", va="top", color="#b91c1c", fontsize=11)
ax.set_xlabel("month")
ax.set_ylabel("value of USD 100")
ax.grid(True, axis="y")
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(ASSETS / "ch55-sharpe-gamed.svg", bbox_inches="tight")
