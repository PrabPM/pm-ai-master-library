"""Chapter 57, Lab 6: the learning rate a loss surface can stand."""
import numpy as np

curvature = np.array([1.0, 25.0])          # f(w) = 0.5 * (1 * w1^2 + 25 * w2^2)


def steps_to_converge(eta, curvature, start=(10.0, 1.0), tol=1e-6, cap=10_000):
    """Gradient descent steps until f < tol; None if it blows up."""
    w = np.array(start)
    for step in range(1, cap + 1):
        w = w - eta * curvature * w            # the gradient is curvature * w
        f = 0.5 * np.sum(curvature * w ** 2)
        if f < tol:
            return step
        if f > 1e12:
            return None
    return cap


print(f"largest stable step 2/L = {2 / curvature.max():.3f}   "
      f"condition number {curvature.max() / curvature.min():.0f}")
for eta in (0.01, 0.07, 2 / 26, 0.09):
    n = steps_to_converge(eta, curvature)
    print(f"eta {eta:.4f}: " + ("diverges" if n is None else f"{n} steps"))
print("after rescaling both curvatures to 1, eta 1.0:",
      steps_to_converge(1.0, np.array([1.0, 1.0])), "step")

# ---- checks against the hand results ----
assert np.isclose(2 / curvature.max(), 0.08)
assert steps_to_converge(0.09, curvature) is None        # 0.09 > 0.08
assert steps_to_converge(0.07, curvature) < steps_to_converge(0.01, curvature)
assert steps_to_converge(2 / 26, curvature) <= steps_to_converge(0.07, curvature)
assert np.isclose(abs(1 - 0.09 * 25), 1.25)              # growth factor per step
assert steps_to_converge(1.0, np.array([1.0, 1.0])) == 1
