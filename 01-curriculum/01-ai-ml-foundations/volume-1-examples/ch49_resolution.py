"""Chapter 49: one first-order inference by resolution, for a KYB check.

A literal is (sign, predicate, arguments). Names starting with "?" are
variables; everything else is a constant. A clause is a set of literals joined
by OR. The names are invented. This is the smallest engine that can do the
example: no nested terms, and no renaming of variables between clauses.
"""
from collections import deque

KB = {
    "C1": frozenset({(False, "Owns", ("?p", "?b")), (False, "Sanctioned", ("?p",)),
                     (True, "HighRisk", ("?b",))}),   # Owns & Sanctioned -> HighRisk
    "C2": frozenset({(True, "Owns", ("dana", "acme"))}),
    "C3": frozenset({(True, "Owns", ("lee", "birch"))}),
    "C4": frozenset({(True, "Sanctioned", ("dana",))}),
}


def unify(args_a, args_b):
    """Find a substitution that makes two argument lists identical, or None."""
    theta = {}
    for a, b in zip(args_a, args_b):
        a, b = theta.get(a, a), theta.get(b, b)
        if a == b:
            continue
        if a.startswith("?"):
            theta[a] = b
        elif b.startswith("?"):
            theta[b] = a
        else:
            return None                     # two different constants: no match
    return theta


def substitute(clause, theta):
    return frozenset((sign, pred, tuple(theta.get(a, a) for a in args))
                     for sign, pred, args in clause)


def resolvents(c1, c2):
    """Cancel one literal of c1 against its opposite in c2; keep the rest."""
    for sign1, pred1, args1 in c1:
        for sign2, pred2, args2 in c2:
            if pred1 == pred2 and sign1 != sign2 and len(args1) == len(args2):
                theta = unify(args1, args2)
                if theta is not None:
                    rest = (c1 | c2) - {(sign1, pred1, args1), (sign2, pred2, args2)}
                    yield substitute(rest, theta), theta


def show(clause):
    if not clause:
        return "empty clause"
    return " v ".join(sorted(("" if sign else "~") + f"{pred}({', '.join(args)})"
                             for sign, pred, args in clause))


def prove(goal, kb, max_steps=200):
    """Refutation: assume the goal is false and search for a contradiction."""
    negated = frozenset({(not goal[0], goal[1], goal[2])})
    queue = deque([(negated, [f"assume the opposite: {show(negated)}"])])
    for _ in range(max_steps):
        if not queue:
            return None                     # nothing left to try: not provable
        clause, trace = queue.popleft()
        for name, other in kb.items():
            for result, theta in resolvents(clause, other):
                binding = "".join(f", {var} = {val}" for var, val in theta.items())
                step = trace + [f"with {name}{binding}: {show(result)}"]
                if not result:
                    return step             # contradiction found: goal proved
                queue.append((result, step))
    return None


for name, clause in KB.items():
    print(f"{name}: {show(clause)}")
for business in ("acme", "birch"):
    proof = prove((True, "HighRisk", (business,)), KB)
    print(f"goal: HighRisk({business})")
    if proof is None:
        print("  no proof found")
    else:
        for i, line in enumerate(proof, 1):
            print(f"  {i}. {line}")
        print("  contradiction, so the goal follows from the knowledge base")

acme = prove((True, "HighRisk", ("acme",)), KB)
assert acme is not None and len(acme) == 4 and acme[-1].endswith("empty clause")
assert prove((True, "HighRisk", ("birch",)), KB) is None
assert unify(("?p", "acme"), ("dana", "acme")) == {"?p": "dana"}
assert unify(("lee", "birch"), ("dana", "?b")) is None
