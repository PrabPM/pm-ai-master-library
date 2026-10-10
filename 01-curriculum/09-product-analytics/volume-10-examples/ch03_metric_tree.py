"""Chapter 3: split a change in the North Star across the branches of its tree.

Weekly volume = active merchants x attempts per merchant x success rate
                x average payment
Because the tree multiplies, the logs of the ratios add up exactly.
"""
from math import log

last_week = {"active merchants": 9_000, "attempts per merchant": 43.5,
             "success rate": 0.920, "average payment": 50.00}
this_week = {"active merchants": 8_980, "attempts per merchant": 43.4,
             "success rate": 0.831, "average payment": 49.90}


def volume(week):
    v = 1.0
    for value in week.values():
        v *= value
    return v


def decompose(before, after):
    total = log(volume(after) / volume(before))
    return [(name, after[name] / before[name] - 1,
             log(after[name] / before[name]) / total) for name in before]


if __name__ == "__main__":
    v0, v1 = volume(last_week), volume(this_week)
    print(f"Last week ${v0:,.0f}   this week ${v1:,.0f}   change {v1 / v0 - 1:+.1%}")
    print(f"{'input':<24}{'change':>8}{'share of the drop':>20}")
    for name, change, share in decompose(last_week, this_week):
        print(f"{name:<24}{change:>+8.1%}{share:>20.0%}")
