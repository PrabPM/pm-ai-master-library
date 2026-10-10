"""Lab 8 (chapter 68): expected calibration error from a binned table."""
import numpy as np

# (mean predicted fraud probability, observed fraud rate, payments) per score bin
BINS = [(0.05, 0.04, 6000), (0.20, 0.15, 2000), (0.40, 0.30, 1000),
        (0.65, 0.50, 700), (0.90, 0.70, 300)]


def expected_calibration_error(bins):
    total = sum(n for _, _, n in bins)
    return sum(n / total * abs(pred - obs) for pred, obs, n in bins)


if __name__ == "__main__":
    for pred, obs, n in BINS:
        print(f"says {pred:.2f}  happens {obs:.2f}  gap {abs(pred - obs):.2f}  n {n}")
    ece = expected_calibration_error(BINS)
    worst = max(abs(p - o) for p, o, _ in BINS)
    print(f"expected calibration error {ece:.4f}; largest gap {worst:.2f}")

    assert np.isclose(ece, 0.0425) and np.isclose(worst, 0.20)
