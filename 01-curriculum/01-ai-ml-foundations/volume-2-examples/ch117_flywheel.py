"""Chapter 117: testing a claimed data flywheel.

Three measured numbers decide whether the wheel turns:
  label_yield  labeled outcomes produced per payment
  slope        quality gained per doubling of labels (the learning curve)
  response     volume growth per unit of quality gained
PayFlow's numbers here are illustrative.
"""
import numpy as np


def quality(labels, slope=0.03, base_labels=100_000, base_quality=0.60, cap=0.95):
    """Fraud recall at a fixed false-positive rate, as a function of labels."""
    return min(cap, base_quality + slope * np.log2(labels / base_labels))


def simulate(quarters, payments, labels, label_yield, slope=0.03, response=2.0):
    """One row per quarter: (quarter, payments, labels, recall)."""
    rows = [(0, payments, labels, quality(labels, slope))]
    for t in range(1, quarters + 1):
        new_labels = labels + label_yield * payments
        gain = quality(new_labels, slope) - quality(labels, slope)
        payments = payments * (1 + response * gain)
        labels = new_labels
        rows.append((t, payments, labels, quality(labels, slope)))
    return rows


if __name__ == "__main__":
    start = dict(payments=10_000_000, labels=100_000)
    working = simulate(8, label_yield=0.004, **start)
    no_labels = simulate(8, label_yield=0.0, **start)
    flat_curve = simulate(8, label_yield=0.004, slope=0.0, **start)

    print("quarter  payments (millions)  labels   recall")
    for t, u, d, q in working[:2] + working[-1:]:
        print(f"{t:>7}  {u / 1e6:>19.3f}  {d:>7,.0f}  {q:.4f}")
    print(f"no labels captured: recall {no_labels[-1][3]:.4f}, "
          f"payments {no_labels[-1][1] / 1e6:.3f} million")
    print(f"flat learning curve: recall {flat_curve[-1][3]:.4f}, "
          f"payments {flat_curve[-1][1] / 1e6:.3f} million")

    # Diminishing returns: quarters needed for each further 3 points of recall.
    reached, target = [], 0.63
    for t, u, d, q in simulate(40, label_yield=0.004, **start):
        if q >= target - 1e-9:
            reached.append(t)
            target += 0.03
    print("quarter in which recall first reaches 0.63, 0.66, 0.69:", reached[:3])

    t1 = working[1]
    assert np.isclose(t1[2], 140_000)
    assert np.isclose(t1[3], 0.60 + 0.03 * np.log2(1.4)) and np.isclose(t1[3], 0.6146,
                                                                         atol=1e-4)
    assert np.isclose(t1[1] / 1e6, 10.291, atol=1e-3)
    assert np.isclose(no_labels[-1][3], 0.60) and no_labels[-1][1] == 10_000_000
    assert flat_curve[-1][1] == 10_000_000
