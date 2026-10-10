"""Chapter 5. Did unaided awareness really move between two tracker waves?"""
from math import ceil, sqrt
from statistics import NormalDist

Z = NormalDist().inv_cdf(0.975)   # 1.96 for a 95% interval

# "Which payment companies can you name?" asked of food-and-drink owners.
# Columns: wave, respondents who named PayFlow unprompted, respondents.
JANUARY = ("January 2026", 36, 400)
JULY = ("July 2026", 48, 400)


def difference_interval(k1, n1, k2, n2):
    p1, p2 = k1 / n1, k2 / n2
    se = sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = p2 - p1
    return diff, diff - Z * se, diff + Z * se


def respondents_needed(p1, p2):
    """Respondents per wave for the interval around p2 - p1 to exclude zero."""
    variance = p1 * (1 - p1) + p2 * (1 - p2)
    return ceil(Z * Z * variance / (p2 - p1) ** 2)


def main():
    for wave, k, n in (JANUARY, JULY):
        print(f"{wave:<14}{k:>4} of {n} named PayFlow = {k / n:.1%}")
    diff, low, high = difference_interval(*JANUARY[1:], *JULY[1:])
    print(f"Change: {diff * 100:+.1f} points, 95% interval "
          f"{low * 100:+.1f} to {high * 100:+.1f} points")
    need = respondents_needed(JANUARY[1] / JANUARY[2], JULY[1] / JULY[2])
    print(f"Respondents per wave for a 3-point change to clear zero: {need}")


if __name__ == "__main__":
    main()
