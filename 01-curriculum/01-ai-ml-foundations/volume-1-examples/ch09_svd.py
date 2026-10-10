"""Chapter 9. Singular value decomposition and low-rank approximation."""
import numpy as np

X = np.array([[12, 5], [8, 6], [4, 8], [6, 8], [10, 8]], dtype=float)
Xc = X - X.mean(axis=0)               # the centered merchant table from Chapter 8

U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
rank1 = s[0] * np.outer(U[:, 0], Vt[0])          # keep only the strongest piece
print("singular values:", np.round(s, 4), " squared / (n - 1):", s**2 / 4)
print(f"rank-1 error: {np.linalg.norm(Xc - rank1):.4f}")

# Payments per weekday (Mon..Sun, in tens) for the five merchants.
week = np.array([[14, 14, 15, 15, 18, 24, 19],
                 [12, 12, 13, 13, 16, 20, 12],
                 [11, 11, 12, 12, 14, 13, 11],
                 [12, 13, 13, 14, 16, 17, 13],
                 [16, 16, 17, 18, 22, 22, 15]], dtype=float)
Uw, sw, Vtw = np.linalg.svd(week, full_matrices=False)
kept = np.cumsum(sw**2) / np.sum(sw**2)
print("week singular values:", np.round(sw, 2))
for k in (1, 2):
    approx = (Uw[:, :k] * sw[:k]) @ Vtw[:k]      # best rank-k approximation
    worst = np.abs(week - approx).max()
    print(f"rank {k}: keeps {kept[k - 1]:.2%}, worst cell error {worst:.2f}")

# Checks against the hand calculation in the chapter.
assert np.allclose(Xc.T @ Xc, [[40, -12], [-12, 8]])
assert np.allclose(s, [np.sqrt(44), 2]) and np.allclose(s**2 / 4, [11, 1])
assert np.allclose(np.abs(Vt[0]), np.array([3, 1]) / np.sqrt(10))
hand_u1 = np.array([14, 1, -13, -7, 5]) / np.sqrt(440)
assert np.isclose(abs(U[:, 0] @ hand_u1), 1)
assert np.isclose(np.linalg.norm(Xc - rank1), 2)          # equals sigma_2
assert np.allclose((U * s) @ Vt, Xc)                      # U S V^T rebuilds Xc
assert np.allclose(U.T @ U, np.eye(2)) and np.allclose(Vt @ Vt.T, np.eye(2))
assert np.allclose(Xc @ Vt[0], s[0] * U[:, 0])            # A v = sigma u
tail = np.sqrt(np.sum(sw[2:] ** 2))                       # Eckart-Young error
assert np.isclose(np.linalg.norm(week - approx), tail)
assert np.allclose(week.mean(axis=1), X.sum(axis=1))      # matches the merchant table
assert 1 * (5 + 7 + 1) == 13 and 10 * (1_000_000 + 365 + 1) == 10_003_660

# Answers to Check yourself.
D = np.array([[3.0, 0.0], [0.0, -2.0]])
assert np.allclose(np.linalg.svd(D, compute_uv=False), [3, 2])          # Q9.1
assert np.isclose(s[0] ** 2 / np.sum(s**2), 11 / 12)      # share kept by piece 1
assert 1_000_000 * 768 * 4 / 1e9 == 3.072                               # Q9.2
assert 1_000_000 * 64 * 4 / 1e9 == 0.256 and 768 * 64 == 49_152
