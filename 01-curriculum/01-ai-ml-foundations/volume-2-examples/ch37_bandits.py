"""Chapter 37. Three bandit algorithms on a three-offer problem.

PayFlow shows each merchant who opens the dashboard one of three upgrade offers.
The acceptance rates below are the hidden truth; the algorithms only see clicks.
"""
import numpy as np

TRUE_RATE = np.array([0.10, 0.12, 0.16])      # offers A, B, C
BEST = TRUE_RATE.max()
ROUNDS, RUNS = 10_000, 10


def epsilon_greedy(t, shown, accepted, rng, eps=0.1):
    if rng.random() < eps:
        return int(rng.integers(3))
    return int(np.argmax(accepted / np.maximum(shown, 1)))


def ucb1(t, shown, accepted, rng):
    if t <= 3:                                # show every offer once
        return t - 1
    bonus = np.sqrt(2 * np.log(t) / shown)    # wide when an offer is rarely shown
    return int(np.argmax(accepted / shown + bonus))


def thompson(t, shown, accepted, rng):
    draws = rng.beta(1 + accepted, 1 + shown - accepted)   # one sample per offer
    return int(np.argmax(draws))


def ab_test(t, shown, accepted, rng, test_rounds=3_000):
    if t <= test_rounds:                      # equal split, then commit
        return (t - 1) % 3
    return int(np.argmax(accepted / shown))


def run(policy, seed):
    """Cumulative regret after each round of one simulated run."""
    rng = np.random.default_rng(seed)
    shown, accepted = np.zeros(3), np.zeros(3)
    regret = np.zeros(ROUNDS)
    for t in range(1, ROUNDS + 1):
        k = policy(t, shown, accepted, rng)
        shown[k] += 1
        accepted[k] += rng.random() < TRUE_RATE[k]
        regret[t - 1] = BEST - TRUE_RATE[k]   # expected loss from this choice
    return regret.cumsum(), shown


POLICIES = {"epsilon-greedy (0.1)": epsilon_greedy, "UCB1": ucb1,
            "Thompson sampling": thompson, "A/B test, then commit": ab_test}


def experiment():
    curves, shares = {}, {}
    for name, policy in POLICIES.items():
        results = [run(policy, seed) for seed in range(RUNS)]
        curves[name] = np.mean([r for r, _ in results], axis=0)
        shares[name] = np.mean([s[2] for _, s in results]) / ROUNDS
    return curves, shares


if __name__ == "__main__":
    # Hand example 1: UCB1 scores at round t = 100.
    shown, accepted = np.array([20, 30, 50]), np.array([2, 3, 8])
    scores = accepted / shown + np.sqrt(2 * np.log(100) / shown)
    print("UCB1 scores at t = 100:", np.round(scores, 3))
    # Hand example 2: Thompson's belief about offer C after 8 accepts in 50.
    a, b = 1 + 8, 1 + 50 - 8
    print(f"posterior for C: Beta({a}, {b}), mean {a / (a + b):.3f}")

    curves, shares = experiment()
    print(f"mean of {RUNS} runs     regret at 3,000   regret at 10,000   share on C")
    for name in POLICIES:
        c = curves[name]
        print(f"{name:<22}{c[2999]:14.1f}{c[-1]:19.1f}{shares[name]:13.2f}")

    assert np.allclose(scores, [0.1 + np.sqrt(2 * np.log(100) / 20),
                                0.1 + np.sqrt(2 * np.log(100) / 30),
                                0.16 + np.sqrt(2 * np.log(100) / 50)])
    assert np.allclose(np.round(scores, 3), [0.779, 0.654, 0.589])
    assert (a, b) == (9, 43) and np.isclose(a / (a + b), 9 / 52)
    # The equal split loses (0.06 + 0.04 + 0) / 3 per merchant: 100 over 3,000.
    assert np.isclose(curves["A/B test, then commit"][2999], 100.0)
    assert curves["Thompson sampling"][-1] < curves["A/B test, then commit"][-1]
    # Answers to Check yourself.
    assert np.isclose(round(12 / 80 + np.sqrt(2 * np.log(200) / 80), 3), 0.514)
    assert np.isclose(6000 * (0.06 + 0.04 + 0.0) / 3, 200.0)
