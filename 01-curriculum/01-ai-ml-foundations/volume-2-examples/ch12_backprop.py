"""Chapter 12: one backpropagation step by hand, then a network trained in NumPy."""
import numpy as np
from sklearn.linear_model import LogisticRegression

from ch00_payflow_data import fresh_review_sample, review_sample, sigmoid


def forward(x, W1, b1, w2, b2):
    z1 = W1 @ x + b1
    a1 = np.maximum(z1, 0.0)                   # ReLU
    p = sigmoid(w2 @ a1 + b2)
    return z1, a1, p


x, y = np.array([2.0, 1.0]), 1.0
W1, b1 = np.array([[0.5, 0.5], [1.0, -3.0]]), np.zeros(2)
w2, b2 = np.array([2.0, 1.0]), -3.0

z1, a1, p = forward(x, W1, b1, w2, b2)
loss = -np.log(p)
d2 = p - y                                     # dLoss/dz2 for sigmoid + cross-entropy
grad_w2, grad_b2 = d2 * a1, d2
d1 = (w2 * d2) * (z1 > 0)                      # push back through w2, then the ReLU
grad_W1, grad_b1 = np.outer(d1, x), d1
print(f"forward: z1 {z1.tolist()}  a1 {a1.tolist()}  p {p:.3f}  loss {loss:.3f}")
print(f"backward: d2 {d2:.2f}  grad_w2 {(grad_w2 + 0).tolist()}  "
      f"d1 {(d1 + 0).tolist()}")
print("grad_W1", (grad_W1 + 0).tolist())

eps, numeric = 1e-6, np.zeros((2, 2))          # check against finite differences
for i in range(2):
    for j in range(2):
        bumped = W1.copy()
        bumped[i, j] += eps
        numeric[i, j] = (-np.log(forward(x, bumped, b1, w2, b2)[2]) - loss) / eps
assert np.allclose(numeric, grad_W1, atol=1e-4)
assert np.allclose(grad_W1, [[-2, -1], [0, 0]]) and np.allclose(grad_w2, [-0.75, 0])

rate = 0.1
p_new = forward(x, W1 - rate * grad_W1, b1 - rate * grad_b1, w2 - rate * grad_w2,
                b2 - rate * grad_b2)[2]
print(f"after one step of size {rate}: p {p_new:.3f}  loss {-np.log(p_new):.3f}")
assert np.isclose(p_new, sigmoid(1.4075))

# The same mathematics on the review sample: 2 inputs, 16 hidden units, all rows.
R, labels = review_sample()
T, t_labels = fresh_review_sample()
mean, std = R.mean(axis=0), R.std(axis=0)
R, T = (R - mean) / std, (T - mean) / std
rng = np.random.default_rng(12)
W1, b1 = rng.normal(0, 1.0, (16, 2)), np.zeros(16)
w2, b2 = rng.normal(0, 0.25, 16), 0.0
for epoch in range(3001):
    Z1 = R @ W1.T + b1
    A1 = np.maximum(Z1, 0.0)
    P = sigmoid(A1 @ w2 + b2)
    if epoch % 1500 == 0:
        bce = -np.mean(labels * np.log(P) + (1 - labels) * np.log(1 - P))
        print(f"epoch {epoch:>4}: training loss {bce:.3f}")
    D2 = (P - labels) / len(labels)
    D1 = np.outer(D2, w2) * (Z1 > 0)
    W1 -= 0.5 * D1.T @ R
    b1 -= 0.5 * D1.sum(axis=0)
    w2 -= 0.5 * A1.T @ D2
    b2 -= 0.5 * D2.sum()
net_acc = np.mean((sigmoid(np.maximum(T @ W1.T + b1, 0) @ w2 + b2) > 0.5) == t_labels)
line_acc = LogisticRegression().fit(R, labels).score(T, t_labels)
print(f"accuracy on fresh payments: network {net_acc:.3f}   "
      f"logistic regression {line_acc:.3f}")
