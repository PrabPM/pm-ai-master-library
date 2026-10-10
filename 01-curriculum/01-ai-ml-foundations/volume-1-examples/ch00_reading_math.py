"""Front matter. The two small calculations in "Meet PayFlow" and
"How to read the math"."""
import numpy as np

y = np.array([10.0, 20.0, 30.0])        # actual amounts
y_hat = np.array([12.0, 18.0, 33.0])    # predicted amounts
mse = np.mean((y - y_hat) ** 2)         # (1/n) * sum of squared misses
print(round(mse, 2))

# Checks against the hand calculations in the text.
assert np.isclose(mse, 17 / 3)
assert np.isclose(np.sum((y - y_hat) ** 2), 17)
fee = 0.029 * 120.00 + 0.30             # PayFlow's fee on a USD 120.00 payment
assert np.isclose(fee, 3.78) and np.isclose(120.00 - fee, 116.22)
