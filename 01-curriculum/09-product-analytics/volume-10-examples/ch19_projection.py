"""Chapter 19: a driver-based projection of Quickstart, with NPV and IRR.

Months 0-35 are January 2027 to December 2029. Cash flows are discounted from
the end of each month back to the end of December 2026.
"""
from ch17_ltv import MONTHLY_RATE, TAIL, hazards, survival_curve, table
from payflow import MARGIN

MONTHS = 36
BASE = {"approved": 1_000,     # merchants passing KYB each month
        "growth": 0.005,       # monthly growth in approvals
        "lift": 0.05,          # extra share of approved merchants who activate
        "launch": 6,           # month index when Quickstart goes live (Jul 2027)
        "build": 800_000,      # one-time cost, spread evenly before launch
        "run": 10_000,         # monthly running cost after launch
        "margin": MARGIN,      # contribution per active merchant-month
        "churn": 1.0}          # multiplier on every monthly hazard
SCENARIOS = {"Downside": {**BASE, "lift": 0.02, "launch": 9, "build": 1_000_000},
             "Base": BASE,
             "Upside": {**BASE, "lift": 0.08}}


def project(approved, growth, lift, launch, build, run, margin, churn,
            months=MONTHS):
    """Monthly rows of (extra activated, extra active, contribution, cost)."""
    curve = survival_curve([h * churn for h in hazards(table)], months=months,
                           tail=TAIL * churn)
    extra = [approved * (1 + growth) ** t * lift if t >= launch else 0.0
             for t in range(months)]
    rows = []
    for t in range(months):
        active = sum(extra[a] * curve[t - a] for a in range(t + 1))
        cost = build / launch if t < launch else run
        rows.append((extra[t], active, active * margin, cost))
    return rows


def cash_flows(rows):
    return [contribution - cost for _, _, contribution, cost in rows]


def npv(flows, rate=MONTHLY_RATE):
    return sum(f / (1 + rate) ** (t + 1) for t, f in enumerate(flows))


def irr(flows):
    """Annual rate at which NPV is zero, found by bisection on a monthly rate."""
    lo, hi = -0.5, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if npv(flows, mid) > 0 else (lo, mid)
    return (1 + lo) ** 12 - 1


def payback(flows):
    total = 0.0
    for t, f in enumerate(flows):
        total += f
        if total >= 0:
            return t + 1
    return None


if __name__ == "__main__":
    rows = project(**BASE)
    print("Base scenario: +5 points of activation from July 2027")
    print(f"{'year':<6}{'extra activated':>16}{'extra active, Dec':>19}"
          f"{'contribution':>14}{'cost':>10}{'net cash':>11}")
    for y in range(3):
        year = rows[12 * y:12 * y + 12]
        contribution, cost = sum(r[2] for r in year), sum(r[3] for r in year)
        print(f"{2027 + y:<6}{sum(r[0] for r in year):>16,.0f}{year[-1][1]:>19,.0f}"
              f"{contribution:>14,.0f}{cost:>10,.0f}{contribution - cost:>11,.0f}")

    print()
    print(f"{'scenario':<10}{'lift':>6}{'NPV at 10%':>12}{'IRR':>7}"
          f"{'payback':>12}{'3-year ROI':>12}")
    for name, drivers in SCENARIOS.items():
        r = project(**drivers)
        flows = cash_flows(r)
        cost = sum(row[3] for row in r)
        month = payback(flows)
        when = f"month {month}" if month else "not in 3 y"
        print(f"{name:<10}{drivers['lift'] * 100:>+4.0f}pt{npv(flows):>12,.0f}"
              f"{irr(flows):>7.0%}{when:>12}{sum(flows) / cost:>+12.0%}")
