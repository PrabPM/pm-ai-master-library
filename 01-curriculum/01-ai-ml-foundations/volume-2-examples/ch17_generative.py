"""Chapter 17: the three generative objectives, and diffusion on a number line."""
import numpy as np

# VAE: KL divergence from N(mu, sigma^2) to the standard normal prior.
mu, sigma = 1.0, 0.5
kl = 0.5 * (mu ** 2 + sigma ** 2 - 1 - np.log(sigma ** 2))
# GAN: the best possible discriminator at a point x.
p_data, p_gen = 0.3, 0.1
d_star = p_data / (p_data + p_gen)
# Diffusion: one jump to noise level abar, then undo it with the true noise.
x0, abar, eps = 2.0, 0.64, 0.5
xt = np.sqrt(abar) * x0 + np.sqrt(1 - abar) * eps
x0_back = (xt - np.sqrt(1 - abar) * eps) / np.sqrt(abar)
print(f"KL {kl:.3f} nats   best discriminator {d_star:.2f}   "
      f"noised x_t {xt:.2f}   recovered x_0 {x0_back:.2f}")
assert np.isclose(kl, 0.818, atol=5e-4) and np.isclose(xt, 1.9)
assert np.isclose(d_star, 0.75) and np.isclose(x0_back, x0)

# A one-dimensional "dataset": log-amounts with a big cluster and a small one.
rng = np.random.default_rng(17)


def sample_data(n):
    high = rng.random(n) < 0.3
    return np.where(high, rng.normal(1.5, 0.25, n), rng.normal(-1.0, 0.25, n))


T = 100
beta = np.linspace(0.001, 0.12, T)             # noise added at each step
alpha = 1 - beta
abar = np.cumprod(alpha)                       # share of signal left after t steps
edges = np.linspace(-4, 4, 161)                # the "model": one number per bin

# Training: for each step t, the average noise behind each value of x_t.
# A bin average is the least-squares answer, so it minimizes the loss.
table = np.zeros((T, 162))                     # 160 bins plus two overflow bins
for t in range(T):
    x0s, noise = sample_data(50000), rng.normal(size=50000)
    xt = np.sqrt(abar[t]) * x0s + np.sqrt(1 - abar[t]) * noise
    bins = np.digitize(xt, edges)
    total = np.bincount(bins, weights=noise, minlength=162)
    table[t] = total / np.maximum(np.bincount(bins, minlength=162), 1)

# Sampling: start from pure noise and remove the predicted noise step by step.
x = rng.normal(size=5000)
for t in reversed(range(T)):
    predicted = table[t, np.digitize(x, edges)]
    x = (x - beta[t] / np.sqrt(1 - abar[t]) * predicted) / np.sqrt(alpha[t])
    if t > 0:
        x += np.sqrt(beta[t]) * rng.normal(size=5000)

data = sample_data(5000)
print(f"signal left after 10, 50, 100 steps: {abar[9]:.2f}, {abar[49]:.2f}, "
      f"{abar[99]:.3f}")
for name, v in (("data", data), ("generated", x)):
    top = v > 0.25
    print(f"{name:<10} share in the high cluster {top.mean():.2f}   cluster means "
          f"{v[~top].mean():.2f} and {v[top].mean():.2f}   spread {v[~top].std():.2f}")
assert abs(np.mean(x > 0.25) - 0.3) < 0.05
