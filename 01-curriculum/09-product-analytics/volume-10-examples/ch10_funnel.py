"""Chapter 10: step and overall conversion for the August 2026 sign-up funnel."""

STEPS = ["Started sign-up", "Submitted KYB", "KYB approved",
         "First payment in 30 days"]
# merchants who started in August 2026, by how they planned to take payments
FUNNEL = {
    "Payment links (no code)": [690, 531, 452, 321],
    "Plugin or API": [950, 666, 553, 192],
}
TOTAL = [sum(column) for column in zip(*FUNNEL.values())]


def conversion(counts):
    """(step conversion, overall conversion) for each step after the first."""
    return [(counts[i] / counts[i - 1], counts[i] / counts[0])
            for i in range(1, len(counts))]


if __name__ == "__main__":
    print("All merchants who started in August 2026")
    print(f"  {STEPS[0]:<26}{TOTAL[0]:>6,}")
    for step, n, (by_step, overall) in zip(STEPS[1:], TOTAL[1:], conversion(TOTAL)):
        print(f"  {step:<26}{n:>6,}   {by_step:.0%} of previous   "
              f"{overall:.0%} of start")
    print("Approved -> first payment in 30 days, by integration plan")
    for name, counts in FUNNEL.items():
        print(f"  {name:<26}{counts[3]:>4} of {counts[2]} = "
              f"{counts[3] / counts[2]:.0%}")
    stuck = FUNNEL["Plugin or API"][2] - FUNNEL["Plugin or API"][3]
    print(f"Approved plugin or API merchants who never took a payment: {stuck}")
