"""Chapter 16. Random variables: PMF, PDF, CDF and quantiles.

Run: python ch16_random_variables.py
"""
from pathlib import Path

import numpy as np

# [listing]
# Discrete: X = disputes one PayFlow merchant receives in a month
values = np.arange(5)
pmf = np.array([0.50, 0.25, 0.15, 0.07, 0.03])
cdf = np.cumsum(pmf)
print("x   :", values)
print("PMF :", pmf)
print("CDF :", cdf.round(2))
print(f"P(X >= 2) = {1 - cdf[1]:.2f}")

# Continuous: A = payment amount in USD, exponential with mean 80
mean = 80.0


def cdf_amount(a):
    return 1 - np.exp(-a / mean)


print(f"P(A > 200)      = {1 - cdf_amount(200):.4f}")
print(f"P(40 < A < 120) = {cdf_amount(120) - cdf_amount(40):.4f}")
print(f"median = {mean * np.log(2):.2f}   p95 = {-mean * np.log(0.05):.2f}")

rng = np.random.default_rng(16)
amounts = rng.exponential(mean, size=200_000)
print(f"simulated: P(A > 200) = {(amounts > 200).mean():.4f}, "
      f"median = {np.median(amounts):.2f}, p95 = {np.quantile(amounts, 0.95):.2f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(pmf.sum(), 1.0)
assert np.allclose(cdf, [0.50, 0.75, 0.90, 0.97, 1.00])
assert np.isclose(1 - cdf[1], 0.25)
assert np.isclose(1 - cdf_amount(200), np.exp(-2.5))
assert np.isclose(np.exp(-2.5), 0.0821, atol=5e-5)
assert np.isclose(cdf_amount(120) - cdf_amount(40), 0.6065 - 0.2231, atol=1e-4)
assert np.isclose(mean * np.log(2), 55.45, atol=5e-3)
assert abs((amounts > 200).mean() - np.exp(-2.5)) < 0.003
# the density is the derivative of the CDF (finite-difference check at a = 50)
h = 1e-4
density_50 = (cdf_amount(50 + h) - cdf_amount(50 - h)) / (2 * h)
assert np.isclose(density_50, np.exp(-50 / mean) / mean)
# a density can exceed 1: amounts in thousands of USD have mean 0.08, density 12.5 at 0
assert np.isclose(1 / 0.08, 12.5)
# Q16.1: P(X <= 1) and P(1 <= X <= 3) ; Q16.2: P(A <= 80) = 1 - 1/e
assert np.isclose(cdf[1], 0.75) and np.isclose(pmf[1:4].sum(), 0.47)
assert np.isclose(cdf_amount(80), 1 - np.exp(-1))
assert np.isclose(cdf_amount(80), 0.632, atol=5e-4)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    tint, bad = "#eef2ff", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch16", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0), dpi=100)

    ax1.bar(values, pmf, width=0.6, color=tint, edgecolor=accent, label="PMF")
    ax1.step(np.r_[values, 5], np.r_[cdf, 1.0], where="post", color=ink, label="CDF")
    for x, p in zip(values, pmf):
        ax1.text(x, p + 0.02, f"{p:.2f}", ha="center", color=accent, fontsize=10)
    ax1.set_xlim(-0.5, 4.8)
    ax1.set_ylim(0, 1.08)
    ax1.set_xlabel("disputes in a month")
    ax1.set_ylabel("probability")
    ax1.set_title("Discrete: bars add up to 1", fontsize=11, color=ink, loc="left")
    ax1.legend(frameon=False, loc="center right", fontsize=10)

    a = np.linspace(0, 400, 400)
    pdf = np.exp(-a / mean) / mean
    ax2.plot(a, pdf, color=accent)
    ax2.fill_between(a, pdf, where=a >= 200, color=bad, alpha=0.25, linewidth=0)
    ax2.fill_between(a, pdf, where=(a >= 40) & (a <= 120), color=accent, alpha=0.18,
                     linewidth=0)
    ax2.text(80, 0.0022, "0.383", ha="center", color=accent, fontsize=10)
    ax2.annotate("P(A > 200) = 0.082", xy=(240, 0.0004), xytext=(215, 0.0045),
                 color=bad, fontsize=10,
                 arrowprops={"arrowstyle": "-", "color": bad, "linewidth": 0.8})
    ax2.set_xlim(0, 400)
    ax2.set_ylim(0, 0.0135)
    ax2.set_xlabel("payment amount (USD)")
    ax2.set_ylabel("density")
    ax2.set_title("Continuous: area is probability", fontsize=11, color=ink, loc="left")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch16-pmf-pdf.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
