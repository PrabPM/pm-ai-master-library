"""Chapter 6. Inverses and linear systems: recover PayFlow's fee schedule."""
import numpy as np

# Two days for one merchant. Columns: volume (USD), number of payments.
A = np.array([[1000.0, 20.0],
              [2000.0, 60.0]])
b = np.array([35.0, 76.0])            # fees charged each day (USD)
x = np.linalg.solve(A, b)             # solves A x = b without forming the inverse
print("rate and fixed fee:", x, f" condition number: {np.linalg.cond(A):.0f}")

# Four days with small errors in the recorded fees: more equations than unknowns.
A4 = np.array([[1000.0, 20.0], [2000.0, 60.0], [1500.0, 45.0], [800.0, 10.0]])
b4 = np.array([35.10, 75.80, 57.20, 26.10])
fit, *_ = np.linalg.lstsq(A4, b4)
normal = np.linalg.solve(A4.T @ A4, A4.T @ b4)
print("least squares:", np.round(fit, 4), " normal equations:", np.round(normal, 4))

# Two days with the same average ticket (USD 50): the columns are dependent.
same_ticket = np.array([[1000.0, 20.0],
                        [2000.0, 40.0]])
try:
    np.linalg.solve(same_ticket, np.array([35.0, 70.0]))
except np.linalg.LinAlgError as err:
    print("equal tickets:", err)

# Checks against the hand calculation in the chapter.
A_inv = np.linalg.inv(A)
assert np.isclose(np.linalg.det(A), 20000)
assert np.allclose(A_inv * 20000, [[60, -20], [-2000, 1000]])
assert np.allclose(x, [0.029, 0.30])
assert np.allclose(A_inv @ b, x)
assert np.allclose(A_inv @ A, np.eye(2))
assert np.allclose(fit, normal)
assert np.allclose(fit, [0.029, 0.30], atol=0.02)
assert np.isclose(np.linalg.det(same_ticket), 0)
assert np.isinf(np.linalg.cond(same_ticket)) or np.linalg.cond(same_ticket) > 1e15

# Answers to Check yourself.
G = np.array([[2.0, 1.0], [1.0, 1.0]])
assert np.allclose(np.linalg.inv(G), [[1, -1], [-1, 2]])                 # Q6.1
assert np.allclose(np.linalg.solve(G, [10.0, 7.0]), [3, 4])
days = np.array([[1.0, 1.0], [2.0, 1.0], [3.0, 1.0]])
line, *_ = np.linalg.lstsq(days, np.array([2.0, 3.0, 5.0]))
assert np.allclose(line, [1.5, 1 / 3])                                   # Q6.3
assert np.allclose(days.T @ days, [[14, 6], [6, 3]])
assert np.allclose(days.T @ np.array([2.0, 3.0, 5.0]), [23, 10])
