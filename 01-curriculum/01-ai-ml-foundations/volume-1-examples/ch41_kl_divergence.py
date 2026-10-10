"""Chapter 41: KL divergence and drift between two months of payments.

Share of PayFlow payments by merchant category, last month (q, the mix the
fraud model was trained on) and this month (p, what it now sees).
Writes volume-1-assets/ch41-category-drift.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)

categories = ["retail", "food", "travel", "digital goods"]
last_month = np.array([0.50, 0.25, 0.20, 0.05])    # q
this_month = np.array([0.40, 0.25, 0.15, 0.20])    # p


def kl_bits(p, q):
    """D(p || q) in bits. Infinite if q is zero anywhere p is not."""
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    if np.any((q == 0) & (p > 0)):
        return float("inf")
    keep = p > 0
    return float(np.sum(p[keep] * np.log2(p[keep] / q[keep])))


def cross_entropy_bits(p, q):
    return float(-np.sum(p * np.log2(q)))


def entropy_bits(p):
    return float(-np.sum(p * np.log2(p)))


terms = this_month * np.log2(this_month / last_month)
print("category        q      p     p*log2(p/q)")
for name, q_i, p_i, t in zip(categories, last_month, this_month, terms):
    print(f"{name:14} {q_i:.2f}   {p_i:.2f}   {t:+.4f}")
forward = kl_bits(this_month, last_month)
reverse = kl_bits(last_month, this_month)
print(f"D(this month || last month) = {forward:.4f} bits")
print(f"D(last month || this month) = {reverse:.4f} bits")
gap = cross_entropy_bits(this_month, last_month) - entropy_bits(this_month)
print(f"cross-entropy minus entropy  = {gap:.4f} bits")
psi = np.sum((this_month - last_month) * np.log(this_month / last_month))
print(f"population stability index   = {psi:.4f}")

# hand results
assert np.allclose(np.round(terms, 4), [-0.1288, 0.0, -0.0623, 0.4])
assert np.isclose(round(forward, 4), 0.2090) and np.isclose(round(reverse, 4), 0.1440)
assert np.isclose(gap, forward)                        # H(p, q) = H(p) + D(p || q)
assert np.isclose(psi, (forward + reverse) * np.log(2))  # PSI = symmetrized KL, nats
assert kl_bits(this_month, this_month) == 0.0
assert kl_bits([0.5, 0.5, 0.0], [0.5, 0.0, 0.5]) == float("inf")

# noise floor: two samples from the SAME distribution never give exactly zero
rng = np.random.default_rng(41)
for n in (500, 50_000):
    draws = []
    for _ in range(200):
        a = rng.multinomial(n, last_month) / n
        b = rng.multinomial(n, last_month) / n
        draws.append(kl_bits(a, b))
    print(f"no real drift, {n:6,d} payments a month: median D = "
          f"{np.median(draws):.5f}, 95th percentile = {np.percentile(draws, 95):.5f}")


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch41", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, (left, right) = plt.subplots(1, 2, figsize=(7.2, 3.1), dpi=100)
    x = np.arange(4)
    left.bar(x - 0.2, last_month, 0.4, color="#cbd5e1", label="last month (q)")
    left.bar(x + 0.2, this_month, 0.4, color="#4f46e5", label="this month (p)")
    left.set_xticks(x, ["retail", "food", "travel", "digital"])
    left.set_ylabel("share of payments")
    left.legend(frameon=False, fontsize=9)
    colors = ["#b91c1c" if t > 0 else "#6b7280" for t in terms]
    right.bar(x, terms, 0.55, color=colors)
    right.axhline(0, color="#6b7280", linewidth=0.8)
    right.set_xticks(x, ["retail", "food", "travel", "digital"])
    right.set_ylabel("contribution to D(p‖q), bits")
    right.set_title(f"sum = {forward:.3f} bits", fontsize=11, color="#1f2937")
    fig.tight_layout()
    fig.savefig(ASSETS / "ch41-category-drift.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
