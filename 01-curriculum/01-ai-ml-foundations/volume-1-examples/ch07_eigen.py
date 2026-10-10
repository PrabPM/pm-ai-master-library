"""Chapter 7. Eigenvalues and eigenvectors: the directions a matrix only stretches."""
import numpy as np

C = np.array([[10.0, -3.0],
              [-3.0, 2.0]])           # covariance of the merchant table (Chapter 8)

values, vectors = np.linalg.eigh(C)   # for symmetric matrices; ascending order
print("eigenvalues:", values)
print("eigenvectors (columns):")
print(np.round(vectors, 4))

v_top = vectors[:, 1]
print("C @ v :", np.round(C @ v_top, 4))
print("11 * v:", np.round(11 * v_top, 4))

# Power iteration: keep applying C and rescaling. Any start drifts to the top
# eigenvector, because that direction is stretched the most at every step.
v = np.array([1.0, 1.0])
for step in range(1, 6):
    v = C @ v
    v = v / np.linalg.norm(v)
    print(f"step {step}: {np.round(v, 4)}")

# Checks against the hand calculation in the chapter.
assert np.allclose(values, [1, 11])
hand_top = np.array([3.0, -1.0]) / np.sqrt(10)
hand_low = np.array([1.0, 3.0]) / np.sqrt(10)
assert np.isclose(abs(v_top @ hand_top), 1)            # same line; sign may flip
assert np.isclose(abs(vectors[:, 0] @ hand_low), 1)
assert np.allclose(C @ hand_top, 11 * hand_top)
assert np.isclose(hand_top @ hand_low, 0)              # perpendicular
assert np.isclose(values.sum(), np.trace(C))
assert np.isclose(values.prod(), np.linalg.det(C))
Q, L = vectors, np.diag(values)
assert np.allclose(Q @ L @ Q.T, C)                     # C = Q L Q^T
assert np.isclose(abs(v @ hand_top), 1, atol=1e-4)     # power iteration converged

# Answers to Check yourself.
A = np.array([[2.0, 1.0], [1.0, 2.0]])
assert np.allclose(np.linalg.eigvalsh(A), [1, 3])                       # Q7.1
assert np.allclose(A @ np.array([1.0, 1.0]), [3, 3])
P = np.array([[0.9, 0.4], [0.1, 0.6]])       # columns: from active, from dormant
vals, vecs = np.linalg.eig(P)
steady = vecs[:, np.argmax(vals.real)].real
steady = steady / steady.sum()
assert np.allclose(sorted(vals.real), [0.5, 1.0])                       # Q7.2
assert np.allclose(steady, [0.8, 0.2])
R = np.array([[0.0, -1.0], [1.0, 0.0]])      # quarter turn: no real eigenvectors
assert np.allclose(np.linalg.eigvals(R).imag, [1, -1])                  # Q7.3
