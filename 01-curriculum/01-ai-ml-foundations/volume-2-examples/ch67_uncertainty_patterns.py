"""Chapter 67: choosing an interface pattern from confidence, stakes and
reversibility. Illustrative numbers.
"""
from dataclasses import dataclass


@dataclass
class Feature:
    name: str
    p_correct: float        # measured share of outputs that are right
    cost_if_wrong: float    # USD lost when a wrong output goes through
    cost_to_confirm: float  # USD of a person's attention to check one output
    reversible: bool        # can the effect be undone cheaply afterwards?


def expected_error_cost(f):
    return (1 - f.p_correct) * f.cost_if_wrong


def pattern(f, min_useful=0.5):
    if f.p_correct < min_useful:
        return "abstain and offer a person"
    if f.reversible and expected_error_cost(f) <= f.cost_to_confirm:
        return "apply, show it, offer undo"
    if f.reversible:
        return "suggest; a person confirms"
    return "approval card before acting"


features = [
    Feature("categorize a transaction", 0.90, 0.50, 0.10, True),
    Feature("prefill dispute evidence", 0.95, 2.00, 0.20, True),
    Feature("draft a support reply", 0.80, 20.00, 0.50, True),
    Feature("refund USD 640", 0.97, 640.00, 0.10, False),
    Feature("promise a payout date", 0.35, 50.00, 0.50, True),
]
print(f"{'feature':26s} {'error cost':>10s}  {'confirm':>7s}  pattern")
for f in features:
    print(f"{f.name:26s} {expected_error_cost(f):10.2f}  {f.cost_to_confirm:7.2f}  "
          f"{pattern(f)}")

# ---- checks against the hand-worked numbers ----
assert abs(expected_error_cost(features[0]) - 0.05) < 1e-9
assert abs(expected_error_cost(features[3]) - 19.20) < 1e-9
assert pattern(features[0]) == "apply, show it, offer undo"
assert pattern(features[3]) == "approval card before acting"
assert pattern(features[4]) == "abstain and offer a person"
