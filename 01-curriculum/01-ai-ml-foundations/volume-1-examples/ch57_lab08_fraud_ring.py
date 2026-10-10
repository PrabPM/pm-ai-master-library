"""Chapter 57, Lab 8: breadth-first search from a known fraudulent merchant."""
from collections import deque

edges = [("M1", "M2"), ("M2", "M3"), ("M3", "M4"), ("M4", "M7"), ("M5", "M6")]
nodes = [f"M{i}" for i in range(1, 9)]
graph = {n: [] for n in nodes}
for u, v in edges:                 # undirected: store each edge both ways
    graph[u].append(v)
    graph[v].append(u)


def bfs_distances(graph, start):
    """Hops from start to every merchant it can reach."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


dist = bfs_distances(graph, "M1")
print("hops from M1:", dist)
print("within 2 hops:", sorted(n for n, d in dist.items() if 0 < d <= 2))
print("never reached:", sorted(set(nodes) - set(dist)))
degrees = {n: len(graph[n]) for n in nodes}
print("degrees M1..M8:", list(degrees.values()),
      " sum", sum(degrees.values()), "= 2 x", len(edges), "edges")

# ---- checks against the hand results ----
assert dist == {"M1": 0, "M2": 1, "M3": 2, "M4": 3, "M7": 4}
assert sum(degrees.values()) == 2 * len(edges)          # handshake lemma
assert sorted(set(nodes) - set(dist)) == ["M5", "M6", "M8"]
