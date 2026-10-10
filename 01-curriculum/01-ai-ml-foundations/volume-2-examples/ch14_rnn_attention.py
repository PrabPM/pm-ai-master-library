"""Chapter 14: why recurrent gradients vanish, what a gate changes, soft lookup."""
import numpy as np

# A one-number recurrent network: h_t = tanh(w * h_{t-1} + x_t).
def gradient_back(w, steps, x=0.2):
    """d h_T / d h_0: one factor of w * (1 - h_t^2) per step, multiplied together."""
    h, grad, history = 0.0, 1.0, []
    for t in range(steps):
        h = np.tanh(w * h + x)
        grad *= w * (1 - h ** 2)
        history.append(abs(grad))
    return history


print(f"ten factors of 0.5: {0.5 ** 10:.5f}   fifty factors of 1.5: {1.5 ** 50:.1e}")
for w in (0.5, 0.9):
    g = gradient_back(w, 50)
    print(f"w = {w}: gradient after 10 steps {g[9]:.1e}, after 50 steps {g[49]:.1e}")
assert gradient_back(0.5, 10)[9] <= 0.5 ** 10

# A gated memory cell: c_t = f * c_{t-1} + i * candidate, so d c_T / d c_0 = f^T.
for forget in (0.9, 0.99):
    print(f"forget gate {forget}: gradient after 50 steps {forget ** 50:.1e}")

# Attention as a soft lookup: one query, three stored (key, value) pairs.
query = np.array([1.0, 0.0])
keys = np.array([[2.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
values = np.array([10.0, 20.0, 30.0])
scores = keys @ query                          # how well each key matches
weights = np.exp(scores) / np.exp(scores).sum()   # softmax: positive, sums to 1
answer = weights @ values
print(f"scores {scores.tolist()}  weights {np.round(weights, 3).tolist()}  "
      f"answer {answer:.2f}")
assert np.allclose(weights, [0.665, 0.090, 0.245], atol=5e-4)
assert np.isclose(answer, 15.8, atol=0.01)

sharp = np.exp(5 * scores) / np.exp(5 * scores).sum()
print(f"scores times 5: weights {np.round(sharp, 3).tolist()}  "
      f"answer {sharp @ values:.2f}")
