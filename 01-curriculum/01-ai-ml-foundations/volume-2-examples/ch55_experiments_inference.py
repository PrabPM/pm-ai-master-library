"""Chapter 55: sample size for a classical test, Thompson sampling for a short
campaign, and the cost of language-model calls. Illustrative numbers and prices.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

ASSETS = Path(__file__).resolve().parent.parent / "volume-2-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})


def sample_size(p1, p2, alpha=0.05, power=0.80):
    """Visitors per arm for a two-sided test of two conversion rates."""
    z = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return int(np.ceil(z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2))


rates = np.array([0.040, 0.042, 0.045, 0.050])     # true conversion of four offers
rng = np.random.default_rng(55)
wins, losses = np.ones(4), np.ones(4)
shown = np.zeros(4)
history = []
for batch in range(40):                            # 40 batches of 1,000 visitors
    draws = rng.beta(wins, losses, size=(1000, 4)) # one belief per visitor per offer
    picks = np.bincount(draws.argmax(axis=1), minlength=4)
    conversions = rng.binomial(picks, rates)
    wins += conversions
    losses += picks - conversions
    shown += picks
    history.append(shown / shown.sum())
bandit = (wins - 1).sum()
equal = 40_000 * rates.mean()

calls, tok_in, tok_out = 1_000_000, 1500, 300
large = (tok_in * 3.00 + tok_out * 15.00) / 1e6    # USD per call, large model
small = (tok_in * 0.25 + tok_out * 1.25) / 1e6     # USD per call, small model
hit, to_small = 0.25, 0.60                         # cache hit rate, share routed down
before = calls * large
after = calls * (1 - hit) * (to_small * small + (1 - to_small) * large)

print("visitors per arm to detect 4% -> 5%:", sample_size(0.04, 0.05))
print("traffic share by offer:", np.round(shown / shown.sum(), 2))
print(f"conversions: bandit {bandit:.0f}, equal split would expect {equal:.0f}")
print(f"cost per call: large USD {large:.4f}, small USD {small:.5f}")
print(f"monthly bill: USD {before:,.0f} -> USD {after:,.2f} "
      f"({1 - after / before:.0%} lower)")

# ---- checks against the hand-worked numbers ----
assert abs(sample_size(0.04, 0.05) - 7.84 * 0.0859 / 0.0001) < 15
assert np.isclose(large, 0.009) and np.isclose(small, 0.00075)
assert np.isclose(before, 9000.0) and np.isclose(after, 3037.50)
assert shown.argmax() == 3 and bandit > equal

# ---- figure ----
history = np.array(history)
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
colors = ["#cbd5e1", "#6b7280", "#b45309", "#4f46e5"]
for k in range(4):
    ax.plot(np.arange(1, 41), history[:, k], color=colors[k], lw=2,
            label=f"offer {k + 1}: converts {rates[k]:.1%}")
ax.axhline(0.25, color="#1f2937", ls=":", lw=1.5, label="an equal split")
ax.set_xlabel("visitors so far, thousands")
ax.set_ylabel("cumulative share of traffic")
ax.set_ylim(0, 0.75)
ax.grid(axis="y")
ax.legend(frameon=False, loc="upper left", ncol=2, fontsize=10)
fig.savefig(ASSETS / "ch55-bandit-traffic.svg", bbox_inches="tight",
            metadata={"Date": None})
