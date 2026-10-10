"""Chapter 40. Minimax, alpha-beta pruning and expectimax on one small tree.

PayFlow (MAX) picks one of three fraud rule sets. A fraud ring (MIN) then picks
one of three attacks. A leaf is PayFlow's net saving that week, in USD thousands.
"""
import math
import random

RULES = ["A", "B", "C"]
TREE = [[3, 5, 4], [2, 6, 7], [6, 1, 8]]      # TREE[rule][attack]
ATTACK_MIX = [0.5, 0.3, 0.2]                  # how often each attack is seen


def minimax(node, maximizing):
    if not isinstance(node, list):            # a leaf: just report its value
        return node
    values = [minimax(child, not maximizing) for child in node]
    return max(values) if maximizing else min(values)


def alphabeta(node, maximizing, alpha=-math.inf, beta=math.inf, seen=None):
    """alpha: the best MAX can already force. beta: the best MIN can force."""
    if not isinstance(node, list):
        if seen is not None:
            seen.append(node)                 # record every leaf we evaluate
        return node
    value = -math.inf if maximizing else math.inf
    for child in node:
        score = alphabeta(child, not maximizing, alpha, beta, seen)
        if maximizing:
            value = max(value, score)
            alpha = max(alpha, value)
        else:
            value = min(value, score)
            beta = min(beta, value)
        if alpha >= beta:                     # the opponent will avoid this branch
            break                             # so skip its remaining children
    return value


def expectimax(tree, mix):
    """MAX moves, then chance picks the attack with probabilities `mix`."""
    return [sum(p * leaf for p, leaf in zip(mix, leaves)) for leaves in tree]


if __name__ == "__main__":
    worst = [min(leaves) for leaves in TREE]
    print("worst case per rule:", dict(zip(RULES, worst)),
          "-> minimax value", minimax(TREE, True))
    seen = []
    value = alphabeta(TREE, True, seen=seen)
    leaves = [leaf for branch in TREE for leaf in branch]
    print("alpha-beta value", value, "| leaves evaluated:", seen,
          f"({len(seen)} of {len(leaves)})")
    averages = expectimax(TREE, ATTACK_MIX)
    print("expectimax per rule:", dict(zip(RULES, [round(v, 1) for v in averages])),
          "-> choose", RULES[averages.index(max(averages))])
    b, d = 30, 6
    print(f"b = {b}, d = {d}: minimax evaluates {b ** d:,} leaves,",
          f"alpha-beta at best {2 * b ** (d // 2) - 1:,}")

    # Checks against the hand trace in the chapter.
    assert worst == [3, 2, 1] and minimax(TREE, True) == value == 3
    assert seen == [3, 5, 4, 2, 6, 1]         # 6 and 7 under B, 8 under C are pruned
    assert [round(v, 1) for v in averages] == [3.8, 4.2, 4.9]
    assert 2 * 30 ** 3 - 1 == 53_999 and 30 ** 6 == 729_000_000
    # Alpha-beta always returns the minimax value: 200 random depth-3 trees.
    rng = random.Random(40)
    for _ in range(200):
        t = [[[rng.randint(-9, 9) for _ in range(3)] for _ in range(3)]
             for _ in range(3)]
        assert alphabeta(t, True) == minimax(t, True)
    # Check yourself: visiting rule C first, alpha-beta prunes nothing.
    seen = []
    alphabeta([TREE[2], TREE[1], TREE[0]], True, seen=seen)
    assert len(seen) == 9
    mix = expectimax(TREE, [0.2, 0.2, 0.6])
    assert [round(v, 1) for v in mix] == [4.0, 5.8, 6.2]
