"""Chapter 66: a launch rule with one primary metric and non-inferiority
guardrails. Illustrative experiment counts.
"""
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm

ASSETS = Path(__file__).resolve().parent.parent / "volume-2-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})

Z = norm.ppf(0.95)                       # one-sided 95%


def diff_and_se(p_control, p_treat, n):
    """Difference of two rates (treatment - control) and its standard error."""
    se = math.sqrt(p_control * (1 - p_control) / n + p_treat * (1 - p_treat) / n)
    return p_treat - p_control, se


def primary_wins(p_control, p_treat, n):
    d, se = diff_and_se(p_control, p_treat, n)
    return d - Z * se > 0, d - Z * se            # lower bound must clear zero


def guardrail_holds(p_control, p_treat, n, margin):
    d, se = diff_and_se(p_control, p_treat, n)
    return d + Z * se < margin, d + Z * se       # upper bound must stay under margin


n = 10_000                                       # merchants per arm
print("chance of a false alarm across 12 metrics:", round(1 - 0.95 ** 12, 2),
      "  Bonferroni level:", round(0.05 / 12, 4))
ok, low = primary_wins(0.040, 0.049, n)
print(f"primary: assisted resolution +0.9 pt, lower bound {low:+.4f} -> "
      f"{'win' if ok else 'no win'}")
guardrails = {"complaint rate": (0.020, 0.023, 0.005),
              "refund rate": (0.010, 0.009, 0.003)}
verdicts = [ok]
for name, (pc, pt, margin) in guardrails.items():
    held, high = guardrail_holds(pc, pt, n, margin)
    verdicts.append(held)
    print(f"{name + ':':15s} change {pt - pc:+.3f}, upper bound {high:+.4f}, "
          f"margin {margin:.3f} -> {'holds' if held else 'not shown safe'}")
print("decision:", "ship" if all(verdicts) else "hold")
held4, high4 = guardrail_holds(0.020, 0.023, 4 * n, 0.005)
print(f"same complaint rates with 40,000 per arm: upper bound {high4:+.4f} -> "
      f"{'holds' if held4 else 'not shown safe'}")

# ---- checks against the hand-worked numbers ----
d, se = diff_and_se(0.020, 0.023, n)
assert math.isclose(se, 0.002051, abs_tol=1e-6)
assert math.isclose(d + Z * se, 0.006374, abs_tol=2e-6)
assert math.isclose(1 - 0.95 ** 12, 0.46, abs_tol=0.005)
assert verdicts == [True, False, True] and held4

# ---- figure ----
rows = [("complaint rate\n10,000 per arm", 0.020, 0.023, n, 0.005),
        ("complaint rate\n40,000 per arm", 0.020, 0.023, 4 * n, 0.005),
        ("refund rate\n10,000 per arm", 0.010, 0.009, n, 0.003)]
fig, ax = plt.subplots(figsize=(7.2, 2.8), dpi=100)
for y, (label, pc, pt, m, margin) in enumerate(rows):
    d, se = diff_and_se(pc, pt, m)
    safe = d + Z * se < margin
    color = "#15803d" if safe else "#b91c1c"
    ax.plot([(d - Z * se) * 100, (d + Z * se) * 100], [y, y], color=color, lw=3)
    ax.plot([d * 100], [y], "o", color=color)
    ax.plot([margin * 100] * 2, [y - 0.3, y + 0.3], color="#1f2937", lw=2)
    ax.text(margin * 100, y - 0.38, "margin", color="#1f2937", fontsize=10,
            ha="center")
ax.axvline(0, color="#6b7280", lw=1)
ax.set_yticks(range(len(rows)), [r[0] for r in rows])
ax.set_ylim(-0.6, len(rows) - 0.4)
ax.invert_yaxis()
ax.set_xlabel("change in rate, percentage points (treatment minus control)")
ax.grid(axis="x")
fig.savefig(ASSETS / "ch66-guardrail-intervals.svg", bbox_inches="tight",
            metadata={"Date": None})
