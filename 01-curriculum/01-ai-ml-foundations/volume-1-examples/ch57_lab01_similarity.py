"""Chapter 57, Lab 1: three similarity measures on merchant embeddings."""
import numpy as np

q = np.array([3.0, 4.0, 0.0])                      # the query merchant
cands = {"A": np.array([6.0, 8.0, 0.0]),
         "B": np.array([3.0, 3.0, 1.0]),
         "C": np.array([0.0, 5.0, 5.0])}


def measures(q, v):
    dot = float(q @ v)
    cosine = dot / (np.linalg.norm(q) * np.linalg.norm(v))
    return dot, cosine, float(np.linalg.norm(q - v))


print("raw vectors     dot  cosine  distance")
for name, v in cands.items():
    print(f"{name:12s} {measures(q, v)[0]:6.1f}  {measures(q, v)[1]:6.4f}  "
          f"{measures(q, v)[2]:8.4f}")

print("unit vectors    dot  cosine  distance")
unit = lambda v: v / np.linalg.norm(v)
for name, v in cands.items():
    d, c, e = measures(unit(q), unit(v))
    print(f"{name:12s} {d:6.4f}  {c:6.4f}  {e:8.4f}")

# ---- checks against the hand results ----
assert np.allclose(measures(q, cands["A"]), (50.0, 1.0, 5.0))
assert np.isclose(measures(q, cands["B"])[1], 21 / (5 * np.sqrt(19)))
assert np.isclose(measures(q, cands["B"])[2], np.sqrt(2))
assert np.isclose(measures(q, cands["C"])[0], 20.0)
assert np.isclose(measures(q, cands["C"])[2], np.sqrt(35))
angle_c = np.degrees(np.arccos(measures(q, cands["C"])[1]))
assert np.isclose(angle_c, 55.6, atol=0.1)
for v in cands.values():          # on unit vectors: distance^2 = 2 - 2 cosine
    d, c, e = measures(unit(q), unit(v))
    assert np.isclose(e ** 2, 2 - 2 * c) and np.isclose(d, c)
