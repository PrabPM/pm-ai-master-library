"""Chapter 68: a reliability diagram, expected calibration error and Platt
scaling on synthetic fraud scores.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression

ASSETS = Path(__file__).resolve().parent.parent / "volume-2-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def reliability(score, y, bins=10):
    """Per bin: count, average score (confidence), share of positives (accuracy)."""
    which = np.minimum((score * bins).astype(int), bins - 1)
    rows = [(int((which == b).sum()), score[which == b].mean(), y[which == b].mean())
            for b in range(bins) if (which == b).any()]
    return np.array(rows)


def ece(rows):
    """Expected calibration error: bin-size-weighted gap of the two columns."""
    n, conf, acc = rows.T
    return float(np.sum(n / n.sum() * np.abs(acc - conf)))


hand = np.array([(50, 0.2, 0.3), (30, 0.6, 0.5), (20, 0.9, 0.7)])
print("hand ECE:", round(ece(hand), 2))

rng = np.random.default_rng(68)
n = 40_000
true_logit = rng.normal(-1.0, 1.5, n)
y = rng.random(n) < 1 / (1 + np.exp(-true_logit))
raw = 1 / (1 + np.exp(-2.0 * true_logit))          # an overconfident model
fit, test = np.arange(n) < n // 2, np.arange(n) >= n // 2


platt = LogisticRegression(C=1e6).fit(logit(raw[fit]).reshape(-1, 1), y[fit])
fixed = platt.predict_proba(logit(raw[test]).reshape(-1, 1))[:, 1]
before, after = reliability(raw[test], y[test]), reliability(fixed, y[test])
print(f"ECE before {ece(before):.3f}   after Platt scaling {ece(after):.3f}")
print(f"learned slope {platt.coef_[0, 0]:.2f}, intercept {platt.intercept_[0]:.2f}")
top = before[-1]
print(f"top bin before: {int(top[0])} payments scored {top[1]:.2f} on average, "
      f"{top[2]:.2f} were fraud")

# ---- checks ----
assert np.isclose(ece(hand), 0.12)
assert ece(after) < 0.02 < ece(before)
assert abs(platt.coef_[0, 0] - 0.5) < 0.05

# ---- figure ----
fig, ax = plt.subplots(figsize=(4.6, 3.6), dpi=100)
ax.plot([0, 1], [0, 1], color="#6b7280", ls=":", lw=1.5, label="perfect")
ax.plot(before[:, 1], before[:, 2], "o-", color="#b91c1c", lw=2,
        label=f"raw score, ECE {ece(before):.3f}")
ax.plot(after[:, 1], after[:, 2], "o-", color="#15803d", lw=2,
        label=f"after Platt scaling, ECE {ece(after):.3f}")
ax.set_xlabel("average score in the bin")
ax.set_ylabel("share that were fraud")
ax.grid(True)
ax.legend(frameon=False, loc="upper left", fontsize=10)
fig.savefig(ASSETS / "ch68-reliability-diagram.svg", bbox_inches="tight",
            metadata={"Date": None})
