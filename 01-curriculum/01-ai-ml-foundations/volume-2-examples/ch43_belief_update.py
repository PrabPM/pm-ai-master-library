"""Chapter 43. Belief updates and an information-gathering action.

Hidden state of one PayFlow payment: legitimate or fraud. PayFlow never sees the
state, only signals: whether the device is new, and whether a challenge passes.
"""
import numpy as np

STATES = ["legit", "fraud"]
T = np.eye(2)                                   # the state does not change mid-payment
O = {"new device": np.array([0.10, 0.60]),      # P(observation | legit), (| fraud)
     "known device": np.array([0.90, 0.40]),
     "challenge passed": np.array([0.95, 0.20]),
     "challenge failed": np.array([0.05, 0.80])}
COST_FRAUD, COST_DECLINE, COST_CHALLENGE = 100.0, 15.0, 5.0   # USD


def update(belief, observation):
    """b'(s') = eta * O(o | s') * sum_s T(s' | s) b(s)."""
    predicted = belief @ T                      # predict: where the state may be now
    unnormalized = O[observation] * predicted   # correct: weigh by the evidence
    return unnormalized / unnormalized.sum()    # eta makes it sum to 1


def act_now(belief):
    """Expected value of the two final actions, and the better one."""
    approve = -belief[1] * COST_FRAUD           # lose the amount if it is fraud
    decline = -belief[0] * COST_DECLINE         # lose a good sale if it is legit
    return approve, decline, max(approve, decline)


def challenge(belief):
    """Pay for the challenge, see its result, then take the better final action."""
    value = -COST_CHALLENGE
    for outcome in ("challenge passed", "challenge failed"):
        chance = O[outcome] @ belief            # P(outcome) under the belief
        value += chance * act_now(update(belief, outcome))[2]
    return value


if __name__ == "__main__":
    prior = np.array([0.96, 0.04])
    b1 = update(prior, "new device")
    b2 = update(b1, "challenge passed")
    b3 = update(b1, "challenge failed")
    print(f"prior P(fraud) = {prior[1]:.2f}")
    print(f"after a new device      P(fraud) = {b1[1]:.2f}")
    print(f"then challenge passed   P(fraud) = {b2[1]:.2f}")
    print(f"or challenge failed     P(fraud) = {b3[1]:.2f}")
    print("expected value (USD) of each action")
    best = []
    for p in (0.04, 0.20, 0.80):
        b = np.array([1 - p, p])
        approve, decline, _ = act_now(b)
        values = {"approve": approve, "decline": decline, "challenge": challenge(b)}
        best.append(max(values, key=values.get))
        print(f"P(fraud) = {p:.2f}: " + "  ".join(f"{k} {v:6.2f}"
                                                 for k, v in values.items())
              + f"  -> {best[-1]}")

    # Checks against the hand calculation in the chapter.
    assert np.isclose(b1[1], 0.024 / (0.024 + 0.096)) and np.isclose(b1[1], 0.20)
    assert np.isclose(b2[1], 0.04 / 0.80) and np.isclose(b3[1], 0.16 / 0.20)
    assert np.isclose(O["challenge passed"] @ b1, 0.80)
    assert np.isclose(challenge(b1), -5 + 0.8 * (-5) + 0.2 * (-3))        # -9.6
    assert best == ["approve", "challenge", "decline"]
    # The order of two independent signals does not change the final belief.
    alt = update(update(prior, "challenge passed"), "new device")
    assert np.allclose(alt, b2)
    # Check yourself: a known device lowers the belief below the prior.
    assert np.isclose(update(prior, "known device")[1], 0.016 / (0.016 + 0.864))
    high = np.array([0.20, 0.80])                   # Q43.2: a pass leaves 0.457
    assert np.isclose(update(high, "challenge passed")[1], 0.16 / 0.35)
    assert np.isclose(challenge(high), -8.0) and np.isclose(act_now(high)[1], -3.0)
