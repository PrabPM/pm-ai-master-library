"""Lab 1 (chapters 9 and 63): choose a fraud threshold by expected cost."""
import numpy as np

# threshold: (true positives, false positives, false negatives) per 10,000 payments
COUNTS = {0.30: (45, 400, 5), 0.50: (40, 150, 10), 0.70: (30, 40, 20)}


def summarize(tp, fp, fn, cost_fn, cost_fp):
    precision, recall = tp / (tp + fp), tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    return precision, recall, f1, fn * cost_fn + fp * cost_fp


if __name__ == "__main__":
    for cost_fp in (6, 20):
        print(f"missed fraud costs USD 120, false block costs USD {cost_fp}")
        for t, (tp, fp, fn) in COUNTS.items():
            p, r, f1, cost = summarize(tp, fp, fn, 120, cost_fp)
            print(f"  threshold {t:.2f}: precision {p:.3f} recall {r:.2f} "
                  f"F1 {f1:.3f} cost USD {cost:,}")

    costs6 = {t: summarize(*c, 120, 6)[3] for t, c in COUNTS.items()}
    costs20 = {t: summarize(*c, 120, 20)[3] for t, c in COUNTS.items()}
    assert costs6 == {0.30: 3000, 0.50: 2100, 0.70: 2640}
    assert min(costs6, key=costs6.get) == 0.50
    assert min(costs20, key=costs20.get) == 0.70
    assert np.isclose(summarize(*COUNTS[0.50], 120, 6)[0], 40 / 190)
