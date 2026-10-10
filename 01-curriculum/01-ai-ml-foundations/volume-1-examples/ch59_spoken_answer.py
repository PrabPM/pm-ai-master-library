"""Chapter 59: the numbers used in the spoken answer on gradient descent."""
import numpy as np


def descend(eta, steps, w=0.0):
    """Gradient descent on L(w) = (w - 3)^2, whose gradient is 2 * (w - 3)."""
    path = [w]
    for _ in range(steps):
        w = w - eta * 2 * (w - 3)
        path.append(w)
    return np.array(path)


print("learning rate 0.1:", np.round(descend(0.1, 4), 4))
print("learning rate 1.1:", np.round(descend(1.1, 4), 4))
gap = np.abs(descend(0.1, 4) - 3)
print("share of the gap closed per step at 0.1:", np.round(1 - gap[1:] / gap[:-1], 2))

# ---- checks against the numbers spoken aloud ----
small, big = descend(0.1, 4), descend(1.1, 4)
assert np.isclose(2 * (0 - 3), -6) and np.isclose(small[1], 0.6)
assert np.isclose(2 * (0.6 - 3), -4.8) and np.isclose(small[2], 1.08)
assert np.allclose(1 - gap[1:] / gap[:-1], 0.2)
assert np.isclose(big[1], 6.6) and abs(big[1] - 3) > abs(big[0] - 3)
assert np.all(np.diff(np.abs(big - 3)) > 0)          # further away every step
assert np.isclose(abs(1 - 2 * 1.1), 1.2)             # error multiplies by -1.2
# A 150-words-a-minute speaker takes about two and a half minutes for 400 words.
assert np.isclose(400 / 150, 2.67, atol=0.01)
