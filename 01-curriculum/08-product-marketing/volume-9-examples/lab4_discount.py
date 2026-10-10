"""Lab 4. A flat discount against a volume tier for a four-shop restaurant group."""
from payflow import INSTANT_COST, INSTANT_FEE

VOLUME = 40_000          # Casa Verde's expected instant payout volume per month ($)
FLAT_DISCOUNT = 0.006    # the 0.6% rate the sales team asked for
TIER_LIMIT = 10_000      # list price applies up to here each month
TIER_RATE = 0.007        # rate on volume above the limit


def tiered_fee(volume):
    below = min(volume, TIER_LIMIT)
    return INSTANT_FEE * below + TIER_RATE * (volume - below)


def main():
    cost = INSTANT_COST * VOLUME
    list_fee = INSTANT_FEE * VOLUME
    offers = [("List price, 1.0%", list_fee),
              ("Flat discount, 0.6%", FLAT_DISCOUNT * VOLUME),
              ("Tier: 1.0% then 0.7%", tiered_fee(VOLUME))]
    print(f"{'Offer':<22}{'Fee':>8}{'Margin':>9}{'Price realization':>20}")
    for name, fee in offers:
        print(f"{name:<22}{fee:>8,.0f}{fee - cost:>9,.0f}{fee / list_fee:>20.1%}")
    list_margin = INSTANT_FEE - INSTANT_COST
    flat_margin = FLAT_DISCOUNT - INSTANT_COST
    print(f"Volume needed at 0.6% to match the list-price margin: "
          f"{list_margin / flat_margin:.1f} times as much")


if __name__ == "__main__":
    main()
