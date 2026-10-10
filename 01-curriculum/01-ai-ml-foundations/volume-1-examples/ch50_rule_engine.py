"""Chapter 50: a tiny rule engine for payment risk decisions.

A rule has a name, a condition on the facts, and one effect: either a decision
(allow, review, block) or a new fact that later rules can use.
"""
from dataclasses import dataclass
from typing import Callable, Optional

SEVERITY = {"allow": 0, "review": 1, "block": 2}


@dataclass
class Rule:
    name: str
    when: Callable[[dict], bool]
    decision: Optional[str] = None      # allow / review / block
    adds_fact: Optional[str] = None     # or: derive a fact for other rules


RULES = [
    Rule("R1 sanctioned owner", lambda f: f["owner_sanctioned"], decision="block"),
    Rule("R2 large amount on new device",
         lambda f: f["amount"] > 1000 and f["new_device"], adds_fact="risky_pattern"),
    Rule("R3 risky pattern, not verified",
         lambda f: f.get("risky_pattern") and not f["verified"], decision="review"),
    Rule("R4 model score 0.90 or more", lambda f: f["score"] >= 0.90,
         decision="block"),
    Rule("R5 trusted merchant", lambda f: f["trusted_merchant"], decision="allow"),
]


def decide(facts, rules, default="allow"):
    """Forward chaining, then the most severe decision wins."""
    facts, fired = dict(facts), []
    changed = True
    while changed:                      # keep going until no rule adds a new fact
        changed = False
        for rule in rules:
            if rule not in fired and rule.when(facts):
                fired.append(rule)
                if rule.adds_fact:
                    facts[rule.adds_fact] = True
                    changed = True
    votes = [r for r in fired if r.decision]
    if not votes:
        return default, ["no rule fired: default"]
    decision = max(votes, key=lambda r: SEVERITY[r.decision]).decision
    return decision, [r.name for r in fired]


def first_match(facts, rules, default="allow"):
    """The other common policy: the first decision rule that fires wins."""
    for rule in rules:
        if rule.decision and rule.when(facts):
            return rule.decision, [rule.name]
    return default, ["no rule fired: default"]


base = {"amount": 80, "new_device": False, "verified": True, "score": 0.10,
        "owner_sanctioned": False, "trusted_merchant": False}
cases = {
    "A ordinary payment": base,
    "B large, new device, unverified": dict(base, amount=2500, new_device=True,
                                            verified=False),
    "C trusted merchant, score 0.95": dict(base, trusted_merchant=True, score=0.95),
    "D trusted merchant, sanctioned owner": dict(base, trusted_merchant=True,
                                                 owner_sanctioned=True),
}
results = {}
for label, facts in cases.items():
    results[label], reasons = decide(facts, RULES)
    print(f"{label}: {results[label].upper()}")
    print("    because:", "; ".join(reasons))

case_c = cases["C trusted merchant, score 0.95"]
r5_first = [RULES[4]] + RULES[:4]
print("case C under 'first match wins':")
print("    rules in the order above ->", first_match(case_c, RULES)[0])
print("    R5 moved to the top      ->", first_match(case_c, r5_first)[0])

assert list(results.values()) == ["allow", "review", "block", "block"]
assert decide(case_c, RULES)[1] == ["R4 model score 0.90 or more",
                                    "R5 trusted merchant"]
assert decide(case_c, r5_first)[0] == "block"       # severity ignores order
assert first_match(case_c, RULES)[0] == "block"
assert first_match(case_c, r5_first)[0] == "allow"  # first-match depends on order
