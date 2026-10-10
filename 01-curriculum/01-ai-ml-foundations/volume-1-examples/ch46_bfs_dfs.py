"""Chapter 46: breadth-first and depth-first search on the chapter 44 network.

M1 has been confirmed as fraudulent. Which nodes can be reached from it, how
many hops away is each one, and how much work does the search do?
"""
from collections import deque

edges = [("M1", "D1"), ("M1", "B1"), ("M2", "D1"), ("M2", "B2"), ("M3", "B2"),
         ("M3", "D2"), ("M3", "D1"), ("M4", "D3"), ("M4", "B3"), ("M5", "D4"),
         ("M5", "B4")]
adj = {}
for u, v in edges:                       # adjacency lists, in the order given
    adj.setdefault(u, []).append(v)
    adj.setdefault(v, []).append(u)


def bfs(adj, start):
    """Visit in order of distance. Returns hop counts, parents and work done."""
    dist, parent = {start: 0}, {start: None}
    queue = deque([start])
    dequeued = edge_checks = 0
    while queue:
        node = queue.popleft()           # oldest first: a queue
        dequeued += 1
        for neighbor in adj[node]:
            edge_checks += 1
            if neighbor not in dist:     # the visited check: each node enters once
                dist[neighbor] = dist[node] + 1
                parent[neighbor] = node
                queue.append(neighbor)
    return dist, parent, dequeued, edge_checks


def dfs(adj, start):
    """Go as deep as possible before backing up. Returns the visit order."""
    order, seen = [], set()
    stack = [start]
    while stack:
        node = stack.pop()               # newest first: a stack
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        stack.extend(reversed(adj[node]))   # so the first neighbor is tried first
    return order


def path_to(parent, node):
    path = []
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


dist, parent, dequeued, edge_checks = bfs(adj, "M1")
print("BFS visit order:", " ".join(dist))
print("hops from M1:   ", " ".join(f"{n}:{d}" for n, d in dist.items()))
print("DFS visit order:", " ".join(dfs(adj, "M1")))
print("shortest path to D2:", " -> ".join(path_to(parent, "D2")))
within_two = sorted(n for n, d in dist.items() if 0 < d <= 2)
print("within 2 hops of M1:", " ".join(within_two))
component_edges = sum(1 for u, v in edges if u in dist)
print(f"work: {dequeued} nodes dequeued + {edge_checks} edge checks "
      f"(V = {len(dist)}, E = {component_edges}, 2E = {2 * component_edges})")

assert list(dist) == ["M1", "D1", "B1", "M2", "M3", "B2", "D2"]
assert dist == {"M1": 0, "D1": 1, "B1": 1, "M2": 2, "M3": 2, "B2": 3, "D2": 3}
assert dfs(adj, "M1") == ["M1", "D1", "M2", "B2", "M3", "D2", "B1"]
assert path_to(parent, "D2") == ["M1", "D1", "M3", "D2"]
assert dequeued == 7 and edge_checks == 14 == 2 * component_edges
assert "M4" not in dist and "M5" not in dist        # other components: unreachable
