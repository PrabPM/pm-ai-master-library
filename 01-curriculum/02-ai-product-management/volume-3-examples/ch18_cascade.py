"""Chapter 18: does a cheap-model-first cascade pay? It depends on the check."""
from ch18_unit_economics import answer_cost
from payflow import AGENT_COST_PER_MIN, LARGE, SMALL, WRONG_ANSWER_MINUTES

SMALL_RIGHT = 0.81            # small model's success on the golden set
LARGE_RIGHT = 0.92            # large model's success on the same cases
LARGE_RIGHT_IF_SMALL_RIGHT = 0.98
FALSE_ALARMS = 0.10           # share of good small answers escalated anyway
SMALL_SECONDS, LARGE_SECONDS, ESCALATED_SECONDS = 3.6, 6.1, 8.8   # typical waits
WRONG_COST = WRONG_ANSWER_MINUTES * AGENT_COST_PER_MIN            # $2.10


# [listing]
def cascade(catch_rate):
    """Small model first; a check escalates doubtful answers to the large one.
    catch_rate = share of the small model's WRONG answers the check escalates."""
    small_wrong = 1 - SMALL_RIGHT
    large_right_if_small_wrong = (
        (LARGE_RIGHT - SMALL_RIGHT * LARGE_RIGHT_IF_SMALL_RIGHT) / small_wrong)
    escalated = SMALL_RIGHT * FALSE_ALARMS + small_wrong * catch_rate
    success = (SMALL_RIGHT * (1 - FALSE_ALARMS)
               + SMALL_RIGHT * FALSE_ALARMS * LARGE_RIGHT_IF_SMALL_RIGHT
               + small_wrong * catch_rate * large_right_if_small_wrong)
    ai_cost = answer_cost(model=SMALL) + escalated * answer_cost(model=LARGE)
    seconds = (1 - escalated) * SMALL_SECONDS + escalated * ESCALATED_SECONDS
    return success, ai_cost, seconds, escalated
# [end listing]


def setups():
    rows = [("Large model only", LARGE_RIGHT, answer_cost(model=LARGE),
             LARGE_SECONDS, 0.0),
            ("Small model only", SMALL_RIGHT, answer_cost(model=SMALL),
             SMALL_SECONDS, 0.0)]
    for catch in (0.50, 0.70, 0.90):
        rows.append((f"Cascade, check catches {catch:.0%}", *cascade(catch)))
    return rows


def main():
    print(f"{'Setup':<28}{'Success':>8}{'AI cost':>9}{'Plus errors':>13}"
          f"{'Wait s':>8}{'Escalated':>11}")
    for name, success, ai_cost, seconds, escalated in setups():
        with_errors = ai_cost + (1 - success) * WRONG_COST
        print(f"{name:<28}{success:>8.1%}{ai_cost:>9.4f}{with_errors:>13.3f}"
              f"{seconds:>8.1f}{escalated:>11.0%}")


if __name__ == "__main__":
    main()
