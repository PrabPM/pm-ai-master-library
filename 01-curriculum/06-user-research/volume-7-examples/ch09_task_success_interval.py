"""Chapter 9: what "3 of 5 succeeded" can and cannot tell you.

Adjusted Wald interval (Agresti and Coull, 1998): add z*z/2 successes and
z*z/2 failures, then use the usual formula. It behaves well for tiny samples.
"""
from statistics import NormalDist

Z = NormalDist().inv_cdf(0.975)  # 1.96 for a 95% interval


def adjusted_wald(successes, n, z=Z):
    n_adj = n + z * z
    p_adj = (successes + z * z / 2) / n_adj
    half = z * (p_adj * (1 - p_adj) / n_adj) ** 0.5
    return max(0.0, p_adj - half), min(1.0, p_adj + half)


if __name__ == "__main__":
    print("observed        95% interval for the true success rate")
    for successes, n in ((5, 5), (4, 5), (3, 5), (2, 5), (12, 20), (60, 100)):
        low, high = adjusted_wald(successes, n)
        print(f"{successes:>3} of {n:<3}      {low:>4.0%} to {high:.0%}")
