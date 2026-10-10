"""Chapter 1: linear regression by hand, by formula and by gradient descent."""
import numpy as np
from sklearn.linear_model import LinearRegression

from ch00_payflow_data import matrix, payouts

# Four payouts worked by hand: amount in USD thousands -> delay in hours.
x = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([3.0, 5.0, 6.0, 8.0])
X = np.column_stack([np.ones(4), x])           # the column of ones is the intercept
w = np.linalg.solve(X.T @ X, X.T @ y)          # normal equations
resid = y - X @ w
sse = resid @ resid
r2 = 1 - sse / ((y - y.mean()) @ (y - y.mean()))
print(f"four payouts: intercept {w[0]:.2f}  slope {w[1]:.2f}  SSE {sse:.2f}  "
      f"R^2 {r2:.3f}")
assert np.allclose(w, [1.5, 1.6]) and np.isclose(sse, 0.2)

# The payouts table: 400 rows, three features.
table = payouts()
F = matrix(table, ["amount_k", "weekend", "new_bank"])
d = table["delay_hours"]
A = np.column_stack([np.ones(len(d)), F])
w_exact = np.linalg.solve(A.T @ A, A.T @ d)

w_gd = np.zeros(4)
for step in range(4000):
    grad = -2 / len(d) * A.T @ (d - A @ w_gd)  # gradient of the mean squared error
    w_gd -= 0.02 * grad

sk = LinearRegression().fit(F, d)
rmse = np.sqrt(np.mean((d - A @ w_exact) ** 2))
print("normal equations", np.round(w_exact, 3))
print("gradient descent", np.round(w_gd, 3))
print("scikit-learn    ", np.round(np.r_[sk.intercept_, sk.coef_], 3))
print(f"RMSE {rmse:.2f} hours   R^2 {sk.score(F, d):.3f}")
assert np.allclose(w_exact, w_gd, atol=1e-3)
assert np.allclose(w_exact, np.r_[sk.intercept_, sk.coef_])
