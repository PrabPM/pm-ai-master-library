"""Chapter 59: demographic parity and equal opportunity on synthetic approvals
for PayFlow Capital, and why the two can pull apart. Illustrative data.
"""
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


def audit(approved, qualified, group):
    """Selection rate and true-positive rate per group, and the two gaps."""
    out = {}
    for g in ("A", "B"):
        m = group == g
        out[g] = (approved[m].mean(), approved[m & qualified].mean())
    dp_gap = abs(out["A"][0] - out["B"][0])        # demographic parity difference
    eo_gap = abs(out["A"][1] - out["B"][1])        # equal opportunity difference
    return out, dp_gap, eo_gap


# The hand example as arrays: 100 applicants per group.
group = np.array(["A"] * 100 + ["B"] * 100)
qualified = np.array([True] * 60 + [False] * 40 + [True] * 40 + [False] * 60)
approved = np.array([True] * 54 + [False] * 6 + [True] * 6 + [False] * 34
                    + [True] * 30 + [False] * 10 + [True] * 2 + [False] * 58)
hand, dp_hand, eo_hand = audit(approved, qualified, group)
ROW = "{:19s} {:5.2f}  {:5.2f} {:5.2f}  {:5.2f}  {:5.2f} {:5.2f}"
print("policy              sel A  sel B   gap  TPR A  TPR B   gap  B wrongly approved")
print(ROW.format("hand example", hand["A"][0], hand["B"][0], dp_hand,
                 hand["A"][1], hand["B"][1], eo_hand))

# A larger synthetic book: same score quality in both groups, different base rates.
rng = np.random.default_rng(59)
n = 20_000
grp = np.where(rng.random(n) < 0.5, "A", "B")
qual = rng.random(n) < np.where(grp == "A", 0.60, 0.40)
thin_file = np.where(grp == "B", 0.4, 0.0)              # B has shorter histories
score = rng.normal(np.where(qual, 1.0, -1.0) - thin_file, 1.0)   # higher is safer


def decide(thr_a, thr_b):
    return score > np.where(grp == "A", thr_a, thr_b)


def thr_for(mask, rate):
    """Threshold that approves the given share of the masked applicants."""
    return float(np.quantile(score[mask], 1 - rate))


policies = {"one threshold": decide(0.0, 0.0)}
tpr_a = policies["one threshold"][(grp == "A") & qual].mean()
sel_a = policies["one threshold"][grp == "A"].mean()
policies["equal opportunity"] = decide(0.0, thr_for((grp == "B") & qual, tpr_a))
policies["demographic parity"] = decide(0.0, thr_for(grp == "B", sel_a))
results = {}
for name, appr in policies.items():
    res, dp, eo = audit(appr, qual, grp)
    bad = appr[(grp == "B") & ~qual].mean()             # unqualified B approved
    results[name] = (res, dp, eo)
    print(ROW.format(name, res["A"][0], res["B"][0], dp, res["A"][1], res["B"][1], eo)
          + f"  {bad:.2f}")

# ---- checks against the hand-worked numbers ----
assert np.isclose(hand["A"][0], 0.60) and np.isclose(hand["B"][0], 0.32)
assert np.isclose(hand["A"][1], 0.90) and np.isclose(hand["B"][1], 0.75)
assert np.isclose(dp_hand, 0.28) and np.isclose(eo_hand, 0.15)
assert results["equal opportunity"][2] < 0.01 < results["equal opportunity"][1]
assert results["demographic parity"][1] < 0.01 < results["demographic parity"][2]

# ---- figure ----
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0), dpi=100, sharey=True)
names = list(policies)
xpos = np.arange(len(names))
for ax, idx, title in [(axes[0], 0, "Selection rate"),
                       (axes[1], 1, "True-positive rate")]:
    ax.bar(xpos - 0.18, [results[k][0]["A"][idx] for k in names], 0.36,
           color="#4f46e5", label="group A")
    ax.bar(xpos + 0.18, [results[k][0]["B"][idx] for k in names], 0.36,
           color="#b45309", label="group B")
    ax.set_xticks(xpos, ["one\nthreshold", "equal\nopportunity", "demographic\nparity"])
    ax.set_title(title, fontsize=11, color="#1f2937")
    ax.grid(axis="y")
axes[0].set_ylim(0, 1.05)
axes[0].legend(frameon=False, loc="upper left", ncol=2, fontsize=10)
fig.savefig(ASSETS / "ch59-fairness-tradeoff.svg", bbox_inches="tight",
            metadata={"Date": None})
