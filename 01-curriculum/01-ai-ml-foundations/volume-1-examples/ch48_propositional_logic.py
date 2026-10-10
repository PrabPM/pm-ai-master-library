"""Chapter 48: propositional logic and a truth-table check of payment rules.

H = amount is over USD 1,000     N = the device is new
V = customer passed 3-D Secure   B = block the payment
"""
from itertools import product


def implies(p, q):
    """p -> q is false only when p is true and q is false."""
    return (not p) or q


def tf(value):
    return "T" if value else "F"


# p -> q, (not p) or q, and the contrapositive (not q) -> (not p) agree in all rows
for p, q in product([True, False], repeat=2):
    assert implies(p, q) == ((not p) or q) == implies(not q, not p)
assert [implies(p, q) for p, q in product([True, False], repeat=2)] == \
    [True, False, True, True]

# De Morgan: not (H and N) is the same as (not H) or (not N), in every row
assert all((not (h and n)) == ((not h) or (not n))
           for h, n in product([True, False], repeat=2))


def check(rules):
    """For every input, list the decisions B that satisfy every rule."""
    report = {}
    for h, n, v in product([True, False], repeat=3):
        allowed = [b for b in (True, False) if all(rule(h, n, v, b) for rule in rules)]
        if not allowed:
            report[(h, n, v)] = "CONFLICT"
        elif len(allowed) == 2:
            report[(h, n, v)] = "no rule applies"
        else:
            report[(h, n, v)] = "block" if allowed[0] else "allow"
    return report


def r1(h, n, v, b):
    return implies(h and n, b)             # high amount on a new device -> block


def r2(h, n, v, b):
    return implies(v, not b)               # verified payments are never blocked


def r1_fixed(h, n, v, b):
    return implies(h and n and not v, b)   # ... -> block, unless verified


report = check([r1, r2])
print("H N V | policy {R1, R2}")
for (h, n, v), verdict in report.items():
    print(f"{tf(h)} {tf(n)} {tf(v)} | {verdict}")
fixed = check([r1_fixed, r2])
print("conflicts before the fix:", list(report.values()).count("CONFLICT"),
      "| after:", list(fixed.values()).count("CONFLICT"))

assert report[(True, True, True)] == "CONFLICT"
assert report[(True, True, False)] == "block"
assert list(report.values()).count("allow") == 3
assert list(report.values()).count("no rule applies") == 3
assert "CONFLICT" not in fixed.values() and fixed[(True, True, True)] == "allow"
