"""Chapter 43: perplexity of a toy language model for PayFlow support tickets.

A bigram model predicts each word from the one before it. It is trained on
eight short tickets and scored on three it has not seen.
"""
from collections import Counter

import numpy as np

train = ["my payout is delayed", "my payout is on hold",
         "the payout is delayed again", "my refund is delayed",
         "the refund is pending", "my card was declined",
         "the card was declined again", "my payout was sent"]
held_out = ["my refund is on hold", "the payout was declined",
            "the refund was sent"]


def tokens(sentence):
    return ["<s>"] + sentence.split() + ["</s>"]


def perplexity(probabilities):
    """exp of the average surprise, in nats, of the tokens that occurred."""
    probabilities = np.asarray(probabilities, dtype=float)
    if np.any(probabilities == 0):
        return float("inf")
    return float(np.exp(-np.mean(np.log(probabilities))))


# ---- by hand: four tokens with probabilities 1/2, 1/4, 1/4, 1/8 -----------
hand = [1 / 2, 1 / 4, 1 / 4, 1 / 8]
bits = -np.mean(np.log2(hand))
print(f"hand example: {bits:.1f} bits per token, perplexity = {perplexity(hand):.1f}")
assert np.isclose(bits, 2.0) and np.isclose(perplexity(hand), 4.0)
assert np.isclose(perplexity(hand), 2**bits)

# ---- train the counts -------------------------------------------------------
unigram, bigram = Counter(), Counter()
for sentence in train:
    t = tokens(sentence)
    unigram.update(t[1:])                      # every token we have to predict
    bigram.update(zip(t[:-1], t[1:]))
context = Counter()
for (prev, _), count in bigram.items():
    context[prev] += count
vocab = sorted(unigram)                        # 14 words plus the end marker
V = len(vocab)
total = sum(unigram.values())


def p_uniform(prev, word):
    return 1 / V


def p_unigram(prev, word):
    return (unigram[word] + 1) / (total + V)                 # add-one smoothing


def p_bigram(prev, word, k=1):
    return (bigram[(prev, word)] + k) / (context[prev] + k * V)


def score(model, sentences):
    probs = []
    for sentence in sentences:
        t = tokens(sentence)
        probs += [model(prev, word) for prev, word in zip(t[:-1], t[1:])]
    return perplexity(probs), len(probs)


print(f"vocabulary size V = {V}, training tokens = {total}")
results = {}
for name, model in [("uniform guess", p_uniform), ("unigram", p_unigram),
                    ("bigram", p_bigram)]:
    results[name], n_tokens = score(model, held_out)
    print(f"{name:14} held-out perplexity = {results[name]:6.2f}  "
          f"({np.log2(results[name]):.2f} bits per token, {n_tokens} tokens)")
print(f"bigram on its own training tickets = {score(p_bigram, train)[0]:.2f}")
raw = score(lambda prev, word: p_bigram(prev, word, k=0), held_out)[0]
print(f"bigram with no smoothing, held-out = {raw}")

assert np.isclose(results["uniform guess"], V)       # uniform over V -> exactly V
assert results["bigram"] < results["unigram"] < results["uniform guess"]
assert score(p_bigram, train)[0] < results["bigram"]
assert raw == float("inf")                           # "refund was" was never seen
for prev in list(context):                           # each row is a distribution
    assert np.isclose(sum(p_bigram(prev, w) for w in vocab), 1.0)
