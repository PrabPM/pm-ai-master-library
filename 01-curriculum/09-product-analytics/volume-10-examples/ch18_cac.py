"""Chapter 18: CAC four ways, payback, and ROAS versus ROI. Q3 2026."""
from ch17_ltv import CURVE, LTV_36
from payflow import MARGIN, unit_economics

SPEND = {"paid media": 420_000, "marketing team and tools": 120_000,
         "sales assist": 90_000, "KYB checks and onboarding": 60_000}
NEW = {"paid": 800, "organic": 700}       # activated merchants, by claimed source
ALL_NEW = sum(NEW.values())
PER_MERCHANT = SPEND["sales assist"] + SPEND["KYB checks and onboarding"]

CAC = {
    "blended, media only": SPEND["paid media"] / ALL_NEW,
    "paid, media only": SPEND["paid media"] / NEW["paid"],
    "blended, fully loaded": sum(SPEND.values()) / ALL_NEW,
    # paid merchants carry all media and marketing, plus their share of the rest
    "paid, fully loaded": (SPEND["paid media"] + SPEND["marketing team and tools"]
                           + PER_MERCHANT * NEW["paid"] / ALL_NEW) / NEW["paid"],
}


def payback_month(cac, curve=CURVE, margin=MARGIN):
    """First month (1 = activation month) when cumulative margin covers CAC."""
    total = 0.0
    for age, share in enumerate(curve):
        total += margin * share
        if total >= cac:
            return age + 1
    return None


if __name__ == "__main__":
    print(f"{'CAC definition':<24}{'CAC':>7}{'payback':>10}{'LTV:CAC':>9}")
    for name, cac in CAC.items():
        print(f"{name:<24}{cac:>7,.0f}{payback_month(cac):>7} mo"
              f"{LTV_36 / cac:>9.1f}")
    print(f"(LTV = ${LTV_36:,.0f}: 36 months, discounted, from Chapter 17)")

    print()
    u = unit_economics()
    months = sum(CURVE[:12])               # active months per merchant in year 1
    media, loaded = SPEND["paid media"], CAC["paid, fully loaded"] * NEW["paid"]
    print(f"Paid media ${media:,} -> {NEW['paid']} merchants, "
          f"{months:.2f} active months each in year 1")
    for label, per_month in [("payment volume", u["volume"]),
                             ("revenue", u["revenue"]),
                             ("net revenue", u["net_revenue"]),
                             ("contribution margin", u["contribution"])]:
        total = NEW["paid"] * months * per_month
        print(f"  {label:<22}{'$' + format(total, ',.0f'):>12}   / media spend = "
              f"{total / media:>6.1f}x")
    gain = NEW["paid"] * months * u["contribution"]
    print(f"12-month ROI on media alone:        {gain / media - 1:+.0%}")
    print(f"12-month ROI on all paid costs (${loaded:,.0f}): "
          f"{gain / loaded - 1:+.0%}")
