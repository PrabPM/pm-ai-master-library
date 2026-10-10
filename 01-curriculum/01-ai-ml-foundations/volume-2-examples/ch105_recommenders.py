"""Chapter 105. Recommenders in depth: in-batch softmax for a two-tower model, the
sampling-bias (logQ) correction, and a listwise ranking loss.

Run: python ch105_recommenders.py
"""
import numpy as np

# [listing]
def in_batch_loss(scores, item_prob=None):
    """Row r is one merchant; column r holds the app that merchant installed."""
    logits = scores if item_prob is None else scores - np.log(item_prob)
    log_p = logits - np.log(np.exp(logits).sum(1, keepdims=True))
    return -np.diag(log_p)


# dot products of 3 merchant vectors (rows) with the 3 apps in the batch (columns)
scores = np.array([[3.0, 0.5, 0.2],
                   [1.5, 2.0, 0.0],
                   [1.0, 0.3, 2.5]])
item_prob = np.array([0.6, 0.1, 0.3])              # share of all installs per app
plain = in_batch_loss(scores)
fixed = in_batch_loss(scores, item_prob)
print("per-merchant loss, plain    :", plain.round(3), "mean", plain.mean().round(3))
print("per-merchant loss, corrected:", fixed.round(3), "mean", fixed.mean().round(3))
weights = np.exp(scores[1]) / item_prob            # merchant 1's corrected terms
print("merchant 1 terms after dividing by popularity:", weights.round(2))


def listwise_loss(scores, relevance):
    """ListNet top-one loss: cross-entropy between two softmax distributions."""
    target = np.exp(relevance) / np.exp(relevance).sum()
    log_p = scores - np.log(np.exp(scores).sum())
    return -(target * log_p).sum()


relevance = np.array([2.0, 0.0, 1.0, 0.0])         # graded labels for 4 candidates
print("listwise loss, good order:",
      listwise_loss(np.array([2.0, 0.0, 1.0, 0.0]), relevance).round(3))
print("listwise loss, reversed  :",
      listwise_loss(np.array([0.0, 2.0, 0.0, 1.0]), relevance).round(3))
# [/listing]

# Hand-worked row for merchant 1 (scores 1.5, 2.0, 0.0; positive is column 1)
e = np.exp
assert np.allclose(e([1.5, 2.0, 0.0]).round(3), [4.482, 7.389, 1.0])
assert round(e(2.0) / (e(1.5) + e(2.0) + 1), 3) == 0.574
assert round(plain[1], 3) == 0.555
terms = np.array([e(1.5) / 0.6, e(2.0) / 0.1, 1 / 0.3])
assert np.allclose(terms.round(2), [7.47, 73.89, 3.33]) and np.allclose(weights, terms)
assert round(terms[1] / terms.sum(), 3) == 0.872 and round(fixed[1], 3) == 0.136
# The correction equals importance-weighting each term by 1 / item_prob
assert np.allclose(fixed, -np.log(np.diag(e(scores) / item_prob)
                                  / (e(scores) / item_prob).sum(1)))
# With equal item probabilities the correction changes nothing
assert np.allclose(in_batch_loss(scores, np.full(3, 1 / 3)), plain)
# Listwise loss is smallest when scores reproduce the relevance pattern
good = listwise_loss(np.array([2.0, 0.0, 1.0, 0.0]), relevance)
bad = listwise_loss(np.array([0.0, 2.0, 0.0, 1.0]), relevance)
assert good < bad
target = e(relevance) / e(relevance).sum()
assert np.isclose(good, -(target * np.log(target)).sum())   # equals target entropy

# Q105.1: scores [1.0, 1.0], positive first, item probabilities 0.8 and 0.2
q = in_batch_loss(np.array([[1.0, 1.0], [0.0, 0.0]]), np.array([0.8, 0.2]))
assert np.isclose(q[0], -np.log((1 / 0.8) / (1 / 0.8 + 1 / 0.2)))
assert round(q[0], 3) == 1.609 and np.isclose(q[0], np.log(5))
assert np.isclose(in_batch_loss(np.array([[1.0, 1.0], [0.0, 0.0]]))[0], np.log(2))
