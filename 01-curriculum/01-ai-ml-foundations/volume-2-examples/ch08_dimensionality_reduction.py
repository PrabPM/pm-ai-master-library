"""Chapter 8: PCA by hand, then what a t-SNE picture keeps and what it distorts."""
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, trustworthiness

# PCA by hand: five merchants, payments this week and last week, already centered.
X = np.array([[3.0, 3.0], [-3.0, -3.0], [1.0, -1.0], [-1.0, 1.0], [0.0, 0.0]])
C = X.T @ X / (len(X) - 1)
values, vectors = np.linalg.eigh(C)
order = np.argsort(values)[::-1]
values, vectors = values[order], vectors[:, order]
pc1 = vectors[:, 0] * np.sign(vectors[0, 0])
print("covariance", C.tolist(), " eigenvalues", np.round(values, 6).tolist())
print(f"first component {np.round(pc1, 3).tolist()} keeps "
      f"{values[0] / values.sum():.0%} of the variance")
print("scores on it:", np.round(X @ pc1, 3).tolist())
pca = PCA(n_components=1).fit(X)
assert np.allclose(C, [[5, 4], [4, 5]]) and np.allclose(values, [9, 1])
assert np.isclose(pca.explained_variance_ratio_[0], 0.9)
assert np.allclose(np.abs(pca.components_[0]), np.abs(pc1))

# Three merchant segments in ten dimensions: A and B are close, C is far away,
# and C is four times as spread out as the others.
rng = np.random.default_rng(8)
centers = np.zeros((3, 10))
centers[1, 0], centers[2, 1] = 6.0, 60.0
spread = np.array([1.0, 1.0, 4.0])
seg = np.repeat([0, 1, 2], 50)
H = centers[seg] + rng.normal(size=(150, 10)) * spread[seg, None]


def report(name, Z):
    mid = np.array([Z[seg == k].mean(axis=0) for k in range(3)])
    size = [np.linalg.norm(Z[seg == k] - mid[k], axis=1).mean() for k in range(3)]
    far = np.linalg.norm(mid[0] - mid[2]) / np.linalg.norm(mid[0] - mid[1])
    print(f"{name:<20} gap ratio {far:4.1f}   size ratio {size[2] / size[0]:3.1f}   "
          f"trustworthiness {trustworthiness(H, Z):.2f}")


report("original 10-D", H)
report("PCA to 2-D", PCA(n_components=2).fit_transform(H))
for perplexity in (5, 30):
    Z = TSNE(perplexity=perplexity, max_iter=500, random_state=0).fit_transform(H)
    report(f"t-SNE, perplexity {perplexity}", Z)
