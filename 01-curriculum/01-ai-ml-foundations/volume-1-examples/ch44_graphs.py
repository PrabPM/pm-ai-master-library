"""Chapter 44: a payments network as a graph.

Nodes are PayFlow merchants (M), the devices they log in from (D) and the bank
accounts they are paid out to (B). An edge means "this merchant used this
device" or "this merchant is paid out to this bank account".
"""
from collections import defaultdict

edges = [("M1", "D1"), ("M1", "B1"), ("M2", "D1"), ("M2", "B2"), ("M3", "B2"),
         ("M3", "D2"), ("M3", "D1"),                 # three merchants, linked
         ("M4", "D3"), ("M4", "B3"),                 # an ordinary merchant
         ("M5", "D4"), ("M5", "B4")]                 # another ordinary merchant

# adjacency list: for every node, the set of its neighbors
adj = defaultdict(set)
for u, v in edges:
    adj[u].add(v)
    adj[v].add(u)                                    # undirected: store both ways
nodes = sorted(adj)

degree = {node: len(adj[node]) for node in nodes}
print(f"{len(nodes)} nodes, {len(edges)} edges")
print("degrees:", " ".join(f"{n}:{d}" for n, d in degree.items()))
print(f"sum of degrees = {sum(degree.values())} = 2 x {len(edges)} edges")
assert sum(degree.values()) == 2 * len(edges)        # handshake lemma


def connected_components(adj):
    """Group nodes that can reach each other. Chapter 46 explains the search."""
    seen, components = set(), []
    for start in sorted(adj):
        if start in seen:
            continue
        component, frontier = set(), [start]
        while frontier:
            node = frontier.pop()
            if node in component:
                continue
            component.add(node)
            frontier.extend(adj[node] - component)
        seen |= component
        components.append(sorted(component))
    return components


components = connected_components(adj)
for component in components:
    merchants = [n for n in component if n.startswith("M")]
    flag = "  <- review: several merchants linked" if len(merchants) > 1 else ""
    print(f"component of {len(component)}: {' '.join(component)}{flag}")

assert len(nodes) == 13 and len(edges) == 11
assert [len(c) for c in components] == [7, 3, 3]
assert components[0] == ["B1", "B2", "D1", "D2", "M1", "M2", "M3"]
assert degree["D1"] == 3 and degree["M3"] == 3 and degree["B2"] == 2

# memory: a matrix stores every possible pair, a list only the real edges
print(f"adjacency matrix cells: {len(nodes) ** 2}, "
      f"adjacency list entries: {sum(degree.values())}")
