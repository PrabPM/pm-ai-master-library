"""Lab 4 (chapters 26, 28 and 100): recall at k and mean reciprocal rank."""
import numpy as np

# Rank of the first relevant passage for five questions (None = not in the top 10).
RANKS = {"dense only": [1, 3, 7, 2, None], "hybrid": [1, 2, 4, 2, 6]}


def recall_at(ranks, k):
    return np.mean([r is not None and r <= k for r in ranks])


def mrr(ranks):
    return np.mean([0 if r is None else 1 / r for r in ranks])


if __name__ == "__main__":
    for name, ranks in RANKS.items():
        print(f"{name:<10} recall@3 {recall_at(ranks, 3):.2f}  "
              f"recall@5 {recall_at(ranks, 5):.2f}  MRR {mrr(ranks):.4f}")

    assert np.isclose(recall_at(RANKS["dense only"], 5), 0.6)
    assert np.isclose(recall_at(RANKS["hybrid"], 5), 0.8)
    assert np.isclose(mrr(RANKS["dense only"]), (1 + 1 / 3 + 1 / 7 + 1 / 2) / 5)
    assert np.isclose(mrr(RANKS["hybrid"]), 0.4833, atol=1e-4)
