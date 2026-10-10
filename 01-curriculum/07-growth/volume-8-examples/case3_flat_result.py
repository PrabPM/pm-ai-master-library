"""Case 3: a flat result still tells you what you ruled out."""
from math import sqrt

c_n, c_yes = 14_950, 897    # old Plus paywall: subscribed within 30 days
t_n, t_yes = 15_020, 931    # new comparison-table paywall
pc, pt = c_yes / c_n, t_yes / t_n
diff = pt - pc
se = sqrt(pc * (1 - pc) / c_n + pt * (1 - pt) / t_n)
print(f"Control {pc:.2%}, treatment {pt:.2%}, difference {diff * 100:+.2f} points")
print(f"95% CI {(diff - 1.96 * se) * 100:+.2f} to {(diff + 1.96 * se) * 100:+.2f} "
      f"points")
