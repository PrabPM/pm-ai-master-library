"""Numbers behind the model answers in Chapter 25 (Labs)."""
from math import log

from scipy.stats import chisquare
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import (confint_proportions_2indep,
                                          proportion_effectsize,
                                          proportions_ztest)

from ch17_ltv import MONTHLY_RATE
from ch19_projection import irr, npv, payback
from payflow import unit_economics


def lab1():
    print("Lab 1: one name, three numbers")
    for team, top, bottom, what in [
            ("Growth", 513, 1_640, "paid in 30 days / started"),
            ("Product", 513, 1_005, "paid in 30 days / approved"),
            ("Sales", 148, 231, "ever paid / approved, sales-assisted only")]:
        print(f"  {team:<8}{top:>4} / {bottom:>5,} = {top / bottom:.1%}   {what}")


def lab3():
    print("Lab 3: decompose a drop, then segment it")
    # tier: (active merchants, attempts, successful payments, volume in dollars)
    last = {"50 largest": (50, 7_200, 6_600, 2_700_000),
            "everyone else": (8_950, 384_300, 353_600, 15_309_000)}
    this = {"50 largest": (50, 4_150, 3_800, 1_540_000),
            "everyone else": (9_010, 388_900, 358_200, 15_420_000)}

    def factors(week):
        m, a, s, v = (sum(t[i] for t in week.values()) for i in range(4))
        return {"active merchants": m, "attempts per merchant": a / m,
                "success rate": s / a, "average payment": v / s}, v

    f0, v0 = factors(last)
    f1, v1 = factors(this)
    shown = {"active merchants": "{:,.0f}", "attempts per merchant": "{:.2f}",
             "success rate": "{:.1%}", "average payment": "${:.2f}"}
    print(f"  volume ${v0:,.0f} -> ${v1:,.0f} ({v1 / v0 - 1:+.1%})")
    for name, fmt in shown.items():
        share = log(f1[name] / f0[name]) / log(v1 / v0)
        print(f"  {name:<22}{fmt.format(f0[name]):>8} -> {fmt.format(f1[name]):>7}"
              f"{f1[name] / f0[name] - 1:>+8.1%}{share:>7.0%} of the drop")
    for tier in last:
        a, b = last[tier][3], this[tier][3]
        print(f"  {tier:<14} {'$' + format(a, ','):>11} -> {'$' + format(b, ','):>11}"
              f"  ({b - a:+,})")


def lab4():
    print("Lab 4: Instant Payouts subscribers still paying, by start month")
    cohorts = {"Jun": [400, 328, 295, 277], "Jul": [420, 340, 302],
               "Aug": [600, 390], "Sep": [450]}
    for name, counts in cohorts.items():
        row = "".join(f"{c / counts[0]:>7.0%}" for c in counts)
        print(f"  {name}  n={counts[0]:<5}{row}")
    started = sum(c[0] for c in cohorts.values() if len(c) > 1)
    kept = sum(c[1] for c in cohorts.values() if len(c) > 1)
    print(f"  blended month-1 retention: {kept:,} / {started:,} = {kept / started:.1%}")
    print(f"  August leavers: 210, of which payment failed 60 = {60 / 210:.0%}")


def lab5():
    print("Lab 5: bookkeeper referral channel")
    u = unit_economics(volume=14_000, payments=200)
    margin = u["contribution"]
    cac = 300 + 45_000 / 150
    curve = [1.0, 0.95] + [0.95 * 0.98 ** k for k in range(1, 35)]
    total, month = 0.0, None
    for age, share in enumerate(curve):
        total += margin * share
        if month is None and total >= cac:
            month = age + 1
    ltv = sum(margin * s / (1 + MONTHLY_RATE) ** age for age, s in enumerate(curve))
    print(f"  contribution ${margin:.2f} a month, CAC ${cac:,.0f}")
    print(f"  payback in month {month}, 36-month discounted LTV ${ltv:,.0f}, "
          f"LTV:CAC {ltv / cac:.1f}")


def lab6():
    print("Lab 6: dispute automation, 24 months")
    handling = 2_400 * 12 * 0.60            # minutes saved x cost per minute
    wins = 2_400 * 0.04 * 85                # extra disputes won x average amount

    def flows(win_benefit):
        out = []
        for t in range(24):
            if t < 5:
                out.append(-50_000.0)
            else:
                ramp = 0.5 if t < 8 else 1.0
                out.append(ramp * (handling + win_benefit) - 4_000)
        return out

    full = flows(wins)
    print(f"  monthly benefit at full ramp: handling ${handling:,.0f} + "
          f"wins ${wins:,.0f}")
    print(f"  NPV {npv(full):,.0f}, IRR {irr(full):.0%}, payback month "
          f"{payback(full)}")
    print(f"  NPV with no win-rate gain at all: {npv(flows(0)):,.0f}")


def lab7():
    print("Lab 7: KYB form test")
    effect = proportion_effectsize(0.76, 0.73)
    n = NormalIndPower().solve_power(effect, alpha=0.05, power=0.80, ratio=1)
    print(f"  need {n:,.0f} per arm; at 380 starters a week that is "
          f"{2 * n / 380:.1f} weeks")
    x0, n0, x1, n1 = 2_489, 3_410, 2_378, 3_150
    _, p = proportions_ztest([x1, x0], [n1, n0])
    low, high = confint_proportions_2indep(x1, n1, x0, n0, method="wald")
    print(f"  control {x0 / n0:.1%}, treatment {x1 / n1:.1%}, difference "
          f"{x1 / n1 - x0 / n0:+.1%}")
    print(f"  95% CI {low:+.1%} to {high:+.1%}, p = {p:.3f}")
    _, srm = chisquare([n0, n1])
    print(f"  split {n0:,} vs {n1:,}: p = {srm:.4f}")


if __name__ == "__main__":
    for lab in (lab1, lab3, lab4, lab5, lab6, lab7):
        lab()
        print()
