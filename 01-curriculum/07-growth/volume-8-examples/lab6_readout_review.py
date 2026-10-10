"""Lab 6: check the split before believing a teammate's readout."""
from scipy.stats import chisquare

control, treatment = 5_210, 4_790
stat, p = chisquare([control, treatment])
print(f"Split {control:,} vs {treatment:,}: chi-square {stat:.2f}, p = {p:.5f}")
print("Sample ratio mismatch" if p < 0.001 else "Split is fine")
segments, alpha = 12, 0.05
print(f"Segments examined: {segments}. Expected false wins by chance: "
      f"{segments * alpha:.1f}")
print(f"Chance of at least one: {1 - (1 - alpha) ** segments:.0%}")
