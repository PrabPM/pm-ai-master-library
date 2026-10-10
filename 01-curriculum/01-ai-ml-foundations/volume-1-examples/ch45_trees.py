"""Chapter 45: trees, on PayFlow's merchant onboarding (KYB) decision flow.

A node is either a leaf (a string: the decision) or a pair
(question, {answer: child node}).
"""
import numpy as np

kyb = ("registered?", {
    "no": "reject",
    "yes": ("identity verified?", {
        "no": "manual review",
        "yes": ("bank account matches?", {
            "no": "manual review",
            "yes": "approve"})})})


def is_leaf(node):
    return isinstance(node, str)


def count_nodes(node):
    return 1 if is_leaf(node) else 1 + sum(count_nodes(c) for c in node[1].values())


def count_leaves(node):
    return 1 if is_leaf(node) else sum(count_leaves(c) for c in node[1].values())


def height(node):
    """Edges on the longest path from this node down to a leaf."""
    return 0 if is_leaf(node) else 1 + max(height(c) for c in node[1].values())


def decide(node, answers, path=()):
    """Walk from the root to a leaf; the path taken is the explanation."""
    if is_leaf(node):
        return node, path
    question, children = node
    answer = answers[question]
    return decide(children[answer], answers, path + (f"{question} {answer}",))


def leaf_probabilities(node, pass_rate, reach=1.0, out=None):
    """Probability of ending at each decision if every check passes at pass_rate."""
    out = {} if out is None else out
    if is_leaf(node):
        out[node] = out.get(node, 0.0) + reach
        return out
    for answer, child in node[1].items():
        share = pass_rate if answer == "yes" else 1 - pass_rate
        leaf_probabilities(child, pass_rate, reach * share, out)
    return out


n = count_nodes(kyb)
print(f"nodes = {n}, edges = {n - 1}, leaves = {count_leaves(kyb)}, "
      f"height = {height(kyb)}")
assert (n, count_leaves(kyb), height(kyb)) == (7, 4, 3)

application = {"registered?": "yes", "identity verified?": "yes",
               "bank account matches?": "no"}
decision, path = decide(kyb, application)
print("decision:", decision)
print("because: ", " -> ".join(path))
assert decision == "manual review" and len(path) == 3

probs = leaf_probabilities(kyb, pass_rate=0.9)
print("shares at 90% per check:",
      {k: round(v, 3) for k, v in probs.items()})
print(f"approval with 3 checks: {0.9 ** 3:.3f}, with 4 checks: {0.9 ** 4:.3f}")
assert np.isclose(probs["approve"], 0.729) and np.isclose(sum(probs.values()), 1.0)
assert np.isclose(probs["manual review"], 0.171) and np.isclose(probs["reject"], 0.1)

# a decision-tree model: yes/no questions all the way down
depth, trees = 6, 200
print(f"binary tree of depth {depth}: at most {2 ** depth} leaves")
print(f"{trees} such trees: at most {trees * depth:,} comparisons per payment")
assert 2**depth == 64 and trees * depth == 1200
