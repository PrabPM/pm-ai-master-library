"""Chapter 45. Labels, a leaky feature, and walk-forward validation.

The price is a seeded random walk: tomorrow's direction is a coin flip, so an
honest model cannot beat 50% accuracy. Any score far above that is leakage.
"""
import numpy as np


def fixed_horizon_label(price, t, h):
    """+1 if the price is higher h days after day t, else -1."""
    return 1 if price[t + h] > price[t] else -1


def triple_barrier_label(price, t, up, down, horizon):
    """+1 or -1 for the first barrier touched, 0 if time runs out first."""
    for day in range(t + 1, t + horizon + 1):
        move = price[day] / price[t] - 1
        if move >= up:
            return 1, day
        if move <= -down:
            return -1, day
    return 0, t + horizon


def build_table(price, as_of_day_t):
    """Features for days 1..n-2 and the label 'price is higher tomorrow'."""
    t = np.arange(1, len(price) - 1)
    today_return = price[t] / price[t - 1] - 1
    if as_of_day_t:                             # only data that exists on day t
        smooth = (price[t - 1] + price[t]) / 2
    else:                                       # centered average: uses day t + 1
        smooth = (price[t - 1] + price[t] + price[t + 1]) / 3
    X = np.column_stack([np.ones(len(t)), today_return, smooth / price[t] - 1])
    y = (price[t + 1] > price[t]).astype(float)
    return X, y


def accuracy(X, y, train, test):
    """Fit a linear model on the train rows, score direction on the test rows."""
    w, *_ = np.linalg.lstsq(X[train], y[train], rcond=None)
    return np.mean((X[test] @ w > 0.5) == (y[test] == 1))


def walk_forward(n, folds=5, first_train=500, gap=1):
    """Train on everything before a block, skip `gap` rows, test on the block."""
    size = (n - first_train) // folds
    for k in range(folds):
        start = first_train + k * size
        yield np.arange(0, start - gap), np.arange(start, start + size)


if __name__ == "__main__":
    tiny = np.array([100.0, 101, 99, 102, 104, 103])
    fixed = fixed_horizon_label(tiny, 0, 2)
    barrier, day = triple_barrier_label(tiny, 0, up=0.025, down=0.025, horizon=5)
    print(f"fixed-horizon label {fixed:+d} | triple-barrier label {barrier:+d}",
          f"(barrier touched on day {day})")

    rng = np.random.default_rng(45)
    price = 100 * np.cumprod(1 + rng.normal(0, 0.01, 1500))
    X_leaky, y = build_table(price, as_of_day_t=False)
    X_honest, _ = build_table(price, as_of_day_t=True)
    n = len(y)
    shuffled = rng.permutation(n)
    cut = int(0.7 * n)
    random_split = accuracy(X_leaky, y, shuffled[:cut], shuffled[cut:])
    wf_leaky = np.mean([accuracy(X_leaky, y, tr, te) for tr, te in walk_forward(n)])
    wf_honest = np.mean([accuracy(X_honest, y, tr, te) for tr, te in walk_forward(n)])
    print("accuracy at predicting tomorrow's direction of a random walk")
    print(f"random 70/30 split, features built once on all data  {random_split:.2f}")
    print(f"walk-forward split, features built once on all data  {wf_leaky:.2f}")
    print(f"walk-forward, features rebuilt as of each day        {wf_honest:.2f}")
    folds = list(walk_forward(n))

    # Checks against the chapter.
    assert fixed == -1 and (barrier, day) == (1, 4)
    assert random_split > 0.95 and wf_leaky > 0.95 and abs(wf_honest - 0.5) < 0.05
    assert all(tr[-1] < te[0] - 1 for tr, te in folds)       # the gap is respected
    assert (folds[0][0][-1], folds[0][1][0], folds[0][1][-1]) == (498, 500, 698)
    # The leak, exactly: 3 * (smooth - p_t) + (p_t - p_{t-1}) = p_{t+1} - p_t.
    t = np.arange(1, len(price) - 1)
    smooth = (price[t - 1] + price[t] + price[t + 1]) / 3
    assert np.allclose(3 * (smooth - price[t]) + price[t] - price[t - 1],
                       price[t + 1] - price[t])
    # Check yourself: with a 5-day label, 5 rows before each test block are purged.
    assert all(len(tr) == te[0] - 5 for tr, te in walk_forward(n, gap=5))
