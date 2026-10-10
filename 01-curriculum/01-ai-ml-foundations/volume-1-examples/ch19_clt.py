"""Chapter 19. The central limit theorem by simulation, light and heavy tails.

Run: python ch19_clt.py
"""
from pathlib import Path

import numpy as np

# [listing]
rng = np.random.default_rng(19)
reps = 10_000                       # simulated samples per setting


def expo(size):                     # payment amounts, mean 80, light tail
    return rng.exponential(80.0, size)


def pareto(size):                   # minimum 10, tail exponent 2.2: heavy tail
    return 10 * (1 - rng.random(size)) ** (-1 / 2.2)


def coverage(draw, true_mean, n):
    """Share of intervals mean +- 1.96 sd / sqrt(n) that contain the true mean."""
    x = draw((reps, n))
    m, s = x.mean(axis=1), x.std(axis=1, ddof=1)
    return np.mean(np.abs(m - true_mean) <= 1.96 * s / np.sqrt(n))


means = expo((reps, 100)).mean(axis=1)
print(f"exponential, n=100: sd of sample means {means.std():.2f}, "
      f"theory 80/sqrt(100) = {80 / np.sqrt(100):.2f}")

pareto_mean = 2.2 * 10 / (2.2 - 1)
print("coverage of the 95% interval")
print("    n   exponential   heavy tail")
for n in (10, 30, 200, 2000):
    print(f"{n:5d}   {coverage(expo, 80.0, n):11.3f}   "
          f"{coverage(pareto, pareto_mean, n):10.3f}")
# [/listing]

# Hand-worked values from the chapter
assert abs(means.std() - 8.0) < 0.2 and abs(means.mean() - 80.0) < 0.3
assert np.isclose(np.sqrt(0.9 * 0.1 / 400), 0.015)             # SE of an approval rate
assert np.isclose(1.96 * 0.015, 0.0294)
assert np.isclose(np.sqrt(0.9 * 0.1 / 1600), 0.0075)           # 4x the data halves it
check = np.random.default_rng(190)
big = 10 * (1 - check.random(2_000_000)) ** (-1 / 2.2)
assert abs(big.mean() - pareto_mean) < 0.3                     # mean 18.33
# Q19.1: n needed for a standard error of 0.005 at p = 0.9
assert np.isclose(0.9 * 0.1 / 0.005**2, 3600)
# Q19.2: sd of the mean of 400 amounts with sd 80
assert np.isclose(80 / np.sqrt(400), 4.0) and np.isclose(1.96 * 4.0, 7.84)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    tint, bad = "#eef2ff", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch19", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    g = np.random.default_rng(191)
    n = 30
    sd_pareto = np.sqrt(100 * 2.2 / ((2.2 - 1) ** 2 * (2.2 - 2)))
    ze = (g.exponential(80.0, (40_000, n)).mean(axis=1) - 80.0) / (80.0 / np.sqrt(n))
    zp = ((10 * (1 - g.random((40_000, n))) ** (-1 / 2.2)).mean(axis=1) - pareto_mean)
    zp = zp / (sd_pareto / np.sqrt(n))
    grid = np.linspace(-4, 4, 200)
    bell = np.exp(-grid**2 / 2) / np.sqrt(2 * np.pi)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), dpi=100, sharey=True)
    for ax, z, title in ((axes[0], ze, "Exponential amounts, n = 30"),
                         (axes[1], zp, "Heavy-tailed amounts, n = 30")):
        ax.hist(z, bins=np.linspace(-4, 4, 49), density=True, color=tint,
                edgecolor=accent, linewidth=0.5)
        ax.plot(grid, bell, color=bad, label="normal curve")
        ax.set_xlim(-4, 4)
        ax.set_ylim(0, 1.0)
        ax.set_title(title, fontsize=11, color=ink, loc="left")
        ax.set_xlabel("standardized sample mean")
    axes[0].set_ylabel("density")
    axes[0].legend(frameon=False, fontsize=10, loc="upper right")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch19-clt.svg", bbox_inches="tight", metadata={"Date": None})


figure()
