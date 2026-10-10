"""Chapter 29. The Jacobian of softmax for a three-queue ticket router.

Run: python ch29_jacobian.py
"""
import numpy as np

# [listing]
def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def jacobian(f, z, h=1e-6):
    """Finite differences: column j holds the change in every output per unit z_j."""
    return np.column_stack([(f(z + h * e) - f(z - h * e)) / (2 * h)
                            for e in np.eye(len(z))])


# Scores for the queues billing, disputes, technical (chosen so p is round)
z = np.log(np.array([5.0, 3.0, 2.0]))
p = softmax(z)
J = np.diag(p) - np.outer(p, p)          # the formula: J_ij = p_i (1[i=j] - p_j)
print("p =", p.round(4))
print("J =")
print(J.round(4))
print("largest gap to finite differences:",
      f"{np.abs(J - jacobian(softmax, z)).max():.1e}")
print(f"columns sum to zero: {np.allclose(J.sum(axis=0), 0)}, "
      f"rank: {np.linalg.matrix_rank(J)}")

step = np.array([0.2, 0.0, 0.0])         # raise the billing score by 0.2
print("linear prediction p + J @ step:", (p + J @ step).round(4))
print("exact softmax(z + step)       :", softmax(z + step).round(4))
# [/listing]

# Hand-worked values from the chapter
assert np.allclose(p, [0.5, 0.3, 0.2])
assert np.allclose(J, [[0.25, -0.15, -0.10],
                       [-0.15, 0.21, -0.06],
                       [-0.10, -0.06, 0.16]])
assert np.allclose(J, jacobian(softmax, z), atol=1e-8)
assert np.allclose(J.sum(axis=0), 0) and np.allclose(J.sum(axis=1), 0)
assert np.linalg.matrix_rank(J) == 2 and abs(np.linalg.det(J)) < 1e-12
assert np.allclose(p + J @ step, [0.55, 0.27, 0.18])
assert np.allclose(softmax(z + step), [0.5498, 0.2701, 0.1801], atol=5e-5)
# the linear model fails for a big step: +2.0 on billing predicts 1.00, truth 0.88
big = np.array([2.0, 0.0, 0.0])
assert np.isclose((p + J @ big)[0], 1.0) and np.isclose(softmax(z + big)[0], 0.88,
                                                         atol=5e-3)
# adding the same constant to every score changes nothing: J @ (1, 1, 1) = 0
assert np.allclose(J @ np.ones(3), 0)

# Chain rule for vector functions: the Jacobian of a composition is a product
A = np.array([[1.0, 2.0], [0.0, -1.0], [0.5, 0.5]])       # inner map: z = A @ x
x0 = np.array([0.3, -0.2])
outer_inner = jacobian(lambda v: softmax(A @ v), x0)
pz = softmax(A @ x0)
assert np.allclose(outer_inner, (np.diag(pz) - np.outer(pz, pz)) @ A, atol=1e-8)
# A scalar loss has a 1 x n Jacobian: the gradient written as a row.
# For L = -log p[0], the row is p - (1, 0, 0), which is also (dL/dp) @ J.
loss = lambda v: np.array([-np.log(softmax(v)[0])])
row = jacobian(loss, z)
assert row.shape == (1, 3) and np.allclose(row[0], p - np.array([1.0, 0.0, 0.0]))
assert np.allclose(np.array([-1 / p[0], 0.0, 0.0]) @ J, row[0])
# Determinant as area scaling: (u, v) = (2x + y, x + 3y) scales areas by 5
assert np.isclose(np.linalg.det(np.array([[2.0, 1.0], [1.0, 3.0]])), 5.0)
# Q29.1: raise the disputes score by 0.1 ; Q29.2: shape for 4 inputs, 3 outputs
assert np.allclose(J @ np.array([0.0, 0.1, 0.0]), [-0.015, 0.021, -0.006])
assert jacobian(lambda v: softmax(v[:3]), np.zeros(4)).shape == (3, 4)
