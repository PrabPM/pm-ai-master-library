"""Chapter 18: initialization, normalization and dropout, one experiment each."""
import numpy as np

from ch00_payflow_data import sigmoid

rng = np.random.default_rng(18)


def batch_norm(z, running=None):
    mean, var = (z.mean(axis=0), z.var(axis=0)) if running is None else running
    return (z - mean) / np.sqrt(var + 1e-5)


# Experiment 1: push 512 inputs through 30 ReLU layers of width 256.
width, depth = 256, 30
start = rng.normal(size=(512, width))
print("activation size at layer 30")
for name, scale, norm in [("std 1/sqrt(n), too small", 1.0, False),
                          ("std sqrt(2/n), He", np.sqrt(2.0), False),
                          ("std 2/sqrt(n), too large", 2.0, False),
                          ("too small + batch norm", 1.0, True)]:
    h = start
    for layer in range(depth):
        z = h @ rng.normal(0, scale / np.sqrt(width), (width, width))
        h = np.maximum(batch_norm(z) if norm else z, 0.0)
    print(f"  {name:<25} {np.sqrt(np.mean(h ** 2)):.1e}")
    if not norm:                               # the hand estimate: (scale^2 / 2)^(30/2)
        estimate = (scale ** 2 / 2) ** (depth / 2)
        assert estimate / 4 < np.sqrt(np.mean(h ** 2)) < estimate * 4

# Batch norm by hand, and the classic serving bug.
batch = np.array([[2.0], [4.0], [6.0], [8.0]])
normed = batch_norm(batch).ravel()
print("batch (2, 4, 6, 8) normalized:", np.round(normed, 3).tolist())
assert np.allclose(normed, [-1.342, -0.447, 0.447, 1.342], atol=1e-3)
stored = (np.array([5.0]), np.array([5.0]))    # statistics saved during training
for mode, stats in (("training", None), ("inference", stored)):
    outs = [batch_norm(np.array([[amount]]), stats)[0, 0] for amount in (2.0, 8.0)]
    print(f"{mode} mode, one payment at a time: 2.0 -> {outs[0]:.3f}, "
          f"8.0 -> {outs[1]:.3f}")
    assert (outs[0] == outs[1] == 0.0) == (mode == "training")

# Dropout by hand: keep each activation with probability 0.5, rescale survivors.
a, keep = np.array([2.0, 4.0, 6.0, 8.0]), np.array([1, 0, 1, 1])
assert (a * keep / 0.5).tolist() == [4.0, 0.0, 12.0, 16.0]
many = (a * (rng.random((100000, 4)) >= 0.5) / 0.5).mean(axis=0)
print("dropout:", (a * keep / 0.5).tolist(), " mean over many masks:",
      np.round(many, 1).tolist())

# Experiment 3: 100 training rows, 30 features, 64 hidden units: easy to memorize.
w_true = np.zeros(30)
w_true[:4] = [2.0, -1.5, 1.0, 1.0]


def make(n):
    X = rng.normal(size=(n, 30))
    return X, (X @ w_true + 0.3 * X[:, 0] * X[:, 1] + rng.normal(size=n) > 0) * 1.0


Xtr, ytr = make(100)
Xte, yte = make(4000)
for p_drop in (0.0, 0.5):
    init = np.random.default_rng(1)
    W1, b1 = init.normal(0, np.sqrt(2 / 30), (30, 64)), np.zeros(64)
    w2, b2 = init.normal(0, np.sqrt(1 / 64), 64), 0.0
    for epoch in range(3000):
        Z = Xtr @ W1 + b1
        mask = (init.random(Z.shape) >= p_drop) / (1 - p_drop)   # all ones if p = 0
        A = np.maximum(Z, 0.0) * mask
        D2 = (sigmoid(A @ w2 + b2) - ytr) / len(ytr)
        D1 = np.outer(D2, w2) * mask * (Z > 0)
        W1, b1 = W1 - 0.3 * Xtr.T @ D1, b1 - 0.3 * D1.sum(axis=0)
        w2, b2 = w2 - 0.3 * A.T @ D2, b2 - 0.3 * D2.sum()
    acc = [np.mean((np.maximum(X @ W1 + b1, 0) @ w2 + b2 > 0) == y)   # dropout off
           for X, y in ((Xtr, ytr), (Xte, yte))]
    print(f"dropout {p_drop}: train accuracy {acc[0]:.3f}, test accuracy {acc[1]:.3f}")
