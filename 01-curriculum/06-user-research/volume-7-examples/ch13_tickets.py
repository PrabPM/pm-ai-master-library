"""Chapter 13: one week of onboarding support tickets, counted by tag."""
STARTS_THIS_WEEK = 2000
TICKETS = {
    "Document rejected": 139,
    "Which document do you need?": 61,
    "Ownership or business-type question": 54,
    "Lost progress or locked out": 37,
    "Verification is taking too long": 29,
    "Other": 20,
}


def main():
    total = sum(TICKETS.values())
    print(f"{'tag':<38}{'tickets':>8}{'share':>7}{'per 1,000 starts':>18}")
    for tag, count in TICKETS.items():
        print(f"{tag:<38}{count:>8}{count / total:>7.0%}"
              f"{count / STARTS_THIS_WEEK * 1000:>18.1f}")
    print(f"{'All onboarding tickets':<38}{total:>8}{'':>7}"
          f"{total / STARTS_THIS_WEEK * 1000:>18.1f}")


if __name__ == "__main__":
    main()
