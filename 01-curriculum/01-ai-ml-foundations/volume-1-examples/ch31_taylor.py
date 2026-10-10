"""Chapter 31. Taylor approximations and why they set the learning rate.

Run: python ch31_taylor.py
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
def approval(t):
    return 1 - (1 - t) ** 3


t0 = 0.5
d1, d2, d3 = 3 * (1 - t0) ** 2, -6 * (1 - t0), 6.0


def taylor(h, order):
    terms = [approval(t0), d1 * h, d2 * h**2 / 2, d3 * h**3 / 6]
    return sum(terms[:order + 1])


print("step  order 1  order 2  order 3   exact")
for h in (0.1, 0.4):
    print(f"{h:4.2f}  {taylor(h, 1):7.4f}  {taylor(h, 2):7.4f}  {taylor(h, 3):7.4f}  "
          f"{approval(t0 + h):6.4f}")

# Second-order prediction of a gradient step on Chapter 26's loss
w = np.zeros(2)
g, H = grad(w), 2 / len(y) * X.T @ X
print("learning rate  predicted  actual   after 40 steps")
for rate in (0.3, 0.9, 1.1):
    step = -rate * g
    predicted = loss(w) + g @ step + 0.5 * step @ H @ step
    v = w.copy()
    for _ in range(40):
        v = v - rate * grad(v)
    print(f"{rate:13.1f}  {predicted:9.4f}  {loss(w + step):6.4f}   {loss(v):.4g}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(approval(0.5), 0.875) and (d1, d2, d3) == (0.75, -3.0, 6.0)
assert np.isclose(taylor(0.1, 1), 0.95) and np.isclose(taylor(0.1, 2), 0.935)
assert np.isclose(taylor(0.1, 3), 0.936) and np.isclose(approval(0.6), 0.936)
assert np.isclose(taylor(0.4, 1), 1.175) and np.isclose(taylor(0.4, 2), 0.935)
assert np.isclose(approval(0.9), 0.999)
# derivatives used above, checked by finite differences
e = 1e-4
assert np.isclose((approval(t0 + e) - approval(t0 - e)) / (2 * e), d1, atol=1e-6)
assert np.isclose((approval(t0 + e) - 2 * approval(t0) + approval(t0 - e)) / e**2, d2,
                  atol=1e-5)
third = (approval(t0 + 2 * e) - 2 * approval(t0 + e) + 2 * approval(t0 - e)
         - approval(t0 - 2 * e)) / (2 * e**3)
assert np.isclose(third, d3, atol=1e-3)
# the error of the first-order model shrinks like h^2: halving h quarters it
err = lambda h: abs(approval(t0 + h) - taylor(h, 1))
assert np.isclose(err(0.02) / err(0.01), 4.0, rtol=0.05)
# gradient step on the quadratic loss: prediction 3 - rate*|g|^2 + rate^2/2 * g'Hg
gg, gHg = g @ g, g @ H @ g
assert np.isclose(gg, 100 / 9) and np.isclose(gHg, 592 / 27)
assert np.isclose(3 - 0.3 * gg + 0.045 * gHg, loss(w - 0.3 * g))
assert np.isclose(loss(w - 0.3 * g), 1.96 / 3)
# stability limit: rate < 2 / largest eigenvalue = 2 / 2 = 1
assert np.isclose(2 / np.linalg.eigvalsh(H).max(), 1.0)
# exp and log near zero: e^x ~ 1 + x, log(1 + x) ~ x
assert np.isclose(np.exp(0.01), 1.01, atol=1e-4)
assert np.isclose(np.log(1.01), 0.01, atol=1e-4)
# Q31.1: sigmoid near 0 is 0.5 + z/4 ; Q31.2: quadratic estimate at step 0.2
sig = lambda z: 1 / (1 + np.exp(-z))
assert np.isclose(sig(0.4), 0.5 + 0.4 / 4, atol=2e-3)
assert np.isclose(taylor(0.2, 2), 0.965) and np.isclose(approval(0.7), 0.973)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent = "#1f2937", "#6b7280", "#4f46e5"
    bad, good = "#b91c1c", "#15803d"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch31", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    t = np.linspace(0, 1, 300)
    h = t - t0
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=100)
    ax.plot(t, approval(t), color=ink, linewidth=2, label="true curve")
    ax.plot(t, approval(t0) + d1 * h, color=bad, linestyle="--",
            label="first order (tangent line)")
    ax.plot(t, approval(t0) + d1 * h + d2 * h**2 / 2, color=accent, linestyle="-.",
            label="second order (adds curvature)")
    ax.plot(t0, approval(t0), marker="o", color=ink, markersize=5)
    ax.axvspan(0.4, 0.6, color="#eef2ff", linewidth=0)
    ax.text(0.5, 0.08, "trust\nregion", color=accent, fontsize=10, ha="center")
    ax.set_ylim(0, 1.3)
    ax.set_xlim(0, 1)
    ax.set_xlabel("risk threshold t")
    ax.set_ylabel("share approved")
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch31-taylor.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
