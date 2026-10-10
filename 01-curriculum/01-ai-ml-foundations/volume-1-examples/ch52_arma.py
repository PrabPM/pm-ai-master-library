"""Chapter 52: ARMA models built from memory (AR) and shocks (MA)."""
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


def acf(x, h):
    """Sample autocorrelation at lag h."""
    d = np.asarray(x, dtype=float) - np.mean(x)
    return float(np.sum(d[:-h] * d[h:]) / np.sum(d * d))


def simulate_arma(phi, theta, n, rng):
    """x[t] = phi * x[t-1] + e[t] + theta * e[t-1], with e ~ N(0, 1)."""
    e = rng.normal(0, 1, n + 1)
    x = np.zeros(n + 1)
    for t in range(1, n + 1):
        x[t] = phi * x[t - 1] + e[t] + theta * e[t - 1]
    return x[1:]


# The hand example: new-merchant applications per day, fitted as an AR(1).
y = np.array([18, 19, 21, 23, 24, 23, 20, 19, 20, 23], dtype=float)
mu = y.mean()
phi = acf(y, 1)                              # Yule-Walker estimate
shock_sd = np.sqrt(np.var(y) * (1 - phi ** 2))
day11 = mu + phi * (y[-1] - mu)
print(f"mean {mu:.0f}  phi {phi:.2f}  shock sd {shock_sd:.3f}")
print(f"day 11 forecast {day11:.2f}, 95% range "
      f"{day11 - 1.96 * shock_sd:.1f} to {day11 + 1.96 * shock_sd:.1f}")

# Simulate pure memory and pure shock echo, then read their autocorrelations.
rng = np.random.default_rng(152)
ar = simulate_arma(phi=0.7, theta=0.0, n=2000, rng=rng)
ma = simulate_arma(phi=0.0, theta=0.7, n=2000, rng=rng)
print("\nlag        1      2      3      4")
print("AR(1) " + " ".join(f"{acf(ar, h):6.3f}" for h in range(1, 5)))
print("MA(1) " + " ".join(f"{acf(ma, h):6.3f}" for h in range(1, 5)))
print(f"noise band +/- {1.96 / np.sqrt(2000):.3f}")

# ---- checks: hand results against computed ones ----
d = y - mu
assert np.isclose(mu, 21) and np.isclose(np.mean(d * d), 4.0)
assert np.isclose(np.sum(d[:-1] * d[1:]) / len(y), 1.8)
assert np.isclose(phi, 0.45) and np.isclose(shock_sd ** 2, 3.19)
assert np.isclose(day11, 21.9)
assert np.isclose(mu + phi ** 2 * (y[-1] - mu), 21.405)
assert np.isclose(np.log(0.5) / np.log(phi), 0.868, atol=1e-3)   # half-life, days
assert np.isclose(np.log(0.5) / np.log(0.9), 6.58, atol=0.01)
# Theory: AR(1) autocorrelation is phi**h; MA(1) is theta/(1+theta^2), then 0.
band = 1.96 / np.sqrt(2000)
assert all(abs(acf(ar, h) - 0.7 ** h) < 0.05 for h in range(1, 5))
assert abs(acf(ma, 1) - 0.7 / (1 + 0.7 ** 2)) < 0.05
assert all(abs(acf(ma, h)) < band for h in (2, 3, 4))

# ---- checks for the Check-yourself answers ----
assert np.isclose(0.8 ** 3, 0.512) and np.isclose(0.8 ** 4, 0.41, atol=0.001)
assert np.isclose(50 + 0.6 * 10, 56) and np.isclose(50 + 0.6 ** 2 * 10, 53.6)

# ---- Figure 52.1 ----
lags = np.arange(0, 9)
fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), dpi=100, sharey=True)
panels = [(ar, "AR(1), memory 0.7: fades slowly", [0.7 ** h for h in lags]),
          (ma, "MA(1), shock echo 0.7: gone after lag 1",
           [1, 0.7 / 1.49] + [0] * 7)]
for ax, (s, title, theory) in zip(axes, panels):
    ax.axhspan(-band, band, color="#eef2ff")
    ax.bar(lags, [1.0] + [acf(s, h) for h in lags[1:]], width=0.55,
           color="#4f46e5", label="sample")
    ax.plot(lags, theory, "o", color="#1f2937", ms=4, label="theory")
    ax.axhline(0, color="#6b7280", lw=1)
    ax.set_title(title, fontsize=11, color="#1f2937")
    ax.set_xlabel("lag (days)")
    ax.set_xticks(lags)
axes[0].set_ylabel("autocorrelation")
axes[1].legend(frameon=False, loc="upper right")
fig.tight_layout()
fig.savefig(ASSETS / "ch52-acf-ar-ma.svg", bbox_inches="tight")
