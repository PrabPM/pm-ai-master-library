"""Lab 1: PayFlow Terminal's growth model under three options."""
BASE = dict(signups=1_500, activation=0.70, churn=0.05, resurrection=0.01)


def simulate(months=12, active=12_000, dormant=9_000, **change):
    p = {**BASE, **change}
    for _ in range(months):
        new = p["signups"] * p["activation"]
        churned = active * p["churn"]
        resurrected = dormant * p["resurrection"]
        active += new + resurrected - churned
        dormant += churned - resurrected
    return active


options = [
    ("Today's inputs", {}),
    ("A: sign-ups +20%", dict(signups=1_800)),
    ("B: churn 5% -> 4%", dict(churn=0.04)),
    ("C: activation 70% -> 77%", dict(activation=0.77)),
]
print(f"{'Option':<26}{'12 months':>10}{'36 months':>11}")
for label, change in options:
    print(f"{label:<26}{simulate(**change):>10,.0f}{simulate(36, **change):>11,.0f}")
