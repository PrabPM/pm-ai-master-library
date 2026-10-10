"""Chapter 60: ranking uncertain machine-learning bets and valuing a staged plan.
Illustrative numbers.
"""
import numpy as np

# name: reach per quarter, impact, (data, model, compliance) confidence,
#       (build, labeling, evaluation) effort in person-months
bets = {
    "payout-delay explainer": (8_000, 1, (1.0, 0.8, 1.0), (2, 0, 1)),
    "dispute evidence assistant": (3_000, 2, (0.8, 0.8, 1.0), (4, 1, 1)),
    "voice fraud detection": (20_000, 2, (0.5, 0.5, 0.8), (8, 6, 2)),
    "dynamic pricing": (1_500, 3, (0.8, 0.5, 0.5), (6, 0, 2)),
}


def classic_rice(reach, impact, conf, effort):
    """One blanket 80% confidence, and only the build effort counted."""
    return reach * impact * 0.8 / effort[0]


def ml_rice(reach, impact, conf, effort):
    """Confidence is a product of three risks; effort includes labels and evals."""
    return reach * impact * float(np.prod(conf)) / sum(effort)


rank = lambda f: sorted(bets, key=lambda k: -f(*bets[k]))
print(f"{'bet':27s} classic  rank   adapted  rank")
for name, b in bets.items():
    print(f"{name:27s} {classic_rice(*b):7,.0f} {rank(classic_rice).index(name) + 1:5d}"
          f"   {ml_rice(*b):7,.0f} {rank(ml_rice).index(name) + 1:5d}")

# A staged plan for the riskiest bet, in USD thousand.
p_feasible, payoff, build_cost, spike_cost = 0.4, 900, 300, 20
commit_all = p_feasible * payoff - build_cost
staged = -spike_cost + p_feasible * (payoff - build_cost)
print(f"commit everything: {commit_all:.0f}   spike first: {staged:.0f}   "
      f"value of the spike: {staged - commit_all:.0f}")

# ---- checks against the hand-worked numbers ----
assert np.isclose(ml_rice(*bets["dispute evidence assistant"]), 640.0)
assert np.isclose(ml_rice(*bets["voice fraud detection"]), 500.0)
assert np.isclose(classic_rice(*bets["voice fraud detection"]), 4000.0)
assert rank(classic_rice)[0] == "voice fraud detection"
assert rank(ml_rice)[0] == "payout-delay explainer"
assert np.isclose(commit_all, 60.0) and np.isclose(staged, 220.0)
