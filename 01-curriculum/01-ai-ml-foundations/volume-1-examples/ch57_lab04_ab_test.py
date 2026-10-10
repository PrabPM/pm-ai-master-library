"""Chapter 57, Lab 4: is a 0.7-point lift in approval rate real?"""
import numpy as np
from scipy import stats

n_a, x_a = 20_000, 18_200          # control: payments, approved
n_b, x_b = 20_000, 18_340          # new checkout flow
p_a, p_b = x_a / n_a, x_b / n_b
diff = p_b - p_a

pooled = (x_a + x_b) / (n_a + n_b)
se_null = np.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
z = diff / se_null
p_value = 2 * stats.norm.sf(abs(z))
se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
low, high = diff - 1.96 * se, diff + 1.96 * se
print(f"lift {100 * diff:.2f} points   z {z:.2f}   p-value {p_value:.4f}")
print(f"95% interval: {100 * low:.2f} to {100 * high:.2f} points")

# Sample size per arm to detect a 0.3-point lift with 80% power at the 5% level.
delta = 0.003
z_alpha, z_power = stats.norm.ppf(0.975), stats.norm.ppf(0.80)
n_needed = (z_alpha + z_power) ** 2 * 2 * p_a * (1 - p_a) / delta ** 2
print(f"payments per arm to detect 0.3 points: {n_needed:,.0f}")

# ---- checks against the hand results ----
assert np.isclose(pooled, 0.9135) and np.isclose(se_null, 0.002811, atol=1e-6)
assert np.isclose(z, 2.49, atol=0.005) and np.isclose(p_value, 0.0128, atol=2e-4)
assert np.isclose(100 * low, 0.15, atol=0.005)
assert np.isclose(100 * high, 1.25, atol=0.005)
assert abs(n_needed - 142_850) < 300
