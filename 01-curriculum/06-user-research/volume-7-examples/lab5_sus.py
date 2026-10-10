"""Lab 5: System Usability Scale scores for the five PayFlow Assist sessions."""
from statistics import mean

from ch09_sus import sus_score

ANSWERS = {
    "P1": [4, 2, 4, 2, 4, 2, 4, 2, 4, 2],
    "P2": [5, 1, 5, 1, 4, 2, 5, 1, 5, 2],
    "P3": [3, 2, 4, 2, 3, 3, 4, 2, 3, 2],
    "P4": [4, 2, 4, 1, 4, 2, 4, 2, 4, 3],
    "P5": [4, 1, 5, 2, 4, 2, 5, 2, 4, 2],
}
scores = {who: sus_score(a) for who, a in ANSWERS.items()}
print("  ".join(f"{who} {score:.1f}" for who, score in scores.items()))
print(f"mean {mean(scores.values()):.1f}")
