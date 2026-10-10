"""Checks for the small sums quoted in the book's prose, labs and answers."""
from datetime import date

import ch02_segments as ch02
import ch13_channels as ch13
import ch21_attribution as ch21
from payflow import INSTANT_FEE, TYPICAL_CONTRIBUTION, TYPICAL_FEES

checks = []


def check(label, condition):
    assert condition, label
    checks.append(label)


def close(a, b, tolerance=0.005):
    return abs(a - b) <= tolerance


# Meet PayFlow and Chapter 1
check("beta payouts later than 30 minutes", 4_960 - 4_832 == 128)
check("fee on $1,850", close(1_850 * INSTANT_FEE, 18.50))
check("amount received", close(1_850 - 18.50, 1_831.50))
# Chapter 2 and Chapter 19
check("beta merchants who tried it", sum(row[2] for row in ch02.BETA) == 361)
check("beta repeat users", sum(row[3] for row in ch02.BETA) == 217)
check("beta invitees", sum(row[1] for row in ch02.BETA) == 1_200)
check("small merchants", sum(row[5] for row in ch02.BETA) == 60_000)
check("food and drink triers who came back", round(121 / 168 * 100) == 72)
# Chapter 5
check("the slide's 'up 33%'", round((0.12 / 0.09 - 1) * 100) == 33)
# Chapter 9 dates
weekday = {date(2026, 11, 3): 1, date(2026, 11, 10): 1, date(2026, 11, 17): 1,
           date(2026, 11, 13): 4, date(2026, 11, 16): 0, date(2026, 11, 18): 2,
           date(2026, 10, 3): 5, date(2026, 10, 4): 6, date(2026, 11, 6): 4,
           date(2026, 10, 13): 1, date(2026, 12, 15): 1, date(2027, 2, 2): 1,
           date(2027, 2, 9): 1, date(2027, 2, 16): 1}
check("weekdays of the dated events", all(d.weekday() == w for d, w in weekday.items()))
check("timeline is nine weeks",
      (date(2026, 12, 15) - date(2026, 10, 13)).days == 63)
check("four weeks after launch", (date(2026, 12, 15) - date(2026, 11, 17)).days == 28)
check("beta lasted eight weeks", (date(2026, 7, 26) - date(2026, 6, 1)).days + 1 == 56)
check("lift test lasted four weeks",
      (date(2026, 9, 27) - date(2026, 8, 31)).days + 1 == 28)
# Chapters 12 and 13
check("bookkeeper bounties fit the spend", 120 * 150 <= 24_000)
budget = [45_000, 36_000, 30_000, 18_000, 18_000, 15_000, 18_000]
check("launch budget adds up", sum(budget) == 180_000)
check("reserve is a tenth", 18_000 / 180_000 == 0.10)
cacs = {name: spend / merchants for name, spend, merchants, _ in ch13.CHANNELS}
check("CAC range", round(min(cacs.values())) == 47 and max(cacs.values()) == 700)
check("sales CAC is three times search", cacs["Sales team"] == 3 * cacs["Paid search"])
# Chapter 17
check("cents kept per fee dollar",
      round(TYPICAL_CONTRIBUTION / TYPICAL_FEES, 3) == 0.274)
check("Q17.1", close(500_000 * 0.02 * 1.80, 18_000))
check("Q17.2", close(1 / 0.40, 2.5))
# Chapter 19
check("nudged group rate", close(252 / 1_800, 0.14))
check("holdout group rate", close(16 / 200, 0.08))
check("holdout is a tenth", 200 / 2_000 == 0.10)
check("Q19.2", round(0.06 * 1_800) == 108)
check("Sunday message fee", close(2_140 * INSTANT_FEE, 21.40))
ice = {(8, 7, 6): 7.0, (6, 6, 8): 6.7, (5, 5, 9): 6.3, (7, 6, 3): 5.3}
check("ICE averages", all(round(sum(k) / 3, 1) == v for k, v in ice.items()))
# Chapter 21
(n1, k1), (n0, k0) = ch21.SAW_ADS, ch21.HELD_OUT
check("activation rates in the lift test",
      round(k1 / n1 * 100, 2) == 0.19 and round(k0 / n0 * 100, 2) == 0.13)
check("a fifth held out", n0 / (n0 + n1) == 0.2)
check("eleven journey patterns", len(ch21.JOURNEYS) == 11)
check("other patterns", sum(m for _, m in ch21.JOURNEYS) - 110 - 120 - 250 == 520)
check("social then search", ch21.JOURNEYS[0] == (["Paid social", "Paid search"], 110))
# Chapter 22
check("eval adds up", 188 + 9 + 3 == 200 and 188 / 200 == 0.94)
# Labs, cases, answers and templates
check("Lab 1 hours", 30 * 25 / 60 == 12.5)
check("Lab 4 price given away", close(1 - 240 / 400, 0.40))
check("Lab 4 margin given away", round((260 - 100) / 260 * 100) == 62)
check("Lab 4 saving", 400 - 310 == 90)
check("Lab 6 four in five", round((1 - 45 / 230) * 100) == 80)
check("Lab 7 extra fee", close(2_000 * (0.015 - 0.010), 10.00))
check("Case 3 repeat rate", round(1_881 / 3_420 * 100) == 55)
check("Q8.1", close(800 * INSTANT_FEE, 8) and close(20_000 * INSTANT_FEE, 200))
check("Q8.3", close(0.8 / 1.0, 0.80))
check("Q14.2", 9_000 / 12 == 750 and round(800 / 90) == 9)
check("Template 2 fee", close(900 * INSTANT_FEE, 9.00))

print(f"All {len(checks)} prose checks passed.")
