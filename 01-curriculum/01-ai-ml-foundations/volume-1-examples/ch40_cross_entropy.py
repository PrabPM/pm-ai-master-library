"""Chapter 40: cross-entropy (log loss) for a fraud classifier.

Five PayFlow payments, two fraud models. Both get the same four payments right
at a 0.5 threshold; model A is confident and wrong on the fifth.
Writes volume-1-assets/ch40-log-loss-curve.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)

y = np.array([0, 0, 0, 1, 1])                         # 1 = fraud
model_a = np.array([0.10, 0.20, 0.05, 0.90, 0.02])    # predicted P(fraud)
model_b = np.array([0.10, 0.20, 0.05, 0.90, 0.30])


def log_loss_each(y, p, eps=1e-12):
    """Binary cross-entropy per example, in nats."""
    p = np.clip(p, eps, 1 - eps)          # never take log(0)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


def accuracy(y, p):
    return np.mean((p >= 0.5) == (y == 1))


for name, p in [("A", model_a), ("B", model_b)]:
    each = log_loss_each(y, p)
    print(f"model {name} losses: {np.round(each, 4)}  mean {each.mean():.4f}  "
          f"accuracy {accuracy(y, p):.0%}")

base_rate = y.mean()
baseline = log_loss_each(y, np.full(5, base_rate)).mean()
print(f"always predicting the base rate {base_rate:.1f}: mean {baseline:.4f}")

loss_a, loss_b = log_loss_each(y, model_a), log_loss_each(y, model_b)
# hand results: -ln(0.9), -ln(0.8), -ln(0.95), -ln(0.9), -ln(0.02)
assert np.allclose(np.round(loss_a, 4), [0.1054, 0.2231, 0.0513, 0.1054, 3.9120])
assert np.isclose(round(loss_a.mean(), 4), 0.8794)
assert np.isclose(round(loss_b.mean(), 4), 0.3378)
assert accuracy(y, model_a) == accuracy(y, model_b) == 0.8
# the base-rate forecast scores exactly the entropy of the labels
entropy = -(0.4 * np.log(0.4) + 0.6 * np.log(0.6))
assert np.isclose(baseline, entropy) and loss_b.mean() < baseline < loss_a.mean()

share = loss_a[4] / loss_a.sum()
print(f"payment 5 is {share:.0%} of model A's total loss")
qs = (0.9, 0.5, 0.3, 0.02, 0.001)
print("loss when a true fraud is scored", qs)
print("  ", "  ".join(f"{-np.log(q):.3f}" for q in qs))


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch40", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, ax = plt.subplots(figsize=(6.2, 3.3), dpi=100)
    q = np.linspace(0.008, 1, 500)
    ax.plot(q, -np.log(q), color="#6b7280", linewidth=1.6)
    marks = [(0.90, "#15803d", "0.90: confident and right, loss 0.11", (-150, 30)),
             (0.30, "#b45309", "0.30: hedged and wrong, loss 1.20", (14, 6)),
             (0.02, "#b91c1c", "0.02: confident and wrong, loss 3.91", (14, 0))]
    for prob, color, label, offset in marks:
        ax.plot(prob, -np.log(prob), "o", color=color, markersize=7)
        ax.annotate(label, (prob, -np.log(prob)), textcoords="offset points",
                    xytext=offset, color=color, fontsize=10)
    ax.set_xlabel("probability the model gave to what actually happened")
    ax.set_ylabel("loss (nats)")
    ax.set_ylim(0, 5)
    ax.grid(True, linewidth=0.6)
    fig.tight_layout()
    fig.savefig(ASSETS / "ch40-log-loss-curve.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
