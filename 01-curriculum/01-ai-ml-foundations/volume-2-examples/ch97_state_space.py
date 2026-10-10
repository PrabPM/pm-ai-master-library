"""Chapter 97. State space models: a discretized linear recurrence, and what
"selective" adds.

Run: python ch97_state_space.py
"""
import numpy as np

# [listing]
def discretize(a, b, delta):
    """Zero-order hold for the scalar system h' = a h + b x."""
    a_bar = np.exp(delta * a)
    b_bar = (a_bar - 1) / a * b
    return a_bar, b_bar


def run(x, deltas, a=-1.0, b=1.0):
    h, trace = 0.0, []
    for x_t, delta in zip(x, deltas):
        a_bar, b_bar = discretize(a, b, delta)
        h = a_bar * h + b_bar * x_t                # one fixed-size state update
        trace.append(h)
    return np.array(trace)


x = np.array([4.0, 1.0, 1.0, 1.0])                 # first token matters, rest is filler
fixed = run(x, [np.log(2)] * 4)                    # same step for every token
selective = run(x, [np.log(4)] + [np.log(10 / 9)] * 3)   # step chosen per token
print("fixed step    :", fixed.round(3))
print("selective step:", selective.round(3))

L, state = 32_768, 16
print(f"sequence of {L:,} tokens: attention compares {L * (L - 1) // 2:,} pairs;")
print(f"a state space layer does {L:,} updates of a {state}-number state "
      f"per channel")
# [/listing]

# Hand-worked: with delta = ln 2 the update is h = 0.5 h + 0.5 x
assert np.allclose(discretize(-1.0, 1.0, np.log(2)), (0.5, 0.5))
assert np.allclose(fixed, [2.0, 1.5, 1.25, 1.125])
# Selective: first step keeps 0.25 and writes 0.75; later steps keep 0.9, write 0.1
assert np.allclose(discretize(-1.0, 1.0, np.log(4)), (0.25, 0.75))
assert np.allclose(discretize(-1.0, 1.0, np.log(10 / 9)), (0.9, 0.1))
assert np.allclose(selective, [3.0, 2.8, 2.62, 2.458])

# The zero-order-hold formula is the exact solution of h' = a h + b x for a
# constant input over one step: compare with a fine Euler integration.
h, a, b, x_const, delta, n = 0.7, -1.3, 0.8, 2.0, 0.6, 200_000
for _ in range(n):
    h += (delta / n) * (a * h + b * x_const)
a_bar, b_bar = discretize(a, b, delta)
assert np.isclose(h, a_bar * 0.7 + b_bar * x_const, atol=1e-5)

# Matrix form with a diagonal A reduces to the scalar rule per state dimension
A = np.array([-0.5, -2.0])
B = np.array([1.0, 3.0])
A_bar = np.exp(0.3 * A)
B_bar = (A_bar - 1) / (0.3 * A) * (0.3 * B)       # (dA)^-1 (exp(dA) - I) dB
assert np.allclose(B_bar, [discretize(A[i], B[i], 0.3)[1] for i in range(2)])

assert L * (L - 1) // 2 == 536_854_528
# Q97.1: delta = ln 5 -> keep 0.2, write 0.8; from h = 2 with x = 7 -> 6.0
ab, bb = discretize(-1.0, 1.0, np.log(5))
assert np.allclose((ab, bb), (0.2, 0.8)) and np.isclose(ab * 2 + bb * 7, 6.0)
# Q97.2: doubling length quadruples pair count (to within rounding), doubles updates
pairs = lambda n: n * (n - 1) // 2
assert round(pairs(2 * L) / pairs(L), 3) == 4.0
