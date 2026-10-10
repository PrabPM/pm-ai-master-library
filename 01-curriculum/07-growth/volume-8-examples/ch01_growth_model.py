"""Chapter 1: PayFlow's growth model and a one-input-at-a-time sensitivity table."""
BASE = dict(signups=8_000, activation=0.55, churn=0.030, resurrection=0.015)
PROFIT = 84  # gross profit per active merchant per month, in dollars


def simulate(months=12, active=90_000, dormant=60_000, **change):
    p = {**BASE, **change}
    merchant_months = 0
    for _ in range(months):
        new = p["signups"] * p["activation"]
        churned = active * p["churn"]
        resurrected = dormant * p["resurrection"]
        active += new + resurrected - churned
        dormant += churned - resurrected
        merchant_months += active
    return active, merchant_months


base_active, base_months = simulate()
print(f"Base case: {base_active:,.0f} active merchants after 12 months")
print()
print(f"{'Improve one input by 10%':<32}{'Active':>9}{'Extra':>8}{'Extra profit':>14}")
tests = [
    ("Sign-ups 8,000 -> 8,800", dict(signups=8_800)),
    ("Activation 55.0% -> 60.5%", dict(activation=0.605)),
    ("Churn 3.0% -> 2.7%", dict(churn=0.027)),
    ("Resurrection 1.50% -> 1.65%", dict(resurrection=0.0165)),
]
for label, change in tests:
    active, months = simulate(**change)
    profit = (months - base_months) * PROFIT
    print(f"{label:<32}{active:>9,.0f}{active - base_active:>8,.0f}{profit:>14,.0f}")
