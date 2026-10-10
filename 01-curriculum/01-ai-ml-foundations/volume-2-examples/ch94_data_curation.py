"""Chapter 94. Data curation: near-duplicate detection with shingles and MinHash,
an n-gram contamination check, and tokens-per-parameter arithmetic.

Run: python ch94_data_curation.py
"""
import hashlib

import numpy as np

# [listing]
def shingles(text, k=2):
    words = text.lower().split()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


def minhash(shingle_set, n_hashes=256):
    """For each of n salted hash functions, keep the smallest hash value."""
    return [min(hashlib.blake2b(s.encode(), digest_size=8,
                                salt=i.to_bytes(8, "little")).digest()
                for s in shingle_set) for i in range(n_hashes)]


tickets = ["refund not received after dispute closed",
           "refund not received after dispute won",
           "payout delayed by bank holiday"]
sets = [shingles(t) for t in tickets]
sigs = [minhash(s) for s in sets]
for i, j in [(0, 1), (0, 2)]:
    exact = len(sets[i] & sets[j]) / len(sets[i] | sets[j])
    est = np.mean([x == y for x, y in zip(sigs[i], sigs[j])])
    print(f"tickets {i} and {j}: Jaccard {exact:.3f}, MinHash estimate {est:.3f}")

eval_question = "why was my refund not received after the dispute"
leak = shingles(tickets[0], k=4) & shingles(eval_question, k=4)
print("4-word overlaps with the evaluation set:", sorted(leak))
print(f"tokens per parameter: Chinchilla {1.4e12 / 70e9:.0f}, "
      f"8 billion parameters on 15 trillion tokens {15e12 / 8e9:.0f}")
# [/listing]

def jaccard(a, b):
    return len(a & b) / len(a | b)


# Hand-worked: 5 bigrams each, 4 shared, union 6
assert len(sets[0]) == 5 and len(sets[1]) == 5
assert len(sets[0] & sets[1]) == 4 and len(sets[0] | sets[1]) == 6
assert np.isclose(jaccard(sets[0], sets[1]), 2 / 3)
assert jaccard(sets[0], sets[2]) == 0.0
est01 = np.mean([x == y for x, y in zip(sigs[0], sigs[1])])
# standard error of the estimate is sqrt(J(1-J)/n) = sqrt(0.222/256) = 0.029
se = np.sqrt((2 / 3) * (1 / 3) / 256)
assert np.isclose(se, 0.0295, atol=5e-4)
assert abs(est01 - 2 / 3) < 3 * se
assert leak == {"refund not received after"}
assert np.isclose(1.4e12 / 70e9, 20.0) and np.isclose(15e12 / 8e9, 1875.0)

# Q94.1: 6 shared shingles, 10 and 8 in each set -> union 12, Jaccard 0.5
assert np.isclose(6 / (10 + 8 - 6), 0.5)
# Q94.2: standard error with 64 hashes at J = 0.5, and with 256
assert np.isclose(np.sqrt(0.25 / 64), 0.0625)
assert np.isclose(np.sqrt(0.25 / 256), 0.03125)
