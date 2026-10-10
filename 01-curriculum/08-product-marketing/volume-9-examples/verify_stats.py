"""Cross-check the hand-written statistics against statsmodels (optional)."""
import sys

import ch04_message_test as ch04
import ch05_brand_tracker as ch05
import ch21_attribution as ch21

try:
    from statsmodels.stats.proportion import (confint_proportions_2indep,
                                              proportion_confint, proportions_ztest)
except ImportError:
    print("statsmodels is not installed, so the cross-check was skipped.")
    sys.exit(0)

for _, k, n in ch04.HEADLINES:
    ours = ch04.wilson(k, n)
    theirs = proportion_confint(k, n, alpha=0.05, method="wilson")
    assert all(abs(a - b) < 1e-9 for a, b in zip(ours, theirs)), (ours, theirs)

_, low, high = ch05.difference_interval(36, 400, 48, 400)
ref = confint_proportions_2indep(48, 400, 36, 400, method="wald", compare="diff")
assert abs(low - ref[0]) < 1e-9 and abs(high - ref[1]) < 1e-9, (low, high, ref)

(n1, k1), (n0, k0) = ch21.SAW_ADS, ch21.HELD_OUT
_, p_ref = proportions_ztest([k1, k0], [n1, n0])
assert abs(ch21.lift(ch21.SAW_ADS, ch21.HELD_OUT)[3] - p_ref) < 1e-9

print("Wilson intervals, the tracker interval and the lift test match statsmodels.")
