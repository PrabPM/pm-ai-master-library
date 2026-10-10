"""Chapter 30: will an open-weight model fit, and what does its size really mean?

Card sizes and model sizes are illustrative round numbers, not product claims.
Run: python ch30_open_weights.py
"""
import numpy as np


def weight_gb(params_billion, bits):
    """Memory for the weights alone: parameters x bits / 8, in GB (1 GB = 1e9 bytes)."""
    return params_billion * bits / 8


def fits(params_billion, bits, card_gb, headroom=0.20):
    """Leave a share of the card free for the KV cache and working memory."""
    return weight_gb(params_billion, bits) <= card_gb * (1 - headroom)


cards = (24, 80)
print("params  bits  weights  fits-24GB  fits-80GB")
for params in (8, 30, 120):
    for bits in (16, 8, 4):
        gb = f"{weight_gb(params, bits):.0f}GB"
        small, large = ("yes" if fits(params, bits, c) else "no" for c in cards)
        print(f"{params:4d}B  {bits:4d}  {gb:>7s}  {small:>9s}  {large:>9s}")

# Mixture of experts: memory follows total parameters, compute follows active ones.
total, active, bits = 26, 4, 16
print(f"mixture-of-experts, {total} B total and {active} B active per token:")
print(f"  memory follows the total: {weight_gb(total, bits):.0f} GB at {bits} bits")
print(f"  work per token follows the active part: {active / total:.0%} of the weights")

# Checks against the hand calculation in the chapter.
assert weight_gb(8, 16) == 16 and weight_gb(8, 4) == 4
assert weight_gb(30, 16) == 60 and weight_gb(120, 4) == 60
assert fits(8, 16, 24) and not fits(30, 8, 24) and fits(30, 4, 24)
assert np.isclose(active / total, 2 / 13)
