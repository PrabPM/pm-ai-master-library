"""Chapter 19: next-token prediction with temperature, top-k and top-p.

A five-token toy vocabulary. The table NEXT stands in for the network: it returns
the logits a trained model would produce after a given last token.
Run: python ch19_next_token.py
"""
import numpy as np

vocab = ["sent", "pending", "delayed", "today", "<end>"]
# Logits after the prompt "Your payout is". Chosen so that the probabilities at
# temperature 1 are exactly 1/2, 1/4, 1/8, 1/16, 1/16.
logits = np.log(np.array([8.0, 4.0, 2.0, 1.0, 1.0]))


def softmax(z, temperature=1.0):
    z = z / temperature
    e = np.exp(z - z.max())            # subtract the max for numerical safety
    return e / e.sum()


def top_k(p, k):
    keep = np.argsort(-p, kind="stable")[:k]
    out = np.zeros_like(p)
    out[keep] = p[keep]
    return out / out.sum()             # renormalize what is left


def top_p(p, threshold):
    order = np.argsort(-p, kind="stable")
    cumulative = np.cumsum(p[order])
    n_keep = np.searchsorted(cumulative, threshold) + 1   # smallest set that reaches it
    out = np.zeros_like(p)
    out[order[:n_keep]] = p[order[:n_keep]]
    return out / out.sum()


def show(label, p):
    print(f"{label:14s}", "  ".join(f"{w}={x:.4f}" for w, x in zip(vocab, p)))


p1 = softmax(logits)
show("T = 1.0", p1)
show("T = 0.5", softmax(logits, 0.5))
show("T = 2.0", softmax(logits, 2.0))
show("top-k, k = 2", top_k(p1, 2))
show("top-p, p = 0.8", top_p(p1, 0.8))

# The generation loop. NEXT[last token] is the stand-in for one forward pass.
NEXT = {
    "is": logits,
    "sent": np.log(np.array([0.1, 0.1, 0.1, 6.0, 2.0])),
    "pending": np.log(np.array([0.1, 0.1, 0.1, 3.0, 5.0])),
    "delayed": np.log(np.array([0.1, 0.1, 0.1, 4.0, 4.0])),
    "today": np.log(np.array([0.1, 0.1, 0.1, 0.1, 9.0])),
}


def generate(rng=None, temperature=1.0, max_new_tokens=4):
    tokens = ["Your", "payout", "is"]
    for _ in range(max_new_tokens):
        p = softmax(NEXT[tokens[-1]], temperature)
        i = int(np.argmax(p)) if rng is None else int(rng.choice(len(vocab), p=p))
        tokens.append(vocab[i])         # the choice becomes part of the next input
        if vocab[i] == "<end>":
            break
    return " ".join(tokens)


print("greedy:         ", generate())
rng = np.random.default_rng(7)
for n in range(1, 4):
    print(f"sample {n}, T = 1:", generate(rng))

# Checks against the hand calculation in the chapter.
assert np.allclose(p1, [0.5, 0.25, 0.125, 0.0625, 0.0625])
assert np.allclose(softmax(logits, 0.5), np.array([64, 16, 4, 1, 1]) / 86)
roots = np.sqrt([8, 4, 2, 1, 1])
assert np.allclose(softmax(logits, 2.0), roots / roots.sum())
assert np.allclose(top_k(p1, 2), [2 / 3, 1 / 3, 0, 0, 0])
assert np.allclose(top_p(p1, 0.8), [4 / 7, 2 / 7, 1 / 7, 0, 0])
