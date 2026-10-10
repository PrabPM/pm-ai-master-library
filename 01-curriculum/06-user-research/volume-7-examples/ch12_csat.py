"""Chapter 12: CSAT as a top-two-box share, with a Wilson interval.

150 merchants rated the help they got from support on an onboarding ticket,
from 1 (very dissatisfied) to 5 (very satisfied).
"""
import math
from statistics import NormalDist

Z = NormalDist().inv_cdf(0.975)
RATINGS = {5: 61, 4: 44, 3: 20, 2: 13, 1: 12}


def wilson(successes, n, z=Z):
    """95% interval for a proportion (Wilson, 1927)."""
    p = successes / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - half, centre + half


n = sum(RATINGS.values())
satisfied = RATINGS[5] + RATINGS[4]
low, high = wilson(satisfied, n)
average = sum(score * count for score, count in RATINGS.items()) / n
print(f"n = {n}")
print(f"CSAT (rated 4 or 5): {satisfied / n:.0%}, 95% interval {low:.0%} to {high:.0%}")
print(f"average rating: {average:.2f} out of 5")
print(f"rated 1 or 2: {(RATINGS[1] + RATINGS[2]) / n:.0%} "
      f"({RATINGS[1] + RATINGS[2]} merchants to call back)")
