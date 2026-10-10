"""Chapter 5. Determinants and trace: two one-number summaries of a matrix."""
import numpy as np

A = np.array([[3.0, 1.0],
              [1.0, 2.0]])            # stretches the unit square to area 5
S = np.array([[2.0, 1.0],
              [4.0, 2.0]])            # second row is twice the first
M = np.array([[12, 5, 17],
              [8, 6, 14],
              [4, 8, 12]], dtype=float)   # in-store, online, total
C = np.array([[10.0, -3.0],
              [-3.0, 2.0]])           # covariance of the merchant table

det_M = np.round(np.linalg.det(M), 6) + 0.0     # rounds away float noise
print(f"det(A) = {np.linalg.det(A):.1f}   det(S) = {np.linalg.det(S):.1f}")
print(f"det(M) = {det_M:.1f}   rank(M) = {np.linalg.matrix_rank(M)}")
print(f"trace(C) = {np.trace(C):.1f}   det(C) = {np.linalg.det(C):.1f}")

# A tiny determinant does not mean "nearly singular".
small = 0.1 * np.eye(10)
print(f"det(0.1 * I) = {np.linalg.det(small):.1e}   condition number = "
      f"{np.linalg.cond(small):.1f}")

# Checks against the hand calculation in the chapter.
assert np.isclose(np.linalg.det(A), 3 * 2 - 1 * 1)
assert np.isclose(np.linalg.det(S), 0)
hand = 12 * (6 * 12 - 14 * 8) - 5 * (8 * 12 - 14 * 4) + 17 * (8 * 8 - 6 * 4)
assert hand == 0 and np.isclose(np.linalg.det(M), 0, atol=1e-9)
assert np.isclose(np.linalg.det(A @ S), np.linalg.det(A) * np.linalg.det(S))
assert np.isclose(np.linalg.det(A.T), np.linalg.det(A))
assert np.isclose(np.trace(C), 12) and np.isclose(np.linalg.det(C), 11)
assert np.isclose(np.trace(A @ C), np.trace(C @ A))          # swap inside a product
assert np.isclose(np.sum(A**2), 15) and np.isclose(np.trace(A.T @ A), 15)
assert np.isclose(np.linalg.norm(A, "fro"), np.sqrt(15))     # Frobenius norm
assert np.isclose(np.linalg.det(small), 1e-10)
sign, logdet = np.linalg.slogdet(small)        # the stable route for big matrices
assert sign == 1 and np.isclose(logdet, 10 * np.log(0.1))

# Answers to Check yourself.
T = np.array([[1.0, 1.0], [-1.0, 1.0]])
assert np.isclose(np.linalg.det(T), 2)                              # Q5.1
assert np.isclose(np.linalg.det(np.linalg.inv(T)), 0.5)
flip = np.array([[0.0, 1.0], [1.0, 0.0]])
assert np.isclose(np.linalg.det(flip), -1)                          # Q5.2
cov = np.array([[4.0, 1.2, 0.7], [1.2, 2.5, 0.4], [0.7, 0.4, 1.0]])
assert np.isclose(np.trace(cov), 7.5)                               # Q5.3
assert np.isclose(np.ones(3) @ cov @ np.ones(3), 12.1)   # variance of the total
