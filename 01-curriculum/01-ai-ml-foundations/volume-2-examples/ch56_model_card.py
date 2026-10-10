"""Chapter 56: checking a model against the release gates in its PRD and writing
the numbers into a model card. Counts are illustrative.
"""
import json

import numpy as np

# Evaluation counts for PayFlow's payment-risk model v3.2 at its block threshold.
# slice: (fraud payments, fraud caught, good payments, good payments blocked)
COUNTS = {
    "in person": (50, 45, 20_000, 80),
    "online, established merchant": (110, 93, 30_000, 240),
    "online, merchant under 90 days": (40, 26, 4_000, 60),
}
GATES = {"overall recall": (">=", 0.80), "worst-slice recall": (">=", 0.75),
         "overall false-positive rate": ("<=", 0.010), "p95 latency ms": ("<=", 80)}


def rates(fraud, caught, good, blocked):
    return {"recall": caught / fraud, "false_positive_rate": blocked / good}


by_slice = {name: rates(*c) for name, c in COUNTS.items()}
total = np.sum(list(COUNTS.values()), axis=0)
overall = rates(*total)
measured = {"overall recall": overall["recall"],
            "worst-slice recall": min(s["recall"] for s in by_slice.values()),
            "overall false-positive rate": overall["false_positive_rate"],
            "p95 latency ms": 62}


def passes(value, rule):
    op, limit = rule
    return value >= limit if op == ">=" else value <= limit


gate_results = {g: passes(measured[g], rule) for g, rule in GATES.items()}
card = {
    "model": "payment-risk v3.2 (gradient-boosted trees)",
    "intended_use": "score card payments before authorization",
    "out_of_scope": ["credit decisions", "merchant onboarding"],
    "metrics_by_slice": {k: {m: round(v, 3) for m, v in s.items()}
                         for k, s in by_slice.items()},
    "caveats": [g for g, ok in gate_results.items() if not ok],
}

for name, s in by_slice.items():
    print(f"{name:31s} recall {s['recall']:.3f}  FPR {s['false_positive_rate']:.4f}")
for g, ok in gate_results.items():
    print(f"gate {g:28s} {measured[g]:7.3f} {GATES[g][0]} {GATES[g][1]:<6} "
          f"{'pass' if ok else 'FAIL'}")
print("ship:", all(gate_results.values()),
      "| card caveats:", json.dumps(card["caveats"]))

# ---- checks against the hand-worked numbers ----
assert np.isclose(by_slice["in person"]["recall"], 0.90)
assert np.isclose(by_slice["online, merchant under 90 days"]["recall"], 0.65)
assert np.isclose(overall["recall"], 164 / 200)
assert np.isclose(overall["false_positive_rate"], 380 / 54_000)
assert not all(gate_results.values())
