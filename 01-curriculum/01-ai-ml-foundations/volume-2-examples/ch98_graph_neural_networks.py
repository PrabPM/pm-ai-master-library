"""Chapter 98. Graph neural networks: message passing by hand on five merchants,
neighbor sampling, and attention over neighbors.

Run: python ch98_graph_neural_networks.py
"""
import numpy as np

# [listing]
# Five PayFlow merchants; an edge means "shares a device or a payout bank account".
edges = [(0, 1), (0, 2), (1, 2), (2, 3), (3, 4)]
A = np.zeros((5, 5))
for u, v in edges:
    A[u, v] = A[v, u] = 1
x = np.array([1.0, 1.0, 0.0, 0.0, 0.0])            # 1 = confirmed fraud


def layer(h, A, w_self=0.5, w_nbr=0.5):
    """Mean aggregation: mix each node's value with its neighbors' average."""
    return w_self * h + w_nbr * (A @ h) / A.sum(1)


h1 = layer(x, A)
h2 = layer(h1, A)
print("input   :", x)
print("1 layer :", h1.round(3))
print("2 layers:", h2.round(3))

rng = np.random.default_rng(0)
nbrs = np.flatnonzero(A[2])                        # merchant 2 has three neighbors
picked = rng.choice(nbrs, size=2, replace=False)   # sample two of them
print("sampled neighbors of merchant 2:", picked,
      "-> estimate", round(0.5 * x[2] + 0.5 * x[picked].mean(), 3))

scores = 2.0 * x[nbrs]                             # stand-in for a learned score
alpha = np.exp(scores) / np.exp(scores).sum()
print("attention weights of merchant 2:", alpha.round(3),
      "-> weighted neighbor value", round(float(alpha @ x[nbrs]), 3))
# [/listing]

h = x
for _ in range(30):
    h = layer(h, A)

# Hand-worked values
assert np.allclose(h1, [0.75, 0.75, 1 / 3, 0.0, 0.0])
assert np.allclose(h2, [0.375 + 0.5 * (0.75 + 1 / 3) / 2,
                        0.375 + 0.5 * (0.75 + 1 / 3) / 2,
                        0.5 / 3 + 0.5 * (0.75 + 0.75 + 0) / 3,
                        0.5 * (1 / 3 + 0) / 2,
                        0.0])
assert np.allclose(h2.round(3), [0.646, 0.646, 0.417, 0.083, 0.0])
# Attention: scores 2, 2, 0 -> e^2 / (2 e^2 + 1)
assert np.allclose(alpha, np.array([np.e ** 2, np.e ** 2, 1]) / (2 * np.e ** 2 + 1))
assert np.allclose(alpha.round(3), [0.468, 0.468, 0.063])
assert round(float(alpha @ x[nbrs]), 3) == 0.937
# The sampled estimate is one of the three possible pairs: mean 1.0 or 0.5
assert round(0.5 * x[picked].mean(), 3) in (0.5, 0.25)
# Over-smoothing: after many layers every node holds almost the same number,
# the degree-weighted average of the inputs (degrees 2, 2, 3, 2, 1)
deg = A.sum(1)
assert np.allclose(h, (deg @ x) / deg.sum(), atol=1e-2)
assert np.isclose((deg @ x) / deg.sum(), 0.4)

# Q98.1: merchant 3 after one layer if merchant 2 were confirmed fraud too
x_q = np.array([1.0, 1.0, 1.0, 0.0, 0.0])
assert np.isclose(layer(x_q, A)[3], 0.25)
# Q98.2: number of layers for merchant 4 to be affected by merchants 0 and 1
h3 = layer(h2, A)
assert h2[4] == 0.0 and h3[4] > 0
