"""Chapter 4: the widest street by hand, then kernels."""
import numpy as np
from sklearn.svm import SVC

from ch00_payflow_data import fresh_review_sample, review_sample

# Four payments worked by hand: (velocity, amount in USD hundreds), -1 legit, +1 fraud.
X = np.array([[1.0, 1.0], [0.0, 1.0], [3.0, 3.0], [4.0, 3.0]])
y = np.array([-1, -1, 1, 1])
svm = SVC(kernel="linear", C=1e6).fit(X, y)    # a huge C means "no violations"
w, b = svm.coef_[0], svm.intercept_[0]
print(f"w = {np.round(w, 3)}  b = {b:.3f}  street width = {2 / np.linalg.norm(w):.3f}")
print("support vectors:", svm.support_vectors_.tolist())


def phi(x):                                    # the kernel idea in one dimension
    return np.array([1.0, np.sqrt(2) * x, x ** 2])


x, z = 3.0, -1.0
print(f"kernel (1 + xz)^2 = {(1 + x * z) ** 2:.1f}   "
      f"phi(x) . phi(z) = {phi(x) @ phi(z):.1f}")
assert np.allclose(w, [0.5, 0.5], atol=1e-3) and np.isclose(b, -2.0, atol=1e-3)
assert np.isclose(2 / np.linalg.norm(w), 2 * np.sqrt(2), atol=1e-3)
assert np.isclose((1 + x * z) ** 2, phi(x) @ phi(z))

# The review sample: a curved fraud region that a straight street cannot follow.
R, labels = review_sample()
T, t_labels = fresh_review_sample()
mean, std = R.mean(axis=0), R.std(axis=0)      # SVMs need features on one scale
for name, model in [("linear", SVC(kernel="linear", C=1.0)),
                    ("RBF", SVC(kernel="rbf", C=1.0, gamma=1.0))]:
    model.fit((R - mean) / std, labels)
    acc = model.score((T - mean) / std, t_labels)
    print(f"{name:<6} kernel: accuracy on fresh payments {acc:.3f}, "
          f"{len(model.support_)} support vectors of {len(R)}")
