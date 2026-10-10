"""Chapter 89: speculative decoding simulated on a three-token vocabulary.

Run: python ch89_speculative.py
"""
import numpy as np

rng = np.random.default_rng(0)
p = np.array([0.6, 0.3, 0.1])        # target model's next-token distribution
q = np.array([0.5, 0.2, 0.3])        # draft model's guess at the same distribution
residual = np.maximum(p - q, 0)
residual /= residual.sum()           # where the target wanted more than the draft gave


def draw(dist):
    return int(np.searchsorted(np.cumsum(dist), rng.random()))


def speculative_token():
    """One position: the draft proposes, the target accepts or corrects."""
    x = draw(q)
    if rng.random() < min(1.0, p[x] / q[x]):
        return x, True
    return draw(residual), False


def tokens_per_pass(gamma):
    """Draft gamma tokens, verify them in one target pass, count tokens kept."""
    kept = 0
    for _ in range(gamma):
        _, accepted = speculative_token()
        kept += 1                    # an accepted draft token, or the correction
        if not accepted:
            return kept              # the rest is discarded
    return kept + 1                  # all accepted: one bonus token


def expected_tokens(alpha, gamma):
    return (1 - alpha ** (gamma + 1)) / (1 - alpha)


def speedup(alpha, gamma, c):
    """c: cost of a draft step relative to a target pass."""
    return expected_tokens(alpha, gamma) / (gamma * c + 1)


n = 100_000
draws = [speculative_token() for _ in range(n)]
out = np.bincount([x for x, _ in draws], minlength=3) / n
alpha = float(np.minimum(p, q).sum())
print("target distribution:", p.tolist())
print("speculative output: ", np.round(out, 3).tolist())
print(f"acceptance rate: formula {alpha:.2f}, "
      f"simulated {np.mean([a for _, a in draws]):.3f}")

gamma = 4
sim = np.mean([tokens_per_pass(gamma) for _ in range(40_000)])
print(f"tokens per target pass at gamma = {gamma}: formula "
      f"{expected_tokens(alpha, gamma):.3f}, simulated {sim:.3f}")
print("acceptance  tokens/pass  speedup (draft cost 5% of a target pass)")
for a in (0.5, 0.7, 0.8, 0.9):
    print(f"   {a:.1f}        {expected_tokens(a, gamma):.2f}        "
          f"{speedup(a, gamma, 0.05):.2f}x")

# Checks against the hand calculation in the chapter.
assert np.isclose(alpha, 0.8) and np.allclose(residual, [0.5, 0.5, 0.0])
assert np.abs(out - p).max() < 0.005
assert np.isclose(expected_tokens(0.8, 4), 3.3616)
assert abs(sim - 3.3616) < 0.03
assert np.isclose(speedup(0.8, 4, 0.05), 3.3616 / 1.2)
