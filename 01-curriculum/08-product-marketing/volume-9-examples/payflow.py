"""Shared PayFlow numbers. PayFlow is fictional: every figure is made up."""

FEE_RATE, FEE_FIXED = 0.029, 0.30      # what PayFlow charges per payment
COST_RATE, COST_FIXED = 0.021, 0.10    # what card networks and banks charge PayFlow
SERVICING = 18.00                      # support and fraud losses per merchant-month
MONTHLY_CHURN = 0.03                   # share of small merchants who leave each month

# Instant Payouts.
INSTANT_FEE = 0.010    # the merchant pays 1% of the amount paid out
INSTANT_COST = 0.0035  # PayFlow pays 0.35% to push the money to a debit card


def monthly_fees(volume, payments):
    return FEE_RATE * volume + FEE_FIXED * payments


def monthly_contribution(volume, payments):
    card_costs = COST_RATE * volume + COST_FIXED * payments
    return monthly_fees(volume, payments) - card_costs - SERVICING


def months_kept(months, churn=MONTHLY_CHURN):
    """Expected number of months a merchant is still active in the first `months`."""
    return sum((1 - churn) ** k for k in range(months))


def money(amount, places=2):
    """Format dollars with the minus sign in front: -$177.00, not $-177.00."""
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.{places}f}"


def payback_month(cac, contribution, churn=MONTHLY_CHURN, limit=120):
    """First month in which cumulative contribution covers the acquisition cost."""
    total = 0.0
    for month in range(1, limit + 1):
        total += contribution * (1 - churn) ** (month - 1)
        if total >= cac:
            return month
    return None


# A typical new small merchant: $6,000 of card sales a month in 150 payments.
TYPICAL_FEES = monthly_fees(6_000, 150)                   # 219.00
TYPICAL_CONTRIBUTION = monthly_contribution(6_000, 150)   # 60.00
# A merchant won by the sales team is about three times larger.
SALES_CONTRIBUTION = monthly_contribution(18_000, 450)    # 216.00

if __name__ == "__main__":
    print(f"Typical merchant: fees ${TYPICAL_FEES:,.2f} a month, "
          f"contribution ${TYPICAL_CONTRIBUTION:,.2f}")
    print(f"Contribution margin rate: {TYPICAL_CONTRIBUTION / TYPICAL_FEES:.1%}")
    print(f"Sales-won merchant: contribution ${SALES_CONTRIBUTION:,.2f} a month")
    print(f"Expected active months in year one: {months_kept(12):.2f}")
    print(f"Lifetime contribution, typical: "
          f"${TYPICAL_CONTRIBUTION / MONTHLY_CHURN:,.0f}")
