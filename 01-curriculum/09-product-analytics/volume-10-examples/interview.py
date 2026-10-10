"""Chapters 27 and 28: the arithmetic behind the interview answers."""
from ch03_metric_tree import last_week, this_week, volume
from payflow import COST_FIXED, COST_PCT, FEE_FIXED, FEE_PCT, unit_economics

# ---- Chapter 28: an estimate you can check --------------------------------
population = 2_000_000
people_per_shop = 2_500          # assumption: one coffee shop per 2,500 people
independent = 0.60               # assumption: share not owned by a chain
card_payments_per_day = 240      # assumption: 300 customers, 80% pay by card
average_payment = 6.50
days_open = 350
share_won = 0.10

shops = population / people_per_shop * independent
payments = card_payments_per_day * days_open
volume_per_shop = payments * average_payment
revenue = FEE_PCT * volume_per_shop + FEE_FIXED * payments
cost = COST_PCT * volume_per_shop + COST_FIXED * payments
flat_revenue = 0.026 * volume_per_shop      # a flat 2.6% with no fixed fee

if __name__ == "__main__":
    lost = volume(last_week) - volume(this_week)
    u = unit_economics()
    print(f"Chapter 27: volume lost in the week ${lost:,.0f}")
    print(f"  revenue at {u['revenue'] / u['volume']:.2%} of volume: "
          f"${lost * u['revenue'] / u['volume']:,.0f}")
    print(f"  contribution at {u['contribution'] / u['volume']:.2%} of volume: "
          f"${lost * u['contribution'] / u['volume']:,.0f}")

    print()
    won = shops * share_won
    print(f"Chapter 28: independent coffee shops {shops:,.0f}, won {won:.0f}")
    print(f"One shop, one year: {payments:,} card payments, "
          f"${volume_per_shop:,.0f} volume")
    print(f"  at 2.9% + $0.30: revenue ${revenue:,.0f} "
          f"({revenue / volume_per_shop:.1%} of volume), net ${revenue - cost:,.0f}")
    print(f"  at a flat 2.6%:  revenue ${flat_revenue:,.0f}")
    print(f"Yearly revenue from {won:.0f} shops: ${won * flat_revenue / 1e6:.1f}M "
          f"to ${won * revenue / 1e6:.1f}M")
