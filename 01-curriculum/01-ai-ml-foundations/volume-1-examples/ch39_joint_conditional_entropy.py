"""Chapter 39: joint and conditional entropy from a two-way table.

X = where the card was issued (domestic, cross-border).
Y = payment outcome (succeeded, failed). Shares of all PayFlow payments.
"""
import numpy as np

#                  succeeded  failed
joint = np.array([[0.7500, 0.0625],     # domestic
                  [0.1250, 0.0625]])    # cross-border
regions = ["domestic", "cross-border"]
assert np.isclose(joint.sum(), 1.0)


def H(p):
    """Entropy in bits of any array of probabilities that sums to 1."""
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 0]
    return float(np.sum(p * np.log2(1 / p)))


p_x = joint.sum(axis=1)                 # marginal of region: 0.8125, 0.1875
p_y = joint.sum(axis=0)                 # marginal of outcome: 0.875, 0.125
H_xy, H_x, H_y = H(joint), H(p_x), H(p_y)
print(f"H(X,Y) = {H_xy:.4f}   H(X) = {H_x:.4f}   H(Y) = {H_y:.4f}")

# conditional entropy, straight from its definition: a weighted average of the
# entropy of the outcome inside each region
H_y_given_x = 0.0
for i, region in enumerate(regions):
    within = joint[i] / p_x[i]          # P(Y | X = region)
    print(f"  {region:12} share {p_x[i]:.4f}  P(fail) = {within[1]:.4f}  "
          f"H(Y | X = {region}) = {H(within):.4f}")
    H_y_given_x += p_x[i] * H(within)
print(f"H(Y|X) = {H_y_given_x:.4f}")
print(f"chain rule: H(X) + H(Y|X) = {H_x + H_y_given_x:.4f}")
print(f"H(X) + H(Y) = {H_x + H_y:.4f}  (larger than H(X,Y): the two overlap)")
removed = H_y - H_y_given_x
print(f"knowing the region removes {removed:.4f} bits = {removed / H_y:.1%} of H(Y)")

# hand results
assert np.isclose(round(H_xy, 4), 1.1863)
assert np.isclose(round(H_x, 4), 0.6962) and np.isclose(round(H_y, 4), 0.5436)
assert np.isclose(H_x + H_y_given_x, H_xy)          # chain rule
assert H_xy <= H_x + H_y and H_y_given_x <= H_y     # overlap; conditioning helps
assert H(joint[1] / p_x[1]) > H_y                    # ...on average, not everywhere
