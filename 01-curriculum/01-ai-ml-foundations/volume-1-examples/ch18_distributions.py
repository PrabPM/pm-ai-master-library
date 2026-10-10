"""Chapter 18. Binomial, Poisson, normal, Pareto and multinomial at PayFlow.

Run: python ch18_distributions.py
"""
from pathlib import Path

import numpy as np
from scipy import stats

# [listing]
rng = np.random.default_rng(18)

# Binomial: approvals among 400 payments, each approved with p = 0.9
n, p = 400, 0.9
mu, sd = n * p, np.sqrt(n * p * (1 - p))
print(f"binomial: mean {mu:.0f}, sd {sd:.1f}, P(X <= 345) = "
      f"{stats.binom.cdf(345, n, p):.4f} (normal approx "
      f"{stats.norm.cdf((345.5 - mu) / sd):.4f})")

# Poisson: support tickets, 3 per 10 minutes on average
lam = 3
print(f"poisson: P(0) = {stats.poisson.pmf(0, lam):.4f}, "
      f"P(X >= 8) = {stats.poisson.sf(7, lam):.4f}")

# Pareto: payment size with minimum USD 10 and tail exponent 1.5
xm, alpha = 10, 1.5
print(f"pareto: mean {alpha * xm / (alpha - 1):.0f}, "
      f"P(X > 1000) = {(xm / 1000) ** alpha:.4f}")
draws = xm * (1 - rng.random(100_000)) ** (-1 / alpha)     # inverse-CDF sampling
top = np.sort(draws)[-1000:].sum() / draws.sum()
print(f"  100,000 draws: mean {draws.mean():.1f}, largest {draws.max():,.0f}, "
      f"top 1% carry {top:.0%} of volume")

# Multinomial: 1,000 payments across card, wallet, bank transfer
probs = np.array([0.60, 0.25, 0.15])
one_draw = rng.multinomial(1000, probs)
print("multinomial: expected", 1000 * probs, "one draw", one_draw)
# [/listing]

# Hand-worked values from the chapter
within = [stats.norm.cdf(k) - stats.norm.cdf(-k) for k in (1, 2, 3)]
assert np.allclose(within, [0.6827, 0.9545, 0.9973], atol=5e-5)   # 68 / 95 / 99.7
assert np.isclose(mu, 360) and np.isclose(sd, 6.0)
assert np.isclose((345 - mu) / sd, -2.5)
assert np.isclose(stats.poisson.pmf(0, lam), np.exp(-3))
assert np.isclose(np.exp(-3), 0.0498, atol=5e-5)
assert np.isclose(stats.poisson.pmf(1, lam), 3 * np.exp(-3))
assert np.isclose(stats.poisson.pmf(2, lam), 4.5 * np.exp(-3))
assert np.isclose(alpha * xm / (alpha - 1), 30)
assert np.isclose((xm / 1000) ** alpha, 0.001)
assert np.isclose(xm * 2 ** (1 / alpha), 15.87, atol=5e-3)          # Pareto median
assert abs(np.median(draws) - xm * 2 ** (1 / alpha)) < 0.2
# theoretical share of the top 1% for a Pareto: 0.01 ** (1 - 1 / alpha)
assert np.isclose(0.01 ** (1 - 1 / alpha), 0.2154, atol=5e-5)
# multinomial: sd of the card count and the negative covariance between counts
assert np.isclose(np.sqrt(1000 * 0.60 * 0.40), 15.49, atol=5e-3)
sim = rng.multinomial(1000, probs, size=50_000)
assert abs(np.cov(sim[:, 0], sim[:, 1])[0, 1] - (-1000 * 0.60 * 0.25)) < 5
# Poisson is the limit of a binomial with many trials and a small probability
assert abs(stats.binom.pmf(2, 3000, 0.001) - stats.poisson.pmf(2, 3)) < 1e-3
# an alert at "8 or more tickets" fires about 1.7 times a day by chance (144 intervals)
assert np.isclose(144 * stats.poisson.sf(7, lam), 1.71, atol=5e-3)
# Q18.1: 10,000 payments at p = 0.9 -> mean 9,000, sd 30, so 8,940 is 2 sd low
assert np.isclose(np.sqrt(10_000 * 0.9 * 0.1), 30)
assert np.isclose((8940 - 9000) / 30, -2)
# Q18.2: tickets in an hour are Poisson with mean 18 and sd sqrt(18)
assert np.isclose(stats.poisson.std(18), 4.24, atol=5e-3)


def figures():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    tint, bad = "#eef2ff", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch18", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(7.2, 2.6), dpi=100)
    k = np.arange(335, 386)
    a1.bar(k, stats.binom.pmf(k, n, p), width=1.0, color=tint, edgecolor=accent,
           linewidth=0.6)
    a1.set_title("Binomial\nn = 400, p = 0.9", fontsize=11, color=ink, loc="left")
    a1.set_xlabel("approvals")
    a1.set_ylabel("probability")
    a1.set_xticks([340, 360, 380])
    k = np.arange(0, 12)
    a2.bar(k, stats.poisson.pmf(k, lam), width=0.7, color=tint, edgecolor=accent)
    a2.set_title("Poisson\nrate 3 per interval", fontsize=11, color=ink, loc="left")
    a2.set_xlabel("tickets")
    a2.set_xticks([0, 3, 6, 9])
    z = np.linspace(-4, 4, 300)
    a3.plot(z, stats.norm.pdf(z), color=accent)
    a3.fill_between(z, stats.norm.pdf(z), where=np.abs(z) <= 2, color=accent,
                    alpha=0.15, linewidth=0)
    a3.text(0, 0.15, "95%", ha="center", color=accent, fontsize=10)
    a3.set_title("Normal\nmean 0, sd 1", fontsize=11, color=ink, loc="left")
    a3.set_xlabel("standard deviations")
    a3.set_xticks([-2, 0, 2])
    a3.set_ylim(0, 0.44)
    fig.tight_layout()
    if out.is_dir():
        fig.savefig(out / "ch18-binomial-poisson-normal.svg", bbox_inches="tight",
                    metadata={"Date": None})

    fig, (b1, b2) = plt.subplots(1, 2, figsize=(7.2, 2.9), dpi=100)
    x = np.logspace(1, 4, 200)
    b1.loglog(x, (xm / x) ** alpha, color=bad, label="Pareto, exponent 1.5")
    b1.loglog(x, np.clip(stats.expon.sf(x - xm, scale=20), 1e-12, 1), color=accent,
              label="exponential, same mean")
    b1.set_ylim(1e-6, 2)
    b1.set_xlabel("payment size x (USD, log scale)")
    b1.set_ylabel("P(X > x)")
    b1.set_title("Heavy tail: a straight line on log-log axes", fontsize=11, color=ink,
                 loc="left")
    b1.legend(frameon=False, fontsize=10, loc="upper right")
    methods = ["card", "wallet", "bank transfer"]
    one = one_draw
    pos = np.arange(3)
    b2.bar(pos - 0.18, 1000 * probs, width=0.36, color=tint, edgecolor=accent,
           label="expected")
    b2.bar(pos + 0.18, one, width=0.36, color=accent, label="one draw of 1,000")
    b2.set_xticks(pos)
    b2.set_xticklabels(methods)
    b2.set_ylabel("payments")
    b2.set_title("Multinomial: counts that share a total", fontsize=11, color=ink,
                 loc="left")
    b2.legend(frameon=False, fontsize=10)
    fig.tight_layout()
    if out.is_dir():
        fig.savefig(out / "ch18-pareto-multinomial.svg", bbox_inches="tight",
                    metadata={"Date": None})


figures()
