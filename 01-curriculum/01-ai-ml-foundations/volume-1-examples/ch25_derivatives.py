"""Chapter 25. Derivatives: how fast approval rate moves with the risk threshold.

Run: python ch25_derivatives.py
"""
from pathlib import Path

import numpy as np

# [listing]
def approval(t):
    """Share of payments scoring at or below the threshold t."""
    return 1 - (1 - t) ** 3


def d_approval(t):
    """Derivative by the chain and power rules."""
    return 3 * (1 - t) ** 2


def central(f, x, h=1e-5):
    """Slope of a short secant centered on x."""
    return (f(x + h) - f(x - h)) / (2 * h)


print("threshold  approval  slope (rule)  slope (finite difference)")
for t in (0.3, 0.5, 0.8):
    print(f"{t:9.1f}  {approval(t):8.4f}  {d_approval(t):12.4f}  "
          f"{central(approval, t):12.4f}")

print("secant slopes from 0.5 to 0.5 + h:")
for h in (0.4, 0.1, 0.01, 0.001):
    print(f"  h = {h:<5}  {(approval(0.5 + h) - approval(0.5)) / h:.4f}")

predicted = approval(0.5) + d_approval(0.5) * 0.02
print(f"raise the threshold 0.50 -> 0.52: predicted {predicted:.4f}, "
      f"actual {approval(0.52):.4f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(approval(0.5), 0.875) and np.isclose(d_approval(0.5), 0.75)
assert np.isclose(central(approval, 0.5), 0.75)
assert np.isclose((approval(0.51) - approval(0.49)) / 0.02, 0.7501, atol=5e-5)
assert np.isclose(predicted, 0.89)
assert np.isclose(approval(0.52), 0.889408)
for t in (0.1, 0.3, 0.5, 0.8, 0.95):
    assert np.isclose(central(approval, t), d_approval(t), atol=1e-8)

# Every rule in the chapter's table, checked with finite differences at x = 0.7
x = 0.7
sig = lambda v: 1 / (1 + np.exp(-v))
rules = [
    (lambda v: v**4, 4 * x**3),                                   # power
    (lambda v: 3 * v**2 + 5 * v, 6 * x + 5),                      # sum, constant
    (lambda v: v**2 * np.exp(v), 2 * x * np.exp(x) + x**2 * np.exp(x)),   # product
    (np.exp, np.exp(x)),                                          # exponential
    (np.log, 1 / x),                                              # logarithm
    (sig, sig(x) * (1 - sig(x))),                                 # sigmoid
    (lambda v: np.exp(-2 * v**2), -4 * x * np.exp(-2 * x**2)),    # chain
]
for f, expected in rules:
    assert np.isclose(central(f, x), expected, atol=1e-7)
assert np.isclose(sig(0.0) * (1 - sig(0.0)), 0.25)
# second derivative of approval: -6(1 - t), negative, so the curve bends downward
second = (approval(0.5 + 1e-4) - 2 * approval(0.5) + approval(0.5 - 1e-4)) / 1e-8
assert np.isclose(second, -3.0, atol=1e-4)
# a local slope fails for a large move: 0.75 * 0.4 = 0.30 predicted, 0.124 actual
assert np.isclose(approval(0.9) - approval(0.5), 0.124)
# Q25.1: slope at 0.9 ; Q25.2: break-even threshold for a calibrated score
assert np.isclose(d_approval(0.9), 0.03)
assert np.isclose(3.20 / (100 + 3.20), 0.031, atol=5e-5)
value = lambda p: 3.20 * (1 - p) - 100 * p          # expected value of approving
assert abs(value(3.20 / 103.20)) < 1e-12 and value(0.02) > 0 > value(0.05)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent, bad = "#1f2937", "#6b7280", "#4f46e5", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch25", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    t = np.linspace(0, 1, 300)
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=100)
    ax.plot(t, approval(t), color=accent, label="approval rate A(t)")
    tt = np.linspace(0.2, 0.8, 10)
    ax.plot(tt, 0.875 + 0.75 * (tt - 0.5), color=bad, linewidth=1.2,
            label="tangent at 0.5: slope 0.75")
    ts = np.array([0.3, 1.0])
    ax.plot(ts, 0.875 + 0.31 * (ts - 0.5), color=ink, linestyle="--", linewidth=1.2,
            label="secant from 0.5 to 0.9: slope 0.31")
    ax.plot([0.5, 0.9], approval(np.array([0.5, 0.9])), color=ink, marker="o",
            markersize=4, linestyle="none")
    ax.set_xlabel("risk threshold t (block payments scoring above t)")
    ax.set_ylabel("share approved")
    ax.set_ylim(0, 1.15)
    ax.set_xlim(0, 1)
    ax.legend(frameon=False, fontsize=10, loc="lower right")
    ax.grid(True, linewidth=0.6)
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch25-tangent.svg", bbox_inches="tight",
                    metadata={"Date": None})


assert np.isclose((approval(0.9) - approval(0.5)) / 0.4, 0.31)
figure()
