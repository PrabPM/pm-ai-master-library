"""Chapter 35: momentum, RMSprop and Adam on a stretched bowl.

Loss J(theta) = (c * theta_1^2 + theta_2^2) / 2. With c = 100 the bowl is one
hundred times steeper along theta_1, the picture you get when one feature is
measured in much larger units than another.
Writes volume-1-assets/ch35-optimizer-paths.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)
START = np.array([1.0, 1.0])


def make_bowl(c):
    curv = np.array([float(c), 1.0])
    return (lambda th: 0.5 * np.sum(curv * th**2)), (lambda th: curv * th)


def gd(grad, eta, steps):
    th, path = START.copy(), [START.copy()]
    for _ in range(steps):
        th = th - eta * grad(th)
        path.append(th.copy())
    return np.array(path)


def momentum(grad, eta, steps, beta=0.9):
    th, v, path = START.copy(), np.zeros(2), [START.copy()]
    for _ in range(steps):
        v = beta * v + grad(th)                 # running sum of gradients
        th = th - eta * v
        path.append(th.copy())
    return np.array(path)


def rmsprop(grad, eta, steps, rho=0.9, eps=1e-8):
    th, s, path = START.copy(), np.zeros(2), [START.copy()]
    for _ in range(steps):
        g = grad(th)
        s = rho * s + (1 - rho) * g**2          # running mean of squared gradients
        th = th - eta * g / (np.sqrt(s) + eps)  # per-coordinate step size
        path.append(th.copy())
    return np.array(path)


def adam(grad, eta, steps, b1=0.9, b2=0.999, eps=1e-8, correct=True):
    th, m, v, path = START.copy(), np.zeros(2), np.zeros(2), [START.copy()]
    for t in range(1, steps + 1):
        g = grad(th)
        m = b1 * m + (1 - b1) * g               # momentum's idea
        v = b2 * v + (1 - b2) * g**2            # RMSprop's idea
        m_hat = m / (1 - b1**t) if correct else m
        v_hat = v / (1 - b2**t) if correct else v
        th = th - eta * m_hat / (np.sqrt(v_hat) + eps)
        path.append(th.copy())
    return np.array(path)


def steps_until_below(loss, path, tol=1e-3):
    above = np.where(np.array([loss(p) for p in path]) >= tol)[0]
    return int(above[-1]) + 1 if above[-1] < len(path) - 1 else None


# ---- one Adam step by hand --------------------------------------------------
loss, grad = make_bowl(100)
g1 = grad(START)
m1, v1 = 0.1 * g1, 0.001 * g1**2
m_hat, v_hat = m1 / (1 - 0.9), v1 / (1 - 0.999)


def show(a):
    return "(" + ", ".join(f"{round(float(value), 4):g}" for value in a) + ")"


print("gradient at (1, 1):      ", show(g1))
print("m_1 and v_1:             ", show(m1), show(v1))
print("m_hat and v_hat:         ", show(m_hat), show(v_hat))
theta1 = adam(grad, 0.1, 1)[1]
print("theta after one step:    ", show(theta1))
no_fix = adam(grad, 0.1, 1, correct=False)[1]
print("without bias correction: ", show(no_fix))
assert np.allclose(g1, [100, 1]) and np.allclose(m1, [10, 0.1])
assert np.allclose(v1, [10, 0.001]) and np.allclose(m_hat, [100, 1])
assert np.allclose(v_hat, [10000, 1]) and np.allclose(theta1, [0.9, 0.9])
assert np.allclose(1 - no_fix, 0.1 * 0.1 / np.sqrt(0.001), atol=1e-6)

# ---- first steps: plain descent overshoots the steep direction; RMSprop and
# Adam move both parameters by the same amount
assert np.allclose(gd(grad, 0.019, 1)[1], [-0.9, 0.981])
first_rms = rmsprop(grad, 0.1, 1)[1]
assert np.isclose(first_rms[0], first_rms[1]) and np.allclose(first_rms, no_fix)
# RMSprop at a constant rate hovers near the minimum instead of settling
hover = [loss(p) for p in rmsprop(grad, 0.01, 1000)[-100:]]
assert 1e-3 < min(hover) and max(hover) < 2e-3

# ---- how many steps to converge, before and after rescaling a feature ------
print("steps until the loss stays below 0.001")
print("  method             bowl 100:1   bowl 10,000:1")
counts = {}
for c in (100, 10_000):
    loss_c, grad_c = make_bowl(c)
    eta_gd, eta_mom = 1.9 / c, 0.5 / c   # re-tuned for each bowl; 2 / c diverges
    counts[c] = {
        "gradient descent": steps_until_below(loss_c, gd(grad_c, eta_gd, 30_000)),
        "momentum": steps_until_below(loss_c, momentum(grad_c, eta_mom, 30_000)),
        "Adam": steps_until_below(loss_c, adam(grad_c, 0.1, 1_000)),   # unchanged
    }
for name in counts[100]:
    print(f"  {name:17} {counts[100][name]:10,d} {counts[10_000][name]:14,d}")
assert counts[100]["Adam"] < counts[100]["momentum"] < counts[100]["gradient descent"]
assert counts[10_000]["gradient descent"] > 50 * counts[10_000]["Adam"]


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch35", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.9), dpi=100, sharey=True)
    t1 = np.linspace(-1.15, 1.15, 301)
    t2 = np.linspace(-0.45, 1.15, 201)
    mesh1, mesh2 = np.meshgrid(t1, t2)
    runs = [("Gradient descent", gd(grad, 0.019, 30), "#b91c1c"),
            ("Momentum", momentum(grad, 0.005, 30), "#b45309"),
            ("Adam", adam(grad, 0.1, 30), "#4f46e5")]
    for ax, (name, path, color) in zip(axes, runs):
        ax.contour(mesh1, mesh2, 0.5 * (100 * mesh1**2 + mesh2**2),
                   levels=[1, 5, 15, 30, 50], colors="#cbd5e1", linewidths=1.0)
        ax.plot(path[:, 0], path[:, 1], "o-", color=color, markersize=2.5,
                linewidth=1.0)
        ax.plot(0, 0, "*", color="#15803d", markersize=12)
        ax.plot(1, 1, "o", color="#1f2937", markersize=5)
        ax.set_title(f"{name}, 30 steps", fontsize=11, color="#1f2937")
        ax.set_xlabel("θ₁ (steep)")
        ax.set_xticks([-1, 0, 1])
    axes[0].set_ylabel("θ₂ (shallow)")
    fig.tight_layout()
    fig.savefig(ASSETS / "ch35-optimizer-paths.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
