"""Chapter 9. Score five releases to decide how much launch each one gets."""

# Each criterion is scored 1 (low) to 5 (high). The weights add up to 10.
WEIGHTS = {"reach": 3, "revenue": 3, "news": 2, "change": 2}

# reach   = share of merchants who will notice
# revenue = effect on revenue or retention
# news    = how new this is to the market
# change  = how much customers must learn, do or accept
RELEASES = [
    ("Instant Payouts", {"reach": 4, "revenue": 5, "news": 5, "change": 4}),
    ("Assist payout explanations", {"reach": 3, "revenue": 3, "news": 4,
                                    "change": 3}),
    ("Fee change, international cards", {"reach": 3, "revenue": 4, "news": 1,
                                         "change": 5}),
    ("Dispute evidence templates", {"reach": 2, "revenue": 3, "news": 3, "change": 2}),
    ("New CSV export columns", {"reach": 2, "revenue": 1, "news": 1, "change": 1}),
]


def score(marks):
    return sum(WEIGHTS[name] * marks[name] for name in WEIGHTS)


def tier(points):
    if points >= 38:
        return 1
    return 2 if points >= 24 else 3


def main():
    print(f"{'Release':<33}{'Reach':>6}{'Rev':>5}{'News':>6}{'Change':>8}"
          f"{'Score':>7}{'Tier':>6}")
    for name, marks in RELEASES:
        points = score(marks)
        print(f"{name:<33}{marks['reach']:>6}{marks['revenue']:>5}{marks['news']:>6}"
              f"{marks['change']:>8}{points:>7}{tier(points):>6}")
    print("Maximum 50. Tier 1 is 38 or more, Tier 2 is 24 to 37, Tier 3 is the rest.")


if __name__ == "__main__":
    main()
