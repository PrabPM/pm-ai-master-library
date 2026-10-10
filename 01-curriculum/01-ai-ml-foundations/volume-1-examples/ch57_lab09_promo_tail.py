"""Chapter 57, Lab 9: how long does a promotion's bump last?"""
import numpy as np

extra = np.array([200.0, 80.0, 30.0, 12.0, 5.0])   # thousand payments over baseline

# AR(1) through the origin: tomorrow's extra = phi * today's extra.
phi = np.sum(extra[:-1] * extra[1:]) / np.sum(extra[:-1] ** 2)
half_life = np.log(0.5) / np.log(phi)
tail = extra[-1] * phi / (1 - phi)                   # days 6, 7, ... summed
total = extra.sum() + tail
print(f"phi {phi:.4f}   half-life {half_life:.2f} days")
print(f"day 6 forecast {extra[-1] * phi:.2f} thousand; unseen tail {tail:.2f}")
print(f"total extra payments {total:.1f} thousand, "
      f"of which day 1 was {100 * extra[0] / total:.0f}%")
print(f"fee revenue at USD 1.75 each: USD {total * 1000 * 1.75:,.0f}")

# ---- checks against the hand results ----
assert np.isclose(phi, 18820 / 47444)
assert np.isclose(half_life, 0.75, atol=0.005)
assert np.isclose(tail, 3.29, atol=0.005)
assert np.isclose(total, 330.29, atol=0.01)
assert np.isclose(extra.sum() / total, 0.99, atol=0.001)
