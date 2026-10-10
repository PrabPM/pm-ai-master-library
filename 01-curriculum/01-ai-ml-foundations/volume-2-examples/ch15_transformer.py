"""Chapter 15: scaled dot-product attention and one transformer block in NumPy."""
import numpy as np


def softmax(z):
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def attention(Q, K, V, mask=None):
    scores = Q @ K.T / np.sqrt(K.shape[-1])
    if mask is not None:
        scores = np.where(mask, scores, -1e9)  # masked positions get no weight
    weights = softmax(scores)                  # each row sums to 1
    return weights @ V, weights


# Four token vectors chosen for easy arithmetic: d_k = 4, so sqrt(d_k) = 2.
X = np.array([[2.0, 0, 0, 0], [0, 2.0, 0, 0], [2.0, 2.0, 0, 0], [0, 0, 2.0, 0]])
out, weights = attention(X, X, X)              # self-attention: Q = K = V = X
print("attention weights (row = the token asking, column = the token read)")
print(np.round(weights, 3))
print("new vector for token 3:", np.round(out[2], 3).tolist())
assert np.allclose(weights[2], [0.105, 0.105, 0.776, 0.014], atol=5e-4)
assert np.allclose(weights.sum(axis=1), 1.0)

causal = np.tril(np.ones((4, 4), dtype=bool))  # token i may read tokens 1..i only
print("token 3 with a causal mask:", np.round(attention(X, X, X, causal)[1][2], 3))


def layer_norm(x):
    return (x - x.mean(axis=-1, keepdims=True)) / (x.std(axis=-1, keepdims=True) + 1e-5)


def block(x, p, heads=2):
    """Pre-norm block: x + attention(norm(x)), then x + feed-forward(norm(x))."""
    h, d = layer_norm(x), x.shape[1] // heads
    Q, K, V = h @ p["q"], h @ p["k"], h @ p["v"]
    parts = [attention(Q[:, s], K[:, s], V[:, s])[0]         # one result per head
             for s in (slice(i * d, (i + 1) * d) for i in range(heads))]
    x = x + np.concatenate(parts, axis=1) @ p["o"]
    return x + np.maximum(layer_norm(x) @ p["w1"], 0.0) @ p["w2"]


def positions(n, d):
    angle = np.arange(n)[:, None] / 10000 ** (2 * np.arange(d // 2)[None, :] / d)
    pe = np.zeros((n, d))
    pe[:, 0::2], pe[:, 1::2] = np.sin(angle), np.cos(angle)
    return pe


rng = np.random.default_rng(15)
p = {name: rng.normal(0, 0.5, shape) for name, shape in
     [("q", (4, 4)), ("k", (4, 4)), ("v", (4, 4)), ("o", (4, 4)), ("w1", (4, 16)),
      ("w2", (16, 4))]}
swap = [1, 0, 2, 3]                            # exchange the first two tokens
same = np.allclose(block(X, p)[swap], block(X[swap], p))
pe = positions(4, 4)
moved = np.allclose(block(X + pe, p)[swap], block(X[swap] + pe, p))
print("position 1 encoding:", np.round(pe[1], 3).tolist())
print(f"no positions: swapping two tokens just swaps their outputs -> {same}")
print(f"with positions added, is that still true? -> {moved}")
assert same and not moved
