"""Chapter 21: word vectors from co-occurrence counts, and what cosine means.

Run: python ch21_embeddings.py
"""
import numpy as np

sentences = [
    "refund approved for customer",
    "refund denied for customer",
    "dispute denied for customer",
    "payout delayed by bank",
    "payout sent by bank",
]
vocab = sorted({w for s in sentences for w in s.split()})
index = {w: i for i, w in enumerate(vocab)}

# Static word vectors: row w counts how often w shares a sentence with each word.
C = np.zeros((len(vocab), len(vocab)))
for s in sentences:
    words = s.split()
    for a in words:
        for b in words:
            if a != b:
                C[index[a], index[b]] += 1


def cosine(u, v):
    return float(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)))


def word(w):
    return C[index[w]]


def sentence(text):
    """Sentence embedding by mean pooling: average the word vectors, then normalize."""
    e = np.mean([word(w) for w in text.split()], axis=0)
    return e / np.linalg.norm(e)


print("word pairs")
for a, b in [("approved", "denied"), ("delayed", "sent"), ("approved", "delayed")]:
    print(f"  cos({a}, {b}) = {cosine(word(a), word(b)):.3f}")

query = "refund approved"
print(f"sentences compared with '{query}'")
for other in ["refund denied", "dispute denied", "payout delayed"]:
    print(f"  cos = {cosine(sentence(query), sentence(other)):.3f}   {other}")

# Storage for an index of one million ticket embeddings.
n, d = 1_000_000, 1024
print(f"index size: {n:,} x {d} float32 = {n * d * 4 / 1e9:.1f} GB; "
      f"int8 = {n * d / 1e9:.1f} GB")

# Checks against the hand calculation in the chapter.
assert np.isclose(cosine(word("approved"), word("denied")), 5 / np.sqrt(3 * 10))
assert np.isclose(cosine(word("approved"), word("delayed")), 0.0)
assert cosine(sentence("refund approved"), sentence("refund denied")) > 0.9
