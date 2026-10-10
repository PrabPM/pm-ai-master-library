"""Chapter 17: how big must a canary be to see a rare failure at least once?"""
import math

from payflow import ANSWERS_PER_TICKET, COMPLEX_TICKETS

WORKING_DAYS = 22


# [listing]
def chance_to_see(failure_rate, answers):
    """Probability that at least one failure shows up in this many answers."""
    return 1 - (1 - failure_rate) ** answers


def answers_needed(failure_rate, confidence=0.95):
    """Answers to serve before you would see a failure with this confidence."""
    return math.ceil(math.log(1 - confidence) / math.log(1 - failure_rate))
# [end listing]


def main():
    print("Chance of seeing at least one failure")
    print(f"{'Failure rate':<14}{'200 answers':>12}{'1,000':>8}{'5,000':>8}"
          f"{'Needed for 95%':>17}")
    for rate in (0.05, 0.01, 0.002, 0.0005):
        cells = "".join(f"{chance_to_see(rate, n):>{w}.0%}"
                        for n, w in ((200, 12), (1_000, 8), (5_000, 8)))
        print(f"{rate:<14.2%}{cells}{answers_needed(rate):>17,}")
    per_day = COMPLEX_TICKETS * ANSWERS_PER_TICKET / WORKING_DAYS
    need = answers_needed(0.002)
    print(f"Assist writes about {per_day:,.0f} answers a working day. "
          f"To collect {need:,}:")
    print(f"  shadow on every ticket: {math.ceil(need / per_day)} days;  "
          f"5% canary: {math.ceil(need / (per_day * 0.05))} days")


if __name__ == "__main__":
    main()
