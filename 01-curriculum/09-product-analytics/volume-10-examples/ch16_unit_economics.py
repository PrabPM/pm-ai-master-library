"""Chapter 16: unit economics of one small merchant, then the segment's quarter."""
from payflow import (COST_FIXED, COST_PCT, FEE_FIXED, FEE_PCT, PAYMENTS, VOLUME,
                     unit_economics)

u = unit_economics()


def one_payment(amount):
    """What PayFlow keeps on a single card payment, before other costs."""
    fee = FEE_PCT * amount + FEE_FIXED
    cost = COST_PCT * amount + COST_FIXED
    return fee, cost, fee - cost


if __name__ == "__main__":
    print(f"One active small merchant, one month: {PAYMENTS} payments, "
          f"${VOLUME:,.0f} volume")
    lines = [("Revenue (2.9% + $0.30)", u["revenue"]),
             ("- interchange, network, processor", -u["processing"]),
             ("= Net revenue", u["net_revenue"]),
             ("- fraud and dispute losses", -u["losses"]),
             ("- support", -u["support"]),
             ("- payouts", -u["payouts"]),
             ("= Contribution margin", u["contribution"])]
    for label, value in lines:
        print(f"  {label:<36}{value:>9,.2f}{value / VOLUME:>8.2%} of volume")
    print(f"  Contribution margin ratio: {u['contribution'] / u['revenue']:.1%} "
          f"of revenue")

    print()
    for amount in (5, 50, 500):
        fee, cost, kept = one_payment(amount)
        print(f"${amount:>3} payment: fee ${fee:.2f} ({fee / amount:.1%}), "
              f"cost ${cost:.2f}, PayFlow keeps ${kept:.2f} ({kept / amount:.2%})")

    print()
    months = 29_400                       # active merchant-months in Q3 2026
    fixed = {"Sales and marketing": 690_000, "Product and engineering": 1_150_000,
             "General and administrative": 420_000}
    revenue, contribution = months * u["revenue"], months * u["contribution"]
    print(f"Small-business segment, Q3 2026 ({months:,} merchant-months)")
    print(f"  {'Revenue':<30}{revenue:>12,.0f}")
    print(f"  {'Variable costs':<30}{-(revenue - contribution):>12,.0f}")
    print(f"  {'Contribution margin':<30}{contribution:>12,.0f}")
    for name, cost in fixed.items():
        print(f"  {name:<30}{-cost:>12,.0f}")
    operating = contribution - sum(fixed.values())
    print(f"  {'Operating income':<30}{operating:>12,.0f}"
          f"   ({operating / revenue:.1%} of revenue)")
