"""Chapter 22: how looking early and often manufactures false wins."""
import numpy as np
from scipy.stats import norm

rng = np.random.default_rng(21)
TESTS, N, RATE = 20_000, 4_300, 0.55  # A/A tests: both groups get the same thing


def false_win_rate(looks, alpha=0.05):
    """Share of A/A tests that show p < alpha at any one of the looks."""
    seen = np.linspace(N / looks, N, looks).round()  # merchants per group so far
    steps = np.diff(seen, prepend=0).astype(int)
    a = rng.binomial(steps, RATE, (TESTS, looks)).cumsum(axis=1)
    b = rng.binomial(steps, RATE, (TESTS, looks)).cumsum(axis=1)
    pooled = (a + b) / (2 * seen)
    z = (a - b) / seen / np.sqrt(2 * pooled * (1 - pooled) / seen)
    return (2 * norm.sf(np.abs(z)) < alpha).any(axis=1).mean()


print("Looks  Threshold  A/A tests that 'win'")
for looks, alpha in [(1, 0.05), (5, 0.05), (10, 0.05), (33, 0.05), (5, 0.0158)]:
    print(f"{looks:>5}{alpha:>11.4f}{false_win_rate(looks, alpha):>22.1%}")
