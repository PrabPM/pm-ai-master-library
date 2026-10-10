"""Chapter 13: a convolution by hand, pooling, receptive fields and skip connections."""
import numpy as np
from scipy.signal import correlate2d

# A 5x5 crop of a scanned certificate: the corner of a dark stamp on white paper.
image = np.array([[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0],
                  [0, 0, 1, 1, 1],
                  [0, 0, 1, 1, 1],
                  [0, 0, 1, 1, 1]], dtype=float)
kernel = np.array([[-1, 0, 1],
                   [-1, 0, 1],
                   [-1, 0, 1]], dtype=float)      # responds to a left-to-right step


def max_pool(feature, k=2, stride=1):
    size = (feature.shape[0] - k) // stride + 1
    out = np.zeros((size, size))
    for r in range(size):
        for c in range(size):
            window = feature[r * stride:r * stride + k, c * stride:c * stride + k]
            out[r, c] = window.max()
    return out


def conv2d(image, kernel, stride=1):
    k = kernel.shape[0]
    size = (image.shape[0] - k) // stride + 1
    out = np.zeros((size, size))
    for r in range(size):
        for c in range(size):
            window = image[r * stride:r * stride + k, c * stride:c * stride + k]
            out[r, c] = (window * kernel).sum()   # multiply, then add up
    return out


feature = conv2d(image, kernel)
print("feature map\n", feature)
print("after 2x2 max pooling\n", max_pool(feature))
assert np.array_equal(feature, [[1, 1, 0], [2, 2, 0], [3, 3, 0]])
assert np.array_equal(feature, correlate2d(image, kernel, mode="valid"))
assert np.array_equal(max_pool(feature), [[2, 2], [3, 3]])

print("weights: convolution", kernel.size + 1, " fully connected", 25 * 9 + 9)
print("patch width seen after 1, 2, 3, 5 stacked 3x3 layers:",
      [1 + 2 * layers for layers in (1, 2, 3, 5)])

# What skip connections fix: how much gradient reaches the first of 50 layers.
rng = np.random.default_rng(13)
width, depth = 64, 50
for name, skip in (("plain", 0.0), ("residual", 1.0)):
    h = rng.normal(size=width)
    jacobian = np.eye(width)
    for layer in range(depth):
        W = rng.normal(0, 0.5 / np.sqrt(width), (width, width))
        z = W @ h
        local = (1 - np.tanh(z) ** 2)[:, None] * W          # d tanh(Wh) / dh
        jacobian = (skip * np.eye(width) + local) @ jacobian
        h = skip * h + np.tanh(z)
    print(f"{name:<8} network: gradient reaching layer 1 has size "
          f"{np.linalg.norm(jacobian, 2):.2e}")
