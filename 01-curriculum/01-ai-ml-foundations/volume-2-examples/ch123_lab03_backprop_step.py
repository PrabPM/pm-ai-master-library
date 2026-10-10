"""Lab 3 (chapter 12): one gradient step for one neuron, checked numerically."""
import numpy as np


def forward(w, b, x):
    return 1 / (1 + np.exp(-(w @ x + b)))          # sigmoid of the weighted sum


def loss(w, b, x, y):
    p = forward(w, b, x)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


if __name__ == "__main__":
    x = np.array([0.8, 1.0])                       # scaled amount, new-card flag
    w, b, y, lr = np.array([0.5, -0.3]), 0.1, 1.0, 0.5

    p = forward(w, b, x)
    grad_w, grad_b = (p - y) * x, (p - y)          # cross-entropy with a sigmoid
    w_new, b_new = w - lr * grad_w, b - lr * grad_b
    print(f"p = {p:.4f}, loss = {loss(w, b, x, y):.4f}")
    print(f"gradient: w {np.round(grad_w, 4)}, b {grad_b:.4f}")
    print(f"after the step: w {np.round(w_new, 4)}, b {b_new:.4f}")
    print(f"new p = {forward(w_new, b_new, x):.4f}, "
          f"new loss = {loss(w_new, b_new, x, y):.4f}")

    eps = 1e-6
    numeric = np.array([(loss(w + eps * np.eye(2)[i], b, x, y)
                         - loss(w - eps * np.eye(2)[i], b, x, y)) / (2 * eps)
                        for i in range(2)])
    print("numeric gradient for w:", np.round(numeric, 4))
    assert np.allclose(numeric, grad_w, atol=1e-6)
    assert np.isclose(p, 0.5498, atol=1e-4)
    assert np.allclose(w_new, [0.6801, -0.0749], atol=1e-4)
    assert np.isclose(forward(w_new, b_new, x), 0.6888, atol=1e-4)
