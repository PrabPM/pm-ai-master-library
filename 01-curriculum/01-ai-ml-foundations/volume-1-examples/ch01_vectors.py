"""Chapter 1. Vectors: two PayFlow merchants as lists of numbers and as arrows.

Each vector is (in-store payments, online payments) per day, in tens.
"""
import numpy as np

corner = np.array([8.0, 6.0])     # Corner Hardware
juniper = np.array([12.0, 5.0])   # Juniper Bakery

combined = corner + juniper       # add matching components
holiday = 1.5 * corner            # scale every component
dot = corner @ juniper            # multiply matching components, then add
len_c = np.linalg.norm(corner)    # length, also called the Euclidean norm
len_j = np.linalg.norm(juniper)
cos = dot / (len_c * len_j)
angle = np.degrees(np.arccos(cos))

print("corner + juniper =", combined)
print("1.5 * corner     =", holiday, "with length", np.linalg.norm(holiday))
print("dot product      =", dot)
print("lengths          =", len_c, "and", len_j)
print(f"cosine           = {cos:.4f}")
print(f"angle            = {angle:.2f} degrees")

# Checks against the hand calculation in the chapter.
assert np.allclose(combined, [20, 11])
assert np.allclose(holiday, [12, 9]) and np.isclose(np.linalg.norm(holiday), 15)
assert np.isclose(dot, 126)
assert np.isclose(len_c, 10) and np.isclose(len_j, 13)
assert np.isclose(cos, 126 / 130)
assert np.isclose(round(angle, 2), 14.25)
# The law of cosines gives the same dot product.
gap = np.linalg.norm(corner - juniper)
assert np.isclose(gap**2, len_c**2 + len_j**2 - 2 * dot)

# Answers to Check yourself.
harbor, northwind = np.array([6.0, 8.0]), np.array([4.0, 8.0])
assert np.isclose(harbor @ northwind, 88)                      # Q1.1
assert np.isclose(np.linalg.norm(harbor), 10)
assert np.isclose(np.linalg.norm(northwind), np.sqrt(80))
assert np.isclose(np.array([1.0, 0.0]) @ np.array([0.0, 1.0]), 0)  # Q1.2
