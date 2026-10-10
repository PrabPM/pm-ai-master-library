"""Chapter 34: stochastic and mini-batch gradient descent.

Part 1 uses the four merchants of chapter 33 to show that per-example gradients
average to the full gradient. Part 2 trains the same linear model on 2,000
synthetic merchants with full-batch, mini-batch and single-example updates.
Writes volume-1-assets/ch34-batch-sizes.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)

# ---- Part 1: four merchants, one weight ------------------------------------
x4 = np.array([1.0, 1.0, 1.0, 3.0])   # weekly payments, thousands
y4 = np.array([2.0, 3.0, 4.0, 9.0])   # disputes
for w in (0.0, 3.0):                  # 3.0 is the best weight
    per_example = x4 * (w * x4 - y4)
    print(f"per-example gradients at w = {w:.0f}: {per_example}  "
          f"mean: {per_example.mean():.1f}")
at_start = x4 * (0.0 * x4 - y4)
assert np.allclose(at_start, [-2, -3, -4, -27]) and np.isclose(at_start.mean(), -9)
assert np.isclose(at_start[[0, 3]].mean(), -14.5)     # a batch of merchants 1, 4
assert np.allclose(x4 * (3.0 * x4 - y4), [1, 0, -1, 0])

# ---- Part 2: 2,000 synthetic merchants, five features ----------------------
rng = np.random.default_rng(34)
n, d = 2000, 5
base = rng.standard_normal((n, 1))
X = 0.8 * base + 0.6 * rng.standard_normal((n, d))   # correlated features
true_w = np.array([2.0, -1.0, 0.5, 1.5, -0.5])
y = X @ true_w + rng.standard_normal(n)              # noisy target


def loss(w):
    return np.mean((X @ w - y) ** 2) / 2


def batch_gradient(w, idx):
    return X[idx].T @ (X[idx] @ w - y[idx]) / len(idx)


def train(batch_size, epochs=5, eta=0.05, seed=0):
    order_rng = np.random.default_rng(seed)
    w = np.zeros(d)
    seen, history = 0, [(0.0, loss(w))]
    for _ in range(epochs):
        order = order_rng.permutation(n)             # reshuffle every epoch
        for start in range(0, n, batch_size):
            idx = order[start:start + batch_size]
            w = w - eta * batch_gradient(w, idx)     # same rule as chapter 33
            seen += len(idx)
            history.append((seen / n, loss(w)))
    return w, np.array(history)


best = loss(np.linalg.lstsq(X, y, rcond=None)[0])
print(f"lowest possible loss {best:.4f}; loss after epochs 1, 2 and 5:")
runs = {}
for name, b in [("full batch", n), ("mini-batch of 32", 32), ("single example", 1)]:
    w_end, hist = train(b)
    runs[name] = hist
    by_epoch = [hist[hist[:, 0] <= e + 1e-9][-1, 1] for e in (1, 2, 5)]
    print(f"  {name:16} ({len(hist) - 1:6,d} updates): "
          + "  ".join(f"{v:.4f}" for v in by_epoch))

assert runs["mini-batch of 32"][-1, 1] < runs["full batch"][-1, 1]
assert runs["mini-batch of 32"][-1, 1] < best * 1.05
assert len(runs["full batch"]) - 1 == 5

# gradient noise shrinks like 1 / sqrt(batch size)
w0 = np.zeros(d)
noise = {}
for b in [1, 4, 16, 64]:
    draws = [batch_gradient(w0, rng.choice(n, b, replace=False))[0]
             for _ in range(4000)]
    noise[b] = np.std(draws)
print("gradient noise (std) at batch size 1, 4, 16, 64: "
      + "  ".join(f"{noise[b]:.3f}" for b in noise))
assert 1.8 < noise[1] / noise[4] < 2.2 and 1.8 < noise[4] / noise[16] < 2.2


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch34", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
    single = runs["single example"][::20]
    ax.semilogy(single[:, 0], single[:, 1] - best, color="#b45309", linewidth=0.9,
                label="single example (B = 1)")
    mini = runs["mini-batch of 32"]
    ax.semilogy(mini[:, 0], mini[:, 1] - best, color="#4f46e5", linewidth=1.8,
                label="mini-batch (B = 32)")
    fb = runs["full batch"]
    ax.semilogy(fb[:, 0], fb[:, 1] - best, "o-", color="#1f2937", linewidth=1.5,
                markersize=5, label="full batch (B = 2,000)")
    ax.set_xlabel("passes over the data (epochs)")
    ax.set_ylabel("loss above the minimum")
    ax.grid(True, linewidth=0.6)
    ax.legend(frameon=False, fontsize=10, loc="lower left")
    fig.tight_layout()
    fig.savefig(ASSETS / "ch34-batch-sizes.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
