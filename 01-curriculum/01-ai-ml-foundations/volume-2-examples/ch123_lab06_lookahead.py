"""Lab 6 (chapter 45): a feature that looks into the future."""
import numpy as np


def accuracy(feature, target):
    """Predict 'up tomorrow' when the feature is positive."""
    return float(np.mean((feature > 0) == target))


if __name__ == "__main__":
    rng = np.random.default_rng(12)
    days = 1000
    volume = 5000 + np.cumsum(rng.normal(0, 60, days))     # daily payments
    t = np.arange(6, days - 4)
    up_tomorrow = volume[t + 1] > volume[t]

    centered = np.array([volume[i - 3:i + 4].mean() for i in t]) - volume[t]
    trailing = np.array([volume[i - 6:i + 1].mean() for i in t]) - volume[t]

    acc_leaky = accuracy(centered, up_tomorrow)
    acc_honest = accuracy(-trailing, up_tomorrow)
    print(f"centered 7-day average (uses days t+1 to t+3): accuracy {acc_leaky:.3f}")
    print(f"trailing 7-day average (uses days up to t):     accuracy {acc_honest:.3f}")
    print(f"share of days that went up: {up_tomorrow.mean():.3f}")

    assert acc_leaky > 0.65 and abs(acc_honest - 0.5) < 0.05
