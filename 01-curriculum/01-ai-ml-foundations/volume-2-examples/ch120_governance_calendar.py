"""Chapter 120: a governance calendar and a regulatory countdown.

Dates are the EU AI Act application dates as amended in July 2026. This is a
study aid, not legal advice.
"""
from datetime import date

TODAY = date(2026, 10, 9)

# (cadence, forum, meetings per year, hours each)
CALENDAR = [
    ("weekly", "evaluation and cost review", 52, 0.5),
    ("every 2 weeks", "security triage", 26, 0.5),
    ("monthly", "legal and privacy review", 12, 1.0),
    ("monthly", "finance and margin review", 12, 1.0),
    ("quarterly", "risk committee", 4, 1.5),
    ("quarterly", "customer and sales feedback", 4, 1.5),
    ("yearly", "provenance and data inventory audit", 1, 3.0),
]

MILESTONES = [
    (date(2024, 8, 1), "AI Act entered into force"),
    (date(2025, 2, 2), "prohibited practices and AI literacy"),
    (date(2025, 8, 2), "general-purpose model obligations"),
    (date(2026, 8, 2), "transparency duties (Article 50)"),
    (date(2026, 12, 2), "content marking for systems already on the market"),
    (date(2027, 12, 2), "high-risk systems listed in Annex III"),
    (date(2028, 8, 2), "high-risk AI inside regulated products (Annex I)"),
]


def days_until(d, today=TODAY):
    return (d - today).days


def describe(d, today=TODAY):
    n = days_until(d, today)
    return f"in {n} days" if n > 0 else f"{-n} days ago"


def yearly_load(calendar):
    """Meetings and hours a year."""
    meetings = sum(n for _, _, n, _ in calendar)
    hours = sum(n * h for _, _, n, h in calendar)
    return meetings, hours


if __name__ == "__main__":
    meetings, hours = yearly_load(CALENDAR)
    print(f"{meetings} governance meetings a year, {hours:.0f} PM hours, "
          f"{hours / 52:.1f} hours a week")
    print()
    for d, what in MILESTONES:
        print(f"{d.isoformat()}  {what:<50} {describe(d)}")

    assert meetings == 111 and hours == 78
    assert days_until(date(2026, 12, 2)) == 54
    assert days_until(date(2027, 12, 2)) == 419
    assert days_until(date(2028, 8, 2)) == 663
