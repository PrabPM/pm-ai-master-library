"""Chapter 10: the onboarding funnel for one weekly cohort of small merchants.

Counts are merchants who completed each step within 7 days of starting.
"""
STEPS = [
    ("1 Create account", 2000),
    ("2 Business details", 1840),
    ("3 Owner identity", 1560),
    ("4 Documents accepted", 1270),
    ("5 Bank account linked", 1190),
    ("6 Approved", 1160),
]


def main():
    started = STEPS[0][1]
    total_lost = started - STEPS[-1][1]
    print(f"{'step':<24}{'reached':>8}{'of start':>10}{'lost here':>11}"
          f"{'of losses':>11}")
    previous = started
    for name, reached in STEPS:
        lost = previous - reached
        share = f"{lost / total_lost:.0%}" if lost else ""
        row = (f"{name:<24}{reached:>8,}{reached / started:>10.0%}"
               f"{(lost if lost else ''):>11}{share:>11}")
        print(row.rstrip())
        previous = reached
    print(f"\nlost in total: {total_lost} of {started:,} "
          f"({total_lost / started:.0%})")


if __name__ == "__main__":
    main()
