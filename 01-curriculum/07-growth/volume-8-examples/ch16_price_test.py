"""Chapter 16: read a price test on revenue over time, not on sign-ups."""
ARMS = {  # price: (share of merchants shown the offer who subscribe, monthly churn)
    25: (0.060, 0.030),
    35: (0.046, 0.045),
}
SHOWN = 1_000

print(f"{'Price':>6}{'Subscribers':>13}{'Month 1':>10}{'12 months':>11}"
      f"{'Left at 12 mo':>15}")
for price, (take_rate, churn) in ARMS.items():
    subscribers = SHOWN * take_rate
    paid_months = sum((1 - churn) ** month for month in range(12))
    print(f"{'$' + str(price):>6}{subscribers:>13.0f}"
          f"{'$' + format(subscribers * price, ',.0f'):>10}"
          f"{'$' + format(subscribers * price * paid_months, ',.0f'):>11}"
          f"{subscribers * (1 - churn) ** 12:>15.0f}")
