"""Chapter 13: how sure can you be of an eval pass rate, and how many cases
do you need to tell 92% from 95%?"""
import math
from statistics import NormalDist

Z95 = NormalDist().inv_cdf(0.975)      # 1.96, for a 95% interval
Z80 = NormalDist().inv_cdf(0.80)       # 0.84, for 80% power


# [listing]
def wilson_interval(passed, n, z=Z95):
    """95% confidence interval for a pass rate measured on n cases."""
    p = passed / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return centre - half, centre + half


def cases_per_version(p1, p2):
    """Cases needed for EACH version, tested on different cases, to detect
    p1 versus p2 at 5% significance with 80% power."""
    mean = (p1 + p2) / 2
    a = Z95 * math.sqrt(2 * mean * (1 - mean))
    b = Z80 * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil((a + b) ** 2 / (p1 - p2) ** 2)
# [end listing]


def cases_paired(p1, p2, disagree):
    """Cases needed when BOTH versions answer the same cases. `disagree` is
    the share of cases where exactly one of the two versions passes."""
    d = abs(p1 - p2)
    a = Z95 * math.sqrt(disagree)
    b = Z80 * math.sqrt(disagree - d * d)
    return math.ceil((a + b) ** 2 / (d * d))


def zero_failures_rules_out(n):
    """If n test cases all pass, failure rates above this are unlikely (95%)."""
    return 1 - 0.05 ** (1 / n)


def main():
    for label, passed, n in (("Current version", 221, 240),
                             ("Candidate version", 228, 240)):
        low, high = wilson_interval(passed, n)
        print(f"{label:<18}{passed}/{n} = {passed / n:.1%}   "
              f"95% interval {low:.1%} to {high:.1%}")
    print()
    print("Cases needed to tell 92% from 95%")
    print(f"  different cases for each version: {cases_per_version(0.92, 0.95):,} each")
    for disagree in (0.09, 0.05):
        print(f"  same cases, versions disagree on {disagree:.0%}: "
              f"{cases_paired(0.92, 0.95, disagree):,}")
    print()
    print("Zero failures does not mean zero risk")
    for n in (20, 300):
        print(f"  0 failures in {n:>3} attacks only rules out failure rates above "
              f"{zero_failures_rules_out(n):.1%}")


if __name__ == "__main__":
    main()
