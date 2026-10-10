"""Chapter 58, Case 3: sizing a vector index and choosing a similarity measure."""
import numpy as np

# ---- 1. Memory arithmetic for the real system ----
tickets, dims = 4_000_000, 768
GB = 1e9


def gigabytes(n, d, bytes_per_number=4):
    return n * d * bytes_per_number / GB


print(f"raw float32, 768 dims: {gigabytes(tickets, dims):.2f} GB")
print(f"float16, 768 dims:     {gigabytes(tickets, dims, 2):.2f} GB")
print(f"float32, 256 dims:     {gigabytes(tickets, 256):.2f} GB")
print(f"graph index, M = 32 at 8 * M bytes per ticket: "
      f"{tickets * 8 * 32 / GB:.2f} GB")

# ---- 2. A scaled-down experiment: 20,000 tickets, 64 dims ----
rng = np.random.default_rng(583)
n, d, latent = 20_000, 64, 12
mix = rng.normal(0, 1, (latent, d))
topics = rng.normal(0, 1, (n + 200, latent)) * np.linspace(3, 0.5, latent)
vecs = topics @ mix + 0.3 * rng.normal(0, 1, (n + 200, d))
vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
vecs *= rng.lognormal(0, 0.2, (n + 200, 1))        # lengths vary by about 20%
corpus, queries = vecs[:n], vecs[n:]


def top10(scores):
    return np.argsort(-scores, axis=1)[:, :10]


def overlap(a, b):
    """Share of each query's ten neighbors that two rankings have in common."""
    return np.array([len(set(x) & set(y)) / 10 for x, y in zip(a, b)])


def unit(v):
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def neg_dist(q, c):
    """Minus the squared Euclidean distance, so that larger is closer."""
    return -((q ** 2).sum(1)[:, None] - 2 * q @ c.T + (c ** 2).sum(1)[None, :])


by_dot = top10(queries @ corpus.T)
by_cos = top10(unit(queries) @ unit(corpus).T)
norms = np.linalg.norm(corpus, axis=1)
print(f"\nraw vectors: dot and cosine top-10 agree on "
      f"{100 * overlap(by_dot, by_cos).mean():.0f}% of neighbors")
print(f"mean length of a dot-product neighbor: {norms[by_dot].mean():.2f}  "
      f"(corpus average {norms.mean():.2f})")
by_euc_unit = top10(neg_dist(unit(queries), unit(corpus)))
print(f"unit vectors: Euclidean and cosine top-10 agree on "
      f"{100 * overlap(by_euc_unit, by_cos).mean():.0f}%")

# ---- 3. Fewer dimensions: variance kept and recall@10, with its uncertainty ----
center = unit(corpus).mean(axis=0)
_, sing, vt = np.linalg.svd(unit(corpus) - center, full_matrices=False)
kept = np.cumsum(sing ** 2) / np.sum(sing ** 2)
print("\ndims  variance kept  recall@10  95% interval")
for k in (8, 12, 16, 32):
    c_k = (unit(corpus) - center) @ vt[:k].T
    q_k = (unit(queries) - center) @ vt[:k].T
    r = overlap(top10(neg_dist(q_k, c_k)), by_cos)
    half = 1.96 * r.std(ddof=1) / np.sqrt(len(r))
    print(f"{k:4d}  {kept[k - 1]:13.3f}  {r.mean():9.3f}  "
          f"{r.mean() - half:.3f} to {r.mean() + half:.3f}")

# ---- checks ----
assert np.isclose(gigabytes(tickets, dims), 12.288)
assert np.isclose(gigabytes(tickets, 256), 4.096)
assert np.isclose(tickets * 8 * 32 / GB, 1.024)
assert overlap(by_euc_unit, by_cos).mean() == 1.0     # same ranking on unit vectors
assert overlap(by_dot, by_cos).mean() < 0.8
assert norms[by_dot].mean() > 1.2 * norms.mean()
