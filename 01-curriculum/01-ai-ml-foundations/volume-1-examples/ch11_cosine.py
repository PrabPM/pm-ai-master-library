"""Chapter 11. Cosine similarity, dot product and Euclidean distance compared."""
import numpy as np

merchants = ["Juniper", "Corner", "Northwind", "Harbor", "Summit"]
X = np.array([[12, 5], [8, 6], [4, 8], [6, 8], [10, 8]], dtype=float)
q = np.array([3.0, 4.0])              # a new merchant: 30 in-store, 40 online


def cosine(u, v):
    return (u @ v) / (np.linalg.norm(u) * np.linalg.norm(v))


dot = X @ q
cos = np.array([cosine(x, q) for x in X])
dist = np.linalg.norm(X - q, axis=1)

print("merchant     dot  cosine  distance")
for name, a, b, c in zip(merchants, dot, cos, dist):
    print(f"{name:10s} {a:5.0f}  {b:6.4f}  {c:8.3f}")
print("largest dot product: ", merchants[np.argmax(dot)])
print("largest cosine:      ", merchants[np.argmax(cos)])
print("smallest distance:   ", merchants[np.argmin(dist)])

Xn = X / np.linalg.norm(X, axis=1, keepdims=True)    # scale every row to length 1
qn = q / np.linalg.norm(q)
dist_n = np.linalg.norm(Xn - qn, axis=1)
print("after normalizing:", merchants[np.argmax(Xn @ qn)], merchants[np.argmin(dist_n)])

# Checks against the hand calculation in the chapter.
assert np.allclose(dot, [56, 48, 44, 50, 62])
assert np.allclose(cos, [56 / 65, 0.96, 44 / (5 * np.sqrt(80)), 1.0,
                         62 / (5 * np.sqrt(164))])
assert np.allclose(dist**2, [82, 29, 17, 25, 65])
assert merchants[np.argmax(dot)] == "Summit"
assert merchants[np.argmax(cos)] == "Harbor"
assert merchants[np.argmin(dist)] == "Northwind"
assert np.allclose(dist_n**2, 2 - 2 * cos)        # unit vectors: d^2 = 2 - 2 cos
assert np.allclose(Xn @ qn, cos)
assert np.array_equal(np.argsort(-(Xn @ qn)), np.argsort(dist_n))   # same ranking

# Answers to Check yourself.
assert np.isclose(cosine(np.array([2.0, 1.0]), np.array([200.0, 100.0])), 1)  # Q11.1
a, b, c = np.array([1.0, 0.0]), np.array([1.0, 1.0]), np.array([0.0, 1.0])
d_ac = 1 - cosine(a, c)
d_ab_bc = (1 - cosine(a, b)) + (1 - cosine(b, c))
assert np.isclose(d_ac, 1) and np.isclose(d_ab_bc, 2 - np.sqrt(2))            # Q11.2
assert d_ac > d_ab_bc                             # triangle inequality fails
assert np.isclose(np.sqrt(2 - 2 * 0.92), 0.4)                                 # Q11.3
