"""Chapter 39. A* on a small grid with three heuristics.

A PayFlow technician walks from the service desk S to a broken card reader G on
a food-hall floor. Each step up, down, left or right costs 1; # is a stall.
"""
import heapq

GRID = [".....#G",
        ".#.....",
        "S......",
        ".......",
        "......."]
ROWS, COLS = len(GRID), len(GRID[0])
START = next((r, c) for r in range(ROWS) for c in range(COLS) if GRID[r][c] == "S")
GOAL = next((r, c) for r in range(ROWS) for c in range(COLS) if GRID[r][c] == "G")


def neighbors(cell):
    r, c = cell
    for nr, nc in ((r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)):
        if 0 <= nr < ROWS and 0 <= nc < COLS and GRID[nr][nc] != "#":
            yield (nr, nc)


def manhattan(cell):
    return abs(cell[0] - GOAL[0]) + abs(cell[1] - GOAL[1])


def a_star(h):
    """Expand the frontier cell with the lowest f = g + h. Returns (path, expanded)."""
    frontier = [(h(START), h(START), 0, START, [START])]   # (f, h, tie, cell, path)
    best_g, expanded, tie = {START: 0}, [], 0
    while frontier:
        f, _, _, cell, path = heapq.heappop(frontier)
        if cell in expanded:
            continue
        expanded.append(cell)
        if cell == GOAL:
            return path, expanded
        g = len(path) - 1                      # cost so far: one per step
        for nxt in neighbors(cell):
            if g + 1 < best_g.get(nxt, float("inf")):      # a cheaper way to nxt
                best_g[nxt] = g + 1
                tie += 1
                heapq.heappush(frontier,
                               (g + 1 + h(nxt), h(nxt), tie, nxt, path + [nxt]))
    return None, expanded


HEURISTICS = {"h = 0 (uniform-cost)": lambda cell: 0,
              "h = Manhattan": manhattan,
              "h = 3 x Manhattan": lambda cell: 3 * manhattan(cell)}

if __name__ == "__main__":
    results = {name: a_star(h) for name, h in HEURISTICS.items()}
    for name, (path, expanded) in results.items():
        print(f"{name:<21} path cost {len(path) - 1:>2}   "
              f"cells expanded {len(expanded)}")

    # True cost-to-go h*(n) for every cell, by uniform-cost search from the goal.
    true_cost, queue = {GOAL: 0}, [GOAL]
    while queue:
        cell = queue.pop(0)
        for nxt in neighbors(cell):
            if nxt not in true_cost:
                true_cost[nxt] = true_cost[cell] + 1
                queue.append(nxt)
    admissible = all(manhattan(c) <= true_cost[c] for c in true_cost)
    consistent = all(manhattan(c) <= 1 + manhattan(n)
                     for c in true_cost for n in neighbors(c))
    inflated_ok = all(3 * manhattan(c) <= true_cost[c] for c in true_cost)
    print(f"Manhattan admissible: {admissible}, consistent: {consistent};",
          f"3 x Manhattan admissible: {inflated_ok}")

    # Checks against the chapter.
    costs = [len(path) - 1 for path, _ in results.values()]
    counts = [len(expanded) for _, expanded in results.values()]
    assert costs == [8, 8, 10] and true_cost[START] == 8
    assert counts[0] > counts[1] > counts[2]
    assert admissible and consistent and not inflated_ok
    assert manhattan(START) == 8 and 3 * manhattan(START) == 24
    # Hand trace: f at the cell just left of the wall, (0, 4), reached in 6 steps.
    assert 6 + manhattan((0, 4)) == 8 and 6 + 3 * manhattan((0, 4)) == 12
    assert 7 + 3 * manhattan((1, 4)) == 16 < 1 + 3 * manhattan((2, 1)) == 22
    assert 7 + manhattan((1, 4)) == 10 > 1 + manhattan((2, 1)) == 8
    # Answers to Check yourself.
    half_path, half_expanded = a_star(lambda cell: 0.5 * manhattan(cell))
    assert len(half_path) - 1 == 8 and counts[1] < len(half_expanded) < counts[0]
    assert (4 + 0, 4 + 5, 4 + 3 * 5) == (4, 9, 19)
