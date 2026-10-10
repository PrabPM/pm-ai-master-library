"""Chapter 38: entropy as average surprise.

PayFlow's payment-status distribution (illustrative): 28 of every 32 payments
succeed, 2 are declined by the card issuer, 1 is blocked by PayFlow's risk
rules and 1 is abandoned by the customer during authentication.
Writes volume-1-assets/ch38-surprise-and-entropy.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)

status = {"succeeded": 28 / 32, "declined": 2 / 32, "blocked": 1 / 32,
          "abandoned": 1 / 32}


def entropy_bits(p):
    """H = sum of p * log2(1/p), with the convention 0 * log(1/0) = 0."""
    p = np.asarray(p, dtype=float)
    p = p[p > 0]
    return float(np.sum(p * np.log2(1 / p)))


p = np.array(list(status.values()))
assert np.isclose(p.sum(), 1.0)
print("status      p        surprise (bits)   p x surprise")
for name, prob in status.items():
    s = np.log2(1 / prob)
    print(f"{name:10} {prob:.5f}   {s:8.4f}        {prob * s:8.4f}")
H = entropy_bits(p)
print(f"entropy H = {H:.4f} bits")
print(f"largest possible with 4 outcomes = {np.log2(4):.1f} bits")
print(f"in nats: {H * np.log(2):.4f}")

# hand result: 0.875 * log2(8/7) + (1/16)*4 + 2 * (1/32)*5
by_hand = 0.875 * np.log2(8 / 7) + 0.0625 * 4 + 2 * 0.03125 * 5
assert np.isclose(H, by_hand) and np.isclose(round(H, 4), 0.7311)
assert np.isclose(entropy_bits([0.25] * 4), 2.0)
assert entropy_bits([1.0, 0.0, 0.0, 0.0]) == 0.0

print("entropy of a yes/no label")
for rate in (0.5, 0.1, 0.01):
    print(f"  P(yes) = {rate:<4}: {entropy_bits([rate, 1 - rate]):.4f} bits")
assert np.isclose(entropy_bits([0.5, 0.5]), 1.0)
assert np.isclose(round(entropy_bits([0.01, 0.99]), 4), 0.0808)


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch38", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.2, 3.1), dpi=100)
    q = np.linspace(0.012, 1, 400)
    left.plot(q, np.log2(1 / q), color="#6b7280", linewidth=1.5)
    marks = [("succeeded", 28 / 32, (-28, 30)), ("declined", 2 / 32, (10, -2)),
             ("blocked, abandoned", 1 / 32, (10, 0))]
    for name, prob, offset in marks:
        left.plot(prob, np.log2(1 / prob), "o", color="#4f46e5", markersize=6)
        left.annotate(name, (prob, np.log2(1 / prob)), textcoords="offset points",
                      xytext=offset, color="#4f46e5", fontsize=10)
    left.set_xlabel("probability of the outcome")
    left.set_ylabel("surprise (bits)")
    left.set_title("Rare outcomes are surprising", fontsize=11, color="#1f2937")
    left.grid(True, linewidth=0.6)
    r = np.linspace(0.0005, 0.9995, 500)
    right.plot(r, -(r * np.log2(r) + (1 - r) * np.log2(1 - r)), color="#4f46e5",
               linewidth=1.8)
    for rate, offset in [(0.5, (-38, -48)), (0.01, (10, 6))]:
        h = entropy_bits([rate, 1 - rate])
        right.plot(rate, h, "o", color="#1f2937", markersize=6)
        right.annotate(f"P = {rate}: {h:.2f} bits", (rate, h),
                       textcoords="offset points", xytext=offset, fontsize=10,
                       color="#1f2937")
    right.set_xlabel("P(yes) for a yes/no label")
    right.set_ylabel("entropy (bits)")
    right.set_title("Uncertainty peaks at 50/50", fontsize=11, color="#1f2937")
    right.grid(True, linewidth=0.6)
    fig.tight_layout()
    fig.savefig(ASSETS / "ch38-surprise-and-entropy.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
