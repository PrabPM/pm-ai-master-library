"""Chapter 2: logistic regression by hand, from scratch and with scikit-learn."""
import numpy as np
from sklearn.linear_model import LogisticRegression

from ch00_payflow_data import payments, sigmoid

# The hand example: score = -4 + 1.0 * velocity + 2.0 * new_card.
b, w_hand = -4.0, np.array([1.0, 2.0])
pay_a, pay_b = np.array([3.0, 1.0]), np.array([1.0, 0.0])
p_a, p_b = sigmoid(b + w_hand @ pay_a), sigmoid(b + w_hand @ pay_b)
print(f"payment A: p = {p_a:.3f}   payment B: p = {p_b:.3f}   "
      f"odds ratio for a new card = {np.exp(2.0):.2f}")
print(f"loss if A is fraud {-np.log(p_a):.3f}   loss if B is fraud {-np.log(p_b):.3f}")
assert np.isclose(p_a, 0.731, atol=5e-4) and np.isclose(p_b, 0.047, atol=5e-4)

# The payments table: 20,000 rows, about 2% fraud.
t = payments()
names = ["log_amount", "night", "new_card", "foreign", "velocity"]
X = np.column_stack([np.log(t["amount"] / 40.0), t["hour"] < 6, t["new_card"],
                     t["foreign_card"], t["velocity_1h"]]).astype(float)
y = t["is_fraud"]
A = np.column_stack([np.ones(len(y)), X])      # column of ones for the intercept

w = np.zeros(A.shape[1])
for step in range(10):
    p = sigmoid(A @ w)
    grad = A.T @ (p - y) / len(y)              # gradient of the mean cross-entropy
    curv = (A * (p * (1 - p))[:, None]).T @ A / len(y)
    w -= np.linalg.solve(curv, grad)           # Newton step: gradient / curvature
p = sigmoid(A @ w)
loss = -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

sk = LogisticRegression(C=np.inf, tol=1e-8, max_iter=5000).fit(X, y)  # no penalty
w_sk = np.r_[sk.intercept_, sk.coef_[0]]
print(" " * 12 + "".join(f"{n:>11}" for n in ["intercept"] + names))
print("from scratch" + "".join(f"{v:11.3f}" for v in w))
print("scikit-learn" + "".join(f"{v:11.3f}" for v in w_sk))
print(f"mean cross-entropy {loss:.4f}   odds ratio for new_card {np.exp(w[3]):.2f}")
assert np.allclose(w, w_sk, atol=1e-3)
