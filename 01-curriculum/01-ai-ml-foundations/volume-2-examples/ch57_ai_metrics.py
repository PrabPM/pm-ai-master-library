"""Chapter 57: latency percentiles, throughput, drift (PSI) and cost per
inference for PayFlow's support assistant. Seeded synthetic data.
"""
import math
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


def percentile(values, p):
    """Nearest-rank percentile: the smallest value with at least p% at or below it."""
    ordered = np.sort(values)
    return float(ordered[math.ceil(p / 100 * len(ordered)) - 1])


def psi(expected_share, actual_share):
    """Population stability index over matching bins."""
    e, a = np.asarray(expected_share), np.asarray(actual_share)
    return float(np.sum((a - e) * np.log(a / e)))


hand = np.array([80, 85, 90, 95, 100, 110, 120, 150, 400, 900])     # milliseconds
print("ten requests: mean", hand.mean(), " p50", percentile(hand, 50),
      " p90", percentile(hand, 90), " p95", percentile(hand, 95))

rng = np.random.default_rng(57)
latency = rng.lognormal(mean=np.log(1.1), sigma=0.45, size=5000)    # seconds
slow = rng.random(5000) < 0.02                                      # cold starts
latency[slow] *= 5
p50, p95, p99 = (percentile(latency, p) for p in (50, 95, 99))
print(f"5,000 requests: mean {latency.mean():.2f}s  p50 {p50:.2f}s  p95 {p95:.2f}s"
      f"  p99 {p99:.2f}s  over the 3s target: {np.mean(latency > 3):.1%}")
workers = 12
print(f"throughput with {workers} workers: {workers / latency.mean():.1f} requests/s")

print("hand PSI:", round(psi([0.5, 0.5], [0.7, 0.3]), 4))
train_len = rng.lognormal(4.0, 0.6, 20_000)          # ticket length at training time
live_len = rng.lognormal(4.25, 0.6, 20_000)          # longer tickets this month
edges = np.quantile(train_len, np.linspace(0, 1, 11))[1:-1]
share = lambda x: np.bincount(np.searchsorted(edges, x), minlength=10) / len(x)
print(f"PSI of ticket length, 10 bins: {psi(share(train_len), share(live_len)):.3f}")

tokens_cost, fixed, requests, resolved = 3200.0, 1800.0, 400_000, 0.62
per_request = (tokens_cost + fixed) / requests
print(f"cost per inference USD {per_request:.4f}; "
      f"per resolved ticket USD {per_request / resolved:.4f}")

# ---- checks against the hand-worked numbers ----
assert hand.mean() == 213 and percentile(hand, 50) == 100
assert percentile(hand, 90) == 400 and percentile(hand, 95) == 900
assert np.isclose(psi([0.5, 0.5], [0.7, 0.3]), 0.1695, atol=5e-5)
assert np.isclose(per_request, 0.0125)
assert p50 < latency.mean() < p95 < p99

# ---- figure ----
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
ax.hist(np.clip(latency, 0, 8), bins=80, color="#cbd5e1")
for value, name, color in [(p50, "p50", "#15803d"), (latency.mean(), "mean", "#6b7280"),
                           (p95, "p95", "#b45309"), (p99, "p99", "#b91c1c")]:
    ax.axvline(value, color=color, lw=1.5)
    ax.text(value + 0.05, ax.get_ylim()[1] * (0.92 if name != "mean" else 0.60),
            f"{name} {value:.2f}s", color=color, fontsize=10)
ax.set_xlabel("response time, seconds (values above 8 shown at 8)")
ax.set_ylabel("requests")
fig.savefig(ASSETS / "ch57-latency-percentiles.svg", bbox_inches="tight",
            metadata={"Date": None})
