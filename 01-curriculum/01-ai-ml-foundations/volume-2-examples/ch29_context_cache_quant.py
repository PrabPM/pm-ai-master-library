"""Chapter 29: what the KV cache saves, and 8-bit quantization of weights.

Run: python ch29_context_cache_quant.py
"""
import numpy as np

rng = np.random.default_rng(0)
T, d = 8, 16                                   # tokens to generate, vector width
x = rng.normal(size=(T, d))                    # one input vector per token
Wq, Wk, Wv = (rng.normal(size=(d, d)) / np.sqrt(d) for _ in range(3))


def attend(q, K, V):
    scores = K @ q / np.sqrt(d)                # one score per earlier token
    w = np.exp(scores - scores.max())
    return (w / w.sum()) @ V


# Without a cache: at every step, redo attention for every position so far.
scores_without = 0
for t in range(1, T + 1):
    K, V = x[:t] @ Wk.T, x[:t] @ Wv.T          # recomputed from scratch
    outputs = [attend(Wq @ x[i], K[:i + 1], V[:i + 1]) for i in range(t)]
    scores_without += sum(i + 1 for i in range(t))
last_without = outputs[-1]

# With a KV cache: keep each token's key and value, compute only the new row.
K_cache, V_cache, scores_with = [], [], 0
for t in range(T):
    K_cache.append(Wk @ x[t])                  # one new key and value per step
    V_cache.append(Wv @ x[t])
    last_with = attend(Wq @ x[t], np.array(K_cache), np.array(V_cache))
    scores_with += t + 1

print(f"attention scores computed for {T} tokens: "
      f"{scores_without} without a cache, {scores_with} with one")
print("same output for the last token:", np.allclose(last_without, last_with))


def quantize_int8(w):
    scale = np.abs(w).max() / 127              # one scale for the whole tensor
    q = np.clip(np.round(w / scale), -127, 127).astype(np.int8)
    return q, scale


w = np.array([0.8, -0.31, 0.127, -1.27])
q, scale = quantize_int8(w)
print(f"scale = {scale:.4f}   integers = {q.tolist()}")
print(f"restored = {np.round(q * scale, 4).tolist()}   "
      f"largest error = {np.abs(w - q * scale).max():.4f}")

W = rng.normal(scale=0.02, size=(4096, 4096))
Q, s = quantize_int8(W)
err = np.abs(W - Q * s)
print(f"4096 x 4096 layer: {W.size * 4 / 1e6:.1f} MB as float32, "
      f"{W.size * 2 / 1e6:.1f} MB as float16, {Q.nbytes / 1e6:.1f} MB as int8")
print(f"mean error = {err.mean():.6f}   largest = {err.max():.6f}   "
      f"half a step = {s / 2:.6f}")

# Checks against the hand calculation in the chapter.
assert scores_without == T * (T + 1) * (T + 2) // 6 == 120
assert scores_with == T * (T + 1) // 2 == 36
assert q.tolist() == [80, -31, 13, -127] and np.isclose(scale, 0.01)
assert np.isclose(np.abs(w - q * scale).max(), 0.003)
assert err.max() <= s / 2 + 1e-9
