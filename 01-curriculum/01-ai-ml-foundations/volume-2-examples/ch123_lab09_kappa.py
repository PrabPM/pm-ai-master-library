"""Lab 9 (chapter 77): Cohen's kappa for two annotators."""
import numpy as np


def cohens_kappa(both_yes, both_no, a_only, b_only):
    n = both_yes + both_no + a_only + b_only
    observed = (both_yes + both_no) / n
    a_yes, b_yes = (both_yes + a_only) / n, (both_yes + b_only) / n
    by_chance = a_yes * b_yes + (1 - a_yes) * (1 - b_yes)
    return observed, by_chance, (observed - by_chance) / (1 - by_chance)


if __name__ == "__main__":
    observed, by_chance, kappa = cohens_kappa(70, 90, 25, 15)
    print(f"observed agreement {observed:.3f}")
    print(f"agreement expected by chance {by_chance:.4f}")
    print(f"kappa {kappa:.3f}")
    cost = 20_000 * 0.08 * 2
    print(f"double-labeling 20,000 tickets at USD 0.08 each: USD {cost:,.0f}")

    assert np.isclose(observed, 0.80) and np.isclose(by_chance, 0.50375)
    assert np.isclose(kappa, 0.597, atol=1e-3)
