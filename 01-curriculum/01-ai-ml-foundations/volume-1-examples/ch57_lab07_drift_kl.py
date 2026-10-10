"""Chapter 57, Lab 7: has the merchant category mix drifted?"""
import numpy as np

old = np.array([0.50, 0.30, 0.15, 0.05])   # retail, food, travel, digital goods
new = np.array([0.40, 0.30, 0.20, 0.10])


def entropy(p):
    return float(-np.sum(p * np.log2(p)))


def kl(p, q):
    """D(p || q) in bits: extra bits paid for coding p with a code built for q."""
    return float(np.sum(p * np.log2(p / q)))


print(f"entropy old {entropy(old):.4f} bits, new {entropy(new):.4f} bits")
print(f"KL(new || old) {kl(new, old):.4f} bits   "
      f"KL(old || new) {kl(old, new):.4f} bits")
print(f"cross-entropy H(new, old) {entropy(new) + kl(new, old):.4f} bits")

# Noise floor: KL of a 500-payment sample drawn from the OLD mix against old.
rng = np.random.default_rng(57)
noise = []
for _ in range(2000):
    sample = rng.multinomial(500, old) / 500
    sample = np.clip(sample, 1e-9, None)
    noise.append(kl(sample, old))
print(f"noise floor at n=500: median {np.median(noise):.4f}, "
      f"95th percentile {np.percentile(noise, 95):.4f} bits")

# ---- checks against the hand results ----
assert np.isclose(entropy(old), 1.6477, atol=1e-4)
assert np.isclose(entropy(new), 1.8464, atol=1e-4)
assert np.isclose(kl(new, old), 0.0542, atol=1e-4)
assert np.isclose(kl(old, new), 0.0487, atol=1e-4)
assert kl(new, old) > 3 * np.percentile(noise, 95)
