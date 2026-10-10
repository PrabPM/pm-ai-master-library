"""Chapter 28: why word overlap misleads, and a confidence interval on a pass rate.

Run: python ch28_evaluation.py
"""
from collections import Counter

import numpy as np

reference = "payouts arrive in two business days"
candidates = {
    "A (right, reworded)": "you get your money within 2 working days",
    "B (wrong number)": "payouts arrive in ten business days",
}


def ngrams(text, n):
    words = text.split()
    return Counter(tuple(words[i:i + n]) for i in range(len(words) - n + 1))


def overlap_f1(candidate, reference):
    """ROUGE-1 style: unigram precision and recall, combined as F1."""
    c, r = ngrams(candidate, 1), ngrams(reference, 1)
    shared = sum((c & r).values())                 # clipped counts
    if shared == 0:
        return 0.0
    precision, recall = shared / sum(c.values()), shared / sum(r.values())
    return 2 * precision * recall / (precision + recall)


def bigram_precision(candidate, reference):
    """BLEU style: share of the candidate's word pairs found in the reference."""
    c, r = ngrams(candidate, 2), ngrams(reference, 2)
    return sum((c & r).values()) / sum(c.values())


for name, text in candidates.items():
    print(f"{name:20s} unigram F1 = {overlap_f1(text, reference):.3f}   "
          f"bigram precision = {bigram_precision(text, reference):.3f}")


def wilson(passed, n, z=1.96):
    """95% Wilson score interval for a pass rate."""
    p = passed / n
    center = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return center - half, center + half


print("golden set results")
for label, passed, n in [("prompt v1", 42, 50), ("prompt v2", 45, 50),
                         ("prompt v1", 420, 500), ("prompt v2", 450, 500)]:
    lo, hi = wilson(passed, n)
    print(f"  {label}: {passed}/{n} = {passed / n:.2f}   95% interval "
          f"{lo:.3f} to {hi:.3f}")

# Checks against the hand calculation in the chapter.
assert np.isclose(overlap_f1(candidates["A (right, reworded)"], reference), 1 / 7)
assert np.isclose(overlap_f1(candidates["B (wrong number)"], reference), 5 / 6)
assert np.isclose(bigram_precision(candidates["B (wrong number)"], reference), 3 / 5)
lo, hi = wilson(42, 50)
assert np.isclose(lo, 0.7149, atol=5e-4) and np.isclose(hi, 0.9166, atol=5e-4)
