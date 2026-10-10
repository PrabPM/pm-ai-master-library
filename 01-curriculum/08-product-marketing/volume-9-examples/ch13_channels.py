"""Chapter 13. Average, blended and marginal cost of a new merchant, by channel."""
from payflow import SALES_CONTRIBUTION, TYPICAL_CONTRIBUTION

# August 2026. A merchant is counted for the channel of its last touch before sign-up
# and counts once it has taken its first card payment ("activated").
# Columns: channel, spend ($), activated merchants, contribution per merchant-month.
CHANNELS = [
    ("Paid search", 60_000, 300, TYPICAL_CONTRIBUTION),
    ("Paid social", 42_000, 60, TYPICAL_CONTRIBUTION),
    ("Bookkeeper referrals", 24_000, 120, TYPICAL_CONTRIBUTION),
    ("Sales team", 54_000, 90, SALES_CONTRIBUTION),
    ("Organic", 20_000, 430, TYPICAL_CONTRIBUTION),
]
PAID = ("Paid search", "Paid social")

# Paid search by slice of monthly budget: what each extra $20,000 bought. The last
# slice is Grace's forecast for September from the bids she would have to place.
SEARCH_SLICES = [
    ("First $20,000", 20_000, 125),
    ("Second $20,000", 20_000, 100),
    ("Third $20,000", 20_000, 75),
    ("Next $20,000 (forecast)", 20_000, 40),
]


def main():
    print(f"{'Channel':<23}{'Spend':>9}{'Merchants':>11}{'CAC':>7}"
          f"{'Simple payback':>16}")
    for name, spend, merchants, contribution in CHANNELS:
        cac = spend / merchants
        print(f"{name:<23}{spend:>9,}{merchants:>11,}{cac:>7,.0f}"
              f"{cac / contribution:>9.1f} months")
    spend = sum(c[1] for c in CHANNELS)
    merchants = sum(c[2] for c in CHANNELS)
    paid_spend = sum(c[1] for c in CHANNELS if c[0] in PAID)
    paid_merchants = sum(c[2] for c in CHANNELS if c[0] in PAID)
    print(f"{'Blended, all channels':<23}{spend:>9,}{merchants:>11,}"
          f"{spend / merchants:>7,.0f}")
    print(f"{'Paid channels only':<23}{paid_spend:>9,}{paid_merchants:>11,}"
          f"{paid_spend / paid_merchants:>7,.0f}")

    print()
    print(f"{'Paid search slice':<25}{'Merchants':>10}{'Marginal CAC':>14}"
          f"{'Average CAC so far':>20}")
    total_spend = total_merchants = 0
    for name, slice_spend, slice_merchants in SEARCH_SLICES:
        total_spend += slice_spend
        total_merchants += slice_merchants
        print(f"{name:<25}{slice_merchants:>10}{slice_spend / slice_merchants:>14,.0f}"
              f"{total_spend / total_merchants:>20,.0f}")


if __name__ == "__main__":
    main()
