"""Chapter 50: dynamic pricing as rules plus a bandit. Illustrative numbers only."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-2-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})

VOLUME = 2_000_000.0          # yearly card volume of a mid-size merchant, USD
COST = 1.9                    # PayFlow's own cost, percent of volume
FLOOR, CAP = COST + 0.3, 2.9  # rules: keep 0.3 points of margin, never above list


def accept_prob(rate):
    """True share of merchants who accept a quote (unknown to PayFlow)."""
    return 1 / (1 + np.exp(-3.662 * (2.9 - rate)))


def margin(rate):
    """Yearly margin in USD if the merchant accepts this rate."""
    return (rate - COST) / 100 * VOLUME


grid = np.array([2.0, 2.3, 2.6, 2.9])                 # candidate rates, percent
allowed = grid[(grid >= FLOOR) & (grid <= CAP)]       # the rules act first
rng = np.random.default_rng(50)
wins = np.ones(len(allowed))                          # Beta(1, 1) prior per rate
losses = np.ones(len(allowed))
earned = 0.0
for quote in range(3000):                             # Thompson sampling
    belief = rng.beta(wins, losses)                   # one plausible accept rate each
    k = int(np.argmax(belief * margin(allowed)))      # best expected margin
    accepted = rng.random() < accept_prob(allowed[k])
    wins[k] += accepted
    losses[k] += not accepted
    earned += accepted * margin(allowed[k])

print("rules removed:", [float(r) for r in grid if r not in allowed])
for k, r in enumerate(allowed):
    n_k = int(wins[k] + losses[k] - 2)
    seen = f"{(wins[k] - 1) / n_k:.2f}" if n_k else "  - "
    print(f"rate {r:.1f}%  quoted {n_k:4d}  accepted {seen}  true {accept_prob(r):.2f}"
          f"  expected margin USD {accept_prob(r) * margin(r):6,.0f}")
flat = 3000 * accept_prob(2.9) * margin(2.9)
print(f"bandit earned USD {earned / 1e6:.2f} million; "
      f"list price for everyone would expect USD {flat / 1e6:.2f} million")

# ---- checks against the hand-worked table ----
hand = {2.3: 7_200.0, 2.6: 10_500.0, 2.9: 10_000.0}
for r, m in hand.items():
    assert np.isclose(accept_prob(r) * margin(r), m, rtol=2e-3), (r, m)
assert 2.0 not in allowed and allowed[int(np.argmax(wins + losses))] == 2.6

# ---- figure ----
r = np.linspace(1.9, 3.3, 200)
fig, ax = plt.subplots(figsize=(7.2, 3.4), dpi=100)
ax.axvspan(FLOOR, CAP, color="#eef2ff", label="allowed by the rules")
ax.plot(r, accept_prob(r) * margin(r) / 1000, color="#4f46e5", lw=2)
ax.plot(allowed, accept_prob(allowed) * margin(allowed) / 1000, "o", color="#1f2937")
ax.plot([2.0], [accept_prob(2.0) * margin(2.0) / 1000], "x", color="#b91c1c", ms=8)
for x, y, t, dx in [(2.3, 7.2, "2.3%: 7,200", -34), (2.6, 10.5, "2.6%: 10,500", -4),
                    (2.9, 10.0, "2.9%: 10,000", 44)]:
    ax.annotate(t, (x, y), textcoords="offset points", xytext=(dx, 10), ha="center",
                color="#1f2937")
ax.annotate("2.0%: below the floor", (2.0, accept_prob(2.0) * margin(2.0) / 1000),
            textcoords="offset points", xytext=(8, -14), color="#b91c1c")
ax.set_xlabel("quoted rate, percent of volume")
ax.set_ylabel("expected yearly margin, USD thousand")
ax.set_ylim(0, 13.5)
ax.grid(axis="y")
ax.legend(frameon=False, loc="lower right")
fig.savefig(ASSETS / "ch50-margin-curve.svg", bbox_inches="tight",
            metadata={"Date": None})
