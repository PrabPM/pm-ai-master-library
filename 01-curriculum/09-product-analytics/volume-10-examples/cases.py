"""Numbers behind Chapter 26 (Worked cases 2 and 3). Case 1 is SQL only."""
import numpy as np

from ch17_ltv import (LTV_36, MONTHLY_RATE, hazards, ltv, rows, survival_curve)
from ch19_projection import BASE, cash_flows, npv, project
from ch23_attribution import INCREMENTAL, SPEND, attribute, last_touch
from payflow import SPRING_PUSH, survival_table

before = hazards(survival_table([r for r in rows if r[0] < SPRING_PUSH]))
after = hazards(survival_table([r for r in rows if r[0] >= SPRING_PUSH]))
LTV_RECENT = ltv(survival_curve(after, borrow=before), monthly_rate=MONTHLY_RATE)
PER_MERCHANT = 150_000 / 1_500        # sales assist and onboarding, Chapter 18


def case2():
    print("Case 2: the partner bonus")
    claimed = attribute(last_touch)["Partner"]
    real = INCREMENTAL["Partner"]
    spend = SPEND["Partner"]
    print(f"  last-touch: {claimed:.0f} merchants at ${spend / claimed:,.0f} each")
    print(f"  holdout:    {real} incremental merchants at ${spend / real:,.0f} each")
    print(f"  LTV of merchants activated since April: ${LTV_RECENT:,.0f}")
    print(f"  value created per incremental merchant: "
          f"${LTV_RECENT - PER_MERCHANT - spend / real:,.0f}")
    social = SPEND["Social"] / INCREMENTAL["Social"]
    moved = spend / social
    print(f"  the same ${spend:,} in social at ${social:,.0f} per incremental "
          f"merchant: {moved:.0f} merchants, {moved - real:+.0f}")


def case3():
    print("Case 3: Quickstart after the pilot, against more paid media")
    for label, lift in [("pilot estimate", 0.055), ("low end of CI", 0.020),
                        ("high end of CI", 0.089)]:
        v = npv(cash_flows(project(**{**BASE, "lift": lift})))
        print(f"  Quickstart NPV at {lift:+.1%} ({label}): {v:>10,.0f}")
    rng = np.random.default_rng(26)
    se = (0.089 - 0.020) / (2 * 1.96)
    draws = [npv(cash_flows(project(**{**BASE, "lift": x})))
             for x in rng.normal(0.055, se, size=4_000)]
    print(f"  lift uncertainty only: mean {np.mean(draws):,.0f}, "
          f"chance of loss {np.mean(np.array(draws) < 0):.0%}")

    budget = 800_000
    cost_now = 420_000 / (0.60 * 800)          # media per incremental merchant
    recent = survival_curve(after, borrow=before, months=60)
    for years in (3, 5):
        months = 12 * years
        quick = npv(cash_flows(project(**{**BASE, "lift": 0.055}, months=months)))
        value = ltv(recent[:months], monthly_rate=MONTHLY_RATE) - PER_MERCHANT
        print(f"  {years}-year view: Quickstart NPV {quick:,.0f}")
        for label, worse in [("today's incremental cost", 1.00),
                             ("next dollars 25% worse", 1.25)]:
            merchants = budget / (cost_now * worse)
            print(f"      paid media, {label}: {merchants:,.0f} merchants, "
                  f"NPV {merchants * value - budget:,.0f}")
    print(f"  (3-year LTV used for paid merchants ${LTV_RECENT:,.0f}; "
          f"all merchants ${LTV_36:,.0f})")


if __name__ == "__main__":
    case2()
    print()
    case3()
