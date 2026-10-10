"""Chapter 21: read the guided-setup experiment: effect, interval, p-value."""
from math import sqrt

from scipy.stats import norm


def compare(label, c_n, c_yes, t_n, t_yes):
    pc, pt = c_yes / c_n, t_yes / t_n
    diff = pt - pc
    se = sqrt(pc * (1 - pc) / c_n + pt * (1 - pt) / t_n)
    pooled = (c_yes + t_yes) / (c_n + t_n)
    z = diff / sqrt(pooled * (1 - pooled) * (1 / c_n + 1 / t_n))
    low, high = (diff - 1.96 * se) * 100, (diff + 1.96 * se) * 100
    print(label)
    p_value = 2 * norm.sf(abs(z))
    print(f"  control {pc:.1%}, treatment {pt:.1%}, "
          f"difference {diff * 100:+.1f} points")
    print(f"  95% CI {low:+.1f} to {high:+.1f} points, p = {p_value:.4f}")


compare("Primary: activated within 14 days", 4_660, 2_563, 4_672, 2_714)
compare("Guardrail: first payout failed", 2_563, 49, 2_714, 84)
