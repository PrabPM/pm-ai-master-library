"""Chapter 36. REINFORCE, baselines, an actor-critic and PPO's clipped objective."""
import numpy as np

from ch32_retry_mdp import ACTIONS, COST, GAMMA, LOST, PAID, STATES, P, R, step

NET2 = STATES.index("net-2")


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


def grad_log_pi(theta, a):
    """Gradient of log pi(a) for a softmax policy: one-hot(a) minus pi."""
    g = -softmax(theta)
    g[a] += 1.0
    return g


def actor_critic(episodes=40_000, lr_actor=0.02, lr_critic=0.01, seed=36):
    rng = np.random.default_rng(seed)
    theta = np.zeros((len(STATES), 4))        # actor: action scores per state
    V = np.zeros(len(STATES))                 # critic: one value per state
    for _ in range(episodes):
        s = 0 if rng.random() < 0.5 else 2    # start at net-1 or funds-1
        while s not in (PAID, LOST):
            a = int(rng.choice(4, p=softmax(theta[s])))
            reward, s2 = step(s, a, rng)
            delta = reward + GAMMA * V[s2] - V[s]     # TD error: better than expected?
            V[s] += lr_critic * delta                 # critic moves toward the target
            theta[s] += lr_actor * delta * grad_log_pi(theta[s], a)   # actor step
            s = s2
    return theta, V


def ppo_clip(ratio, advantage, eps=0.2):
    """One sample's term in PPO's clipped objective."""
    return min(ratio * advantage, float(np.clip(ratio, 1 - eps, 1 + eps)) * advantage)


if __name__ == "__main__":
    # REINFORCE at one state (net-2, the last attempt) under a uniform policy.
    theta = np.zeros(4)
    pi = softmax(theta)
    exact = pi * (R[NET2] - pi @ R[NET2])     # true gradient of the expected reward
    baseline = pi @ R[NET2]                   # value of the state under pi
    rng = np.random.default_rng(36)
    n = 200_000
    a = rng.choice(4, size=n, p=pi)           # sampled actions
    paid = rng.random(n) < P[NET2, a, PAID]
    G = 10.0 * paid - np.array(COST)[a]       # sampled one-step returns
    score = np.eye(4)[a] - pi                 # grad of log pi for each sample
    plain = G[:, None] * score
    with_baseline = (G - baseline)[:, None] * score
    print("gradient at net-2 for [now later route stop]")
    print("exact          ", np.round(exact, 3))
    print("REINFORCE      ", np.round(plain.mean(axis=0), 3),
          f" variance {plain.var(axis=0).sum():.1f}")
    print("with a baseline", np.round(with_baseline.mean(axis=0), 3),
          f" variance {with_baseline.var(axis=0).sum():.1f}")

    theta_ac, V_ac = actor_critic()
    picks = []
    for s in range(4):
        probs = softmax(theta_ac[s])
        picks.append(f"{STATES[s]} {ACTIONS[probs.argmax()]} {probs.max():.2f}")
    print("actor-critic, most likely action and its probability:")
    print(" | ".join(picks))
    cases = [(1.5, 2), (0.5, 2), (1.5, -2), (0.5, -2)]
    print("PPO clipped term for (ratio, advantage):")
    print("   ".join(f"({r}, {A:+d}) -> {ppo_clip(r, A):+.1f}" for r, A in cases))

    # Checks against the hand calculation in the chapter.
    assert np.allclose(pi, 0.25) and np.isclose(baseline, 3.575)
    assert np.allclose(grad_log_pi(theta, 2), [-0.25, -0.25, 0.75, -0.25])
    assert np.allclose(7.5 * grad_log_pi(theta, 2), [-1.875, -1.875, 5.625, -1.875])
    assert np.allclose((7.5 - 3.575) * grad_log_pi(theta, 2),
                       [-0.98125, -0.98125, 2.94375, -0.98125])
    assert np.allclose(exact, [0.05625, 0.10625, 0.73125, -0.89375])
    assert np.abs(plain.mean(axis=0) - exact).max() < 0.03         # both unbiased
    assert np.abs(with_baseline.mean(axis=0) - exact).max() < 0.03
    assert with_baseline.var(axis=0).sum() < plain.var(axis=0).sum()
    assert [ppo_clip(r, A) for r, A in cases] == [2.4, 1.0, -3.0, -1.6]
    best = [softmax(theta_ac[s]).argmax() for s in range(4)]
    assert [ACTIONS[b] for b in best] == ["route", "route", "later", "later"]
    # Answer to Q36.1: the sampled action is `stop`, so G = 0.
    assert np.allclose((0 - 3.575) * grad_log_pi(theta, 3),
                       [0.89375, 0.89375, 0.89375, -2.68125])
