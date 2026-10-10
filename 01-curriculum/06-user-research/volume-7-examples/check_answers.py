"""Checks the arithmetic quoted in the book's prose and in its answers."""
from ch09_sus import sus_score
from ch09_task_success_interval import adjusted_wald
from ch11_margin_of_error import ANSWERS, POPULATION, margin
from ch12_nps import nps

assert sus_score([5, 1, 5, 2, 4, 1, 5, 1, 4, 2]) == 90.0             # Q9.1
low, high = adjusted_wald(4, 5)
assert (round(low * 100), round(high * 100)) == (36, 98)             # Q9.2
assert round(margin(0.3, 100), 2) == 0.09                            # Q11.2
assert round(nps(90, 70, 40)[0]) == 25                               # Q12.1
assert 400 / 10_000 * 1000 == 40 and round(480 / 13_000 * 1000) == 37  # Q13.1
assert round((0.8 - 0.5) / (1 - 0.5), 1) == 0.6                      # Q15.2

n = sum(ANSWERS.values())


def span(key):
    p = ANSWERS[key] / n
    m = margin(p, n, POPULATION)
    return round((p - m) * 100), round((p + m) * 100)


# Ranges quoted in Chapters 11 and 20.
assert span("Did not have a document or number to hand") == (30, 42)
assert span("Did not understand a question") == (14, 24)
assert span("It was taking too long") == (2, 8)
assert 78 / n - 41 / n > 0.17                                        # the 17-point gap
assert 280 + 290 == 570 and 2000 - 1160 == 840                       # funnel prose
assert 400 - 61 == 339 and 300 - 212 == 88 and 60 - 48 == 12         # counts in prose
print("all answer checks passed")
