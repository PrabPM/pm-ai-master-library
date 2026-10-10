"""Chapter 2. Matrices: a table of merchants, and a machine that moves vectors."""
import numpy as np

merchants = ["Juniper Bakery", "Corner Hardware", "Northwind Outfitters",
             "Harbor Books", "Summit Cycles"]
# Rows are merchants. Columns are in-store and online payments per day, in tens.
X = np.array([[12, 5],
              [8, 6],
              [4, 8],
              [6, 8],
              [10, 8]], dtype=float)

# View 1: the matrix as a table. One product scores every merchant at once.
w = np.array([5.0, 20.0])         # USD of fees per ten in-store / online payments
fees = X @ w
print("shape of X:", X.shape, " shape of X transposed:", X.T.shape)
print("fees per day (USD):", fees)
print("column totals:", X.sum(axis=0))

# View 2: the matrix as a machine. T turns (in-store, online) into
# (total, online minus in-store).
T = np.array([[1.0, 1.0],
              [-1.0, 1.0]])
juniper = X[0]
print("T @ juniper:", T @ juniper)
by_columns = juniper[0] * T[:, 0] + juniper[1] * T[:, 1]
print("same thing from the columns of T:", by_columns)

# Checks against the hand calculation in the chapter.
assert np.allclose(fees, [160, 160, 180, 190, 210])
assert np.allclose(X.sum(axis=0), [40, 35])
assert np.allclose(T @ juniper, [17, -7])
assert np.allclose(by_columns, T @ juniper)
assert np.allclose(np.eye(2) @ juniper, juniper)        # identity changes nothing
assert X[2, 1] == 8                                     # row 3, column 2

# Answers to Check yourself.
assert np.allclose(T @ np.array([4.0, 8.0]), [12, 4])   # Q2.1
assert np.isclose(X[3] @ np.array([1.0, 1.0]), 14)      # Q2.2, Harbor's total
assert 5_000_000 * 200 * 8 == 8_000_000_000             # Q2.3, 8 GB
