"""Chapter 9: scoring the System Usability Scale (Brooke, 1986).

Ten statements, each answered 1 (strongly disagree) to 5 (strongly agree).
Odd-numbered statements are positive, even-numbered ones are negative.
"""
from statistics import mean, stdev

from scipy import stats

# One row per participant in the round-2 test: answers to statements 1..10.
RESPONSES = {
    "P1": [4, 2, 4, 1, 4, 2, 5, 2, 4, 3],
    "P2": [3, 3, 3, 2, 3, 3, 4, 3, 3, 3],
    "P3": [5, 1, 4, 1, 4, 2, 5, 1, 4, 2],
    "P4": [2, 4, 3, 3, 3, 3, 3, 4, 2, 3],
    "P5": [4, 2, 4, 2, 3, 2, 4, 2, 4, 3],
}


def sus_score(answers):
    assert len(answers) == 10 and all(1 <= a <= 5 for a in answers)
    odd = sum(a - 1 for a in answers[0::2])    # statements 1, 3, 5, 7, 9
    even = sum(5 - a for a in answers[1::2])   # statements 2, 4, 6, 8, 10
    return (odd + even) * 2.5                  # 0 to 100, not a percentage


if __name__ == "__main__":
    scores = {who: sus_score(a) for who, a in RESPONSES.items()}
    for who, score in scores.items():
        print(f"{who}: {score:5.1f}")

    n = len(scores)
    m, sd = mean(scores.values()), stdev(scores.values())
    half = stats.t.ppf(0.975, n - 1) * sd / n ** 0.5
    print(f"mean {m:.1f}, standard deviation {sd:.1f}, n = {n}")
    print(f"95% interval for the mean: {m - half:.0f} to {m + half:.0f}")
