"""Chapter 14. Joint, marginal and conditional probability from a count table.

Run: python ch14_conditional_probability.py
"""
import numpy as np

# [listing]
# 10,000 payments: merchant age by dispute outcome
#                   disputed  not disputed
counts = np.array([[20, 980],      # new merchants
                   [30, 8970]])    # established merchants
joint = counts / counts.sum()

p_new = joint[0].sum()             # marginal: add across the row
p_disputed = joint[:, 0].sum()     # marginal: add down the column
p_both = joint[0, 0]
print(f"P(new) = {p_new:.3f}   P(disputed) = {p_disputed:.4f}   P(both) = {p_both:.4f}")
print(f"P(disputed | new)         = {p_both / p_new:.4f}")
print(f"P(disputed | established) = {joint[1, 0] / joint[1].sum():.4f}")
print(f"P(new | disputed)         = {p_both / p_disputed:.2f}")
print(f"if independent, P(both) would be {p_new * p_disputed:.4f}")

# Total probability: decline rate across three banks
share = np.array([0.60, 0.30, 0.10])       # P(bank)
decline = np.array([0.04, 0.06, 0.12])     # P(declined | bank)
print(f"overall decline rate              = {share @ decline:.4f}")
rerouted = np.array([0.65, 0.30, 0.05])
print(f"after moving 5 points from C to A = {rerouted @ decline:.4f}")
# [/listing]

# Hand-worked values from the chapter
assert np.isclose(p_new, 0.10) and np.isclose(p_disputed, 0.005)
assert np.isclose(p_both, 0.002)
assert np.isclose(p_both / p_new, 0.02)
assert np.isclose(joint[1, 0] / joint[1].sum(), 30 / 9000)
assert np.isclose(p_both / p_disputed, 0.40)
assert np.isclose(p_new * p_disputed, 0.0005)
assert np.isclose(share @ decline, 0.024 + 0.018 + 0.012)
assert np.isclose(rerouted @ decline, 0.026 + 0.018 + 0.006)
# chain rule: P(both) = P(disputed | new) P(new) = P(new | disputed) P(disputed)
assert np.isclose(0.02 * 0.10, 0.40 * 0.005)

# Q14.1: P(established | disputed) = 0.6 ; P(not disputed | new) = 0.98
assert np.isclose(joint[1, 0] / p_disputed, 0.6)
assert np.isclose(joint[0, 1] / p_new, 0.98)

# Q14.2 (Simpson's paradox): bank B wins in each segment and loses overall
a_dom, a_int = (950, 1000), (140, 200)     # approved, attempted at bank A
b_dom, b_int = (194, 200), (750, 1000)     # bank B
assert b_dom[0] / b_dom[1] > a_dom[0] / a_dom[1]      # 97% vs 95%
assert b_int[0] / b_int[1] > a_int[0] / a_int[1]      # 75% vs 70%
overall_a = (a_dom[0] + a_int[0]) / (a_dom[1] + a_int[1])
overall_b = (b_dom[0] + b_int[0]) / (b_dom[1] + b_int[1])
assert np.isclose(overall_a, 1090 / 1200) and np.isclose(overall_b, 944 / 1200)
assert overall_b < overall_a
