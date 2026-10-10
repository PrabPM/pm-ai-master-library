"""Chapter 33. Bellman backups and value iteration on the retry problem."""
import numpy as np

from ch32_retry_mdp import ACTIONS, GAMMA, STATES, P, R, evaluate

V = np.zeros(len(STATES))
for sweep in range(1, 100):
    Q = R + GAMMA * P @ V              # one Bellman backup for every (s, a)
    V_new = Q.max(axis=1)              # act greedily in every state
    change = np.abs(V_new - V).max()
    print(f"sweep {sweep}: V = {np.round(V_new[:4], 3)}  largest change {change:.3f}")
    V = V_new
    if change < 1e-9:
        break

policy = Q.argmax(axis=1)
print("optimal action values Q*[s, a]")
print("        " + "".join(f"{a:>7}" for a in ACTIONS))
for s in range(4):
    row = "".join(f"{Q[s, a]:7.3f}" for a in range(4))
    print(f"{STATES[s]:<8}{row}   best: {ACTIONS[policy[s]]}")

# Checks against the two hand sweeps in the chapter.
assert np.allclose(R[0], [3.8, 4.0, 6.5, 0.0])
assert np.allclose(R[2], [0.8, 4.0, -1.5, 0.0])
assert np.allclose(V[:4], [7.31, 6.5, 5.8, 4.0])
assert np.allclose(Q[0], [3.8 + 0.9 * 0.6 * 6.5, 4.0 + 0.9 * 0.5 * 6.5,
                          6.5 + 0.9 * 0.1 * 6.5, 0.0])
assert np.allclose(Q[2], [0.8 + 0.9 * 0.9 * 4.0, 4.0 + 0.9 * 0.5 * 4.0,
                          -1.5 + 0.9 * 0.9 * 4.0, 0.0])
assert [ACTIONS[a] for a in policy[:4]] == ["now", "route", "later", "later"]
assert sweep == 3
# The Bellman expectation equation holds for the optimal policy.
assert np.allclose(evaluate(policy), V)
# The greedy-on-immediate-reward policy is worse at net-1.
myopic = R.argmax(axis=1)
assert ACTIONS[myopic[0]] == "route" and np.isclose(evaluate(myopic)[0], 7.085)

# Answers to Check yourself.
R2 = R.copy()
R2[:2, 2] = 10 * 0.9 - 2.0                          # Q33.2: route costs USD 2.00
V2 = np.zeros(6)
for _ in range(5):
    Q2 = R2 + GAMMA * P @ V2
    V2 = Q2.max(axis=1)
assert ACTIONS[Q2[0].argmax()] == "route" and np.isclose(Q2[0, 2], 7.63)
assert np.isclose(Q2[0, 0], 3.8 + 0.54 * 7.0)       # now is worth 7.58
