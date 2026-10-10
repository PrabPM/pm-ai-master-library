"""Chapter 8: what a consent banner change does to measured traffic.

Two weeks of EU visits to PayFlow's marketing site. The banner was redesigned
between them so that "Reject" is as easy to click as "Accept".
"""

WEEK = ("visitors", "share who consent", "sign-ups by consenting visitors",
        "sign-ups recorded on the server for everyone")
BEFORE = (40_000, 0.78, 655, 801)
AFTER = (40_300, 0.52, 478, 806)


def measured(week):
    visitors, consent, tagged_signups, server_signups = week
    return {"visitors seen by analytics": visitors * consent,
            "sign-ups seen by analytics": tagged_signups,
            "sign-ups in the product database": server_signups}


if __name__ == "__main__":
    before, after = measured(BEFORE), measured(AFTER)
    print(f"{'':<34}{'before':>9}{'after':>9}{'change':>9}")
    for name in before:
        a, b = before[name], after[name]
        print(f"{name:<34}{a:>9,.0f}{b:>9,.0f}{b / a - 1:>+9.0%}")
    for label, week in [("before", BEFORE), ("after", AFTER)]:
        visitors, consent, tagged, server = week
        print(f"Sign-up rate {label}: consenting visitors "
              f"{tagged / (visitors * consent):.1%}, all visitors "
              f"{server / visitors:.1%}")
