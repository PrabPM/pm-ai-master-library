"""Chapter 12: Net Promoter Score with its confidence interval.

Each answer is scored +1 (promoter, 9-10), 0 (passive, 7-8) or -1 (detractor,
0-6). NPS is the mean of those scores times 100, so its standard error is the
standard error of a mean.
"""
import math
from statistics import NormalDist

Z = NormalDist().inv_cdf(0.975)   # 1.96 for 95% confidence

# Answers to the 0-10 "would you recommend" question, this quarter.
COUNTS = {0: 4, 1: 2, 2: 3, 3: 5, 4: 6, 5: 11, 6: 14, 7: 22, 8: 32, 9: 38, 10: 43}


def nps(promoters, passives, detractors):
    """Return the score and the half-width of its 95% interval, in points."""
    n = promoters + passives + detractors
    p, d = promoters / n, detractors / n
    score = p - d
    se = math.sqrt((p + d - score * score) / n)
    return score * 100, Z * se * 100


if __name__ == "__main__":
    promoters = COUNTS[9] + COUNTS[10]
    passives = COUNTS[7] + COUNTS[8]
    detractors = sum(COUNTS[s] for s in range(0, 7))
    n = promoters + passives + detractors
    score, half = nps(promoters, passives, detractors)
    print(f"n = {n}: {promoters} promoters, {passives} passives, "
          f"{detractors} detractors")
    print(f"NPS = {score:+.0f}, 95% interval {score - half:+.0f} to "
          f"{score + half:+.0f}")

    print("\nthe same mix of answers at other sample sizes")
    for size in (50, 100, 180, 400, 1000, 2500):
        k = size / n
        _, h = nps(promoters * k, passives * k, detractors * k)
        print(f"n = {size:>5,}: NPS = {score:+.0f} +/- {h:>4.1f} points")
