"""Chapter 95. Mixture of experts: top-k gating, the load-balancing loss, and why
total and active parameters are two different bills.

Run: python ch95_mixture_of_experts.py
"""
import numpy as np

# [listing]
def route(logits, k=2):
    """Keep the k largest router logits; softmax over the survivors only."""
    top = np.argsort(-logits)[:k]
    w = np.exp(logits[top] - logits[top].max())
    return top, w / w.sum()


logits = np.array([2.0, 1.0, 0.0, -1.0])           # router scores for one token
expert_out = np.array([0.9, 0.5, -0.3, 0.2])       # what each expert would say
top, gate = route(logits)
print("experts chosen:", top, " gate weights:", gate.round(3))
print("layer output:", round(float(gate @ expert_out[top]), 3))


def balance_loss(router_logits):
    """Switch Transformer auxiliary loss with alpha = 1: N * sum(f_e * P_e)."""
    n = router_logits.shape[1]
    probs = np.exp(router_logits - router_logits.max(1, keepdims=True))
    probs /= probs.sum(1, keepdims=True)
    f = np.bincount(probs.argmax(1), minlength=n) / len(probs)   # share of tokens
    return f, n * float(f @ probs.mean(0))


rng = np.random.default_rng(0)
tokens = rng.normal(size=(1000, 4))                # router logits for 1,000 tokens
for name, bias in [("balanced", 0.0), ("collapsing", 2.0)]:
    f, loss = balance_loss(tokens + np.array([bias, 0, 0, 0]))
    print(f"{name:10s} load per expert {f.round(2)}  loss {loss:.2f}")

for name, total, active in [("Mixtral 8x7B", 46.7, 12.9), ("DeepSeek-V3", 671, 37)]:
    print(f"{name}: {total * 2:.0f} GB of 16-bit weights, "
          f"{active / total:.1%} of them used per token")
# [/listing]

# Hand-worked: softmax over logits 2 and 1 is 1 / (1 + e^-1)
assert list(top) == [0, 1]
assert np.isclose(gate[0], 1 / (1 + np.exp(-1))) and round(gate[0], 3) == 0.731
assert np.isclose(gate @ expert_out[top], 0.731 * 0.9 + 0.269 * 0.5, atol=1e-3)
assert round(float(gate @ expert_out[top]), 3) == 0.792

# Uniform routing gives loss exactly 1; full collapse with P = 0.7 gives 2.8
N = 4
assert np.isclose(N * np.sum(np.full(N, 1 / N) * np.full(N, 1 / N)), 1.0)
assert np.isclose(N * np.sum(np.array([1, 0, 0, 0]) * np.array([.7, .1, .1, .1])), 2.8)
f_bal, l_bal = balance_loss(tokens)
f_col, l_col = balance_loss(tokens + np.array([2.0, 0, 0, 0]))
assert abs(l_bal - 1.0) < 0.05 and l_col > 1.5 and f_col[0] > 0.6

# Model-card arithmetic
assert np.isclose(46.7 * 2, 93.4) and round(12.9 / 46.7, 3) == 0.276
assert round(37 / 671, 3) == 0.055

# Q95.1: logits [1, 3, 0, 2], k = 2 -> experts 1 and 3, weights 0.731 / 0.269
t2, g2 = route(np.array([1.0, 3.0, 0.0, 2.0]))
assert list(t2) == [1, 3] and round(g2[0], 3) == 0.731
# Q95.2: 32 billion total, 9 billion active, 16-bit weights
assert np.isclose(32 * 2, 64) and round(9 / 32, 2) == 0.28
