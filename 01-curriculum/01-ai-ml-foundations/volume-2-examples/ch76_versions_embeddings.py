"""Chapter 76. Dataset versions by content hash, snapshot storage, and why a new
embedding model invalidates an index built with the old one."""
import hashlib

import numpy as np

# ---- 1. A dataset version is a hash of its content -------------------------------
rows = ["pay_001,m_17,4200,approved", "pay_002,m_17,1999,declined",
        "pay_003,m_42,650,approved"]


def version_id(rows):
    return hashlib.sha256("\n".join(rows).encode()).hexdigest()[:12]


v_a = version_id(rows)
v_b = version_id(rows[:2] + ["pay_003,m_42,651,approved"])     # one cent changed
print("snapshot A", v_a)
print("snapshot B", v_b, "(one amount changed by one cent)")
assert v_a != v_b and version_id(list(rows)) == v_a

# ---- 2. Storage for 30 daily snapshots of a 40 GB table --------------------------
size_gb, days, changed = 40, 30, 0.05
full_copies = size_gb * days
copy_on_write = size_gb + (days - 1) * changed * size_gb
print(f"\nfull copies {full_copies} GB, copy-on-write {copy_on_write:.0f} GB, "
      f"ratio {full_copies / copy_on_write:.1f}x")
assert full_copies == 1200 and np.isclose(copy_on_write, 98.0)

index_gb = 2_000_000 * 384 * 4 / 1e9          # merchants x dimensions x 4 bytes
print(f"index of 2 million 384-d float32 vectors: {index_gb:.2f} GB")
assert np.isclose(index_gb, 3.072)

# ---- 3. Two embedding models, the same meaning, different coordinates ------------
# By hand in 2-D: model v2 is model v1 turned by 90 degrees.
v1 = {"cafe": np.array([1.0, 0.0]), "gym": np.array([0.0, 1.0])}
turn = np.array([[0.0, -1.0], [1.0, 0.0]])
v2 = {name: turn @ vec for name, vec in v1.items()}
query = v2["cafe"]                              # the query is embedded by v2
scores = {name: float(query @ vec) for name, vec in v1.items()}   # index is v1
print("\nv2 query for 'cafe' against the v1 index:", scores)
assert scores == {"cafe": 0.0, "gym": 1.0}

# At scale: 500 merchants, 32 dimensions, v2 = v1 under a random orthogonal map.
rng = np.random.default_rng(76)
E1 = rng.normal(size=(500, 32))
E1 /= np.linalg.norm(E1, axis=1, keepdims=True)
Q, R = np.linalg.qr(rng.normal(size=(32, 32)))
Q = Q * np.sign(np.diag(R))                     # a random orthogonal matrix
E2 = E1 @ Q                                     # same geometry, new coordinates


def hit_rate(queries, index):
    """Share of merchants whose own vector is the top result."""
    return float(np.mean(np.argmax(queries @ index.T, axis=1) == np.arange(500)))


noisy = rng.normal(scale=0.02, size=E1.shape)   # a query is never an exact copy
print(f"v1 query, v1 index: {hit_rate(E1 + noisy, E1):.3f}")
print(f"v2 query, v2 index: {hit_rate((E1 + noisy) @ Q, E2):.3f}")
print(f"v2 query, v1 index: {hit_rate((E1 + noisy) @ Q, E1):.3f}")
print(f"mean cosine between a merchant's v1 and v2 vectors: "
      f"{np.mean(np.sum(E1 * E2, axis=1)):+.3f}")
assert np.allclose(E1 @ E1.T, E2 @ E2.T)        # every pairwise similarity survives
assert hit_rate((E1 + noisy) @ Q, E2) == 1.0
assert hit_rate((E1 + noisy) @ Q, E1) < 0.05
