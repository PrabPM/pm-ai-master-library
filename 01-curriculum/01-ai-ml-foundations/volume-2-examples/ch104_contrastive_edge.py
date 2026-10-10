"""Chapter 104. Contrastive multimodal training and edge deployment: the symmetric
contrastive loss on a 3x3 similarity matrix, and 8-bit quantization arithmetic.

Run: python ch104_contrastive_edge.py
"""
import numpy as np

# [listing]
def contrastive_loss(sim, tau):
    """Symmetric cross-entropy over a batch; true pairs sit on the diagonal."""
    logits = sim / tau
    rows = np.exp(logits) / np.exp(logits).sum(1, keepdims=True)   # image -> text
    cols = np.exp(logits) / np.exp(logits).sum(0, keepdims=True)   # text -> image
    l_i2t, l_t2i = -np.log(np.diag(rows)).mean(), -np.log(np.diag(cols)).mean()
    return l_i2t, l_t2i, (l_i2t + l_t2i) / 2


# 3 storefront photos (rows) against 3 descriptions (columns)
sim = np.array([[0.9, 0.1, 0.0],
                [0.2, 0.8, 0.1],
                [0.1, 0.3, 0.6]])
print("image->text %.4f  text->image %.4f  loss %.4f" % contrastive_loss(sim, 0.5))


def quantize(x, bits=8):
    """Affine quantization to unsigned integers."""
    s = (x.max() - x.min()) / (2 ** bits - 1)
    z = int(round(-x.min() / s))
    q = np.clip(np.round(x / s) + z, 0, 2 ** bits - 1).astype(np.uint8)
    return q, s, z


w = np.array([-1.0, -0.2, 0.0, 0.4, 1.55])
q, s, z = quantize(w)
print("scale", round(s, 4), "zero point", z, "codes", q)
print("restored", (s * (q.astype(float) - z)).round(3))
layer = np.random.default_rng(0).normal(0, 0.05, size=1_000_000)   # a large layer
q8, s8, z8 = quantize(layer)
err = np.abs(s8 * (q8.astype(float) - z8) - layer).max()
print(f"worst rounding error {err:.5f}, half a step is {s8 / 2:.5f}")
params = 25_000_000
print(f"model: {params * 4 / 1e6:.0f} MB as float32, {params / 1e6:.0f} MB as int8")
# [/listing]

# Hand-worked first row: logits 1.8, 0.2, 0.0
row = np.exp([1.8, 0.2, 0.0])
assert np.allclose(row.round(3), [6.050, 1.221, 1.000])
assert round(row[0] / row.sum(), 4) == 0.7314
assert round(-np.log(row[0] / row.sum()), 4) == 0.3128
l_i2t, l_t2i, loss = contrastive_loss(sim, 0.5)
# per-row costs quoted in the chapter: 0.313, 0.437, 0.651
per_row = -np.log(np.diag(np.exp(sim / 0.5) / np.exp(sim / 0.5).sum(1, keepdims=True)))
assert np.allclose(per_row.round(3), [0.313, 0.437, 0.651])
assert round(l_i2t, 4) == 0.4667 and round(l_t2i, 4) == 0.4539
assert round(loss, 4) == 0.4603
# A perfectly separated batch costs nothing
assert contrastive_loss(np.eye(3), 0.05)[2] < 1e-6
# A random-guess batch (all similarities equal) costs ln N
assert np.isclose(contrastive_loss(np.zeros((3, 3)), 0.5)[2], np.log(3))

# Hand-worked quantization: range 2.55 over 255 steps -> s = 0.01, z = 100
assert np.isclose(s, 0.01) and z == 100
assert list(q) == [0, 80, 100, 140, 255]
assert np.allclose(s * (q.astype(float) - z), w)
# Size arithmetic and the rounding-error bound
assert params * 4 == 100_000_000 and q8.itemsize == 1
assert err <= s8 / 2 * 1.0001

# Latency budget arithmetic used in the chapter (illustrative numbers)
network_p95, server_model, budget = 180, 15, 100
assert network_p95 + server_model == 195 and network_p95 + server_model > budget

# Q104.1: 2x2 batch, similarities [[0.8, 0.2], [0.4, 0.6]], tau = 0.2
sim2 = np.array([[0.8, 0.2], [0.4, 0.6]])
a, b, c = contrastive_loss(sim2, 0.2)
# logits [[4, 1], [2, 3]]: rows give 1/(1+e^-3) and 1/(1+e^-1); columns 1/(1+e^-2)
assert round(a, 4) == 0.1809 and round(b, 4) == 0.1269 and round(c, 4) == 0.1539
# Q104.2: range [-0.5, 2.05] at 8 bits -> s = 0.01, z = 50; x = 1.0 -> code 150
q2, s2, z2 = quantize(np.array([-0.5, 1.0, 2.05]))
assert np.isclose(s2, 0.01) and z2 == 50 and q2[1] == 150
