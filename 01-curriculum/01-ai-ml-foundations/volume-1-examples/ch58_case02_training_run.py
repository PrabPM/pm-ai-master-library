"""Chapter 58, Case 2: a training run that will not converge."""
import numpy as np

rng = np.random.default_rng(582)
n = 2000
amount = rng.gamma(2.0, 150.0, n)                  # payment amount, USD
card_age = rng.uniform(0, 10, n)                   # years since the card was added
logit = -1.0 + 0.004 * amount - 0.35 * card_age
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(float)   # 1 = disputed


def with_bias(*columns):
    return np.column_stack([np.ones(n), *columns])


def loss_and_grad(w, X):
    z = np.clip(X @ w, -500, 500)
    p = 1 / (1 + np.exp(-z))
    eps = 1e-12
    loss = -np.mean(y * np.log(p + eps) + (1 - y) * np.log(1 - p + eps))
    return loss, X.T @ (p - y) / n


def train(X, eta, steps=200):
    w = np.zeros(X.shape[1])
    history = []
    for _ in range(steps):
        loss, grad = loss_and_grad(w, X)
        history.append(loss)
        w = w - eta * grad
    return np.array(history)


def curvature(X):
    """Eigenvalues of the largest Hessian the logistic loss can have here."""
    eig = np.linalg.eigvalsh(X.T @ X / (4 * n))
    return eig.max(), eig.max() / eig.min()


raw = with_bias(amount, card_age)
scaled = with_bias((amount - amount.mean()) / amount.std(),
                   (card_age - card_age.mean()) / card_age.std())

for name, X in (("raw features", raw), ("standardized", scaled)):
    L, kappa = curvature(X)
    print(f"{name}: curvature {L:,.2f}, condition number {kappa:,.1f}, "
          f"max step {2 / L:.5f}")

runs = [("raw, eta 0.1", raw, 0.1), ("raw, eta 0.00002", raw, 2e-5),
        ("standardized, eta 1.0", scaled, 1.0)]
print("\nloss at step      0       10      50      199   went up on")
for name, X, eta in runs:
    h = train(X, eta)
    ups = int(np.sum(np.diff(h) > 0))
    print(f"{name:22s}" + "".join(f"{h[i]:8.4f}" for i in (0, 10, 50, 199))
          + f"   {ups:3d} steps")

# ---- checks ----
L_raw, k_raw = curvature(raw)
L_std, k_std = curvature(scaled)
assert np.isclose(train(raw, 0.1)[0], np.log(2))           # all-zero weights
assert 0.1 > 2 / L_raw and 1.0 < 2 / L_std                 # why one fails, one works
assert k_raw > 1000 * k_std
assert 1600 < 0.1 / (2 / L_raw) < 1750                     # "about 1,700 times"
assert 1e5 < np.mean(amount ** 2) < 1.6e5                  # against 1 for the bias
h_bad, h_slow, h_good = (train(X, e) for _, X, e in runs)
assert np.sum(np.diff(h_bad) > 0) > 20                     # oscillates
assert np.all(np.diff(h_good) < 1e-12)                     # never goes up
assert h_good[-1] < h_slow[-1] < h_slow[0]
