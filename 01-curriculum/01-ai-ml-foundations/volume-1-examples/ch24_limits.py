"""Chapter 24. Limits and continuity: one numerical limit and one jump.

Run: python ch24_limits.py
"""
from pathlib import Path

import numpy as np

# [listing]
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# A limit: the slope of the sigmoid at 0 is what this ratio approaches as h shrinks
print("       h   (sigmoid(h) - sigmoid(0)) / h")
for h in (1.0, 0.1, 0.01, 0.001, 1e-6, 1e-13, 1e-17):
    print(f"{h:8.0e}   {(sigmoid(h) - sigmoid(0.0)) / h:.6f}")


# A jump: the monthly fee if the rate drops from 2.9% to 2.7% at USD 100,000
def monthly_fee(volume):
    rate = 0.029 if volume < 100_000 else 0.027
    return rate * volume


print("monthly volume -> fee")
for v in (99_000, 99_999, 99_999.99, 100_000, 100_000.01, 101_000):
    print(f"{v:12,.2f} -> {monthly_fee(v):9,.2f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(sigmoid(1.0), 0.7311, atol=5e-5)
assert np.isclose((sigmoid(1.0) - 0.5) / 1.0, 0.2311, atol=5e-5)
assert np.isclose((sigmoid(0.1) - 0.5) / 0.1, 0.2498, atol=5e-5)
assert np.isclose((sigmoid(1e-6) - 0.5) / 1e-6, 0.25, atol=1e-6)      # the limit
assert (sigmoid(1e-17) - 0.5) / 1e-17 == 0.0          # h too small for floating point
# one-sided limits at the threshold: 2,900 from below, 2,700 from above
assert np.isclose(monthly_fee(100_000 - 1e-6), 2900.0, atol=1e-3)
assert np.isclose(monthly_fee(100_000 + 1e-6), 2700.0, atol=1e-3)
assert np.isclose(monthly_fee(100_000), 2700.0)
# a continuous design: 2.7% only on the volume above the threshold
def marginal_fee(volume):
    return 0.029 * min(volume, 100_000) + 0.027 * max(volume - 100_000, 0)


assert np.isclose(marginal_fee(100_000 - 1e-6), marginal_fee(100_000 + 1e-6), atol=1e-3)
# Q24.1: a tiered per-payment fee jumps from 29.30 to 25.30 at USD 1,000
assert np.isclose(0.029 * 1000 + 0.30, 29.30) and np.isclose(0.025 * 1000 + 0.30, 25.30)
# Q24.2: volume above 100,000 at which the fee is back to 2,900
assert np.isclose(2900 / 0.027, 107_407.41, atol=5e-3)


def figure():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ink, muted, accent, bad = "#1f2937", "#6b7280", "#4f46e5", "#b91c1c"
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch24", "font.family": "Helvetica",
        "text.color": ink,
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": muted, "axes.labelcolor": ink, "xtick.color": muted,
        "ytick.color": muted, "grid.color": "#e5e7eb"})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9), dpi=100)
    z = np.linspace(-6, 6, 400)
    ax1.plot(z, sigmoid(z), color=accent, label="sigmoid: continuous")
    ax1.plot([-6, 0], [0, 0], color=bad, linestyle="--")
    ax1.plot([0, 6], [1, 1], color=bad, linestyle="--", label="hard threshold: a jump")
    ax1.set_xlabel("risk score minus threshold")
    ax1.set_ylabel("output")
    ax1.set_ylim(-0.05, 1.5)
    ax1.set_yticks([0, 0.5, 1])
    ax1.legend(frameon=False, fontsize=10, loc="upper left")
    ax1.set_title("Smooth versus step", fontsize=11, color=ink, loc="left")

    lo = np.linspace(90, 100, 50)
    hi = np.linspace(100, 110, 50)
    ax2.plot(lo, 0.029 * lo * 1000, color=accent)
    ax2.plot(hi, 0.027 * hi * 1000, color=accent)
    ax2.plot([100], [2900], marker="o", markersize=6, markerfacecolor="white",
             markeredgecolor=accent, linestyle="none")
    ax2.plot([100], [2700], marker="o", markersize=6, color=accent, linestyle="none")
    ax2.annotate("jump of USD 200", xy=(100, 2800), xytext=(101.3, 2640), color=bad,
                 fontsize=10)
    ax2.plot([100, 100], [2700, 2900], color=bad, linestyle=":", linewidth=1)
    ax2.set_xlabel("monthly volume (USD thousand)")
    ax2.set_ylabel("monthly fee (USD)")
    ax2.set_title("A pricing tier that jumps", fontsize=11, color=ink, loc="left")
    fig.tight_layout()
    out = Path(__file__).resolve().parent.parent / "volume-1-assets"
    out.mkdir(exist_ok=True)
    if out.is_dir():
        fig.savefig(out / "ch24-continuity.svg", bbox_inches="tight",
                    metadata={"Date": None})


figure()
