"""Chapter 30. The Hessian: curvature, positive definiteness and Newton's step.

Run: python ch30_hessian.py
"""
from pathlib import Path

import numpy as np

X = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])    # the loss of Chapter 26
y = np.array([1.0, 2.0, 2.0])


def loss(w):
    return np.mean((X @ w - y) ** 2)


def grad(w):
    return 2 / len(y) * X.T @ (X @ w - y)


# [listing]
def numerical_hessian(f, w, h=1e-4):
    """Entry (i, j): how fast slope i changes along input j."""
    n = len(w)
    H = np.zeros((n, n))
    for i, ei in enumerate(np.eye(n)):
        for j, ej in enumerate(np.eye(n)):
            H[i, j] = (f(w + h * ei + h * ej) - f(w + h * ei - h * ej)
                       - f(w - h * ei + h * ej) + f(w - h * ei - h * ej)) / (4 * h * h)
    return H


w = np.array([0.0, 0.0])
H = 2 / len(y) * X.T @ X
print("Hessian           :", H.round(4).tolist())
print("numerical Hessian :", numerical_hessian(loss, w).round(4).tolist())
curvatures, directions = np.linalg.eigh(H)
print("eigenvalues       :", curvatures.round(4), "-> positive definite, a bowl")
print("condition number  :", round(curvatures.max() / curvatures.min(), 2))

newton = w - np.linalg.solve(H, grad(w))
print("one Newton step   :", newton.round(4), "gradient there:",
      np.abs(grad(newton)).round(12))


def saddle(v):
    return v[0] ** 2 - v[1] ** 2


print("saddle eigenvalues:", np.linalg.eigvalsh(numerical_hessian(saddle, w)).round(4))
# [/listing]

# Hand-worked values from the chapter
assert np.allclose(H, [[4 / 3, 2 / 3], [2 / 3, 4 / 3]])
assert np.allclose(numerical_hessian(loss, w), H, atol=1e-6)
assert np.allclose(curvatures, [2 / 3, 2.0])
assert np.isclose(curvatures.max() / curvatures.min(), 3.0)
assert np.isclose(np.trace(H), 8 / 3) and np.isclose(np.linalg.det(H), 4 / 3)
# eigenvectors: (1, -1) for 2/3 and (1, 1) for 2
assert np.isclose(abs(directions[:, 0] @ np.array([1, -1]) / np.sqrt(2)), 1.0)
assert np.isclose(abs(directions[:, 1] @ np.array([1, 1]) / np.sqrt(2)), 1.0)
assert np.allclose(np.linalg.inv(H), [[1.0, -0.5], [-0.5, 1.0]])
assert np.allclose(newton, [2 / 3, 5 / 3]) and np.allclose(grad(newton), 0)
# positive definite: h^T H h > 0 for every direction tried
rng = np.random.default_rng(30)
for h in rng.normal(size=(1000, 2)):
    assert h @ H @ h > 0
# the Hessian is the Jacobian of the gradient (finite differences of grad)
eps = 1e-6
Jg = np.column_stack([(grad(w + eps * e) - grad(w - eps * e)) / (2 * eps)
                      for e in np.eye(2)])
assert np.allclose(Jg, H, atol=1e-8)
assert np.allclose(np.linalg.eigvalsh(numerical_hessian(saddle, w)), [-2, 2], atol=1e-6)

# Newton's method on a loss that is not quadratic and has a true minimum:
# one fraud example with feature 2, log loss plus a small L2 penalty
def f(v):
    return np.log1p(np.exp(-2 * v)) + 0.05 * v**2


def f1(v):
    return -2 / (1 + np.exp(2 * v)) + 0.1 * v


def f2(v):
    s = 1 / (1 + np.exp(-2 * v))
    return 4 * s * (1 - s) + 0.1


v = 0.0
for _ in range(6):
    assert np.isclose(f1(v), (f(v + 1e-6) - f(v - 1e-6)) / 2e-6, atol=1e-8)
    assert np.isclose(f2(v), (f1(v + 1e-6) - f1(v - 1e-6)) / 2e-6, atol=1e-7)
    v = v - f1(v) / f2(v)
assert abs(f1(v)) < 1e-10 and f2(v) > 0          # converged to a minimum
# without the penalty there is no minimum: the slope never reaches zero
assert all(-2 / (1 + np.exp(2 * t)) < 0 for t in (0.0, 5.0, 10.0))
# Q30.1: f = x^2 + 4xy + y^2 has Hessian eigenvalues -2 and 6: a saddle
assert np.allclose(np.linalg.eigvalsh(np.array([[2.0, 4.0], [4.0, 2.0]])),
                   [-2.0, 6.0])
# Q30.2: largest safe learning rate for this loss is 2 / 2 = 1
assert np.isclose(2 / curvatures.max(), 1.0)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    bad, good = "#b91c1c", "#15803d"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch30", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.3), dpi=100)
    c = np.array([2 / 3, 5 / 3])
    a, b = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
    bowl = ((a + c[0] - 1) ** 2 + (b + c[1] - 2) ** 2 + (a + b + c.sum() - 2) ** 2) / 3
    ax1.contour(a, b, bowl, levels=[0.3, 0.8, 1.6, 2.8, 4.4], colors="#cbd5e1",
                linewidths=1.2)
    ax1.annotate("", xy=(0.92, -0.92), xytext=(0, 0),
                 arrowprops={"arrowstyle": "->", "color": accent, "linewidth": 1.5})
    ax1.annotate("", xy=(0.53, 0.53), xytext=(0, 0),
                 arrowprops={"arrowstyle": "->", "color": bad, "linewidth": 1.5})
    ax1.text(0.3, -1.0, "curvature 2/3\n(gentle)", color=accent, fontsize=10,
             ha="right", va="center")
    ax1.text(0.62, 0.62, "curvature 2\n(steep)", color=bad, fontsize=10, va="bottom")
    ax1.plot(0, 0, marker="*", markersize=11, color=good)
    ax1.set_title("Bowl: both eigenvalues positive", fontsize=11, color=ink, loc="left")
    sad = a**2 - b**2
    neg = ax2.contour(a, b, sad, levels=[-3, -2, -1], colors=bad, linewidths=1.0,
                      linestyles="solid")
    pos = ax2.contour(a, b, sad, levels=[1, 2, 3], colors=accent, linewidths=1.0)
    ax2.clabel(neg, fmt="%+.0f", fontsize=9, manual=[(0, 1.0), (0, 1.41), (0, 1.73)])
    ax2.clabel(pos, fmt="%+.0f", fontsize=9, manual=[(1.0, 0), (1.41, 0), (1.73, 0)])
    ax2.plot(0, 0, marker="o", markersize=5, color=ink)
    ax2.text(0.12, -0.38, "flat here,\nnot a minimum", color=ink, fontsize=10,
             ha="center", va="top")
    ax2.set_title("Saddle: one positive, one negative", fontsize=11, color=ink,
                  loc="left")
    for ax in (ax1, ax2):
        ax.set_aspect("equal")
        ax.set_xticks([-2, 0, 2])
        ax.set_yticks([-2, 0, 2])
        ax.set_xlabel("step in w1")
    ax1.set_ylabel("step in w2")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch30-bowl-saddle.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
