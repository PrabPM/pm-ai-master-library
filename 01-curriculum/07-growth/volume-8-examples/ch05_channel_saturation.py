"""Chapter 5: average cost versus marginal cost on a channel that saturates."""
from math import exp

CEILING, SCALE = 1_740, 250_000  # curve fitted to PayFlow's paid search history
PROFIT = 84                      # gross profit per active merchant per month


def activated(spend):
    """Activated merchants per month at a given monthly spend."""
    return CEILING * (1 - exp(-spend / SCALE))


print(f"{'Spend':>9}{'Merchants':>11}{'Average CAC':>13}{'Next $10k CAC':>15}"
      f"{'Payback':>10}")
for spend in range(50_000, 450_000, 50_000):
    merchants = activated(spend)
    marginal = 10_000 / (activated(spend + 10_000) - merchants)
    print(f"{spend:>9,}{merchants:>11,.0f}{spend / merchants:>13,.0f}"
          f"{marginal:>15,.0f}{marginal / PROFIT:>7.1f} mo")
