"""Chapter 57, Lab 5: one neuron, one payment, the chain rule by hand."""
import numpy as np

x = np.array([2.0, 1.0])           # amount in USD hundreds, new-card flag
w = np.array([0.5, -1.0])
b = 0.1
y = 1.0                            # this payment was fraud


def loss(w, b):
    p = 1 / (1 + np.exp(-(w @ x + b)))
    return float(-(y * np.log(p) + (1 - y) * np.log(1 - p)))


z = w @ x + b
p = 1 / (1 + np.exp(-z))
grad_w = (p - y) * x               # chain rule: dL/dz = p - y, dz/dw = x
grad_b = p - y
print(f"z {z:.2f}   p {p:.5f}   loss {loss(w, b):.5f}")
print("gradient by the chain rule:  ", np.round(grad_w, 5), round(grad_b, 5))

h = 1e-6                           # central differences, one weight at a time
numeric = [(loss(w + h * e, b) - loss(w - h * e, b)) / (2 * h) for e in np.eye(2)]
print("gradient by finite difference:", np.round(numeric, 5))

w_new, b_new = w - 0.1 * grad_w, b - 0.1 * grad_b
print(f"after one step of size 0.1: w {np.round(w_new, 4)}  b {b_new:.4f}  "
      f"loss {loss(w_new, b_new):.5f}")

# ---- checks against the hand results ----
assert np.isclose(z, 0.1) and np.isclose(p, 0.52498, atol=1e-5)
assert np.isclose(loss(w, b), 0.64440, atol=1e-5)
assert np.allclose(grad_w, [-0.95004, -0.47502], atol=1e-5)
assert np.allclose(numeric, grad_w, atol=1e-6)
assert np.allclose(w_new, [0.5950, -0.9525], atol=1e-4)
assert loss(w_new, b_new) < loss(w, b)
