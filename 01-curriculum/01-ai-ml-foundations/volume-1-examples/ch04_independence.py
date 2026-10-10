"""Chapter 4. Linear independence: which columns carry new information?"""
import numpy as np

# Three days for one merchant: payments, volume (USD), PayFlow fees (USD).
count = np.array([100.0, 50.0, 200.0])
volume = np.array([2000.0, 3000.0, 1000.0])
fees = 0.029 * volume + 0.30 * count          # 2.9% + USD 0.30 per payment
F = np.column_stack([count, volume, fees])

print("fees column:", fees)
print("rank with the fees column:   ", np.linalg.matrix_rank(F))
print("rank without the fees column:", np.linalg.matrix_rank(F[:, :2]))

# Recover the weights that rebuild the fees column from the other two.
weights, *_ = np.linalg.lstsq(F[:, :2], fees)
print("fees = %.3f * count + %.3f * volume" % tuple(weights))

# A product of columns is redundant in meaning but not linearly dependent.
ticket = volume / count                       # average ticket, USD
G = np.column_stack([count, ticket, volume])  # volume = count * ticket
print("rank of [count, ticket, volume]:", np.linalg.matrix_rank(G))

# Checks against the hand calculation in the chapter.
assert np.allclose(fees, [88, 102, 89])
assert np.linalg.matrix_rank(F) == 2 and np.linalg.matrix_rank(F[:, :2]) == 2
assert np.allclose(weights, [0.30, 0.029])
assert np.allclose(0.30 * count + 0.029 * volume - fees, 0)
assert np.linalg.matrix_rank(G) == 3

# Answers to Check yourself.
table = np.array([[12, 5, 17], [8, 6, 14], [4, 8, 12]], dtype=float)
assert np.linalg.matrix_rank(table) == 2                              # Q4.1
assert np.allclose(table[:, 0] + table[:, 1] - table[:, 2], 0)
one_hot = np.array([[1, 1, 0], [1, 0, 1], [1, 1, 0], [1, 0, 1]], dtype=float)
assert np.linalg.matrix_rank(one_hot) == 2                            # Q4.2
assert np.linalg.matrix_rank(np.array([[8.0, 4.0], [6.0, 3.0]])) == 1  # Q4.3
