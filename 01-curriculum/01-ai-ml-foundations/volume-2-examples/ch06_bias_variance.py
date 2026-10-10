"""Chapter 6: underfit, overfit, and what L1 and L2 penalties do to coefficients."""
import numpy as np
from numpy.polynomial import Polynomial
from scipy.optimize import minimize_scalar
from sklearn.linear_model import Lasso, LinearRegression, Ridge

# Shrinkage by hand, on the four payouts of Chapter 1 after centering.
xc = np.array([-1.5, -0.5, 0.5, 1.5])
yc = np.array([-2.5, -0.5, 0.5, 2.5])
sxx, sxy = xc @ xc, xc @ yc
print(f"Sxx {sxx:.0f}  Sxy {sxy:.0f}  plain slope {sxy / sxx:.2f}")
for lam in (5.0, 16.0):
    ridge = sxy / (sxx + lam)
    lasso = max(sxy - lam / 2, 0.0) / sxx
    r_num = minimize_scalar(lambda w: ((yc - w * xc) ** 2).sum() + lam * w ** 2).x
    l_num = minimize_scalar(lambda w: ((yc - w * xc) ** 2).sum() + lam * abs(w),
                            bounds=(-5, 5), method="bounded").x
    print(f"lambda {lam:>4}: ridge slope {ridge:.3f}   lasso slope {lasso:.3f}")
    assert np.isclose(ridge, r_num, atol=1e-4) and np.isclose(lasso, l_num, atol=1e-4)

# Train and validation error as a model gets more flexible.
rng = np.random.default_rng(6)


def approval_rate(hour):                       # the truth the models try to recover
    return 90 - 6 * np.exp(-((hour - 3) / 2.5) ** 2) + 2 * np.sin(hour / 4)


h_train, h_val = rng.uniform(0, 24, 30), rng.uniform(0, 24, 300)
y_train = approval_rate(h_train) + rng.normal(0, 1.0, 30)
y_val = approval_rate(h_val) + rng.normal(0, 1.0, 300)
for degree in (1, 8, 16):
    fit = Polynomial.fit(h_train, y_train, degree)
    err_train = np.sqrt(np.mean((fit(h_train) - y_train) ** 2))
    err_val = np.sqrt(np.mean((fit(h_val) - y_val) ** 2))
    print(f"degree {degree:>2}: train RMSE {err_train:.2f}   "
          f"validation RMSE {err_val:.2f}")

X = rng.normal(size=(60, 8))               # only features 1 to 3 matter
y = 3.0 * X[:, 0] - 2.0 * X[:, 1] + 1.0 * X[:, 2] + rng.normal(0, 1.0, 60)
models = [("least squares", LinearRegression()), ("ridge (L2)", Ridge(alpha=20)),
          ("lasso (L1)", Lasso(alpha=0.3))]
for name, model in models:
    coef = model.fit(X, y).coef_
    print(f"{name:<13}", " ".join(f"{c + 0.0:5.2f}" for c in coef))
