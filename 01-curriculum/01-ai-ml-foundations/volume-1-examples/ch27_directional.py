"""Chapter 27. Directional derivatives: the slope along a direction you choose.

Run: python ch27_directional.py
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
w = np.array([0.0, 0.0])
g = grad(w)                                   # (-2, -8/3), length 10/3
directions = {
    "w1 only": (1, 0),
    "w2 only": (0, 1),
    "both equally": (1, 1),
    "steepest descent": -g,
    "along the contour": (-g[1], g[0]),
    "steepest ascent": g,
}
h = 1e-6
print("direction          unit vector      slope   finite diff   cos(angle)")
for name, d in directions.items():
    u = np.array(d, dtype=float)
    u = u / np.linalg.norm(u)                 # a direction must have length 1
    slope = g @ u                             # the directional derivative
    fd = (loss(w + h * u) - loss(w - h * u)) / (2 * h)
    cosine = slope / np.linalg.norm(g)
    print(f"{name:18s} ({u[0]:+.2f}, {u[1]:+.2f})  {slope:+.4f}  {fd:+11.4f}  "
          f"{cosine:+10.2f}")
# [/listing]

# Hand-worked values from the chapter
norm = np.linalg.norm(g)
assert np.isclose(norm, 10 / 3)
assert np.isclose(g @ np.array([1.0, 0.0]), -2.0)
assert np.isclose(g @ np.array([0.0, 1.0]), -8 / 3)
assert np.isclose(g @ (np.array([1.0, 1.0]) / np.sqrt(2)), -14 / (3 * np.sqrt(2)))
assert np.isclose(-14 / (3 * np.sqrt(2)), -3.2998, atol=5e-5)
assert np.isclose(g @ np.array([0.6, 0.8]), -10 / 3)          # steepest descent
assert np.isclose(g @ np.array([0.8, -0.6]), 0.0)             # along the contour
assert np.isclose(-2.0 / norm, -0.6) and np.isclose((-8 / 3) / norm, -0.8)
# no unit direction beats the gradient direction (Cauchy-Schwarz), by brute force
angles = np.linspace(0, 2 * np.pi, 3601)
slopes = g[0] * np.cos(angles) + g[1] * np.sin(angles)
assert slopes.max() <= norm + 1e-12 and slopes.min() >= -norm - 1e-12
assert np.isclose(slopes.max(), norm, atol=1e-5)
# Q27.1: direction (3, 4)/5 ; Q27.2: share of the steepest slope when only w1 moves
assert np.isclose(g @ np.array([0.6, 0.8]), -(2 * 0.6 + 8 / 3 * 0.8))
assert np.isclose(abs(-2.0) / norm, 0.6)
assert np.isclose(-norm * np.cos(np.deg2rad(60)), -5 / 3)       # 60 degrees: half


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    bad, good = "#b91c1c", "#15803d"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch27", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    deg = np.linspace(0, 360, 361)
    rad = np.deg2rad(deg)
    curve = g[0] * np.cos(rad) + g[1] * np.sin(rad)
    fig, ax = plt.subplots(figsize=(7.0, 3.2), dpi=100)
    ax.plot(deg, curve, color=accent)
    ax.axhline(0, color=muted, linewidth=0.8)
    marks = [
        (0.0, "w1 only", ink, (8, 10)),
        (45.0, "both equally", ink, (-50, -17)),
        (np.rad2deg(np.arctan2(0.8, 0.6)), "steepest descent", good, (10, -14)),
        (90.0, "w2 only", ink, (-44, 15)),
        (np.rad2deg(np.arctan2(0.6, -0.8)), "along the contour: 0", muted, (6, -16)),
        (np.rad2deg(np.arctan2(-0.8, -0.6)) % 360, "gradient: steepest ascent", bad,
         (-62, 8)),
    ]
    for angle, label, color, offset in marks:
        value = g[0] * np.cos(np.deg2rad(angle)) + g[1] * np.sin(np.deg2rad(angle))
        ax.plot(angle, value, marker="o", markersize=5, color=color)
        ax.annotate(label, xy=(angle, value), xytext=offset, textcoords="offset points",
                    color=color, fontsize=10)
    ax.set_xlim(-5, 365)
    ax.set_ylim(-4.4, 4.4)
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_xlabel("direction of the step (degrees from the w1 axis)")
    ax.set_ylabel("slope of the loss")
    ax.grid(True, axis="y", linewidth=0.6)
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch27-directions.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
