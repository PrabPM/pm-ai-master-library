"""Chapter 96. Long context: rotary position embeddings, position interpolation
and YaRN-style frequency scaling.

Run: python ch96_long_context.py
"""
import numpy as np

# [listing]
def rope(vec, pos, theta):
    """Rotate each pair of vec by the angle pos * theta."""
    x, y = vec[0::2], vec[1::2]
    c, s = np.cos(pos * theta), np.sin(pos * theta)
    out = np.empty_like(vec)
    out[0::2], out[1::2] = x * c - y * s, x * s + y * c
    return out


one_pair = np.array([np.pi / 6])                   # 30 degrees per position
q = k = np.array([1.0, 0.0])
for m, n in [(3, 1), (10, 8)]:
    score = rope(q, m, one_pair) @ rope(k, n, one_pair)
    print(f"positions {m} and {n}: score {score:.3f}")

d, L_train, s = 8, 1000, 4
theta = 10000.0 ** (-2 * np.arange(d // 2) / d)
turns = L_train * theta / (2 * np.pi)              # turns within training length
ramp = np.clip((turns - 1) / (32 - 1), 0, 1)       # 0 interpolate, 1 keep
yarn = (1 - ramp) * theta / s + ramp * theta
print("pair  theta   turns  interpolated     YaRN")
for i in range(d // 2):
    print(f"{i:4d}  {theta[i]:5.3f}  {turns[i]:6.2f}  {theta[i] / s:12.5f}"
          f"  {yarn[i]:7.5f}")
print(f"YaRN logit multiplier at s = {s}: {(0.1 * np.log(s) + 1) ** 2:.3f}")
# [/listing]

# Hand-worked: 90 and 30 degrees give cos(60 degrees) = 0.5, and so do 300 and 240
assert np.allclose(rope(q, 3, one_pair), [0.0, 1.0], atol=1e-12)
assert np.allclose(rope(k, 1, one_pair), [np.sqrt(3) / 2, 0.5])
assert np.isclose(rope(q, 3, one_pair) @ rope(k, 1, one_pair), 0.5)
assert np.isclose(rope(q, 10, one_pair) @ rope(k, 8, one_pair), 0.5)

# The score depends only on the offset, for any vectors and all four pairs
rng = np.random.default_rng(0)
a, b = rng.normal(size=d), rng.normal(size=d)
assert np.isclose(rope(a, 7, theta) @ rope(b, 2, theta),
                  rope(a, 905, theta) @ rope(b, 900, theta))
# Rotation keeps length
assert np.isclose(np.linalg.norm(rope(a, 123, theta)), np.linalg.norm(a))

# Table values quoted in the chapter
assert np.allclose(theta, [1, 0.1, 0.01, 0.001])
assert np.allclose(turns.round(2), [159.15, 15.92, 1.59, 0.16])
assert np.isclose(ramp[0], 1.0) and np.isclose(ramp[3], 0.0)
assert np.isclose(yarn[0], 1.0) and np.isclose(yarn[3], 0.00025)
assert round((0.1 * np.log(4) + 1) ** 2, 3) == 1.296

# Position interpolation maps position 4,000 onto the angles of position 1,000
assert np.allclose(rope(a, 4000, theta / s), rope(a, 1000, theta))
# ...but two neighboring tokens now differ by a quarter of the trained angle
assert np.isclose(theta[0] / s, 0.25)

# Q96.1: 45 degrees per position, positions 5 and 3 -> cos(90 degrees) = 0
p45 = np.array([np.pi / 4])
assert np.isclose(rope(q, 5, p45) @ rope(k, 3, p45), 0.0, atol=1e-12)
# Q96.2: cost per question (illustrative price of USD 3 per million input tokens)
assert np.isclose(40_000 * 3 / 1e6, 0.12) and np.isclose(2_000 * 3 / 1e6, 0.006)
assert np.isclose(0.12 / 0.006, 20)
