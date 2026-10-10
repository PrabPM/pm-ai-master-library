"""Chapter 12. Embeddings and vector search: exact search, a small approximate
index built from scratch, memory sizing, and why embedding models never mix."""
import numpy as np


def normalize(X):
    """Scale every row to length 1, so a dot product is a cosine."""
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def exact_search(vectors, query, k):
    """Compare the query with every stored vector: always right, cost grows with N."""
    scores = vectors @ query
    return np.argsort(-scores)[:k]


def approximate_search(vectors, centers, cells, query, k, n_probe):
    """Look only inside the n_probe cells whose centers are closest to the query."""
    nearest_cells = np.argsort(-(centers @ query))[:n_probe]
    candidates = np.concatenate([cells[c] for c in nearest_cells])
    scores = vectors[candidates] @ query
    return candidates[np.argsort(-scores)[:k]], len(candidates)


def recall_at_k(found, truth):
    """Share of the true top k that the approximate search also returned."""
    return len(set(found) & set(truth)) / len(truth)


def index_gb(n, d, bytes_per_number):
    """Memory for the raw vectors, in gigabytes (1 GB = 10^9 bytes)."""
    return n * d * bytes_per_number / 1e9


def build_cells(vectors, n_cells, rng, rounds=8):
    """Group the vectors into cells around n_cells centers (plain k-means)."""
    centers = vectors[rng.choice(len(vectors), n_cells, replace=False)]
    for _ in range(rounds):
        cell_of = np.argmax(vectors @ centers.T, axis=1)
        for c in range(n_cells):
            members = vectors[cell_of == c]
            if len(members):
                centers[c] = normalize(members.mean(axis=0))
    cell_of = np.argmax(vectors @ centers.T, axis=1)
    return centers, [np.flatnonzero(cell_of == c) for c in range(n_cells)]


def make_embeddings(n, d, n_topics, rng, spread=1.5):
    """Stand-in for a model's output: points scattered around topic directions."""
    topics = normalize(rng.standard_normal((n_topics, d)))
    noise = rng.standard_normal((n, d)) / np.sqrt(d)
    return normalize(topics[rng.integers(n_topics, size=n)] + spread * noise)


def recall_curve(seed=12, n=20_000, d=64, k=10, n_cells=100, n_queries=200):
    """Recall@k and share of the index scanned, for several values of n_probe."""
    rng = np.random.default_rng(seed)
    data = make_embeddings(n + n_queries, d, 40, rng)
    vectors, queries = data[:n], data[n:]
    centers, cells = build_cells(vectors, n_cells, rng)
    rows = []
    for n_probe in (1, 2, 5, 10, 20, n_cells):
        recalls, scanned = [], []
        for query in queries:
            truth = exact_search(vectors, query, k)
            found, looked_at = approximate_search(vectors, centers, cells, query,
                                                  k, n_probe)
            recalls.append(recall_at_k(found, truth))
            scanned.append(looked_at / n)
        rows.append((n_probe, float(np.mean(scanned)), float(np.mean(recalls))))
    return rows, vectors, queries


# 1. Memory: 10 million support tickets, 768 numbers each.
sizes = [index_gb(10_000_000, 768, b) for b in (4, 1, 1 / 8)]
print("10M x 768 in GB as float32, int8, 1 bit:", sizes)

# 2. Exact search on the five merchant vectors from Chapter 11.
names = ["Juniper", "Corner", "Northwind", "Harbor", "Summit"]
table = normalize(np.array([[12, 5], [8, 6], [4, 8], [6, 8], [10, 8]], float))
top2 = exact_search(table, normalize(np.array([3.0, 4.0])), k=2)
print("two nearest merchants to (3, 4):", [names[i] for i in top2])

# 3. Approximate search: scan fewer vectors, miss a few true neighbors.
rows, vectors, queries = recall_curve()
print("cells probed  share scanned  recall@10")
for n_probe, share, recall in rows:
    print(f"{n_probe:12d}  {share:13.1%}  {recall:9.3f}")

# 4. Two models: model B is model A with every vector rotated the same way.
rng = np.random.default_rng(3)
rotation, _ = np.linalg.qr(rng.standard_normal((64, 64)))
vectors_b, queries_b = vectors @ rotation, queries @ rotation
same, mixed = [], []
for q_a, q_b in zip(queries, queries_b):
    truth = exact_search(vectors, q_a, 10)
    same.append(recall_at_k(exact_search(vectors_b, q_b, 10), truth))
    mixed.append(recall_at_k(exact_search(vectors, q_b, 10), truth))
print(f"recall, query and index from model B: {np.mean(same):.3f}")
print(f"recall, query from B, index from A:   {np.mean(mixed):.3f}")

# Checks against the hand calculation in the chapter.
assert np.allclose(sizes, [30.72, 7.68, 0.96])
assert np.isclose(10_000_000 * 32 * 2 * 4 / 1e9, 2.56)      # graph links, M = 32
assert [names[i] for i in top2] == ["Harbor", "Northwind"]
assert rows[-1][1] == 1.0 and rows[-1][2] == 1.0            # probing all = exact
assert all(a[2] <= b[2] for a, b in zip(rows, rows[1:]))    # recall never drops
assert np.isclose(np.mean(same), 1.0) and np.mean(mixed) < 0.05

# Answers to Check yourself.
assert np.isclose(index_gb(2_000_000, 1024, 4), 8.192)              # Q12.1
assert np.isclose(index_gb(2_000_000, 256, 1), 0.512)
