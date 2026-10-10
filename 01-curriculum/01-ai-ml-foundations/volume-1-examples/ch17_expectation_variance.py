"""Chapter 17. Expectation, variance, covariance and correlation.

Run: python ch17_expectation_variance.py
"""
from pathlib import Path

import numpy as np

# [listing]
amounts = np.array([20.0, 40.0, 60.0, 80.0, 300.0])    # five payments, USD
mean = amounts.mean()
var_pop = ((amounts - mean) ** 2).mean()                # divide by n
var_sample = amounts.var(ddof=1)                        # divide by n - 1
print(f"mean {mean:.0f}, median {np.median(amounts):.0f}")
print(f"population variance {var_pop:.0f}, sd {np.sqrt(var_pop):.1f}")
print(f"sample variance {var_sample:.0f}, sd {np.sqrt(var_sample):.1f}")

fee = 0.029 * amounts + 0.30      # PayFlow's fee is a linear function of the amount
print(f"mean fee {fee.mean():.2f}, sd of fee {fee.std():.3f}")

# Weekly payments (thousands) and disputes for five merchants
x = np.array([2.0, 4.0, 6.0, 8.0, 10.0])
y = np.array([1.0, 3.0, 4.0, 4.0, 8.0])
cov = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)
r = cov / (x.std(ddof=1) * y.std(ddof=1))
print(f"covariance {cov:.2f}, correlation {r:.3f}")

# Dependent but uncorrelated: risk is high for unusually small AND large payments
rng = np.random.default_rng(17)
u = rng.uniform(-1, 1, 5000)                 # how unusual the amount is
risk = u**2 + rng.normal(0, 0.05, 5000)
print(f"U-shape: corr(u, risk) = {np.corrcoef(u, risk)[0, 1]:+.3f}, "
      f"corr(u^2, risk) = {np.corrcoef(u**2, risk)[0, 1]:+.3f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(mean, 100) and np.isclose(np.median(amounts), 60)
assert np.isclose(var_pop, 52_000 / 5)
assert np.isclose(np.sqrt(var_pop), 102.0, atol=0.05)
assert np.isclose(var_sample, 52_000 / 4)
assert np.isclose(np.sqrt(var_sample), 114.0, atol=0.05)
# shortcut: Var(X) = E[X^2] - E[X]^2
assert np.isclose((amounts**2).mean() - mean**2, var_pop)
# linearity: E[aX + b] = aE[X] + b ; sd(aX + b) = |a| sd(X)
assert np.isclose(fee.mean(), 0.029 * 100 + 0.30) and np.isclose(fee.mean(), 3.20)
assert np.isclose(fee.std(), 0.029 * amounts.std())
assert np.isclose(cov, 30 / 4)
assert np.isclose(x.var(ddof=1), 10) and np.isclose(y.var(ddof=1), 6.5)
assert np.isclose(r, 7.5 / np.sqrt(65)) and np.isclose(r, 0.930, atol=5e-4)
assert np.isclose(np.cov(x, y)[0, 1], cov) and np.isclose(np.corrcoef(x, y)[0, 1], r)
assert abs(np.corrcoef(u, risk)[0, 1]) < 0.05 and np.corrcoef(u**2, risk)[0, 1] > 0.95
# Var(X + Y) = Var X + Var Y + 2 Cov(X, Y)
assert np.isclose((x + y).var(ddof=1), x.var(ddof=1) + y.var(ddof=1) + 2 * cov)
# Q17.1: without the USD 300 payment the mean is 50 ; Q17.2: units change, r does not
assert np.isclose(amounts[:4].mean(), 50) and np.isclose(np.median(amounts[:4]), 50)
assert np.isclose(np.corrcoef(1000 * x, y)[0, 1], r)
assert np.isclose(np.cov(1000 * x, y)[0, 1], 1000 * cov)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch17", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    g = np.random.default_rng(170)
    n = 250
    a = g.uniform(-1, 1, n)
    panels = [
        ("Linear", a, 0.9 * a + g.normal(0, 0.22, n)),
        ("No relationship", a, g.normal(0, 0.5, n)),
        ("U-shaped: dependent", a, 2 * a**2 - 0.7 + g.normal(0, 0.1, n)),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.6), dpi=100, sharey=True)
    for ax, (title, px, py) in zip(axes, panels):
        rr = np.corrcoef(px, py)[0, 1]
        ax.scatter(px, py, s=7, color=accent, alpha=0.55, linewidths=0)
        ax.set_title(f"{title}\nr = {rr:+.2f}", fontsize=11, color=ink, loc="left")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.6, 1.6)
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_xlabel("x")
    axes[0].set_ylabel("y")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch17-correlation.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
