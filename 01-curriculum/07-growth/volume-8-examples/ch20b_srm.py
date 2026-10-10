"""Chapter 20: sample ratio mismatch check for a planned 50/50 split."""
from scipy.stats import chisquare


def srm_check(label, control, treatment):
    stat, p = chisquare([control, treatment])  # expects two equal halves
    verdict = "MISMATCH" if p < 0.001 else "split is fine"
    print(f"{label:<15}{control:,} vs {treatment:,}  chi-square {stat:5.2f}  "
          f"p = {p:.5f}  {verdict}")


srm_check("First launch:", 2_440, 2_160)
srm_check("After the fix:", 4_660, 4_672)
