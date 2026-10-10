"""Chapter 28. The chain rule, then backpropagation on a tiny network by hand.

Run: python ch28_backprop.py
"""
import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# [listing]
x = np.array([1.0, 2.0])            # amount (USD hundreds), payments this hour
y = 1.0                             # label: fraud
params = {"W1": np.array([[1.0, 0.5], [-1.0, 0.25]]), "b1": np.zeros(2),
          "w2": np.array([0.5, -1.0]), "b2": -1.0}


def forward(p):
    z1 = p["W1"] @ x + p["b1"]
    a = np.maximum(z1, 0)           # ReLU
    z2 = p["w2"] @ a + p["b2"]
    prob = sigmoid(z2)
    return z1, a, prob, -np.log(prob)


z1, a, prob, loss = forward(params)
print(f"forward: z1 = {z1}, a = {a}, prob = {prob:.2f}, loss = {loss:.4f}")

d_z2 = prob - y                     # dL/dz2
d_w2, d_b2 = d_z2 * a, d_z2
d_a = d_z2 * params["w2"]           # back to the hidden layer
d_z1 = d_a * (z1 > 0)               # ReLU passes slope only where z1 > 0
d_W1, d_b1 = np.outer(d_z1, x), d_z1
print(f"dL/dw2 = {d_w2 + 0.0}, dL/db2 = {d_b2}")
print(f"dL/dW1 = {(d_W1 + 0.0).tolist()}, dL/db1 = {d_b1 + 0.0}")
# [/listing]


def numerical(name, index, h=1e-6):
    """Central-difference derivative of the loss for one parameter entry."""
    hi = {k: np.array(v, dtype=float) for k, v in params.items()}
    lo = {k: np.array(v, dtype=float) for k, v in params.items()}
    hi[name][index] += h
    lo[name][index] -= h
    return (forward(hi)[3] - forward(lo)[3]) / (2 * h)


analytic = {"W1": d_W1, "b1": d_b1, "w2": d_w2, "b2": np.array(d_b2)}
worst = 0.0
for name, value in analytic.items():
    for index in np.ndindex(value.shape):
        worst = max(worst, abs(numerical(name, index) - value[index]))
print(f"largest gap to the numerical gradient: {worst:.1e}")

# Hand-worked values from the chapter
assert np.allclose(z1, [2.0, -0.5]) and np.allclose(a, [2.0, 0.0])
assert np.isclose(prob, 0.5) and np.isclose(loss, np.log(2))
assert np.isclose(d_z2, -0.5)
assert np.allclose(d_w2, [-1.0, 0.0]) and np.isclose(d_b2, -0.5)
assert np.allclose(d_a, [-0.25, 0.5]) and np.allclose(d_z1, [-0.25, 0.0])
assert np.allclose(d_W1, [[-0.25, -0.5], [0.0, 0.0]])
assert np.allclose(d_b1, [-0.25, 0.0])
assert worst < 1e-8

# The two-link chain in the chapter: z = w x + b, p = sigmoid(z), L = -log p
w, b, xs = 0.5, -1.0, 2.0
one = lambda w_, b_: -np.log(sigmoid(w_ * xs + b_))
p1 = sigmoid(w * xs + b)
assert np.isclose(p1, 0.5)
dL_dp, dp_dz, dz_dw = -1 / p1, p1 * (1 - p1), xs
assert np.isclose(dL_dp * dp_dz * dz_dw, -1.0)                # (-2)(0.25)(2)
assert np.isclose((one(w + 1e-6, b) - one(w - 1e-6, b)) / 2e-6, -1.0)
assert np.isclose((one(w, b + 1e-6) - one(w, b - 1e-6)) / 2e-6, -0.5)
# Q28.1: one step on the output weights only, learning rate 0.1
new = dict(params, w2=params["w2"] - 0.1 * d_w2)
assert np.allclose(new["w2"], [0.6, -1.0])
assert np.isclose(forward(new)[2], sigmoid(0.2)) and np.isclose(forward(new)[3], 0.598,
                                                                 atol=5e-4)
# Q28.2: with label 0 the loss is -log(1 - prob) and dL/dz2 = prob - 0 = +0.5
assert np.isclose(prob - 0.0, 0.5)
