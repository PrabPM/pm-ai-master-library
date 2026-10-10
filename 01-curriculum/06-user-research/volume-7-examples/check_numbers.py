"""Checks that the PayFlow numbers used across the book agree with each other."""
from ch10_funnel import STEPS
from ch11_margin_of_error import ANSWERS, POPULATION
from ch12_nps import COUNTS
from ch13_tickets import STARTS_THIS_WEEK, TICKETS
from ch14_segments import BY_INDUSTRY, BY_OWNERS_AND_DEVICE
from lab4_weighting import PICKED, RESPONDENTS

started, approved = STEPS[0][1], STEPS[-1][1]
assert (started, approved) == (2000, 1160) and STARTS_THIS_WEEK == started
assert approved / started == 0.58
for split in (BY_INDUSTRY, BY_OWNERS_AND_DEVICE):
    assert sum(s for s, _ in split.values()) == started
    assert sum(f for _, f in split.values()) == approved
phone_lost = sum(s - f for k, (s, f) in BY_OWNERS_AND_DEVICE.items()
                 if "phone" in k)
assert phone_lost == 564 and started - approved == 840
assert POPULATION == 4 * (started - approved)
assert sum(ANSWERS.values()) == 216 == sum(RESPONDENTS.values())
assert sum(PICKED["No document to hand"].values()) == 78
assert sum(PICKED["Did not understand a question"].values()) == 41
assert sum(PICKED["Lost my progress"].values()) == 32
assert sum(PICKED["Taking too long"].values()) == 11
assert sum(COUNTS.values()) == 180
assert 18 + 63 == COUNTS[9] + COUNTS[10]
assert 24 + 21 == sum(COUNTS[s] for s in range(7))
assert sum(TICKETS.values()) == 340
print("all cross-checks passed")
