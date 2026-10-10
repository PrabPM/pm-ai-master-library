"""Lab 12 (chapter 115): split a privacy budget across releases."""
import numpy as np

BUDGET, SENSITIVITY, TYPICAL_COUNT = 2.6, 1, 40      # per quarter


def plan(releases):
    epsilon = BUDGET / releases
    scale = SENSITIVITY / epsilon
    bound95 = scale * np.log(20)             # 95% of Laplace noise is within this
    return epsilon, scale, bound95


if __name__ == "__main__":
    for name, releases in (("weekly", 13), ("monthly", 3)):
        eps, b, bound = plan(releases)
        print(f"{name:<8} {releases:>2} releases: epsilon {eps:.3f} each, "
              f"scale {b:.2f}")
        print(f"         95% of releases within +/- {bound:.1f}, "
              f"{bound / TYPICAL_COUNT:.0%} of a count of {TYPICAL_COUNT}")

    eps_w, b_w, bound_w = plan(13)
    assert np.isclose(eps_w, 0.2) and np.isclose(b_w, 5) and np.isclose(bound_w, 14.98,
                                                                         atol=0.01)
    assert np.isclose(plan(3)[2], 3.46, atol=0.01)
