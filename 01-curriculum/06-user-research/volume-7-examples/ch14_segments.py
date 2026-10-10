"""Chapter 14: which way of splitting merchants explains who finishes?

One weekly cohort of 2,000 small merchants, counted two ways. A useful basis
produces groups that behave differently from each other.
"""
BY_INDUSTRY = {            # segment: (started, approved within 7 days)
    "Retail": (620, 357),
    "Food and drink": (480, 283),
    "Services": (610, 352),
    "Other": (290, 168),
}
BY_OWNERS_AND_DEVICE = {
    "One owner, computer": (540, 421),
    "One owner, phone": (760, 456),
    "Several owners, computer": (320, 163),
    "Several owners, phone": (380, 120),
}


def report(title, segments):
    lost_all = sum(s - f for s, f in segments.values())
    rates = []
    print(title)
    print(f"  {'segment':<26}{'started':>8}{'finished':>10}{'rate':>7}"
          f"{'of losses':>11}")
    for name, (started, finished) in segments.items():
        rates.append(finished / started)
        print(f"  {name:<26}{started:>8,}{finished:>10,}{rates[-1]:>7.0%}"
              f"{(started - finished) / lost_all:>11.0%}")
    print(f"  finish rate runs from {min(rates):.0%} to {max(rates):.0%}")


if __name__ == "__main__":
    report("Split by industry", BY_INDUSTRY)
    print()
    report("Split by number of owners and device", BY_OWNERS_AND_DEVICE)
