"""Chapter 26. Partial derivatives and the gradient of a two-weight loss.

Run: python ch26_gradient.py
"""
from pathlib import Path

import numpy as np

# [listing]
# Three rated payments: [new device?, foreign card?] and the rating
X = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, 1.0]])
y = np.array([1.0, 2.0, 2.0])


def loss(w):
    """Mean squared error of the score X @ w."""
    return np.mean((X @ w - y) ** 2)


def grad(w):
    """Both partial derivatives at once."""
    return 2 / len(y) * X.T @ (X @ w - y)


def numerical_grad(f, w, h=1e-6):
    """Nudge one weight at a time, hold the others fixed."""
    return np.array([(f(w + h * e) - f(w - h * e)) / (2 * h) for e in np.eye(len(w))])


w = np.array([0.0, 0.0])
g = grad(w)
print(f"loss at (0, 0)       {loss(w):.4f}")
print(f"gradient             {g.round(4)}")
print(f"numerical gradient   {numerical_grad(loss, w).round(4)}")
print(f"gradient length      {np.linalg.norm(g):.4f}")
print(f"steepest descent     {(-g / np.linalg.norm(g)).round(2)}")
step = w - 0.3 * g
print(f"after w - 0.3 * gradient: w = {step.round(2)}, loss {loss(step):.4f}")
w_star = np.linalg.solve(X.T @ X, X.T @ y)
print(f"gradient is zero at  {w_star.round(4)}, loss {loss(w_star):.4f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(loss(w), 3.0)
assert np.allclose(g, [-2.0, -8 / 3])
assert np.allclose(numerical_grad(loss, w), g, atol=1e-6)
assert np.isclose(np.linalg.norm(g), 10 / 3)
assert np.allclose(-g / np.linalg.norm(g), [0.6, 0.8])
assert np.allclose(step, [0.6, 0.8]) and np.isclose(loss(step), 1.96 / 3)
assert np.allclose(w_star, [2 / 3, 5 / 3]) and np.isclose(loss(w_star), 1 / 9)
assert np.allclose(grad(w_star), 0)
# the expanded form used in the chapter gives the same loss and partials
def loss_expanded(w1, w2):
    return ((w1 - 1) ** 2 + (w2 - 2) ** 2 + (w1 + w2 - 2) ** 2) / 3


rng = np.random.default_rng(26)
for w1, w2 in rng.normal(size=(5, 2)):
    v = np.array([w1, w2])
    assert np.isclose(loss_expanded(w1, w2), loss(v))
    assert np.allclose(grad(v), [2 / 3 * (2 * w1 + w2 - 3), 2 / 3 * (w1 + 2 * w2 - 4)])
    assert np.allclose(numerical_grad(loss, v), grad(v), atol=1e-6)
# first-order prediction for a small step h: change in loss ~ gradient . h
h_small = np.array([0.01, -0.02])
assert np.isclose(loss(w + h_small) - loss(w), g @ h_small, atol=1e-3)
# Q26.1: gradient at (1, 1) ; Q26.2: a step that is too long makes the loss worse
assert np.allclose(grad(np.array([1.0, 1.0])), [0.0, -2 / 3])
far = w - 1.2 * g
assert np.allclose(far, [2.4, 3.2]) and np.isclose(loss(far), 5.45, atol=5e-3)
assert loss(far) > loss(w)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    bad, good = "#b91c1c", "#15803d"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch26", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    a, b = np.meshgrid(np.linspace(-2.1, 3.5, 240), np.linspace(-1.1, 3.0, 200))
    z = loss_expanded(a, b)
    fig, ax = plt.subplots(figsize=(6.2, 3.6), dpi=100)
    levels = [0.25, 0.75, 1.5, 3.0, 5.0, 8.0]
    cs = ax.contour(a, b, z, levels=levels, colors="#cbd5e1", linewidths=1.2)
    d = np.array([1.0, 1.0]) / np.sqrt(2)          # label along the short axis
    spots = [tuple(w_star + np.sqrt(c - 1 / 9) * d) for c in levels[:4]]
    ax.clabel(cs, levels=levels[:4], fmt="%.2g", fontsize=9, colors=muted,
              manual=spots)
    ax.plot(*w_star, marker="*", markersize=12, color=good, linestyle="none")
    ax.text(w_star[0] + 0.12, w_star[1] - 0.22, "minimum", color=good, fontsize=10)
    ax.annotate("", xy=(-0.6, -0.8), xytext=(0, 0),
                arrowprops={"arrowstyle": "->", "color": bad, "linewidth": 1.6})
    ax.annotate("", xy=(0.6, 0.8), xytext=(0, 0),
                arrowprops={"arrowstyle": "->", "color": accent, "linewidth": 1.6})
    ax.plot(0, 0, marker="o", markersize=5, color=ink)
    ax.text(-0.75, -0.72, "gradient:\nsteepest increase", color=bad, fontsize=10,
            ha="right", va="center")
    ax.text(0.45, 0.02, "negative gradient:\nsteepest decrease", color=accent,
            fontsize=10, va="top")
    ax.set_aspect("equal")
    ax.set_xlabel("weight w1 (new device)")
    ax.set_ylabel("weight w2 (foreign card)")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch26-contours.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
