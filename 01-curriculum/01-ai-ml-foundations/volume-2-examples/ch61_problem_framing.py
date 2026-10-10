"""Chapter 61: a framed problem as data, and choosing the cheapest approach that
meets the constraints. Illustrative numbers.
"""
from dataclasses import dataclass


@dataclass
class Frame:
    unit: str            # what one prediction is about
    target: str          # what is predicted, defined so it can be labeled
    horizon: str         # how far ahead, and when the answer becomes known
    action: str          # what the product does differently
    constraint: str      # the limit that rules approaches out
    decisions_per_year: int
    value_per_correct: float     # USD
    latency_limit_ms: float


@dataclass
class Approach:
    name: str
    accuracy: float
    cost_per_call: float         # USD
    latency_ms: float
    fixed_per_year: float        # USD: people, labels, monitoring


def net_value(frame, a):
    """Yearly value of the correct decisions minus running and fixed cost."""
    per_decision = a.accuracy * frame.value_per_correct - a.cost_per_call
    return frame.decisions_per_year * per_decision - a.fixed_per_year


def choose(frame, approaches):
    print(f"{frame.unit}: {frame.target}")
    best = None
    for a in approaches:
        ok = a.latency_ms <= frame.latency_limit_ms
        value = net_value(frame, a)
        print(f"  {a.name:26s} {'meets limit' if ok else 'too slow   '}"
              f"  net USD {value:10,.0f}")
        if ok and (best is None or value > net_value(frame, best)):
            best = a
    print("  choose:", best.name)
    return best


checkout = Frame("one card payment", "fraud reported within 90 days", "90 days",
                 "approve, challenge or block", "answer in 100 ms",
                 50_000_000, 0.05, 100)
support = Frame("one support ticket", "agent sends the draft unchanged", "same day",
                "draft a cited reply", "answer in 10 s", 110_000, 4.00, 10_000)
at_checkout = choose(checkout, [
    Approach("rules", 0.80, 0.00001, 2, 50_000),
    Approach("classical ML", 0.92, 0.0001, 10, 200_000),
    Approach("language model", 0.93, 0.002, 800, 150_000)])
for_support = choose(support, [
    Approach("rules (canned replies)", 0.30, 0.0, 5, 20_000),
    Approach("classical ML (intents)", 0.45, 0.0001, 20, 80_000),
    Approach("language model", 0.55, 0.01, 2_000, 60_000),
    Approach("language model + retrieval", 0.80, 0.02, 3_500, 120_000),
    Approach("agent", 0.85, 0.30, 12_000, 250_000)])

# ---- checks against the hand-worked numbers ----
ml = Approach("classical ML", 0.92, 0.0001, 10, 200_000)
assert abs(net_value(checkout, ml) - 2_095_000) < 1e-6
rag = Approach("language model + retrieval", 0.80, 0.02, 3_500, 120_000)
assert abs(net_value(support, rag) - 229_800) < 1e-6
assert at_checkout.name == "classical ML"
assert for_support.name == "language model + retrieval"
