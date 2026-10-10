"""Chapter 4. A five-second test of three headlines, with honest error bars."""
from statistics import NormalDist

# Each headline was shown for five seconds to 80 food-and-drink owners.
# "Understood" = could then say what the product does and who it is for.
HEADLINES = [
    ("A  Accelerate your cash flow", 31, 80),
    ("B  Get paid in minutes, even on weekends", 58, 80),
    ("C  Your weekend sales, in your bank before Monday", 62, 80),
]


def wilson(k, n, confidence=0.95):
    """Wilson score interval for a share k/n. Safer than p +/- 2 SE at small n."""
    z = NormalDist().inv_cdf(0.5 + confidence / 2)
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / (1 + z * z / n)
    return centre - half, centre + half


def main():
    print(f"{'Headline':<52}{'Understood':>11}{'95% interval':>17}")
    for text, k, n in HEADLINES:
        low, high = wilson(k, n)
        print(f"{text:<52}{k / n:>11.1%}{low:>9.1%} to {high:.1%}")


if __name__ == "__main__":
    main()
