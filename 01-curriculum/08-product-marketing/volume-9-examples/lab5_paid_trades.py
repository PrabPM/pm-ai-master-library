"""Lab 5. A paid search campaign for trades businesses, and whether to grow it."""
from payflow import monthly_contribution, payback_month

IMPRESSIONS, CLICK_RATE = 800_000, 0.015
COST_PER_CLICK = 3.50
SIGNUP_RATE, ACTIVATION_RATE = 0.04, 0.25
# A trades merchant: $14,000 of card sales a month in 80 payments.
CONTRIBUTION = monthly_contribution(14_000, 80)
# Forecast for the next slice of budget.
EXTRA_SPEND, EXTRA_MERCHANTS = 14_000, 10


def main():
    clicks = IMPRESSIONS * CLICK_RATE
    spend = clicks * COST_PER_CLICK
    signups = clicks * SIGNUP_RATE
    merchants = signups * ACTIVATION_RATE
    print(f"Clicks {clicks:,.0f}, spend ${spend:,.0f}, sign-ups {signups:,.0f}, "
          f"activated merchants {merchants:,.0f}")
    print(f"Contribution per merchant-month: ${CONTRIBUTION:,.2f}")
    rows = [("Current campaign", spend, merchants),
            ("Extra slice alone", EXTRA_SPEND, EXTRA_MERCHANTS),
            ("Both together", spend + EXTRA_SPEND, merchants + EXTRA_MERCHANTS)]
    print(f"{'':<19}{'Spend':>8}{'Merchants':>11}{'CAC':>7}{'Payback month':>15}")
    for name, cost, count in rows:
        cac = cost / count
        print(f"{name:<19}{cost:>8,.0f}{count:>11,.0f}{cac:>7,.0f}"
              f"{payback_month(cac, CONTRIBUTION):>15}")


if __name__ == "__main__":
    main()
