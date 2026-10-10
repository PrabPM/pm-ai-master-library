"""Chapter 15: do two people apply the same codes? Cohen's kappa (Cohen, 1960).

You and Rosa each coded the same 60 open-text survey answers on your own.
MATRIX[i][j] = answers you gave code i and Rosa gave code j.
"""
CODES = ["Missing document", "Confusing question", "Lost progress", "Other"]
MATRIX = [
    [20, 2, 1, 1],
    [3, 12, 1, 1],
    [1, 1, 9, 0],
    [1, 2, 0, 5],
]

total = sum(map(sum, MATRIX))
agree = sum(MATRIX[i][i] for i in range(len(CODES)))
yours = [sum(row) for row in MATRIX]
rosas = [sum(row[j] for row in MATRIX) for j in range(len(CODES))]

observed = agree / total
by_chance = sum(y * r for y, r in zip(yours, rosas)) / total ** 2
kappa = (observed - by_chance) / (1 - by_chance)

print(f"answers coded by both: {total}")
print(f"same code chosen: {agree} ({observed:.0%})")
print(f"agreement expected by chance: {by_chance:.0%}")
print(f"kappa = {kappa:.2f}")
print("\nwhere you disagreed (your code -> Rosa's code)")
for i, row in enumerate(MATRIX):
    for j, count in enumerate(row):
        if i != j and count >= 2:
            print(f"  {CODES[i]} -> {CODES[j]}: {count}")
