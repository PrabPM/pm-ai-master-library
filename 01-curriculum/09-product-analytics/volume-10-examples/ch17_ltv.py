"""Chapter 17: lifetime value of an activated small merchant, three ways."""
from payflow import COHORTS, MARGIN, SPRING_PUSH, simulate, survival_table

rows = simulate()
table = survival_table(rows)
HORIZON = 36                                  # months
ANNUAL_RATE = 0.10
MONTHLY_RATE = (1 + ANNUAL_RATE) ** (1 / 12) - 1

# pooled hazard over ages 7-11, used to extend the curve past what we observed
TAIL = (sum(left for age, _, left, _, _ in table if age >= 7) /
        sum(at_risk for age, at_risk, _, _, _ in table if age >= 7))


def hazards(tbl):
    return [h for _, _, _, h, _ in tbl]


def survival_curve(observed, months=HORIZON, tail=TAIL, borrow=()):
    """Share of activated merchants still paying at ages 0..months-1.

    observed: monthly hazards for ages 1, 2, ... as far as the data goes.
    borrow:   hazards to use for ages this group has not reached yet.
    After both run out, the tail hazard is assumed to continue.
    """
    known = list(observed) + list(borrow[len(observed):])
    curve = [1.0]
    for age in range(1, months):
        h = known[age - 1] if age <= len(known) else tail
        curve.append(curve[-1] * (1 - h))
    return curve


def ltv(curve, margin=MARGIN, monthly_rate=0.0):
    return sum(margin * s / (1 + monthly_rate) ** age for age, s in enumerate(curve))


def usd(value):
    return "$" + format(value, ",.0f")


def blended_churn(rows):
    """Of these merchants paying in August 2026, the share gone in September."""
    aug = len(COHORTS) - 2
    paying = [(c, last, churned) for c, last, churned, _ in rows
              if c <= aug and last >= aug - c]
    left = sum(1 for c, last, churned in paying if churned and last == aug - c)
    return left / len(paying)


CURVE = survival_curve(hazards(table))
LTV_36 = ltv(CURVE, monthly_rate=MONTHLY_RATE)        # reused in later chapters

if __name__ == "__main__":
    print(f"Monthly contribution margin per active merchant: ${MARGIN:.2f}")
    print("1. Formula: margin / monthly churn")
    for label, churn in [("blended, Aug to Sep", blended_churn(rows)),
                         ("first month", table[0][3]),
                         ("months 7 to 11", TAIL)]:
        print(f"   {label:<22}{churn:>6.1%}  ->  {usd(MARGIN / churn):>7}")
    print("2. Cohort: margin x share still paying, month by month")
    print(f"   {'first 12 months (observed)':<38}{usd(ltv(CURVE[:12])):>7}")
    print(f"   {'36 months, tail at ' + format(TAIL, '.1%') + ' a month':<38}"
          f"{usd(ltv(CURVE)):>7}")
    print(f"3. Same 36 months, discounted at {ANNUAL_RATE:.0%} a year"
          f"{usd(LTV_36):>12}")

    print()
    before = hazards(survival_table([r for r in rows if r[0] < SPRING_PUSH]))
    after = hazards(survival_table([r for r in rows if r[0] >= SPRING_PUSH]))
    print("Discounted 36-month LTV by activation cohort")
    for label, own in [("Oct 2025 to Mar 2026", before),
                       ("Apr 2026 to Sep 2026", after)]:
        curve = survival_curve(own, borrow=before)
        print(f"   {label}: ${ltv(curve, monthly_rate=MONTHLY_RATE):,.0f}"
              f"   (own data to month {len(own)})")
