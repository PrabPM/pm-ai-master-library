"""Chapter 17. From impressions to payback, and why ROAS is not profit."""
from payflow import (TYPICAL_CONTRIBUTION, TYPICAL_FEES, months_kept, payback_month)

# Paid search, August 2026.
SPEND = 60_000
IMPRESSIONS = 1_500_000
CLICK_RATE = 0.02        # clicks per impression
SIGNUP_RATE = 0.05       # sign-ups per click
ACTIVATION_RATE = 0.20   # sign-ups that take a first card payment

# Paid social in the same month, counted the same way (last touch).
SOCIAL_SPEND, SOCIAL_MERCHANTS = 42_000, 60


def chain():
    clicks = IMPRESSIONS * CLICK_RATE
    signups = clicks * SIGNUP_RATE
    merchants = signups * ACTIVATION_RATE
    return clicks, signups, merchants


def year_one(spend, merchants):
    """ROAS and profit per merchant over the first 12 months, allowing for churn."""
    cac = spend / merchants
    kept = months_kept(12)                 # 10.21 of 12 months, at 3% monthly churn
    fees = TYPICAL_FEES * kept             # revenue PayFlow bills
    contribution = TYPICAL_CONTRIBUTION * kept   # what is left after costs
    return {"cac": cac, "roas": fees / cac, "profit": contribution - cac,
            "payback": payback_month(cac, TYPICAL_CONTRIBUTION)}


def main():
    clicks, signups, merchants = chain()
    print(f"Impressions          {IMPRESSIONS:>10,}")
    print(f"Clicks               {clicks:>10,.0f}   {CLICK_RATE:.1%} of impressions")
    print(f"Sign-ups             {signups:>10,.0f}   {SIGNUP_RATE:.1%} of clicks")
    print(f"Activated merchants  {merchants:>10,.0f}   "
          f"{ACTIVATION_RATE:.1%} of sign-ups")
    print(f"Cost per click       {SPEND / clicks:>10,.2f}")
    print(f"Cost per sign-up     {SPEND / signups:>10,.2f}")
    print(f"Cost per merchant    {SPEND / merchants:>10,.2f}   (CAC)")

    search = year_one(SPEND, merchants)
    social = year_one(SOCIAL_SPEND, SOCIAL_MERCHANTS)
    print()
    print(f"{'Year one, per merchant':<26}{'Search':>10}{'Social':>10}")
    print(f"{'CAC':<26}{search['cac']:>10,.0f}{social['cac']:>10,.0f}")
    print(f"{'ROAS on fees':<26}{search['roas']:>10.2f}{social['roas']:>10.2f}")
    print(f"{'Contribution minus CAC':<26}{search['profit']:>+10,.0f}"
          f"{social['profit']:>+10,.0f}")
    print(f"{'Payback month':<26}{search['payback']:>10}{social['payback']:>10}")
    margin = TYPICAL_CONTRIBUTION / TYPICAL_FEES
    print(f"Contribution margin {margin:.1%}, so break-even ROAS is {1 / margin:.2f}")


if __name__ == "__main__":
    main()
