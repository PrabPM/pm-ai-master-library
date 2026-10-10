"""Chapter 24: LoRA. Parameter counts, the merged form, and a tiny training run.

Run: python ch24_lora.py
"""
import numpy as np


def lora_params(d, k, r):
    return r * (d + k)                 # B is d x r, A is r x k


d, k, r = 4096, 4096, 8
full, low = d * k, lora_params(d, k, r)
print(f"one {d} x {k} weight matrix: {full:,} parameters")
print(f"LoRA at rank {r}: {low:,} trainable ({full // low}x fewer, "
      f"{100 * low / full:.2f}% of the matrix)")

layers, matrices_per_layer = 32, 2     # adapt two attention projections per layer
adapter = layers * matrices_per_layer * low
base = 8_000_000_000
print(f"whole adapter: {adapter:,} parameters = {adapter * 2 / 1e6:.1f} MB at 16 bits")
print(f"base model: {base * 2 / 1e9:.0f} GB at 16 bits; 1,000 merchant adapters = "
      f"{1000 * adapter * 2 / 1e9:.1f} GB")

# The mechanism on a small layer: freeze W0, train only B and A.
rng = np.random.default_rng(0)
d, k, r, alpha = 6, 5, 2, 4
scale = alpha / r
W0 = rng.normal(size=(d, k))                                # frozen, pretrained
target = W0 + rng.normal(size=(d, 2)) @ rng.normal(size=(2, k))   # a rank-2 change
X = rng.normal(size=(200, k))
Y = X @ target.T

B = np.zeros((d, r))                   # zero, so the update starts at zero
A = rng.normal(scale=0.5, size=(r, k))
W0_before = W0.copy()
for step in range(301):
    error = X @ (W0 + scale * B @ A).T - Y
    if step % 100 == 0:
        print(f"step {step:4d}  loss = {np.mean(error ** 2):.6f}")
    G = 2 * error.T @ X / error.size   # gradient with respect to the full matrix
    B, A = B - 0.02 * scale * G @ A.T, A - 0.02 * scale * B.T @ G

x = rng.normal(size=k)
two_paths = W0 @ x + scale * B @ (A @ x)        # serve the adapter next to the base
merged = (W0 + scale * B @ A) @ x               # or fold it into the weights once
print("adapter path equals merged weights:", np.allclose(two_paths, merged))
print("frozen weights unchanged:", np.array_equal(W0, W0_before))

# Checks against the hand calculation in the chapter.
assert full == 16_777_216 and low == 65_536 and full // low == 256
assert adapter == 4_194_304
assert lora_params(4, 4, 1) == 8
assert np.mean(error ** 2) < 1e-4
