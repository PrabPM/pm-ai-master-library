"""Chapter 53: simple returns compound, log returns add."""
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

# The hand example: a made-up share price over three days.
price = np.array([100.0, 110.0, 99.0, 103.95])
simple = price[1:] / price[:-1] - 1
log_r = np.log(price[1:] / price[:-1])
print("simple:", np.round(simple, 4), " sum", round(float(simple.sum()), 4))
print("log:   ", np.round(log_r, 5), " sum", round(float(log_r.sum()), 5))
print(f"true total {price[-1] / price[0] - 1:.4f}   "
      f"compounded simple {np.prod(1 + simple) - 1:.4f}   "
      f"exp(log sum) - 1 {np.exp(log_r.sum()) - 1:.4f}")

# The same rule on PayFlow's monthly processed volume, USD million.
volume = np.array([80.0, 92.0, 101.2, 116.38])
growth = volume[1:] / volume[:-1] - 1
quarter = volume[-1] / volume[0] - 1
average = np.exp(np.log(volume[-1] / volume[0]) / 3) - 1
print("\nmonthly growth:", np.round(growth, 4))
print(f"added up {growth.sum():.4f}   actual quarter {quarter:.4f}   "
      f"average month {average:.4f}")

# Across assets it is the simple returns that add.
w = np.array([0.6, 0.4])                    # portfolio weights
r_assets = np.array([0.10, -0.05])          # one-period simple returns
port = float(w @ r_assets)
print(f"\nportfolio: simple {port:.4f}, its log {np.log(1 + port):.5f}, "
      f"weighted logs {float(w @ np.log(1 + r_assets)):.5f}")

# ---- checks: hand results against computed ones ----
total = price[-1] / price[0] - 1
assert np.allclose(simple, [0.10, -0.10, 0.05]) and np.isclose(simple.sum(), 0.05)
assert np.isclose(np.prod(1 + simple) - 1, total) and np.isclose(total, 0.0395)
assert np.allclose(np.round(log_r, 5), [0.09531, -0.10536, 0.04879])
assert np.isclose(log_r.sum(), np.log(price[-1] / price[0]))
assert np.isclose(np.exp(log_r.sum()) - 1, total)
assert np.allclose(growth, [0.15, 0.10, 0.15])
assert np.isclose(quarter, 1.15 * 1.10 * 1.15 - 1)
assert np.isclose((1 + average) ** 3 - 1, quarter)
assert np.isclose(port, 0.04)
assert not np.isclose(np.log(1 + port), float(w @ np.log(1 + r_assets)))
# The second-order link: log(1 + r) is close to r - r^2 / 2 for small r.
assert abs(np.log(1.10) - (0.10 - 0.10 ** 2 / 2)) < 4e-4
assert np.isclose(np.log(1.5), 0.4055, atol=1e-4)
assert np.isclose(np.log(0.5), -0.6931, atol=1e-4)

# ---- checks for the Check-yourself answers ----
assert np.isclose(0.8 * 1.2, 0.96)
assert np.isclose(np.log(0.8) + np.log(1.2), -0.0408, atol=1e-4)
assert np.isclose(np.exp(0.05 + 0.02 - 0.03) - 1, 0.0408, atol=1e-4)
assert np.isclose(0.6 * 10 - 0.4 * 5, 4.0)

# ---- Figure 53.1 ----
r = np.linspace(-0.6, 0.6, 241)
fig, ax = plt.subplots(figsize=(6.4, 3.3), dpi=100)
ax.plot(r * 100, r * 100, color="#6b7280", lw=1.2, ls="--",
        label="if the two were equal")
ax.plot(r * 100, np.log(1 + r) * 100, color="#4f46e5", lw=2,
        label="log return")
for x in (-50, 50):
    y = np.log(1 + x / 100) * 100
    ax.plot([x, x], [x, y], color="#b91c1c", lw=1.2)
    ax.plot([x], [y], "o", color="#b91c1c", ms=4)
ax.annotate("+50% simple is\n+40.5% log", xy=(50, 40.5), xytext=(34, 2),
            color="#1f2937", fontsize=11)
ax.annotate("−50% simple is\n−69.3% log", xy=(-50, -69.3),
            xytext=(-44, -88), color="#1f2937", fontsize=11)
ax.annotate("within about 0.5 points\nbetween −10% and +10%", xy=(0, 0),
            xytext=(8, -42), color="#1f2937", fontsize=11,
            arrowprops={"arrowstyle": "-", "color": "#6b7280"})
ax.set_xlabel("simple return (%)")
ax.set_ylabel("log return (%)")
ax.set_ylim(-95, 65)
ax.grid(True)
ax.legend(frameon=False, loc="upper left")
fig.tight_layout()
fig.savefig(ASSETS / "ch53-log-vs-simple.svg", bbox_inches="tight")
