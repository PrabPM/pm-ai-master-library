"""Chapter 23. Many variants and metrics: corrections, SRM and peeking.

Run: python ch23_many_tests.py
"""
from pathlib import Path

import numpy as np
from scipy import stats

# [listing]
p = np.array([0.002, 0.024, 0.028, 0.045, 0.600])    # sorted
m, q = len(p), 0.05
bh_line = q * np.arange(1, m + 1) / m
k = np.nonzero(p <= bh_line)[0].max() + 1            # largest passing rank
print(f"wins: uncorrected {(p <= q).sum()}, Bonferroni {(p <= q / m).sum()}, "
      f"Benjamini-Hochberg {k}")

# Sample-ratio mismatch: planned 50/50, observed 50,600 / 49,400
observed = np.array([50_600, 49_400])
expected = observed.sum() * np.array([0.5, 0.5])
chi2 = ((observed - expected) ** 2 / expected).sum()
print(f"SRM: chi-square {chi2:.1f}, p = {stats.chi2.sf(chi2, df=1):.5f}")

# Peeking: A/A tests, checked after every 500 users per arm
rng = np.random.default_rng(23)
sims, looks, step, rate = 4000, 20, 500, 0.12
a = rng.binomial(step, rate, (sims, looks)).cumsum(axis=1)
b = rng.binomial(step, rate, (sims, looks)).cumsum(axis=1)
n = step * np.arange(1, looks + 1)
pooled = (a + b) / (2 * n)
z = (a - b) / n / np.sqrt(pooled * (1 - pooled) * 2 / n)
hit = np.abs(z) > 1.96
print(f"false positives with 1, 5 and 20 looks: {hit[:, -1].mean():.3f}, "
      f"{hit[:, 3::4].any(axis=1).mean():.3f}, {hit.any(axis=1).mean():.3f}")
# [/listing]

# Hand-worked values from the chapter
bonferroni = p <= q / m
benjamini_hochberg = np.arange(m) < k
assert (p <= q).sum() == 4
assert bonferroni.tolist() == [True, False, False, False, False]
assert np.allclose(bh_line, [0.01, 0.02, 0.03, 0.04, 0.05])
assert (p <= bh_line).tolist() == [True, False, True, False, False]  # rank 2 fails
assert benjamini_hochberg.tolist() == [True, True, True, False, False]
assert np.array_equal(stats.false_discovery_control(p, method="bh") <= q,
                      benjamini_hochberg)
# Holm: step down, stop at the first failure
holm_line = q / (m - np.arange(m))
assert (p <= holm_line)[0] and not (p <= holm_line)[1]
assert np.isclose(1 - 0.95**5, 0.2262, atol=5e-5)        # any false positive in 5
assert np.isclose(1 - 0.95**20, 0.6415, atol=5e-5)       # and in 20
assert np.isclose(chi2, 2 * 600**2 / 50_000) and np.isclose(chi2, 14.4)
assert stats.chi2.sf(chi2, df=1) < 0.001
assert abs(hit[:, -1].mean() - 0.05) < 0.012
assert hit.any(axis=1).mean() > 0.20
# CUPED: variance left after adjusting with a covariate of correlation 0.7
assert np.isclose(1 - 0.7**2, 0.51)
# Q23.1: 12 comparisons ; Q23.2: a 5,050 / 4,950 split of 10,000 users is not an SRM
assert np.isclose(0.05 / 12, 0.0042, atol=5e-5)
assert np.isclose(1 - 0.95**12, 0.46, atol=5e-3)
chi2_q = 2 * 50**2 / 5000
assert np.isclose(chi2_q, 1.0) and np.isclose(stats.chi2.sf(1.0, 1), 0.32, atol=5e-3)
assert stats.chi2.sf(chi2, df=1) < 0.0005 < stats.chi2.sf(chi2_q, df=1)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent, bad = "#1f2937", "#6b7280", "#4f46e5", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch23", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.0), dpi=100)
    users = n / 1000
    for i in range(40):
        crossed = hit[i].any()
        ax1.plot(users, z[i], color=bad if crossed else muted,
                 linewidth=1.1 if crossed else 0.6, alpha=0.9 if crossed else 0.45)
    ax1.axhline(1.96, color=ink, linewidth=1, linestyle="--")
    ax1.axhline(-1.96, color=ink, linewidth=1, linestyle="--")
    ax1.set_ylim(-3.6, 3.6)
    ax1.set_xlabel("users per arm (thousands)")
    ax1.set_ylabel("z statistic")
    ax1.set_title("40 A/A tests: red ones crossed a line", fontsize=11, color=ink,
                  loc="left")
    ever = np.maximum.accumulate(hit, axis=1).mean(axis=0)
    ax2.plot(np.arange(1, looks + 1), ever, color=accent, marker="o", markersize=3)
    ax2.axhline(0.05, color=ink, linewidth=1, linestyle="--")
    ax2.text(20, 0.062, "promised 5%", color=ink, fontsize=10, ha="right")
    ax2.set_ylim(0, 0.30)
    ax2.set_xticks([1, 5, 10, 15, 20])
    ax2.set_xlabel("number of looks so far")
    ax2.set_ylabel("share declared significant")
    ax2.set_title("False positives grow with looks", fontsize=11, color=ink,
                  loc="left")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch23-peeking.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
