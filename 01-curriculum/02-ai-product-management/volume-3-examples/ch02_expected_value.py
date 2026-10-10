"""Chapter 2: expected monthly value of four ways to do the same job."""
from payflow import COMPLEX_TICKETS, SIMPLE_TICKETS

# [listing]
def expected_value(tickets, reach, p_right, gain, harm, fixed):
    """Dollars per month: gains when right, minus harm when wrong, minus fixed."""
    handled = tickets * reach
    return handled * (p_right * gain - (1 - p_right) * harm) - fixed


def break_even_accuracy(tickets, reach, gain, harm, fixed):
    """The share of right outcomes at which the option earns exactly nothing."""
    return (fixed / (tickets * reach) + harm) / (gain + harm)


SIMPLE, COMPLEX = SIMPLE_TICKETS, COMPLEX_TICKETS      # 3,200 and 4,800 a month
OPTIONS = [  # name, tickets, reach, p(right), gain, harm, fixed cost per month
    ("A  Reason codes on the payout page", SIMPLE, 0.70, 0.98, 5.60, 5.60, 1_500),
    ("B  Search over help articles", COMPLEX, 0.85, 0.60, 2.10, 0.70, 2_000),
    ("C  Assist drafts a cited answer", COMPLEX, 0.85, 0.92, 4.20, 2.10, 4_500),
    ("D  Agent answers and retries alone", COMPLEX, 0.60, 0.85, 12.60, 95.00, 9_000),
]
# [end listing]


def main():
    print(f"{'Option':<38}{'EV per month':>13}{'Break-even accuracy':>21}")
    for name, tickets, reach, p_right, gain, harm, fixed in OPTIONS:
        ev = expected_value(tickets, reach, p_right, gain, harm, fixed)
        be = break_even_accuracy(tickets, reach, gain, harm, fixed)
        print(f"{name:<38}{ev:>13,.0f}{be:>20.0%}")


if __name__ == "__main__":
    main()
