"""Chapter 10. High-dimensional spaces: what changes as dimensions pile up."""
from math import gamma, log, pi, sqrt

import numpy as np


def ball_share_of_cube(d):
    """Fraction of the cube [-1, 1]^d taken up by the unit ball inside it."""
    return pi ** (d / 2) / gamma(d / 2 + 1) / 2**d


def random_cosines(d, pairs, rng):
    """Cosine of the angle between pairs of random directions in d dimensions."""
    u = rng.standard_normal((pairs, d))
    v = rng.standard_normal((pairs, d))
    norms = np.linalg.norm(u, axis=1) * np.linalg.norm(v, axis=1)
    return np.sum(u * v, axis=1) / norms


def distances_to_query(d, n, rng):
    """Distances from one random query to n random points in the unit cube."""
    points = rng.random((n, d))
    query = rng.random(d)
    return np.linalg.norm(points - query, axis=1)


rng = np.random.default_rng(7)
print("   d  nearest  farthest  ratio  sqrt(d/6)  cosine std  1/sqrt(d)")
for d in (2, 10, 100, 1024):
    dist = distances_to_query(d, 1000, rng)
    cos = random_cosines(d, 20000, rng)
    print(f"{d:4d}  {dist.min():7.3f}  {dist.max():8.3f}  "
          f"{dist.max() / dist.min():5.1f}  {sqrt(d / 6):9.3f}  "
          f"{cos.std():10.4f}  {1 / sqrt(d):9.4f}")
    assert abs(cos.std() - 1 / sqrt(d)) < 0.1 / sqrt(d)
    if d >= 100:
        assert abs(np.sqrt(np.mean(dist**2)) - sqrt(d / 6)) < 0.10 * sqrt(d / 6)

shares = [ball_share_of_cube(d) for d in (2, 3, 10, 20)]
print("ball's share of its cube, d = 2, 3, 10, 20:",
      ", ".join(f"{s:.2g}" for s in shares))

# Johnson-Lindenstrauss bound (Dasgupta and Gupta's form) for n points.
n, eps = 1_000_000, 0.1
k = 4 * log(n) / (eps**2 / 2 - eps**3 / 3)
print(f"JL bound for {n:,} points at 10% distortion: {k:,.0f} dimensions")

# Checks against the hand calculation in the chapter.
assert np.isclose(1 / sqrt(1024), 0.03125)
assert np.isclose(sqrt(6 / 6), 1) and np.isclose(sqrt(600 / 6), 10)
assert np.isclose(0.25 / (1 / sqrt(1024)), 8)
assert np.isclose(shares[0], pi / 4) and np.isclose(shares[1], pi / 6)
assert shares[2] < 0.003 and shares[3] < 1e-7
assert 11_800 < k < 11_900

# Answers to Check yourself.
assert np.isclose(1 / sqrt(400), 0.05) and np.isclose(0.25 / 0.05, 5)   # Q10.1
assert np.isclose(sqrt(96 / 6), 4)                                      # Q10.2
