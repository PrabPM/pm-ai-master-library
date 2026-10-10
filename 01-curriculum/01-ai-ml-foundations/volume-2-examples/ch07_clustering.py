"""Chapter 7: k-means by hand, then DBSCAN, mixtures and an honesty check."""
import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture

# k-means by hand: six merchants' average ticket in USD, two clusters.
tickets = np.array([2.0, 3.0, 8.0, 10.0, 25.0, 27.0])
centers = np.array([2.0, 3.0])                 # a poor start: the first two points
history = []
for iteration in range(1, 6):
    assign = np.argmin(np.abs(tickets[:, None] - centers[None, :]), axis=1)
    new = np.array([tickets[assign == k].mean() for k in range(2)])
    wcss = ((tickets - new[assign]) ** 2).sum()
    history.append(new)
    print(f"iteration {iteration}: centers {np.round(new, 2).tolist()}  "
          f"WCSS {wcss:.1f}")
    if np.allclose(new, centers):
        break
    centers = new
assert np.allclose(history[0], [2.0, 14.6])
assert np.allclose(history[1], [13 / 3, 62 / 3])
km = KMeans(n_clusters=2, init=np.array([[2.0], [3.0]]), n_init=1).fit(tickets[:, None])
assert np.allclose(np.sort(km.cluster_centers_.ravel()), [5.75, 26.0])

# A merchant map: a broad crowd, a tight ring of 25 colluding merchants, 10 strays.
rng = np.random.default_rng(7)
crowd = rng.normal([0.0, 0.0], [1.6, 0.9], (300, 2))
ring = rng.normal([3.2, 2.6], 0.12, (25, 2))
strays = rng.uniform(-5, 5, (10, 2))
X = np.vstack([crowd, ring, strays])
is_ring = np.r_[np.zeros(300), np.ones(25), np.zeros(10)].astype(bool)

for k in (2, 3):
    k_labels = KMeans(n_clusters=k, n_init=10, random_state=0).fit_predict(X)
    home = np.bincount(k_labels[is_ring]).argmax()
    print(f"k-means, k = {k}: the ring's cluster holds {np.sum(k_labels == home)}")

d_labels = DBSCAN(eps=0.6, min_samples=8).fit_predict(X)
home = np.bincount(d_labels[is_ring] + 1).argmax() - 1
print(f"DBSCAN: {d_labels.max() + 1} clusters, {np.sum(d_labels == -1)} noise points, "
      f"the ring's cluster holds {np.sum(d_labels == home)}")

gmm = GaussianMixture(n_components=3, n_init=5, random_state=0).fit(X)
home = np.argmin(np.linalg.norm(gmm.means_ - [3.2, 2.6], axis=1))
resp = gmm.predict_proba([[2.9, 2.3]])[0, home]
print(f"mixture: ring weight {gmm.weights_[home]:.3f}, a merchant at (2.9, 2.3) "
      f"is in the ring with p = {resp:.2f}")

# Honesty check: k-means on data with no clusters at all.
blank = rng.uniform(0, 1, (300, 2))
scores = [silhouette_score(blank, KMeans(n_clusters=k, n_init=10, random_state=0)
                           .fit_predict(blank)) for k in (2, 3, 4)]
print("no structure at all: silhouette for k = 2, 3, 4:", np.round(scores, 2).tolist())
