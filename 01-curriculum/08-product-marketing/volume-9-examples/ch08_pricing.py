"""Chapter 8. Two ways to package Instant Payouts, seen from both sides."""
from payflow import INSTANT_COST, INSTANT_FEE, money

FLAT_PRICE = 25.00   # plan B: a monthly subscription with unlimited instant payouts

# Three kinds of adopter from the beta.
# Columns: profile, instant payout volume per month ($), adopters out of 100.
PROFILES = [
    ("Light", 800, 50),
    ("Typical", 5_200, 35),
    ("Heavy", 20_000, 15),
]


def plan_a(volume):
    """Pay as you go: price and PayFlow's margin at 1% of the amount."""
    price = INSTANT_FEE * volume
    return price, price - INSTANT_COST * volume


def plan_b(volume):
    """Flat subscription: price and PayFlow's margin at $25 a month."""
    return FLAT_PRICE, FLAT_PRICE - INSTANT_COST * volume


def main():
    print(f"{'Profile':<9}{'Volume':>8}{'A price':>9}{'B price':>9}{'Picks':>7}"
          f"{'A margin':>10}{'B margin':>10}")
    only_a = both = 0.0
    for name, volume, count in PROFILES:
        a_price, a_margin = plan_a(volume)
        b_price, b_margin = plan_b(volume)
        pick = "A" if a_price <= b_price else "B"
        only_a += count * a_margin
        both += count * (a_margin if pick == "A" else b_margin)
        print(f"{name:<9}{volume:>8,}{a_price:>9.2f}{b_price:>9.2f}{pick:>7}"
              f"{a_margin:>10.2f}{b_margin:>10.2f}")
    print(f"Break-even volume, where A and B cost the same: "
          f"${FLAT_PRICE / INSTANT_FEE:,.0f} a month")
    print(f"Monthly margin per 100 adopters, only A offered: {money(only_a)}")
    print(f"Monthly margin per 100 adopters, A and B offered: {money(both)}")


if __name__ == "__main__":
    main()
