"""Chapter 20. Maximum likelihood for a Bernoulli rate and a Poisson rate.

Run: python ch20_mle.py
"""
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import gammaln

# [listing]
# Bernoulli: 17 of 20 payments approved
k, n = 17, 20


def loglik_bernoulli(p):
    return k * np.log(p) + (n - k) * np.log(1 - p)


p_hat = k / n                                    # the formula derived by hand
best = minimize_scalar(lambda p: -loglik_bernoulli(p), bounds=(0.01, 0.99),
                       method="bounded")
h = 1e-5
slope = (loglik_bernoulli(p_hat + h) - loglik_bernoulli(p_hat - h)) / (2 * h)
print(f"Bernoulli: formula {p_hat:.4f}, numerical maximizer {best.x:.4f}, "
      f"slope at the formula {abs(slope):.6f}")
print(f"  log-likelihood at 0.75, 0.85, 0.95: {loglik_bernoulli(0.75):.3f}, "
      f"{loglik_bernoulli(0.85):.3f}, {loglik_bernoulli(0.95):.3f}")
print(f"  standard error {np.sqrt(p_hat * (1 - p_hat) / n):.4f}")

# Poisson: disputes per day over five days
counts = np.array([2, 4, 3, 6, 5])


def loglik_poisson(lam):
    return np.sum(counts * np.log(lam) - lam - gammaln(counts + 1))


lam_hat = counts.mean()
best = minimize_scalar(lambda lam: -loglik_poisson(lam), bounds=(0.1, 20),
                       method="bounded")
print(f"Poisson: formula {lam_hat:.4f}, numerical maximizer {best.x:.4f}, "
      f"standard error {np.sqrt(lam_hat / len(counts)):.4f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(p_hat, 0.85)
assert abs(minimize_scalar(lambda p: -loglik_bernoulli(p), bounds=(0.01, 0.99),
                           method="bounded").x - 0.85) < 1e-4
assert abs(slope) < 1e-5
# derivative of the log-likelihood: k/p - (n-k)/(1-p), checked by finite differences
for p0 in (0.5, 0.7, 0.9):
    fd = (loglik_bernoulli(p0 + h) - loglik_bernoulli(p0 - h)) / (2 * h)
    assert np.isclose(fd, k / p0 - (n - k) / (1 - p0), atol=1e-5)
assert np.isclose(np.sqrt(0.85 * 0.15 / 20), 0.0798, atol=5e-5)
assert loglik_bernoulli(0.85) > max(loglik_bernoulli(0.75), loglik_bernoulli(0.95))
assert np.isclose(lam_hat, 20 / 5) and abs(best.x - 4.0) < 1e-4
# Poisson score: sum(k)/lam - n, checked by finite differences
for l0 in (2.0, 4.0, 7.0):
    fd = (loglik_poisson(l0 + h) - loglik_poisson(l0 - h)) / (2 * h)
    assert np.isclose(fd, counts.sum() / l0 - len(counts), atol=1e-5)
assert np.isclose(np.sqrt(4 / 5), 0.8944, atol=5e-5)
# curvature gives the standard error: -1 / l''(p_hat) = p(1-p)/n
curv = (loglik_bernoulli(p_hat + 1e-4) - 2 * loglik_bernoulli(p_hat)
        + loglik_bernoulli(p_hat - 1e-4)) / 1e-8
assert np.isclose(-1 / curv, p_hat * (1 - p_hat) / n, rtol=1e-3)
# the normal-variance MLE divides by n (biased), not n - 1
x = np.array([2.0, 4.0, 3.0, 6.0, 5.0])
assert np.isclose(x.var(), 2.0) and np.isclose(x.var(ddof=1), 2.5)
# 1.96 standard errors is about 16 points either way
assert np.isclose(1.96 * np.sqrt(0.85 * 0.15 / 20), 0.156, atol=5e-4)
# Q20.1: 170 of 200 -> same estimate, SE smaller by sqrt(10)
assert np.isclose(np.sqrt(0.85 * 0.15 / 200), 0.0252, atol=5e-5)
# Q20.2: 95% interval for the dispute rate
assert np.isclose(4 - 1.96 * 0.8944, 2.25, atol=5e-3)
assert np.isclose(4 + 1.96 * 0.8944, 5.75, atol=5e-3)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent, bad = "#1f2937", "#6b7280", "#4f46e5", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch20", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    p = np.linspace(0.5, 0.995, 400)
    small = 17 * np.log(p) + 3 * np.log(1 - p)
    large = 170 * np.log(p) + 30 * np.log(1 - p)
    fig, ax = plt.subplots(figsize=(6.4, 3.1), dpi=100)
    ax.plot(p, small - small.max(), color=accent, label="17 of 20 approved")
    ax.plot(p, large - large.max(), color=ink, linestyle="--",
            label="170 of 200 approved")
    ax.axvline(0.85, color=bad, linewidth=1)
    ax.text(0.845, -9.2, "maximum at 0.85", color=bad, fontsize=10, ha="right")
    ax.set_ylim(-10, 0.6)
    ax.set_xlim(0.5, 1.0)
    ax.set_xlabel("candidate approval rate p")
    ax.set_ylabel("log-likelihood minus its maximum")
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    ax.grid(True, axis="y", linewidth=0.6)
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch20-loglik.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
