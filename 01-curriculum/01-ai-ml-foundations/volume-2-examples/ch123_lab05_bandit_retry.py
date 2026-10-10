"""Lab 5 (chapter 37): three ways to learn the best retry delay."""
import numpy as np

TRUE_RATE = np.array([0.55, 0.70, 0.62])       # retry after 1, 6 and 24 hours
ROUNDS = 3000


def run(policy, rng):
    wins, pulls = np.zeros(3), np.zeros(3)
    for t in range(ROUNDS):
        if policy == "equal split":
            arm = t % 3
        elif policy == "epsilon-greedy":
            explore = rng.random() < 0.1 or pulls.min() == 0
            arm = rng.integers(3) if explore else int(np.argmax(wins / pulls))
        else:                                   # Thompson sampling
            arm = int(np.argmax(rng.beta(1 + wins, 1 + pulls - wins)))
        pulls[arm] += 1
        wins[arm] += rng.random() < TRUE_RATE[arm]
    regret = ROUNDS * TRUE_RATE.max() - (pulls * TRUE_RATE).sum()
    return pulls, regret


if __name__ == "__main__":
    out = {}
    for policy in ("equal split", "epsilon-greedy", "Thompson sampling"):
        pulls, regret = run(policy, np.random.default_rng(8))
        out[policy] = regret
        print(f"{policy:<18} pulls {pulls.astype(int)}  "
              f"expected successes lost {regret:6.1f}")

    assert np.isclose(out["equal split"], 1000 * (0.15 + 0.0 + 0.08))
    assert out["Thompson sampling"] < out["equal split"]
    assert out["epsilon-greedy"] < out["equal split"]
