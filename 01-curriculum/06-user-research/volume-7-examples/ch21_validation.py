"""Chapter 21: reading three validation tests against rules set in advance."""
import math
from statistics import NormalDist

Z = NormalDist().inv_cdf(0.975)


def wilson(successes, n, z=Z):
    p = successes / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - half, centre + half


def show(label, successes, n):
    low, high = wilson(successes, n)
    print(f"{label:<34}{successes:>4} of {n:<5}{successes / n:>5.0%}"
          f"   ({low:.0%} to {high:.0%})")


print("1. Fake door: 'Book a free setup call' on the documents step")
show("   clicked the button", 140, 1000)
print("   rule set in advance: go on if the low end is 10% or more\n")

print("2. Wizard of Oz: a person writes the rejection reason")
show("   fixed it, generic message", 14, 50)
show("   fixed it, specific message", 34, 50)
a, b = 14 / 50, 34 / 50
half = Z * math.sqrt(a * (1 - a) / 50 + b * (1 - b) / 50)
print(f"   difference: {(b - a) * 100:.0f} points, 95% interval "
      f"{(b - a - half) * 100:.0f} to {(b - a + half) * 100:.0f}\n")

print("3. Beta: guided onboarding, 300 volunteers")
show("   approved within 7 days", 201, 300)
print("   today's rate for everyone: 58%")
