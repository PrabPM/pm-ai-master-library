"""Chapter 22: the next-token loss, perplexity, and a count-based language model.

Run: python ch22_pretraining.py
"""
from collections import Counter

import numpy as np


def clm_loss(p_correct):
    """Mean negative log-probability the model gave to each true next token."""
    return float(-np.mean(np.log(p_correct)))


# Hand example: probability assigned to the true next token at four positions.
p_correct = np.array([0.5, 0.25, 0.8, 0.1])
loss = clm_loss(p_correct)
print(f"loss = {loss:.4f} nats   perplexity = {np.exp(loss):.3f}")
print(f"uniform guess over 50,000 tokens: perplexity = "
      f"{np.exp(clm_loss(np.full(4, 1 / 50_000))):,.0f}")

# What one training example looks like under each objective.
tokens = "your payout was sent today".split()
print("causal inputs :", tokens[:-1])
print("causal targets:", tokens[1:])
masked = [t if i != 1 else "[MASK]" for i, t in enumerate(tokens)]
print("masked input  :", masked)
print("masked target : position 1 =", tokens[1])

# A bigram model trained by counting, before and after it sees PayFlow text.
general = ["the bank sent the letter today", "your order was sent today",
           "the payment was late", "your letter was late today"]
domain = ["your payout was sent today", "the payout was delayed",
          "your refund was sent", "the refund was delayed today"]
held_out = "your payout was delayed today"


def bigram_perplexity(train, test, vocab):
    pair_counts, first_counts = Counter(), Counter()
    for line in train:
        words = ["<s>"] + line.split()
        for a, b in zip(words, words[1:]):
            pair_counts[a, b] += 1
            first_counts[a] += 1
    words = ["<s>"] + test.split()
    p = [(pair_counts[a, b] + 1) / (first_counts[a] + len(vocab))   # add-one smoothing
         for a, b in zip(words, words[1:])]
    return float(np.exp(clm_loss(np.array(p))))


vocab = {w for line in general + domain + [held_out] for w in line.split()}
before = bigram_perplexity(general, held_out, vocab)
after = bigram_perplexity(general + domain, held_out, vocab)
print(f"vocabulary = {len(vocab)} words")
print(f"held-out sentence: '{held_out}'")
print(f"perplexity after general text only = {before:.2f}")
print(f"perplexity after adding PayFlow text = {after:.2f}")

# Checks against the hand calculation in the chapter.
assert np.isclose(loss, np.log(100) / 4)
assert np.isclose(np.exp(loss), 100 ** 0.25)
assert after < before
