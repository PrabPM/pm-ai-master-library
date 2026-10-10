"""Chapter 4: how many participants does it take to see a problem at least once?

Model from Nielsen and Landauer (1993). L is the chance that one participant
runs into a given problem. The share seen at least once by n people is
1 - (1 - L) ** n.
"""
import math

RATES = (0.31, 0.10, 0.05)
SIZES = (5, 10, 15, 20)


def pct(share):
    return ">99%" if share > 0.995 else f"{share:.0%}"


print("chance one person      seen at least once by n people     n needed")
print("hits the problem          5      10      15      20        for 85%")
for L in RATES:
    seen = "".join(f"{pct(1 - (1 - L) ** n):>8}" for n in SIZES)
    needed = math.ceil(math.log(1 - 0.85) / math.log(1 - L))
    print(f"{L:>16.0%}   {seen}   {needed:>12}")
