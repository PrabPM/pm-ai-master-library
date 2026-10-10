"""Chapter 21. MAP estimation: the Beta-Binomial model and how the prior fades.

Run: python ch21_map.py
"""
from pathlib import Path

import numpy as np
from scipy import stats

# [listing]
a, b = 3, 297        # Beta prior: as if 3 disputes seen in 300 payments


def estimates(k, n):
    mle = k / n
    map_ = (k + a - 1) / (n + a + b - 2)
    posterior_mean = (k + a) / (n + a + b)
    return mle, map_, posterior_mean


print("new merchant, 1 dispute in 5 payments")
print("  MLE %.4f   MAP %.4f   posterior mean %.4f" % estimates(1, 5))

# Check the formula: maximize the log posterior on a grid
grid = np.linspace(0.0001, 0.5, 500_000)
log_posterior = stats.binom.logpmf(1, 5, grid) + stats.beta.logpdf(grid, a, b)
print(f"  grid maximizer of the posterior {grid[log_posterior.argmax()]:.4f}")

print("the same 4% dispute rate with more data")
for n in (50, 500, 5000, 50_000):
    k = int(0.04 * n)
    mle, map_, _ = estimates(k, n)
    print(f"  n={n:6d}  k={k:5d}   MLE {mle:.4f}   MAP {map_:.4f}")
# [/listing]

# Hand-worked values from the chapter
mle, map_, post_mean = estimates(1, 5)
assert np.isclose(mle, 0.20)
assert np.isclose(map_, 3 / 303) and np.isclose(map_, 0.0099, atol=5e-5)
assert np.isclose(post_mean, 4 / 305) and np.isclose(post_mean, 0.0131, atol=5e-5)
assert abs(grid[log_posterior.argmax()] - 3 / 303) < 1e-5
# the posterior is Beta(a + k, b + n - k): check mode and mean against scipy
post = stats.beta(a + 1, b + 4)
assert np.isclose(post.mean(), post_mean)
assert np.isclose(a / (a + b), 0.01) and np.isclose((a - 1) / (a + b - 2), 2 / 298)
assert np.isclose(estimates(2000, 50_000)[1], 2002 / 50_298)
# a flat prior Beta(1, 1) makes MAP equal to the MLE
assert np.isclose((1 + 1 - 1) / (5 + 1 + 1 - 2), 1 / 5)

# Gaussian prior on linear-regression weights gives ridge regression
rng = np.random.default_rng(21)
X = rng.normal(size=(40, 3))
y = X @ np.array([1.5, -2.0, 0.0]) + rng.normal(size=40)
lam = 4.0                       # noise variance / prior variance
ridge = np.linalg.solve(X.T @ X + lam * np.eye(3), X.T @ y)
ols = np.linalg.solve(X.T @ X, X.T @ y)


def neg_log_posterior(w):       # squared error + lam * squared weights (up to scale)
    return np.sum((y - X @ w) ** 2) + lam * np.sum(w**2)


eps = 1e-5
nlp = neg_log_posterior
grad = np.array([(nlp(ridge + eps * e) - nlp(ridge - eps * e)) / (2 * eps)
                 for e in np.eye(3)])
assert np.allclose(grad, 0, atol=1e-5)          # ridge solution maximizes the posterior
assert np.linalg.norm(ridge) < np.linalg.norm(ols)   # and is shrunk toward zero
# Q21.1: 0 disputes in 20 payments ; Q21.2: prior Beta(30, 2970) on the same data
assert np.isclose((0 + a - 1) / (20 + a + b - 2), 2 / 318)
assert np.isclose((1 + 30 - 1) / (5 + 3000 - 2), 30 / 3003)
assert np.isclose((200 + 30 - 1) / (5000 + 3000 - 2), 0.0286, atol=5e-5)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    bad, good = "#b91c1c", "#15803d"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch21", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    r = np.linspace(0.0002, 0.08, 800)
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9), dpi=100)
    for ax, (k, n) in zip(axes, ((2, 50), (200, 5000))):
        prior = stats.beta.pdf(r, a, b)
        post = stats.beta.pdf(r, a + k, b + n - k)
        ax.plot(r * 100, prior / prior.max(), color=muted, linestyle="--",
                label="prior")
        ax.plot(r * 100, post / post.max(), color=accent, label="posterior")
        ax.axvline(100 * k / n, color=bad, linewidth=1, label="MLE (4%)")
        ax.axvline(100 * (k + a - 1) / (n + a + b - 2), color=good, linewidth=1,
                   label="MAP")
        ax.set_title(f"{k} disputes in {n:,} payments", fontsize=11, color=ink,
                     loc="left")
        ax.set_xlabel("dispute rate (%)")
        ax.set_yticks([])
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 1.08)
    axes[0].set_ylabel("density (scaled)")
    axes[1].legend(frameon=False, fontsize=10, loc="upper right")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch21-prior-fades.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
