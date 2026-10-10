"""Chapter 11: margin of error and sample size for a survey proportion.

PayFlow invited a random 1,200 of the 3,360 merchants who started onboarding in
the last four weeks and did not finish. 216 answered.
"""
import math
from statistics import NormalDist

Z = NormalDist().inv_cdf(0.975)   # 1.96 for 95% confidence
POPULATION = 3360
ANSWERS = {
    "Did not have a document or number to hand": 78,
    "Did not understand a question": 41,
    "Lost my progress and had to start again": 32,
    "A document was rejected": 27,
    "Not comfortable sharing the information": 19,
    "It was taking too long": 11,
    "Something else": 8,
}


def margin(p, n, population=None):
    """Half-width of the 95% interval for a share from a random sample."""
    se = math.sqrt(p * (1 - p) / n)
    if population:                       # finite population correction
        se *= math.sqrt((population - n) / (population - 1))
    return Z * se


def sample_size(moe, p=0.5, population=None):
    """Completed answers needed for a margin of error of moe."""
    n0 = Z * Z * p * (1 - p) / (moe * moe)
    if population:
        n0 = n0 / (1 + (n0 - 1) / population)
    return math.ceil(n0)


def main():
    n = sum(ANSWERS.values())
    print(f"invited 1,200, answered {n}, response rate {n / 1200:.0%}\n")
    for reason, count in ANSWERS.items():
        p = count / n
        m = margin(p, n, POPULATION)
        print(f"{reason:<42}{count:>4}{p:>7.1%}  +/- {m * 100:.1f} points")

    print("\nanswers needed for a given margin (95%, worst case of 50%)")
    print("margin    huge population    population of 3,360")
    for moe in (0.10, 0.05, 0.03):
        big, small = sample_size(moe), sample_size(moe, 0.5, POPULATION)
        print(f"+/- {moe:<4.0%}{big:>17,}{small:>23,}")


if __name__ == "__main__":
    main()
