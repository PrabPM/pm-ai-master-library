"""Case 3 (chapter 124): fine-tune, add retrieval, or use a bigger model?

Dispute evidence summaries, 6 million a year. Pilot results are illustrative.
"""
import numpy as np

VOLUME, REWORK = 6_000_000, 1.50        # summaries a year; USD when one fails review

# option: (pass rate, unit cost USD, fixed cost USD per year, weeks to ship)
OPTIONS = {
    "today: small model, prompt only": (0.78, 0.004, 0, 0),
    "add retrieval": (0.88, 0.006, 0, 3),
    "bigger model": (0.86, 0.020, 0, 1),
    "fine-tune small model": (0.85, 0.003, 180_000, 10),
    "retrieval + route 20% to bigger": (0.91, 0.8 * 0.006 + 0.2 * 0.024, 0, 5),
}


def cost_per_summary(pass_rate, unit, fixed):
    return unit + (1 - pass_rate) * REWORK + fixed / VOLUME


if __name__ == "__main__":
    totals = {}
    for name, (pass_rate, unit, fixed, weeks) in OPTIONS.items():
        c = cost_per_summary(pass_rate, unit, fixed)
        totals[name] = c * VOLUME
        print(f"{name:<32} pass {pass_rate:.0%}  USD {c:.4f} each  "
              f"USD {c * VOLUME / 1e6:.2f}M a year  {weeks:>2} weeks")
    best = min(totals, key=totals.get)
    print("lowest total cost:", best)

    assert np.isclose(cost_per_summary(0.78, 0.004, 0), 0.334)
    assert np.isclose(cost_per_summary(0.88, 0.006, 0), 0.186)
    assert np.isclose(cost_per_summary(0.86, 0.020, 0), 0.230)
    assert np.isclose(cost_per_summary(0.85, 0.003, 180_000), 0.258)
    assert np.isclose(cost_per_summary(0.91, 0.0096, 0), 0.1446)
    assert best == "retrieval + route 20% to bigger"
