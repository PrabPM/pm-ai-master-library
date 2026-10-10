"""Chapter 33: gradient descent on a one-weight least-squares loss.

Four PayFlow merchants: weekly payments in thousands (x) and disputes (y).
Model: disputes = w * payments. Loss J(w) = mean((w x - y)^2) / 2.
Writes volume-1-assets/ch33-learning-rates.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)

x = np.array([1.0, 1.0, 1.0, 3.0])   # weekly payments, thousands
y = np.array([2.0, 3.0, 4.0, 9.0])   # disputes that week


def loss(w):
    return np.mean((w * x - y) ** 2) / 2


def grad(w):
    return np.mean(x * (w * x - y))


def descend(eta, steps, w=0.0):
    path = [w]
    for _ in range(steps):
        w = w - eta * grad(w)       # the whole algorithm
        path.append(w)
    return np.array(path)


curvature = np.mean(x**2)            # second derivative of J, called L in the text
w_best = np.sum(x * y) / np.sum(x**2)
print(f"curvature L = {curvature:.1f}, best w = {w_best:.1f}, "
      f"lowest loss = {loss(w_best):.2f}")
print(f"largest stable learning rate 2/L = {2 / curvature:.4f}")

by_hand = descend(0.1, 3)
print("eta = 0.1, first three steps:", np.round(by_hand[1:], 4))
assert np.allclose(by_hand, [0.0, 0.9, 1.53, 1.971])
assert np.isclose(curvature, 3.0) and np.isclose(w_best, 3.0)
assert np.isclose(loss(w_best), 0.25)
assert np.isclose(grad(0.0), -9.0)

paths = {}
for eta, label in [(0.01, "too small"), (0.1, "about right"), (0.7, "too large")]:
    paths[eta] = descend(eta, 20)
    w20 = paths[eta][-1]
    print(f"eta = {eta:<4} ({label:11}) after 20 steps: w = {w20:9.4f}, "
          f"loss = {loss(w20):8.4f}")

# each step multiplies the distance to the best w by (1 - eta * L)
for eta in paths:
    assert np.isclose(paths[eta][-1] - 3.0, -3.0 * (1 - eta * curvature) ** 20)
assert abs(paths[0.7][-1] - 3.0) > abs(paths[0.7][0] - 3.0)   # it diverged


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch33", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.2, 3.1), dpi=100)
    ws = np.linspace(-1.2, 7.2, 200)
    left.plot(ws, [loss(w) for w in ws], color="#6b7280", linewidth=1.5)
    for eta, color, n in [(0.1, "#4f46e5", 6), (0.7, "#b91c1c", 4)]:
        p = paths[eta][:n]
        left.plot(p, [loss(w) for w in p], "o-", color=color, markersize=5,
                  linewidth=1.2)
    left.text(-1.0, 1.2, "η = 0.1", color="#4f46e5", fontsize=10)
    left.text(1.7, 10.3, "η = 0.7 overshoots", color="#b91c1c", fontsize=10)
    left.set_xlabel("weight w")
    left.set_ylabel("loss J(w)")
    left.set_ylim(0, 25)
    styles = [(0.01, "#b45309", "η = 0.01 (too small)"),
              (0.1, "#4f46e5", "η = 0.1 (about right)"),
              (0.7, "#b91c1c", "η = 0.7 (diverges)")]
    for eta, color, label in styles:
        gap = [loss(w) - 0.25 for w in paths[eta]]
        right.semilogy(range(21), gap, color=color, linewidth=1.6, label=label)
    right.set_xlabel("step")
    right.set_ylabel("loss above the minimum")
    right.set_xticks([0, 5, 10, 15, 20])
    right.grid(True, linewidth=0.6)
    right.legend(frameon=False, fontsize=9, loc="center right")
    fig.tight_layout()
    fig.savefig(ASSETS / "ch33-learning-rates.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
