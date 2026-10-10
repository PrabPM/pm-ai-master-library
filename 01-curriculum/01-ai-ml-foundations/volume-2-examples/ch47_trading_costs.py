"""Chapter 47. Q-learning a trading rule, with and without costs in the reward.

Synthetic market: the price sits at USD 100 plus a gap x (in cents) that drifts
back toward zero: x[t+1] = 0.9 * x[t] + noise. Trading one share costs 0.8 cents.
"""
import numpy as np

COST = 0.8                                   # cents per share traded
EDGES = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])   # six buckets for the gap x
POSITIONS = [-1, 0, 1]                       # short one share, flat, long one share
GAMMA = 0.95


def gap_path(steps, seed):
    rng = np.random.default_rng(seed)
    noise, x = rng.normal(0, 1, steps), np.zeros(steps)
    for t in range(1, steps):
        x[t] = 0.9 * x[t - 1] + noise[t]
    return x


def train(cost_in_reward, steps=200_000, seed=47):
    """Tabular Q-learning. State = (gap bucket, current position)."""
    rng = np.random.default_rng(seed)
    x = gap_path(steps, seed)
    bucket = np.digitize(x, EDGES)
    explore, random_action = rng.random(steps) < 0.1, rng.integers(3, size=steps)
    Q = np.zeros((6, 3, 3))                  # Q[bucket, position, new position]
    visits = np.zeros_like(Q)
    pos = 1                                  # index into POSITIONS: start flat
    for t in range(steps - 1):
        b = bucket[t]
        a = random_action[t] if explore[t] else int(Q[b, pos].argmax())
        reward = POSITIONS[a] * (x[t + 1] - x[t])            # profit on the move
        reward -= cost_in_reward * abs(POSITIONS[a] - POSITIONS[pos])
        visits[b, pos, a] += 1
        target = reward + GAMMA * Q[bucket[t + 1], a].max()
        Q[b, pos, a] += (target - Q[b, pos, a]) / visits[b, pos, a] ** 0.7
        pos = a
    return Q.argmax(axis=2)                  # policy[bucket, position]


def backtest(policy, steps=100_000, seed=48):
    """Run a fixed policy on a fresh path. Returns gross, cost, shares traded."""
    x = gap_path(steps, seed)
    bucket = np.digitize(x, EDGES)
    pos, gross, traded = 1, 0.0, 0
    for t in range(steps - 1):
        a = policy[bucket[t], pos]
        traded += abs(POSITIONS[a] - POSITIONS[pos])
        gross += POSITIONS[a] * (x[t + 1] - x[t])
        pos = a
    return gross, COST * traded, traded


def impact_bps(order, daily_volume, daily_vol, y=1.0):
    """Square-root law: cost in basis points of trading `order` in one day."""
    return 1e4 * y * daily_vol * np.sqrt(order / daily_volume)


if __name__ == "__main__":
    print("per 1,000 steps, in cents:  gross   costs     net   shares traded")
    results = {}
    for name, c in [("reward = profit", 0.0), ("reward = profit - costs", COST)]:
        gross, costs, traded = backtest(train(c))
        results[name] = (gross / 100, costs / 100, (gross - costs) / 100, traded / 100)
        print(f"{name:<25}" + "".join(f"{v:8.1f}" for v in results[name][:3])
              + f"{results[name][3]:10.1f}")

    block = impact_bps(100_000, 1_000_000, 0.02)
    sliced = impact_bps(10_000, 1_000_000, 0.02)
    print(f"impact of trading 10% of daily volume: {block:.1f} bps at once,",
          f"{sliced:.1f} bps in ten daily slices")
    notional, edge = 5_000_000, 40.0
    for name, cost in [("at once", block), ("sliced", sliced)]:
        print(f"USD {notional:,} order, {edge:.0f} bps edge, {name}: net "
              f"{edge - cost:+.1f} bps = USD {(edge - cost) * notional / 1e4:+,.0f}")

    naive, aware = results["reward = profit"], results["reward = profit - costs"]
    assert naive[0] > 0 > naive[2]           # a paper profit that is a real loss
    assert aware[2] > 0 and aware[3] < naive[3]
    assert np.isclose(block, 1e4 * 0.02 * np.sqrt(0.1)) and np.isclose(sliced, 20.0)
    assert np.isclose(round(block, 1), 63.2)
    # Hand example in the chapter: one shaped reward.
    assert np.isclose(1 * (0.5) - COST * abs(1 - (-1)), -1.1)
    # Answer to Q47.1: 4% of daily volume, 1.5% daily volatility.
    assert np.isclose(impact_bps(4, 100, 0.015), 30.0)
    assert np.isclose(np.sqrt(2), 1.41, atol=0.01)       # doubling size: +41% per share
