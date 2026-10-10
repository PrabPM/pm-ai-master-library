"""Chapter 54: rolling, exponentially weighted and GARCH volatility."""
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


def acf1(x):
    """Sample autocorrelation at lag 1."""
    d = x - x.mean()
    return float(np.sum(d[:-1] * d[1:]) / np.sum(d * d))


# The hand example: five daily log returns, in percent.
r5 = np.array([1.0, -1.0, 2.0, -2.0, 0.0])
var5 = r5.var(ddof=1)
lam = 0.94
v1 = lam * var5 + (1 - lam) * (-4.0) ** 2      # after a -4% day
v2 = lam * v1 + (1 - lam) * 0.5 ** 2           # after a calm +0.5% day
print(f"daily vol {np.sqrt(var5):.3f}%  annualized {np.sqrt(var5 * 252):.1f}%")
print(f"EWMA vol after the shock {np.sqrt(v1):.3f}%, a day later {np.sqrt(v2):.3f}%")

# Simulate 750 days of GARCH(1,1) returns, in percent per day.
omega, alpha, beta = 0.05, 0.10, 0.85
rng = np.random.default_rng(954)
n = 750
sig2 = np.full(n, omega / (1 - alpha - beta))  # start at the long-run variance
ewma2 = sig2.copy()
r = np.zeros(n)
for t in range(n):
    if t > 0:
        sig2[t] = omega + alpha * r[t - 1] ** 2 + beta * sig2[t - 1]
        ewma2[t] = lam * ewma2[t - 1] + (1 - lam) * r[t - 1] ** 2
    r[t] = np.sqrt(sig2[t]) * rng.normal()
rolling = np.array([r[t - 20:t].std(ddof=1) for t in range(20, n)])

true_sd = np.sqrt(sig2)
print(f"\nlong-run daily vol {true_sd[0]:.2f}%   sample {r.std(ddof=1):.3f}%   "
      f"annualized {r.std(ddof=1) * np.sqrt(252):.1f}%")
print(f"true daily vol ranged from {true_sd.min():.2f}% to {true_sd.max():.2f}%")
print(f"lag-1 autocorrelation: returns {acf1(r):+.3f}, squared {acf1(r ** 2):+.3f}")
print(f"mean abs error vs true vol: rolling-20 "
      f"{np.abs(rolling - true_sd[20:]).mean():.3f}, "
      f"EWMA {np.abs(np.sqrt(ewma2) - true_sd)[20:].mean():.3f}")

# ---- checks: hand results against computed ones ----
assert np.isclose(var5, 2.5) and np.isclose(np.sqrt(var5), 1.5811, atol=1e-4)
assert np.isclose(np.sqrt(var5 * 252), 25.10, atol=0.01)
assert np.isclose(v1, 3.31) and np.isclose(v2, 3.1264)
assert np.isclose(np.sqrt(v1), 1.819, atol=1e-3)
assert np.isclose(np.sqrt(v2), 1.768, atol=1e-3)
assert np.isclose(omega / (1 - alpha - beta), 1.0)
assert abs(acf1(r)) < 0.08 < acf1(r ** 2)       # direction no, size yes
assert abs(r.std(ddof=1) - 1.0) < 0.15
assert np.isclose(np.sqrt(252), 15.87, atol=0.01)

# ---- checks for the Check-yourself answers ----
assert np.isclose(2 * np.sqrt(252), 31.7, atol=0.05)
assert np.isclose(0.9 * 4 + 0.1 * 3 ** 2, 4.5)
assert np.isclose(np.sqrt(4.5), 2.12, atol=0.005)

# ---- Figure 54.1 ----
fig, axes = plt.subplots(2, 1, figsize=(7.2, 3.6), dpi=100, sharex=True,
                         height_ratios=[1, 1.25])
axes[0].plot(r, color="#6b7280", lw=0.8)
axes[0].set_ylabel("return (%)")
axes[0].grid(True, axis="y")
axes[1].plot(true_sd, color="#1f2937", lw=1.4, label="true")
axes[1].plot(np.arange(20, n), rolling, color="#b45309", lw=1.1,
             label="rolling 20-day")
axes[1].plot(np.sqrt(ewma2), color="#4f46e5", lw=1.1, label="EWMA 0.94")
axes[1].set_ylabel("daily vol (%)")
axes[1].set_xlabel("trading day")
axes[1].grid(True, axis="y")
axes[1].set_ylim(0.3, 2.75)
axes[1].legend(frameon=False, ncol=3, loc="upper left")
fig.tight_layout()
fig.savefig(ASSETS / "ch54-volatility-clusters.svg", bbox_inches="tight")
