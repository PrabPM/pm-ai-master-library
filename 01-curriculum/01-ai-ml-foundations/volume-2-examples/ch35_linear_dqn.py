"""Chapter 35. Deep Q-network mechanics with a tiny linear approximator.

Environment: a payment failed with a processor error. The state is the issuer's
health h (the share of that bank's payments approved in the last hour, 0 to 1)
and the attempt number (1 or 2). `now` works with chance h, `route` with 0.9.
"""
import numpy as np

ACTIONS = ["now", "route", "stop"]
GAMMA, RECOVERED = 0.9, 10.0
COST = np.array([0.2, 2.5, 0.0])


def features(h, attempt):
    """phi(s): a constant, the health, a last-attempt flag and their product."""
    last = float(attempt == 2)
    return np.array([1.0, h, last, h * last])


def step(h, attempt, a, rng):
    """Returns (reward, done). A failure at attempt 2 or a stop ends the episode."""
    if a == 2:
        return 0.0, True
    paid = rng.random() < (h if a == 0 else 0.9)
    return RECOVERED * paid - COST[a], bool(paid or attempt == 2)


def train(steps=20_000, replay=True, target_net=True, seed=35):
    rng = np.random.default_rng(seed)
    W = np.zeros((3, 4))                       # online weights, one row per action
    W_target = W.copy()                        # frozen copy used inside targets
    size, batch, lr, eps, sync = 5_000, 32, 0.05, 0.2, 500
    PHI, PHI2 = np.zeros((size, 4)), np.zeros((size, 4))
    A, REW, DONE = np.zeros(size, int), np.zeros(size), np.zeros(size)
    h, attempt = rng.random(), 1
    for t in range(steps):
        phi = features(h, attempt)
        a = int(rng.integers(3)) if rng.random() < eps else int((W @ phi).argmax())
        reward, done = step(h, attempt, a, rng)
        k = t % size                           # overwrite the oldest transition
        PHI[k], A[k], REW[k], PHI2[k], DONE[k] = phi, a, reward, features(h, 2), done
        h, attempt = (rng.random(), 1) if done else (h, 2)

        filled = min(t + 1, size)
        i = rng.integers(filled, size=batch) if replay else np.full(batch, k)
        net = W_target if target_net else W
        y = REW[i] + GAMMA * (1 - DONE[i]) * (PHI2[i] @ net.T).max(axis=1)
        error = y - (W[A[i]] * PHI[i]).sum(axis=1)             # TD errors
        np.add.at(W, A[i], lr * error[:, None] * PHI[i] / batch)
        if t % sync == 0:
            W_target = W.copy()
    return W


def exact_q(h):
    """True optimal values at health h: rows are attempts 1 and 2."""
    q2 = np.array([10 * h - 0.2, 6.5, 0.0])
    q1 = np.array([10 * h - 0.2 + GAMMA * (1 - h) * q2.max(),
                   6.5 + GAMMA * 0.1 * q2.max(), 0.0])
    return q1, q2


def switch_point(W, attempt):
    """Health above which the learned policy prefers `now` to `route`."""
    d = W[0] - W[1]
    return -(d[0] + d[2] * (attempt == 2)) / (d[1] + d[3] * (attempt == 2))


def policy_value(W):
    """Exact average return of the greedy policy over h uniform on [0, 1]."""
    total, grid = 0.0, (np.arange(2000) + 0.5) / 2000
    for h in grid:
        a2 = int((W @ features(h, 2)).argmax())
        v2 = [10 * h - 0.2, 6.5, 0.0][a2]
        a1 = int((W @ features(h, 1)).argmax())
        total += [10 * h - 0.2 + GAMMA * (1 - h) * v2, 6.5 + GAMMA * 0.1 * v2, 0.0][a1]
    return total / len(grid)


if __name__ == "__main__":
    # One semi-gradient step by hand (Worked example).
    phi = features(0.4, 1)
    w_now = np.array([2.0, 5.0, 0.0, 0.0])
    y = -0.2 + GAMMA * 5.0                      # 5.0: best next value, frozen copy
    delta = y - w_now @ phi
    w_new = w_now + 0.1 * delta * phi
    assert np.isclose(w_now @ phi, 4.0) and np.isclose(y, 4.3)
    assert np.isclose(delta, 0.3) and np.allclose(w_new, [2.03, 5.012, 0.0, 0.0])

    W = train()
    best = np.mean([max(exact_q(h)[0]) for h in (np.arange(2000) + 0.5) / 2000])
    q1, _ = exact_q(0.4)
    learned = W @ features(0.4, 1)
    print(f"Q at h = 0.4, attempt 1: learned now {learned[0]:.2f}, "
          f"route {learned[1]:.2f} | exact now {q1[0]:.2f}, route {q1[1]:.2f}")
    print(f"prefers `now` above h = {switch_point(W, 1):.2f} on attempt 1 and "
          f"{switch_point(W, 2):.2f} on attempt 2 | exact 0.35 and 0.67")
    print(f"average return: learned policy {policy_value(W):.3f}, best possible "
          f"{best:.3f}")
    for name, kw in [("without replay", dict(replay=False)),
                     ("without a target network", dict(target_net=False))]:
        print(f"average return {name}: {policy_value(train(**kw)):.3f}")

    assert np.allclose(q1[:2], [7.31, 7.085])
    assert abs((7.085 - 5.65) / 4.15 - 0.346) < 1e-3 and abs(6.7 / 10 - 0.67) < 1e-9
    assert policy_value(W) > best - 0.1
    # Answer to Q35.1: the same step with a frozen-copy value of 6.0.
    assert np.allclose(w_now + 0.1 * (-0.2 + GAMMA * 6.0 - 4.0) * phi,
                       [2.12, 5.048, 0.0, 0.0])
