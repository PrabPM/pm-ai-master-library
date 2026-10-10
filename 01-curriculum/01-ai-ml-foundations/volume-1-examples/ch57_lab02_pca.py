"""Chapter 57, Lab 2: how many dimensions do three merchant features have?"""
import numpy as np

# Eight merchants: monthly volume (USD thousand), payments (hundreds), disputes.
X = np.array([[120, 24, 3], [80, 17, 1], [200, 41, 2], [150, 29, 6],
              [60, 13, 2], [180, 35, 4], [100, 21, 5], [90, 18, 1]], dtype=float)

Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)     # standardize each column
C = Z.T @ Z / (len(Z) - 1)                           # correlation matrix
eigvals, eigvecs = np.linalg.eigh(C)
order = np.argsort(eigvals)[::-1]
eigvals, eigvecs = eigvals[order], eigvecs[:, order]
ratio = eigvals / eigvals.sum()

print("correlation volume~payments:", round(C[0, 1], 4))
print("eigenvalues:", np.round(eigvals, 4), " sum", round(eigvals.sum(), 4))
print("explained variance:", np.round(ratio, 4),
      " cumulative", np.round(np.cumsum(ratio), 4))
print("first component:", np.round(eigvecs[:, 0] * np.sign(eigvecs[0, 0]), 3))
sing = np.linalg.svd(Z, compute_uv=False)
print("singular values squared / (n - 1):", np.round(sing ** 2 / (len(Z) - 1), 4))

# ---- checks ----
assert np.isclose(eigvals.sum(), 3.0)                # trace of a correlation matrix
assert np.allclose(sing ** 2 / (len(Z) - 1), eigvals)
assert np.cumsum(ratio)[1] > 0.95 > np.cumsum(ratio)[0]
assert C[0, 1] > 0.99
