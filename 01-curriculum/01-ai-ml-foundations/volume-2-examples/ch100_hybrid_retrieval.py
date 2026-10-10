"""Chapter 100. Hybrid retrieval and query rewriting: BM25 from scratch, a
stand-in dense retriever, reciprocal rank fusion, and a rewritten query.

Run: python ch100_hybrid_retrieval.py
"""
import math

import numpy as np

docs = ["error PF-4012 bank rejected the payout transfer",
        "why your payout is late and when the money arrives",
        "error PF-4012 on a refund means the card was closed",
        "dispute evidence checklist for merchants"]
tok = [d.lower().split() for d in docs]
N, avgdl = len(docs), sum(map(len, tok)) / len(docs)

# Stand-in for an embedding model (chapter 21): words that mean the same thing
# share a direction, so "funds" and "payout" match although the strings differ.
CONCEPT = {"payout": 0, "money": 0, "funds": 0, "late": 1, "arrives": 1, "arrived": 1,
           "refund": 2, "dispute": 3, "evidence": 3}


def embed(text):
    v = np.zeros(4)
    for t in text.lower().split():
        if t in CONCEPT:
            v[CONCEPT[t]] += 1
    return v / max(np.linalg.norm(v), 1e-9)


def ranking(scores):
    """Document indices from best to worst (ties keep document order)."""
    return [int(i) for i in np.argsort(-np.array(scores), kind="stable")]


# [listing]
def bm25(query, i, k1=1.2, b=0.75):
    score = 0.0
    for t in query.lower().split():
        n_t = sum(t in d for d in tok)             # documents containing t
        f = tok[i].count(t)                        # occurrences in document i
        idf = math.log(1 + (N - n_t + 0.5) / (n_t + 0.5))
        score += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * len(tok[i]) / avgdl))
    return score


def rrf(rankings, k=60):
    fused = np.zeros(N)
    for order in rankings:
        for rank, i in enumerate(order, start=1):
            fused[i] += 1 / (k + rank)
    return fused


query = "funds not arrived PF-4012"
sparse_scores = [bm25(query, i) for i in range(N)]
sparse = ranking(sparse_scores)
dense = ranking([embed(query) @ embed(d) for d in docs])
fused = rrf([sparse, dense])
print("BM25 scores:", np.round(sparse_scores, 4), "order", sparse)
print("dense order:", dense)
print("RRF scores :", fused.round(5), "order", ranking(fused))

rewrite = "payout late PF-4012"                    # from a rewriting model
print("BM25 order after rewriting:", ranking([bm25(rewrite, i) for i in range(N)]))
# [/listing]

# Hand-worked BM25 for the term "pf-4012" in document 0
assert avgdl == 8.0 and [len(t) for t in tok] == [7, 10, 10, 5]
idf = math.log(1 + (4 - 2 + 0.5) / (2 + 0.5))
assert np.isclose(idf, math.log(2))
tf_part = 1 * 2.2 / (1 + 1.2 * (0.25 + 0.75 * 7 / 8))
assert np.isclose(tf_part, 2.2 / 2.0875)
assert np.isclose(sparse_scores[0], idf * tf_part)
assert round(sparse_scores[0], 4) == 0.7305
assert round(sparse_scores[2], 4) == 0.6288 and sparse_scores[1] == 0.0

# Hand-worked fusion
assert sparse == [0, 2, 1, 3] and dense == [1, 0, 2, 3]
assert np.isclose(fused[0], 1 / 61 + 1 / 62) and round(fused[0], 5) == 0.03252
assert np.isclose(fused[1], 1 / 63 + 1 / 61) and round(fused[1], 5) == 0.03227
assert np.isclose(fused[2], 1 / 62 + 1 / 63) and round(fused[2], 5) == 0.03200
assert ranking(fused) == [0, 1, 2, 3]

# Dense scores behind the dense order: cos = 1.0 for the paraphrase, 0.707 for doc 0
dense_scores = [float(embed(query) @ embed(d)) for d in docs]
assert np.allclose(dense_scores, [1 / np.sqrt(2), 1.0, 0.0, 0.0])

# The rewrite lets keyword search find the paraphrased article
assert ranking([bm25(rewrite, i) for i in range(N)]) == [1, 0, 2, 3]

# Multi-query: fuse both retrievers over the original query and two rewrites
queries = [query, rewrite, "bank transfer rejected money late"]
many = [ranking([bm25(q, i) for i in range(N)]) for q in queries]
many += [ranking([embed(q) @ embed(d) for d in docs]) for q in queries]
assert ranking(rrf(many))[:2] in ([0, 1], [1, 0])

# Late interaction (ColBERT-style MaxSim) on toy per-token vectors:
# each query token takes its best-matching document token, then the maxima add up
q_tok = np.array([[1.0, 0.0], [0.0, 1.0]])
d_tok = np.array([[0.8, 0.6], [0.0, 1.0], [0.6, 0.8]])
assert np.isclose((q_tok @ d_tok.T).max(axis=1).sum(), 0.8 + 1.0)

# Q100.1: term in 1 of 4 documents, f = 2, document of average length
idf_q = math.log(1 + 3.5 / 1.5)
assert np.isclose(idf_q * 2 * 2.2 / (2 + 1.2), 1.6555, atol=1e-4)
# Q100.2: ranks (1, 3) versus (2, 2) with k = 60
assert 1 / 61 + 1 / 63 > 2 / 62 and round(1 / 61 + 1 / 63, 5) == 0.03227
assert round(2 / 62, 5) == 0.03226
