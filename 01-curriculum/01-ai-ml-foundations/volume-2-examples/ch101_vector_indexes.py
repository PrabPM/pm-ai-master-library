"""Chapter 101. Vector indexes: memory arithmetic for flat, HNSW and IVF-PQ, and
an inverted-file (IVF) index in NumPy with recall measured against exact search.
A small product quantizer runs after the listing.

Run: python ch101_vector_indexes.py
"""
import numpy as np

rng = np.random.default_rng(0)
N, D, NLIST, K = 20_000, 32, 100, 10
# Synthetic "ticket embeddings": 20 broad topics with a lot of spread
topics = rng.normal(size=(20, D))
X = (topics[rng.integers(0, 20, N)] + rng.normal(size=(N, D))).astype("f4")
queries = (topics[rng.integers(0, 20, 200)] + rng.normal(size=(200, D))).astype("f4")


def sq_dist(a, b):
    """Squared Euclidean distance between every row of a and every row of b."""
    return (a ** 2).sum(1)[:, None] - 2 * a @ b.T + (b ** 2).sum(1)[None, :]


# [listing]
n, d, M, m = 100_000_000, 768, 32, 64              # m = PQ bytes per vector
print(f"flat float32 : {n * d * 4 / 1e9:6.1f} GB")
print(f"HNSW (M=32)  : {n * (d * 4 + M * 2 * 4) / 1e9:6.1f} GB")
print(f"IVF-PQ (m=64): {n * (m + 8) / 1e9:6.1f} GB with 8-byte ids")

# IVF: k-means cells; search only nprobe of them
centroids = X[rng.choice(N, NLIST, replace=False)].copy()
for _ in range(8):                                 # Lloyd's k-means
    cell = sq_dist(X, centroids).argmin(1)
    for c in np.unique(cell):
        centroids[c] = X[cell == c].mean(0)
cell = sq_dist(X, centroids).argmin(1)
lists = [np.flatnonzero(cell == c) for c in range(NLIST)]

exact = sq_dist(queries, X).argsort(1)[:, :K]      # ground truth
nearest_cells = sq_dist(queries, centroids).argsort(1)
recall = {}
for nprobe in (1, 2, 4, 8, 16):
    hits = scanned = 0
    for qi, q in enumerate(queries):
        cand = np.concatenate([lists[c] for c in nearest_cells[qi, :nprobe]])
        top = cand[sq_dist(q[None], X[cand])[0].argsort()[:K]]
        hits += len(set(top) & set(exact[qi]))
        scanned += len(cand)
    recall[nprobe] = hits / (K * len(queries))
    print(f"nprobe {nprobe:2d}: recall@10 {recall[nprobe]:.3f}, "
          f"scanned {scanned / (N * len(queries)):5.1%}")
# [/listing]

# Hand-worked memory arithmetic
assert np.isclose(n * d * 4 / 1e9, 307.2)
assert np.isclose(n * (d * 4 + M * 2 * 4) / 1e9, 332.8)
assert np.isclose(n * (m + 8) / 1e9, 7.2)
assert d * 4 / m == 48                              # compression of the vectors

r = list(recall.values())
assert all(a <= b + 1e-9 for a, b in zip(r, r[1:]))   # more probes never hurts
# probing every cell is an exact search
for qi, q in enumerate(queries[:20]):
    cand = np.concatenate(lists)
    top = cand[sq_dist(q[None], X[cand])[0].argsort()[:K]]
    assert set(top) == set(exact[qi])
assert recall[1] < 0.6 and recall[8] > 0.95

# Product quantization on the same data: 8 sub-vectors of 4 dims, 256 codes each,
# so a 128-byte float32 vector is stored as 8 one-byte codes (16 times smaller).
m_sub, ks = 8, 256
sub = X.reshape(N, m_sub, D // m_sub)
codebooks = np.stack([sub[rng.choice(N, ks, replace=False), j] for j in range(m_sub)])
for _ in range(4):
    for j in range(m_sub):
        code_j = sq_dist(sub[:, j], codebooks[j]).argmin(1)
        for c in np.unique(code_j):
            codebooks[j, c] = sub[code_j == c, j].mean(0)
codes = np.stack([sq_dist(sub[:, j], codebooks[j]).argmin(1)
                  for j in range(m_sub)], axis=1).astype("u1")
assert codes.nbytes == N * m_sub and X.nbytes / codes.nbytes == 16
# Asymmetric distance: query sub-vector to each codeword, then table lookups
q_sub = queries.reshape(len(queries), m_sub, D // m_sub)
tables = np.stack([sq_dist(q_sub[:, j], codebooks[j]) for j in range(m_sub)], 1)
approx = sum(tables[:, j, codes[:, j]] for j in range(m_sub))
pq_order = approx.argsort(1)
pq_recall = np.mean([len(set(a) & set(b)) / K for a, b in zip(pq_order[:, :K], exact)])
# Re-rank the 100 best PQ candidates with the original vectors
rerank = [s[sq_dist(q[None], X[s])[0].argsort()[:K]]
          for q, s in zip(queries, pq_order[:, :100])]
rr_recall = np.mean([len(set(a) & set(b)) / K for a, b in zip(rerank, exact)])
print(f"PQ, 8 bytes per vector: recall@10 {pq_recall:.3f}; "
      f"best 100 re-ranked with full vectors: {rr_recall:.3f}")
assert pq_recall < rr_recall and rr_recall > 0.9

# Q101.1: 50 million vectors of 1,024 dims; HNSW with M = 16; PQ with m = 32
assert np.isclose(50e6 * 1024 * 4 / 1e9, 204.8)
assert np.isclose(50e6 * (1024 * 4 + 16 * 2 * 4) / 1e9, 211.2)
assert np.isclose(50e6 * (32 + 8) / 1e9, 2.0)
# Q101.2: post-filter with 2% of vectors matching: expected survivors of top 10,
# and the candidate count needed to expect 10 survivors
assert np.isclose(10 * 0.02, 0.2) and np.isclose(10 / 0.02, 500)
