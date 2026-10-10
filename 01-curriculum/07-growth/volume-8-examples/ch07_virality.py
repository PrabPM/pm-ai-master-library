"""Chapter 7: the viral factor K, its ceiling, and when cycle time matters."""


def merchants_after(days, seed, k, cycle_days):
    """The seed merchants plus every generation they bring in within `days`."""
    total = generation = seed
    for _ in range(days // cycle_days):
        generation *= k
        total += generation
    return total


k = 12 * 0.03 * 0.55  # payers invoiced x share who sign up x share who activate
print(f"K = 12 x 3% x 55% = {k:.3f}")
print(f"Ceiling for K below 1: 1 / (1 - K) = {1 / (1 - k):.2f}x the seed")
print()
print(f"{'1,000 seed merchants, 180 days later':<40}{'Total':>8}")
scenarios = [
    ("Today: K 0.20, 45-day cycle", k, 45),
    ("Faster: K 0.20, 15-day cycle", k, 15),
    ("Stronger: K 0.40, 45-day cycle", 2 * k, 45),
    ("If K were 1.10, 45-day cycle", 1.10, 45),
    ("If K were 1.10, 15-day cycle", 1.10, 15),
]
for label, factor, cycle in scenarios:
    print(f"{label:<40}{merchants_after(180, 1_000, factor, cycle):>8,.0f}")
