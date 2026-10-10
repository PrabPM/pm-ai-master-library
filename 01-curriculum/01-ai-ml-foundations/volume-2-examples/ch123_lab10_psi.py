"""Lab 10 (chapter 85): population stability index for one feature."""
import numpy as np

EXPECTED = np.array([0.30, 0.30, 0.20, 0.15, 0.05])   # training: amount buckets
ACTUAL = np.array([0.20, 0.25, 0.22, 0.20, 0.13])     # this week


def psi(expected, actual):
    terms = (actual - expected) * np.log(actual / expected)
    return terms, terms.sum()


if __name__ == "__main__":
    terms, total = psi(EXPECTED, ACTUAL)
    labels = ["under 20", "20 to 50", "50 to 100", "100 to 500", "over 500"]
    for label, e, a, term in zip(labels, EXPECTED, ACTUAL, terms):
        print(f"USD {label:<10} trained {e:.2f}  now {a:.2f}  contributes {term:.4f}")
    print(f"PSI = {total:.4f}")

    assert np.isclose(total, 0.1424, atol=1e-4)
    assert np.argmax(terms) == 4 and np.isclose(terms[4], 0.0764, atol=1e-4)
