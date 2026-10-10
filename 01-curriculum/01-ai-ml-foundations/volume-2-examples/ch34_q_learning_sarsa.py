"""Chapter 34. Q-learning and SARSA learn the retry problem from samples.

Both learners act epsilon-greedily with epsilon = 0.3 and never see P or R.
"""
import numpy as np

from ch32_retry_mdp import ACTIONS, GAMMA, LOST, PAID, STATES, P, R, step

EPSILON = 0.3
NET1, NET2, FUNDS1, FUNDS2 = range(4)


def choose(Q, s, rng):
    """Epsilon-greedy: explore with chance EPSILON, otherwise take the best."""
    if rng.random() < EPSILON:
        return int(rng.integers(len(ACTIONS)))
    return int(Q[s].argmax())


def learn(method, episodes=100_000, seed=34, trace=None):
    rng = np.random.default_rng(seed)
    Q = np.zeros((len(STATES), len(ACTIONS)))     # terminal rows stay at zero
    visits = np.zeros_like(Q)
    for episode in range(episodes):
        s = NET1 if rng.random() < 0.5 else FUNDS1
        a = choose(Q, s, rng)
        while s not in (PAID, LOST):
            reward, s2 = step(s, a, rng)
            a2 = choose(Q, s2, rng)               # the action taken next
            if method == "q-learning":
                target = reward + GAMMA * Q[s2].max()
            else:                                 # sarsa
                target = reward + GAMMA * Q[s2, a2]
            visits[s, a] += 1
            alpha = 1 / visits[s, a]              # running average of targets
            Q[s, a] += alpha * (target - Q[s, a])
            s, a = s2, a2
        if trace is not None and episode % 500 == 0:
            trace.append(Q[NET1, 0] - Q[NET1, 2])
    return Q


# Exact targets. Q* comes from value iteration (Chapter 33). Q_eps is the value
# of acting epsilon-greedily for ever: the next state is worth a blend of its
# best action and the average action.
Q_star = np.zeros_like(R)
Q_eps = np.zeros_like(R)
for _ in range(5):
    Q_star = R + GAMMA * P @ Q_star.max(axis=1)
    blend = (1 - EPSILON) * Q_eps.max(axis=1) + EPSILON * Q_eps.mean(axis=1)
    Q_eps = R + GAMMA * P @ blend

if __name__ == "__main__":
    Q_q, Q_s = learn("q-learning"), learn("sarsa")
    print("action values at net-1    now  later  route   stop   picks")
    rows = [("optimal, exact", Q_star), ("Q-learning", Q_q),
            ("epsilon-greedy, exact", Q_eps), ("SARSA", Q_s)]
    for name, Q in rows:
        values = "".join(f"{q:7.2f}" for q in Q[NET1])
        print(f"{name:<23}{values}   {ACTIONS[Q[NET1].argmax()]}")

    # One update by hand: at net-1 the agent tried `now`, it failed (reward -0.2),
    # it landed in net-2 and its next action there happened to be `stop`.
    q_old, alpha, reward = 7.0, 0.1, -0.2
    q_next = np.array([3.8, 4.0, 6.5, 0.0])       # current estimates at net-2
    q_learning_new = q_old + alpha * (reward + GAMMA * q_next.max() - q_old)
    sarsa_new = q_old + alpha * (reward + GAMMA * q_next[3] - q_old)
    print(f"hand update: Q-learning {q_learning_new:.3f}, SARSA {sarsa_new:.3f}")

    assert np.isclose(q_learning_new, 6.865) and np.isclose(sarsa_new, 6.28)
    assert np.allclose(Q_star[NET1], [7.31, 6.925, 7.085, 0.0])
    assert np.allclose(Q_eps[NET2], R[NET2])
    assert np.isclose(0.7 * 6.5 + 0.3 * (3.8 + 4.0 + 6.5 + 0.0) / 4, 5.6225)
    assert np.allclose(Q_eps[NET1, [0, 2]], [3.8 + 0.54 * 5.6225, 6.5 + 0.09 * 5.6225])
    assert np.abs(Q_q[NET1] - Q_star[NET1]).max() < 0.08   # Q-learning finds Q*
    assert np.abs(Q_s[NET1] - Q_eps[NET1]).max() < 0.08    # SARSA finds its own
    assert ACTIONS[Q_q[NET1].argmax()] == "now"
    assert ACTIONS[Q_s[NET1].argmax()] == "route"
