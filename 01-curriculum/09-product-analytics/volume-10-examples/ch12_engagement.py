"""Chapter 12: DAU, WAU, MAU, stickiness and the L28 histogram.

Simulates which of 28 days (Tue 1 Sep to Mon 28 Sep 2026) each small merchant
took at least one successful payment. "Active" means paid, not logged in.
"""
import numpy as np

rng = np.random.default_rng(12)
DAYS = 28
weekday = np.array([(1 + d) % 7 for d in range(DAYS)])    # 0 = Monday

# four kinds of merchant: (share, chance of trading on a weekday, on a weekend,
#                           payments on a day it trades)
KINDS = {"daily shop": (0.34, 0.92, 0.62, 14),
         "part-time shop": (0.13, 0.50, 0.35, 10),
         "weekly invoicer": (0.30, 0.22, 0.03, 9),
         "occasional seller": (0.23, 0.05, 0.05, 4)}
N = 10_400

active = np.zeros((N, DAYS), dtype=bool)
payments = np.zeros(N)
kinds = rng.choice(len(KINDS), size=N, p=[k[0] for k in KINDS.values()])
for i, (share, p_week, p_weekend, per_day) in enumerate(KINDS.values()):
    idx = np.where(kinds == i)[0]
    p = np.where(weekday < 5, p_week, p_weekend)
    active[idx] = rng.random((len(idx), DAYS)) < p
    payments[idx] = active[idx].sum(axis=1) * per_day

days_active = active.sum(axis=1)
is_mau = days_active > 0                     # active at least once in 28 days
mau = int(is_mau.sum())
dau = active.sum(axis=0).mean()              # average merchants active per day
wau = np.mean([active[:, w * 7:(w + 1) * 7].any(axis=1).sum() for w in range(4)])
histogram = np.bincount(days_active[is_mau], minlength=DAYS + 1)[1:]

if __name__ == "__main__":
    print(f"MAU (28 days) {mau:,}   WAU {wau:,.0f}   DAU {dau:,.0f}")
    print(f"Stickiness DAU/MAU = {dau / mau:.0%}   WAU/MAU = {wau / mau:.0%}")
    print()
    print(f"{'days active of 28':<20}{'merchants':>10}{'share':>8}"
          f"{'share of payments':>20}")
    for lo, hi in [(1, 1), (2, 4), (5, 9), (10, 19), (20, 28)]:
        pick = (days_active >= lo) & (days_active <= hi)
        label = f"{lo}" if lo == hi else f"{lo}-{hi}"
        print(f"{label:<20}{pick.sum():>10,}{pick.sum() / mau:>8.0%}"
              f"{payments[pick].sum() / payments.sum():>20.0%}")
    print()
    print(f"Mean days active {days_active[is_mau].mean():.1f}, "
          f"median {np.median(days_active[is_mau]):.0f}")
