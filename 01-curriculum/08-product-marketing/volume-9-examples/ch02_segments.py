"""Chapter 2. Which segment should Instant Payouts go after first?"""
from payflow import INSTANT_FEE

# Beta, June 1 to July 26, 2026. 400 merchants were invited in each segment.
# Columns: segment, invited, tried it, used it 3+ times,
# monthly instant volume per repeat user ($), PayFlow merchants in the segment.
BETA = [
    ("Food and drink", 400, 168, 121, 5_200, 21_000),
    ("Trades", 400, 132, 74, 7_800, 9_000),
    ("Online and retail", 400, 61, 22, 3_100, 30_000),
]

# Lost small-merchant deals, April to June 2026, coded by main reason.
# Columns: reason, all segments, food and drink only.
LOSSES = [
    ("Payout speed", 26, 15),
    ("Price", 21, 6),
    ("Missing integration", 14, 4),
    ("No decision", 12, 4),
    ("Other", 7, 2),
]


def segment_rows():
    rows = []
    for name, invited, tried, repeat, volume, merchants in BETA:
        fee_per_invited = repeat * volume * INSTANT_FEE / invited
        rows.append({
            "name": name,
            "tried": tried / invited,          # trial rate
            "kept": repeat / tried,            # share of triers who came back
            "repeat": repeat / invited,        # repeat users per invited merchant
            "fee": fee_per_invited,            # monthly fees per invited merchant
            "potential": fee_per_invited * merchants,
        })
    return rows


def main():
    print(f"{'Segment':<19}{'Tried':>7}{'Came back':>11}{'Repeat':>8}"
          f"{'Fee/invited':>13}{'If all behaved so':>19}")
    for r in segment_rows():
        print(f"{r['name']:<19}{r['tried']:>7.1%}{r['kept']:>11.1%}"
              f"{r['repeat']:>8.1%}{r['fee']:>13.2f}{r['potential']:>19,.0f}")

    total_all = sum(row[1] for row in LOSSES)
    total_food = sum(row[2] for row in LOSSES)
    print()
    print(f"{'Loss reason':<21}{'All':>5}{'Share':>8}{'Food':>6}{'Share':>8}")
    for reason, n_all, n_food in LOSSES:
        print(f"{reason:<21}{n_all:>5}{n_all / total_all:>8.1%}"
              f"{n_food:>6}{n_food / total_food:>8.1%}")
    print(f"{'Total':<21}{total_all:>5}{'':>8}{total_food:>6}")


if __name__ == "__main__":
    main()
