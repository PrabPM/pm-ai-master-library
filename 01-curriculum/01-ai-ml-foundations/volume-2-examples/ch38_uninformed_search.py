"""Chapter 38. Breadth-first, depth-first and uniform-cost search on a routing graph.

PayFlow must send a payout from its own bank (P) to a merchant's bank (M) through
partner banks A to F. An edge means "can send to"; the number is the fee in USD.
"""
import heapq

GRAPH = {"P": {"A": 1, "B": 8, "C": 2},
         "A": {"D": 1},
         "B": {"E": 5, "M": 9},
         "C": {"E": 3},
         "D": {"F": 1},
         "E": {"M": 4},
         "F": {"M": 12},
         "M": {}}


def search(start, goal, kind):
    """kind picks which path leaves the frontier next:
    "breadth" the oldest, "depth" the newest, "cost" the cheapest so far."""
    frontier = [(0, 0, [start])]              # (fee so far, arrival number, path)
    visited, arrivals = [], 0
    while frontier:
        if kind == "breadth":
            cost, _, path = frontier.pop(0)   # queue: first in, first out
        elif kind == "depth":
            cost, _, path = frontier.pop()    # stack: last in, first out
        else:
            cost, _, path = heapq.heappop(frontier)   # priority queue
        node = path[-1]
        if node in visited:                   # reached before by another path
            continue
        visited.append(node)
        if node == goal:
            return path, cost, visited
        children = list(GRAPH[node].items())
        if kind == "depth":
            children.reverse()                # so A is tried before B
        for nxt, fee in children:
            arrivals += 1
            entry = (cost + fee, arrivals, path + [nxt])
            if kind == "cost":
                heapq.heappush(frontier, entry)
            else:
                frontier.append(entry)
    return None, None, visited


if __name__ == "__main__":
    results = {kind: search("P", "M", kind) for kind in ("breadth", "depth", "cost")}
    for kind, (path, cost, visited) in results.items():
        print(f"{kind:<8} path {'-'.join(path):<10} hops {len(path) - 1}  fee {cost:>2}"
              f"  visited {' '.join(visited)}")
    b, d = 10, 6
    print(f"b = {b}, d = {d}: breadth-first frontier up to {b ** d:,} paths,",
          f"depth-first about {b * d}")

    # Checks against the hand trace in the chapter.
    assert results["breadth"][0] == ["P", "B", "M"] and results["breadth"][1] == 17
    assert results["breadth"][2] == list("PABCDEM")
    assert results["depth"][0] == ["P", "A", "D", "F", "M"]
    assert results["depth"][1] == 15
    assert results["depth"][2] == list("PADFM")
    assert results["cost"][0] == ["P", "C", "E", "M"] and results["cost"][1] == 9
    # Check yourself: with every fee equal to 1, uniform-cost finds a 2-hop path too.
    for node in GRAPH:
        for nxt in GRAPH[node]:
            GRAPH[node][nxt] = 1
    assert search("P", "M", "cost")[1] == 2 == len(search("P", "M", "breadth")[0]) - 1
