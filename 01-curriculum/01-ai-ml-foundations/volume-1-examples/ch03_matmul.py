"""Chapter 3. Matrix multiplication: chaining two steps into one matrix."""
import numpy as np

# Step 1: (in-store, online) -> (total, online, online minus in-store).
B = np.array([[1.0, 1.0],
              [0.0, 1.0],
              [-1.0, 1.0]])
# Step 2: those three numbers -> (fee revenue, review priority).
A = np.array([[5.0, 15.0, 0.0],
              [1.0, 0.0, 2.0]])

AB = A @ B                       # "first B, then A" as a single 2 x 2 matrix
juniper = np.array([12.0, 5.0])

print("A @ B =")
print(AB)
print("step by step:", A @ (B @ juniper))
print("in one step: ", AB @ juniper)
print("shapes:", A.shape, "@", B.shape, "->", AB.shape, "| B @ A ->", (B @ A).shape)

# Order matters even when both products have the same shape.
P = np.array([[2.0, 0.0], [0.0, 1.0]])    # double the first number
Q = np.array([[1.0, 1.0], [0.0, 1.0]])    # add the second number to the first
print("P @ Q =", (P @ Q).tolist(), " Q @ P =", (Q @ P).tolist())

# Checks against the hand calculation in the chapter.
assert np.allclose(AB, [[5, 20], [-1, 3]])
assert np.allclose(B @ juniper, [17, 5, -7])
assert np.allclose(A @ (B @ juniper), [160, 3])
assert np.allclose(AB @ juniper, [160, 3])
assert np.allclose(P @ Q, [[2, 2], [0, 1]]) and np.allclose(Q @ P, [[2, 1], [0, 1]])
assert np.allclose((A @ B).T, B.T @ A.T)                # transpose reverses the order
assert A.shape[0] * A.shape[1] * B.shape[1] == 12       # scalar multiplications

# Answers to Check yourself.
assert np.allclose(AB @ np.array([4.0, 8.0]), [180, 20])            # Q3.1
assert (np.ones((4, 3)) @ np.ones((3, 5))).shape == (4, 5)          # Q3.2
assert 1000 * 768 * 768 == 589_824_000                              # Q3.3
