"""Chapter 14: cohort table -> retention curve -> expected value of a merchant."""
# Merchants still paying, by months since activation (2026 cohorts, to September).
COHORTS = {
    "Jan": [3900, 3129, 2880, 2671, 2574, 2481, 2465, 2397, 2369],
    "Feb": [3950, 3185, 2857, 2661, 2558, 2478, 2420, 2383],
    "Mar": [4100, 3248, 2889, 2710, 2572, 2515, 2467],
    "Apr": [4150, 3355, 2983, 2812, 2642, 2589],
    "May": [4250, 3440, 3090, 2870, 2750],
    "Jun": [4340, 3524, 3157, 2923],
}
ASSIST = [1.00, 0.55, 0.38, 0.28, 0.21, 0.16, 0.12, 0.09, 0.07]  # weekly Assist use
PROFIT = 84  # gross profit per active merchant per month, in dollars

print("Month " + "".join(f"{m:>6}" for m in range(9)))
for name, row in COHORTS.items():
    print(f"{name:<6}" + "".join(f"{n / row[0]:>6.0%}" for n in row))

pooled = []
for m in range(9):
    rows = [r for r in COHORTS.values() if len(r) > m]
    pooled.append(sum(r[m] for r in rows) / sum(r[0] for r in rows))
print("All   " + "".join(f"{r:>6.0%}" for r in pooled))


def active_months(curve, horizon=36):
    """Expected months active, extending the curve at its recent monthly ratio."""
    curve, ratio = list(curve), (curve[-1] / curve[-4]) ** (1 / 3)
    while len(curve) < horizon:
        curve.append(curve[-1] * ratio)
    return sum(curve), ratio


print()
for label, curve in [("Payments", pooled), ("Assist", ASSIST)]:
    months, ratio = active_months(curve)
    print(f"{label:<9} keeps {ratio:.1%} a month lately; "
          f"expected active months out of 36: {months:.1f}")
print(f"Payments: 36-month gross profit per activated merchant = "
      f"${PROFIT * active_months(pooled)[0]:,.0f}")
