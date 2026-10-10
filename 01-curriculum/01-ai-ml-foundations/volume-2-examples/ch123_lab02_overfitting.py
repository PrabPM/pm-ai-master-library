"""Lab 2 (chapter 6): see overfitting in training and validation error."""
import numpy as np


def make_data(rng, n=24):
    x = rng.uniform(0, 1, n)                       # monthly volume, scaled 0 to 1
    y = 20 + 60 * x + rng.normal(0, 8, n)          # support tickets per month
    return x, y


def rmse(coeffs, x, y):
    return float(np.sqrt(np.mean((np.polyval(coeffs, x) - y) ** 2)))


if __name__ == "__main__":
    rng = np.random.default_rng(17)
    x, y = make_data(rng)
    x_train, y_train, x_val, y_val = x[:16], y[:16], x[16:], y[16:]
    results = {}
    for degree in (1, 3, 9):
        coeffs = np.polyfit(x_train, y_train, degree)
        results[degree] = (rmse(coeffs, x_train, y_train), rmse(coeffs, x_val, y_val))
        print(f"degree {degree}: training RMSE {results[degree][0]:5.2f}   "
              f"validation RMSE {results[degree][1]:7.2f}")

    assert results[9][0] < results[3][0] < results[1][0]     # training always falls
    assert results[9][1] > results[1][1]                     # validation gets worse
