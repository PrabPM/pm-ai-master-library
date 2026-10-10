"""Chapter 42. Monte Carlo tree search with UCT on a tiny game.

The game: a pile of 10 chips. Two players take turns removing 1, 2 or 3 chips.
Whoever takes the last chip wins. The known best first move is to take 2.
"""
import math
import random


class Node:
    def __init__(self, chips, parent=None, move=None):
        self.chips, self.parent, self.move = chips, parent, move
        self.children, self.visits, self.wins = [], 0, 0.0
        self.untried = [m for m in (1, 2, 3) if m <= chips]


def uct(wins, visits, parent_visits, c=math.sqrt(2)):
    """Average result plus a bonus that shrinks as the child is visited more."""
    return wins / visits + c * math.sqrt(math.log(parent_visits) / visits)


def mcts(chips, iterations, rng):
    root = Node(chips)
    for _ in range(iterations):
        node = root
        # 1. Selection: walk down while every move here has been tried once.
        while not node.untried and node.children:
            node = max(node.children,
                       key=lambda ch: uct(ch.wins, ch.visits, node.visits))
        # 2. Expansion: add one new child for an untried move.
        if node.untried:
            move = node.untried.pop(rng.randrange(len(node.untried)))
            node.children.append(Node(node.chips - move, node, move))
            node = node.children[-1]
        # 3. Simulation: finish the game with random moves.
        left, turns = node.chips, 0
        while left > 0:
            left -= rng.randint(1, min(3, left))
            turns += 1
        mover_won = turns % 2 == 0            # did the player who moved into node win?
        # 4. Backpropagation: update every node on the path, flipping the winner.
        while node is not None:
            node.visits += 1
            node.wins += mover_won
            mover_won = not mover_won
            node = node.parent
    return root


if __name__ == "__main__":
    # Hand example: three children after 30 visits to the parent.
    stats = {"take 1": (6, 10), "take 2": (9, 15), "take 3": (1, 5)}
    scores = {m: uct(w, n, 30) for m, (w, n) in stats.items()}
    print("UCT by hand:", {m: round(s, 3) for m, s in scores.items()})

    root = mcts(10, 3000, random.Random(42))
    print("pile of 10, after 3,000 iterations")
    for child in sorted(root.children, key=lambda ch: ch.move):
        print(f"take {child.move}: visits {child.visits:>4}  "
              f"win rate {child.wins / child.visits:.2f}")
    best = max(root.children, key=lambda ch: ch.visits)
    print("chosen move: take", best.move)

    assert [round(s, 3) for s in scores.values()] == [1.425, 1.273, 1.366]
    assert best.move == 2 and sum(ch.visits for ch in root.children) == 3000
    # Exact solution by backward induction: a pile is lost if it is a multiple of 4.
    wins = {0: False}
    for n in range(1, 11):
        wins[n] = any(not wins[n - m] for m in (1, 2, 3) if m <= n)
    assert [n for n in wins if not wins[n]] == [0, 4, 8]
    # Check yourself: UCT for 3 wins in 4 visits, parent visited 30 times.
    assert round(uct(3, 4, 30), 3) == 2.054
    # Check yourself: from 9 chips the winning move is to take 1.
    assert max(mcts(9, 3000, random.Random(42)).children,
               key=lambda ch: ch.visits).move == 1
