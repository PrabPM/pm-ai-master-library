"""Chapter 115: the Laplace mechanism for differential privacy, a membership
inference threshold attack, and redaction arithmetic.
"""
import numpy as np


def laplace_release(true_value, sensitivity, epsilon, rng, size=None):
    """Release true_value plus Laplace noise of scale sensitivity / epsilon."""
    return true_value + rng.laplace(0.0, sensitivity / epsilon, size=size)


def laplace_pdf(x, center, scale):
    return np.exp(-np.abs(x - center) / scale) / (2 * scale)


def error_bound(scale, coverage=0.95):
    """Half-width holding `coverage` of the noise: P(|Z| > t) = exp(-t / scale)."""
    return scale * np.log(1 / (1 - coverage))


def worst_ratio(scale, with_record=43, without_record=42):
    """Largest ratio between the release densities of two neighboring datasets."""
    x = np.linspace(20, 65, 4501)
    ratio = laplace_pdf(x, without_record, scale) / laplace_pdf(x, with_record, scale)
    return float(ratio.max())


if __name__ == "__main__":
    rng = np.random.default_rng(5)
    true_count, sensitivity, epsilon = 42, 1, 0.5
    b = sensitivity / epsilon
    print(f"noise scale b = {b:.1f}, standard deviation = {np.sqrt(2) * b:.2f}")
    five = laplace_release(true_count, sensitivity, epsilon, rng, 5)
    print("five releases:", np.round(five, 1))

    bound95 = error_bound(b)
    draws = laplace_release(true_count, 1, epsilon, rng, 200_000)
    inside = np.mean(np.abs(draws - true_count) <= bound95)
    print(f"95% of releases fall within +/- {bound95:.2f}; "
          f"simulated share {inside:.3f}")

    # The guarantee: with or without one merchant (count 42 or 43), no output
    # becomes more than e^epsilon times more likely.
    ratio = worst_ratio(b)
    print(f"largest likelihood ratio {ratio:.4f} <= "
          f"e^epsilon {np.exp(epsilon):.4f}")
    print(f"four weekly releases at epsilon 0.5 spend a total of {4 * epsilon:.1f}")

    # Membership inference: guess "was in training" when the loss is below 1.0.
    members = rng.exponential(0.6, 100_000)        # losses on training records
    outsiders = rng.exponential(1.4, 100_000)      # losses on unseen records
    tpr, fpr = np.mean(members < 1.0), np.mean(outsiders < 1.0)
    print(f"threshold attack: true positive rate {tpr:.3f}, false positive rate "
          f"{fpr:.3f}, advantage {tpr - fpr:.3f}")

    # Redaction: what a recall figure means at volume.
    tickets = 600_000
    for recall in (0.99, 0.999):
        print(f"redaction recall {recall}: {tickets * (1 - recall):,.0f} "
              f"of {tickets:,} account numbers leak")

    assert b == 2.0 and np.isclose(bound95, 5.99, atol=0.01)
    assert abs(inside - 0.95) < 0.005
    assert ratio <= np.exp(epsilon) + 1e-9
    assert np.isclose(ratio, np.exp(0.5))
    assert abs(tpr - (1 - np.exp(-1 / 0.6))) < 0.01          # 0.811 by hand
    assert abs(fpr - (1 - np.exp(-1 / 1.4))) < 0.01          # 0.510 by hand
    assert round(tickets * 0.01) == 6000 and round(tickets * 0.001) == 600
