"""Chapter 12: do two reviewers mean the same thing by "acceptable answer"?"""


# [listing]
def cohen_kappa(both_yes, both_no, only_a_yes, only_b_yes):
    """Agreement between two reviewers, corrected for agreement by chance."""
    n = both_yes + both_no + only_a_yes + only_b_yes
    observed = (both_yes + both_no) / n
    a_yes = (both_yes + only_a_yes) / n
    b_yes = (both_yes + only_b_yes) / n
    by_chance = a_yes * b_yes + (1 - a_yes) * (1 - b_yes)
    return observed, by_chance, (observed - by_chance) / (1 - by_chance)
# [end listing]


ROUNDS = [  # Sam and the quality lead each judge the same 50 Assist answers
    ("Round 1, one-line rubric", 34, 9, 4, 3),
    ("Round 2, rubric with examples", 36, 10, 2, 2),
]


def main():
    print(f"{'Round':<32}{'Agree':>7}{'By chance':>11}{'Kappa':>7}")
    for name, *counts in ROUNDS:
        observed, by_chance, kappa = cohen_kappa(*counts)
        print(f"{name:<32}{observed:>7.0%}{by_chance:>11.0%}{kappa:>7.2f}")


if __name__ == "__main__":
    main()
