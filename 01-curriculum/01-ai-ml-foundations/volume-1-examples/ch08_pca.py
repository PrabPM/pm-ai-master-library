"""Chapter 8. Principal component analysis, step by step, on the merchant table."""
import numpy as np

merchants = ["Juniper", "Corner", "Northwind", "Harbor", "Summit"]
# Columns: in-store and online payments per day, in tens.
X = np.array([[12, 5], [8, 6], [4, 8], [6, 8], [10, 8]], dtype=float)

# 1. Center each column.
mean = X.mean(axis=0)
Xc = X - mean
# 2. Covariance matrix (divide by n - 1).
C = Xc.T @ Xc / (len(X) - 1)
# 3. Eigenvectors of the covariance, largest eigenvalue first.
values, vectors = np.linalg.eigh(C)
order = np.argsort(values)[::-1]
values, vectors = values[order], vectors[:, order]
vectors = vectors * np.sign(vectors[0])      # convention: first entry positive
# 4. Share of the variance on each component.
share = values / values.sum()
# 5. Scores: each merchant's coordinate along component 1.
w1 = vectors[:, 0]
z1 = Xc @ w1
# 6. Rebuild the table from one number per merchant.
X_hat = np.outer(z1, w1) + mean

print("mean:", mean)
print("covariance:", C.tolist())
print("eigenvalues:", np.round(values, 4), " share:", np.round(share, 4))
print("component 1:", np.round(w1, 4))
print("scores:", np.round(z1, 3))
print("Juniper rebuilt:", np.round(X_hat[0], 2), " actual:", X[0])

# Cross-check with NumPy's SVD of the centered table (Chapter 9).
U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
print("SVD check, variances:", np.round(s**2 / (len(X) - 1), 4),
      " direction:", np.round(Vt[0] * np.sign(Vt[0, 0]), 4))

# Checks against the hand calculation in the chapter.
assert np.allclose(mean, [8, 7])
assert np.allclose(Xc, [[4, -2], [0, -1], [-4, 1], [-2, 1], [2, 1]])
assert np.allclose(C, [[10, -3], [-3, 2]]) and np.allclose(C, np.cov(X.T))
assert np.allclose(values, [11, 1]) and np.allclose(share, [11 / 12, 1 / 12])
assert np.allclose(w1, np.array([3, -1]) / np.sqrt(10))
assert np.allclose(z1, np.array([14, 1, -13, -7, 5]) / np.sqrt(10))
assert np.isclose(z1.var(ddof=1), 11)             # variance of the scores
assert np.allclose(X_hat[0], [12.2, 5.6])
assert np.isclose(np.sum((X - X_hat) ** 2), (len(X) - 1) * values[1])
assert np.allclose(s**2 / (len(X) - 1), values)
assert np.allclose(np.abs(Vt[0]), np.abs(w1))

# Answers to Check yourself.
z2 = Xc @ vectors[:, 1]
assert np.isclose(np.corrcoef(z1, z2)[0, 1], 0)                         # Q8.2
tenfold = X * np.array([1.0, 10.0])        # online counted in single payments
vals10, vecs10 = np.linalg.eigh(np.cov(tenfold.T))
assert np.isclose(vals10[-1] / vals10.sum(), 0.974, atol=0.001)         # Q8.3
assert abs(vecs10[1, -1]) > 0.98                  # component 1 is nearly all online
