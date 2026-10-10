"""Chapter 32: convexity, minima and saddle points.

Classifies the critical points of a two-valley loss by the eigenvalues of the
Hessian, checks the convexity inequality, and shows how fast "all eigenvalues
positive" becomes rare as the number of dimensions grows.
Writes volume-1-assets/ch32-three-surfaces.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)


def f(x, y):
    """A loss with two valleys: minima at (-1, 0) and (1, 0)."""
    return (x**2 - 1) ** 2 + y**2


def gradient(x, y):
    return np.array([4 * x * (x**2 - 1), 2 * y])


def hessian(x, y):
    return np.array([[12 * x**2 - 4, 0.0], [0.0, 2.0]])


def classify(eigenvalues):
    if np.all(eigenvalues > 0):
        return "local minimum"
    if np.all(eigenvalues < 0):
        return "local maximum"
    if np.any(eigenvalues > 0) and np.any(eigenvalues < 0):
        return "saddle point"
    return "inconclusive"


kinds = {}
for point in [(-1.0, 0.0), (0.0, 0.0), (1.0, 0.0)]:
    assert np.allclose(gradient(*point), 0.0)          # it is a critical point
    eig = np.linalg.eigvalsh(hessian(*point))
    kinds[point] = classify(eig)
    print(f"{point}: f = {f(*point):.0f}, eigenvalues {eig} -> {kinds[point]}")

# hand result: two minima with a saddle between them
assert kinds[(-1.0, 0.0)] == kinds[(1.0, 0.0)] == "local minimum"
assert kinds[(0.0, 0.0)] == "saddle point"

# convexity test on the segment between the two minima
a, b = np.array([-1.0, 0.0]), np.array([1.0, 0.0])
mid = 0.5 * (a + b)
lhs, rhs = f(*mid), 0.5 * f(*a) + 0.5 * f(*b)
print(f"f(midpoint) = {lhs:.1f}, average of f at the ends = {rhs:.1f}, "
      f"convex: {lhs <= rhs}")
assert np.isclose(lhs, 1.0) and np.isclose(rhs, 0.0)

# How rare is "every eigenvalue positive" for a random symmetric matrix?
rng = np.random.default_rng(32)
trials = 200_000
shares = {}
for n in [1, 2, 3, 4, 5]:
    a_mat = rng.standard_normal((trials, n, n))
    sym = (a_mat + np.transpose(a_mat, (0, 2, 1))) / 2
    shares[n] = np.mean(np.all(np.linalg.eigvalsh(sym) > 0, axis=1))
print("random symmetric n x n matrix: chance that every eigenvalue is positive")
print("  " + "   ".join(f"n={n}: 1 in {1 / s:,.0f}" for n, s in shares.items()))
assert abs(shares[1] - 0.5) < 0.01
assert shares[5] < shares[4] < shares[3] < shares[2] < shares[1]


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch32", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    xs = np.linspace(-1.8, 1.8, 241)
    ys = np.linspace(-1.5, 1.5, 201)
    gx, gy = np.meshgrid(xs, ys)
    panels = [
        ("Bowl (convex)", gx**2 + gy**2, [0.1, 0.4, 0.9, 1.6, 2.5, 3.6],
         [(0, 0, "minimum", "#15803d")]),
        ("Two valleys", f(gx, gy), [0.1, 0.4, 0.9, 1.6, 2.5, 3.6],
         [(-1, 0, "minimum", "#15803d"), (1, 0, "minimum", "#15803d"),
          (0, 0, "saddle", "#b91c1c")]),
        ("Saddle", gx**2 - gy**2, [-1.6, -0.9, -0.4, -0.1, 0.1, 0.4, 0.9, 1.6],
         [(0, 0, "saddle", "#b91c1c")]),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.7), dpi=100)
    for ax, (title, z, levels, marks) in zip(axes, panels):
        ax.contour(gx, gy, z, levels=levels, colors="#4f46e5", linewidths=1.0,
                   negative_linestyles="dashed")
        for mx, my, label, color in marks:
            ax.plot(mx, my, "o", color=color, markersize=7)
            dy = -19 if label == "saddle" else 11
            ax.annotate(label, (mx, my), textcoords="offset points",
                        xytext=(0, dy), ha="center", color=color, fontsize=10,
                        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.5})
        ax.set_title(title, fontsize=11, color="#1f2937")
        ax.set_xticks([-1, 0, 1])
        ax.set_yticks([-1, 0, 1])
        ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(ASSETS / "ch32-three-surfaces.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
