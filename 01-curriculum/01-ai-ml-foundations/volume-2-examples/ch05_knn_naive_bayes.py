"""Chapter 5: nearest neighbors and naive Bayes, by hand and with scikit-learn."""
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

from ch00_payflow_data import TICKETS, fresh_review_sample, review_sample

# Nearest neighbors by hand: (refund rate %, tickets per month) -> churned?
M = np.array([[1.0, 1.0], [2.0, 1.0], [4.0, 3.0], [5.0, 4.0], [3.0, 3.0]])
churned = np.array([0, 0, 1, 1, 1])
query = np.array([3.0, 2.0])
dist = np.sqrt(((M - query) ** 2).sum(axis=1))
nearest = np.argsort(dist, kind="stable")[:3]
print("distances", np.round(dist, 3), " nearest three:", "ABCDE"[nearest[0]],
      "ABCDE"[nearest[1]], "ABCDE"[nearest[2]])
print(f"churn score {churned[nearest].mean():.2f}")
knn = KNeighborsClassifier(n_neighbors=3).fit(M, churned)
assert np.isclose(knn.predict_proba([query])[0, 1], 2 / 3)
assert np.isclose(churned[nearest].mean(), 2 / 3)

# The effect of k on the review sample.
R, labels = review_sample()
T, t_labels = fresh_review_sample()
for k in (1, 15, 151):
    model = KNeighborsClassifier(n_neighbors=k).fit(R, labels)
    print(f"k = {k:>3}: accuracy on the 300 it memorized {model.score(R, labels):.3f}, "
          f"on fresh payments {model.score(T, t_labels):.3f}")

# Naive Bayes by hand: four tickets, five distinct words, add-one smoothing.
counts = {"payouts": {"payout": 2, "late": 1, "missing": 1},
          "disputes": {"chargeback": 1, "dispute": 2, "late": 1}}
vocab, prior = 5, 0.5
score = {}
for queue, words in counts.items():
    total = sum(words.values())
    like = [(words.get(word, 0) + 1) / (total + vocab) for word in ("late", "payout")]
    score[queue] = prior * like[0] * like[1]
posterior = score["payouts"] / sum(score.values())
print(f"scores {score['payouts']:.5f} vs {score['disputes']:.5f}   "
      f"P(payouts | 'late payout') = {posterior:.2f}")

vec = CountVectorizer()
nb = MultinomialNB(alpha=1.0).fit(vec.fit_transform([text for text, _ in TICKETS]),
                                  [queue for _, queue in TICKETS])
sk = nb.predict_proba(vec.transform(["late payout"]))[0]
print("scikit-learn:", dict(zip(nb.classes_.tolist(), np.round(sk, 2).tolist())))
assert np.isclose(posterior, 0.75)
assert np.isclose(sk[list(nb.classes_).index("payouts")], 0.75)
