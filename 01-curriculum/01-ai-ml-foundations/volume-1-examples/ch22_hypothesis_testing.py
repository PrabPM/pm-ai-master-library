"""Chapter 22. Two-proportion z-test: p-value, interval, effect size and power.

Run: python ch22_hypothesis_testing.py
"""
from pathlib import Path

import numpy as np
from scipy.stats import norm

# [listing]
n_c, x_c = 4000, 480        # control
n_t, x_t = 4000, 560        # treatment
p_c, p_t = x_c / n_c, x_t / n_t
diff = p_t - p_c

pooled = (x_c + x_t) / (n_c + n_t)
se_null = np.sqrt(pooled * (1 - pooled) * (1 / n_c + 1 / n_t))
z = diff / se_null
p_value = 2 * norm.sf(abs(z))
print(f"difference {diff:.4f}, z = {z:.3f}, two-sided p = {p_value:.4f}")

se = np.sqrt(p_c * (1 - p_c) / n_c + p_t * (1 - p_t) / n_t)
print(f"95% interval for the lift: {diff - 1.96 * se:.4f} to {diff + 1.96 * se:.4f}")
h = 2 * np.arcsin(np.sqrt(p_t)) - 2 * np.arcsin(np.sqrt(p_c))
print(f"Cohen's h = {h:.4f}")


def n_per_arm(p1, p2, alpha=0.05, power=0.80):
    z_a, z_b = norm.ppf(1 - alpha / 2), norm.ppf(power)
    return (z_a + z_b) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2


need = int(np.ceil(n_per_arm(0.12, 0.13)))
print(f"to detect 12% -> 13% at 80% power: {need:,} per arm")
se_1pt = np.sqrt(0.12 * 0.88 / 4000 + 0.13 * 0.87 / 4000)
print(f"power with 4,000 per arm: {norm.cdf(0.01 / se_1pt - 1.96):.3f}")
# [/listing]

rng = np.random.default_rng(22)       # check the power claim by simulation
c = rng.binomial(need, 0.12, 20_000)
t = rng.binomial(need, 0.13, 20_000)
pp = (c + t) / (2 * need)
zs = (t - c) / need / np.sqrt(pp * (1 - pp) * 2 / need)
print(f"simulated power at {need:,}: {np.mean(np.abs(zs) > 1.96):.3f}")

# Hand-worked values from the chapter
assert np.isclose(p_c, 0.12) and np.isclose(p_t, 0.14) and np.isclose(diff, 0.02)
assert np.isclose(pooled, 0.13)
assert np.isclose(se_null, 0.00752, atol=5e-6)
assert np.isclose(z, 2.660, atol=5e-4)
assert np.isclose(p_value, 0.0078, atol=5e-5)
assert np.isclose(se, 0.00752, atol=5e-6)
assert np.isclose(diff - 1.96 * se, 0.0053, atol=5e-5)
assert np.isclose(diff + 1.96 * se, 0.0347, atol=5e-5)
# sample size by hand: 7.849 * (0.1056 + 0.1131) / 0.0001
assert np.isclose((1.96 + 0.8416) ** 2, 7.849, atol=5e-4)
assert abs(need - 7.849 * (0.1056 + 0.1131) / 0.0001) < 5
assert abs(np.mean(np.abs(zs) > 1.96) - 0.80) < 0.015
# standard error of a 1-point lift (12% vs 13%) with 4,000 per arm
assert np.isclose(se_1pt, 0.00739, atol=5e-6)
assert np.isclose(norm.cdf(0.01 / se_1pt - 1.96), 0.27, atol=5e-3)
# A/A check: with no true difference about 5% of tests come out "significant"
a1, a2 = rng.binomial(4000, 0.12, 40_000), rng.binomial(4000, 0.12, 40_000)
pa = (a1 + a2) / 8000
za = (a1 - a2) / 4000 / np.sqrt(pa * (1 - pa) * 2 / 4000)
assert abs(np.mean(np.abs(za) > 1.96) - 0.05) < 0.005
# "significant" is not "important": 0.05 points is significant at 10 million per arm
se_big = np.sqrt(0.12 * 0.88 / 1e7 + 0.1205 * 0.8795 / 1e7)
assert 0.0005 / se_big > 1.96
# Q22.1: the same rates with 1,000 per arm are not significant
se_q = np.sqrt(0.13 * 0.87 * 2 / 1000)
assert np.isclose(0.02 / se_q, 1.33, atol=5e-3)
assert np.isclose(2 * norm.sf(0.02 / se_q), 0.18, atol=5e-3)
# Q22.2: halving the detectable lift needs about four times the sample
assert 3.8 < n_per_arm(0.12, 0.125) / n_per_arm(0.12, 0.13) < 4.1
assert abs(n_per_arm(0.12, 0.125) - 67_493) < 5


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    bad, good = "#b91c1c", "#15803d"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch22", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    shift = 2.8                      # true effect in standard-error units (80% power)
    zz = np.linspace(-4, 7, 600)
    null, alt = norm.pdf(zz), norm.pdf(zz, shift)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.0, 3.5), dpi=100, sharex=True)
    ax1.plot(zz, null, color=ink)
    ax1.fill_between(zz, null, where=np.abs(zz) >= 1.96, color=bad, alpha=0.4,
                     linewidth=0)
    ax1.set_title("If there is no effect", fontsize=11, color=ink, loc="left")
    ax1.annotate("false positive (Type I error): 2.5% per tail",
                 xy=(2.25, 0.02), xytext=(2.5, 0.27), color=bad, fontsize=10,
                 arrowprops={"arrowstyle": "-", "color": bad, "linewidth": 0.8})
    ax2.plot(zz, alt, color=accent)
    ax2.fill_between(zz, alt, where=zz <= 1.96, color=good, alpha=0.35, linewidth=0)
    ax2.fill_between(zz, alt, where=zz >= 1.96, color=accent, alpha=0.15, linewidth=0)
    ax2.set_title("If the true effect is 2.8 standard errors", fontsize=11, color=ink,
                  loc="left")
    ax2.annotate("missed (Type II error): 20%", xy=(1.45, 0.06), xytext=(-1.75, 0.30),
                 color=good, fontsize=10,
                 arrowprops={"arrowstyle": "-", "color": good, "linewidth": 0.8})
    ax2.text(2.15, 0.07, "detected: 80%", color=accent, fontsize=10)
    for ax in (ax1, ax2):
        ax.axvline(1.96, color=muted, linewidth=1, linestyle=":")
        ax.axvline(-1.96, color=muted, linewidth=1, linestyle=":")
        ax.set_ylim(0, 0.44)
        ax.set_xlim(-4, 7)
        ax.set_yticks([])
    ax2.set_xticks([-4, -1.96, 0, 1.96, 4, 6])
    ax2.set_xticklabels(["-4", "-1.96", "0", "1.96", "4", "6"])
    ax2.set_xlabel("test statistic z (reject the null beyond the dotted lines)")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch22-errors-power.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
