"""Chapter 32. The PayFlow retry problem written as a Markov decision process.

A card payment has failed. The state is the failure type ("net" for a processor or
network error, "funds" for insufficient funds) and the attempt number. The agent
picks one of four actions. Chapters 33, 34 and 36 import this file.
"""
import numpy as np

STATES = ["net-1", "net-2", "funds-1", "funds-2", "paid", "lost"]
ACTIONS = ["now", "later", "route", "stop"]
GAMMA = 0.9                 # discount factor
RECOVERED = 10.0            # USD kept when the payment finally succeeds
COST = [0.2, 1.0, 2.5, 0.0]                       # USD per action, same order
P_SUCCESS = {"net": [0.4, 0.5, 0.9, 0.0],         # chance each action works
             "funds": [0.1, 0.5, 0.1, 0.0]}
PAID, LOST = STATES.index("paid"), STATES.index("lost")


def build():
    """Return P[s, a, s2] (transition chances) and R[s, a] (expected reward)."""
    P = np.zeros((len(STATES), len(ACTIONS), len(STATES)))
    R = np.zeros((len(STATES), len(ACTIONS)))
    for s, name in enumerate(STATES[:4]):
        kind, attempt = name.split("-")
        after_fail = STATES.index(f"{kind}-2") if attempt == "1" else LOST
        for a, action in enumerate(ACTIONS):
            p = P_SUCCESS[kind][a]
            if action == "stop":
                after_fail = LOST
            P[s, a, PAID], P[s, a, after_fail] = p, 1 - p
            R[s, a] = RECOVERED * p - COST[a]
    P[PAID, :, PAID] = P[LOST, :, LOST] = 1.0     # terminal states absorb
    return P, R


P, R = build()
FAIL_TO = np.where(np.arange(len(STATES)) == PAID, 0.0, P).argmax(axis=2)


def step(s, a, rng):
    """Sample one transition. Returns (reward, next state)."""
    paid = rng.random() < P[s, a, PAID]
    return RECOVERED * paid - COST[a], (PAID if paid else int(FAIL_TO[s, a]))


def evaluate(policy):
    """Exact value of a fixed policy: solve V = R_pi + gamma * P_pi V."""
    idx = np.arange(len(STATES))
    P_pi, R_pi = P[idx, policy], R[idx, policy]
    return np.linalg.solve(np.eye(len(STATES)) - GAMMA * P_pi, R_pi)


def simulate(policy, start, episodes, rng):
    """Average discounted return over sampled episodes."""
    total = 0.0
    for _ in range(episodes):
        s, discount = start, 1.0
        while s not in (PAID, LOST):
            reward, s = step(s, policy[s], rng)
            total += discount * reward
            discount *= GAMMA
    return total / episodes


if __name__ == "__main__":
    assert np.allclose(P.sum(axis=2), 1.0)        # every row is a distribution
    print("expected reward right away, R[s, a]")
    print("        " + "".join(f"{a:>7}" for a in ACTIONS))
    for s in range(4):
        print(f"{STATES[s]:<8}" + "".join(f"{R[s, a]:7.2f}" for a in range(4)))

    now, later, route, stop = range(4)
    policies = {"always route": [route, route, later, later, stop, stop],
                "always now": [now, now, later, later, stop, stop],
                "now, then route": [now, route, later, later, stop, stop]}
    rng = np.random.default_rng(32)
    print("value at net-1 of three fixed policies")
    values = {}
    for name, policy in policies.items():
        values[name] = evaluate(policy)[0]
        sim = simulate(policy, 0, 100_000, rng)
        print(f"{name:<16} exact {values[name]:.3f}   simulated {sim:.3f}")
        assert abs(sim - values[name]) < 0.05

    # Checks against the hand calculation in the chapter.
    assert np.isclose(R[0, route], 6.5) and np.isclose(R[0, now], 3.8)
    assert np.isclose(values["always route"], 6.5 + 0.9 * 0.1 * 6.5)      # 7.085
    assert np.isclose(values["always now"], 3.8 + 0.9 * 0.6 * 3.8)        # 5.852
    assert np.isclose(values["now, then route"], 3.8 + 0.9 * 0.6 * 6.5)   # 7.31
    assert np.isclose(-0.2 + GAMMA * (10 - 2.5), 6.55)   # one sampled episode
    # Answers to Check yourself.
    assert np.isclose(evaluate(policies["always now"])[2], 4.0 + 0.9 * 0.5 * 4.0)
    assert np.isclose(1 / (1 - 0.99), 100) and np.isclose(1 / (1 - 0.9), 10)
