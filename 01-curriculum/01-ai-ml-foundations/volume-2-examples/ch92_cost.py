"""Chapter 92: cost per million tokens on your own GPUs, and the break-even point.

Every price and speed here is illustrative. Replace them with your own quotes
and your own measured throughput before deciding anything.
Run: python ch92_cost.py
"""
import numpy as np

GPU_HOUR = 2.50            # USD per GPU-hour, rented
TOKENS_PER_S = 1500        # tokens per second from one GPU at full load, within SLO
HOURS, SECONDS = 730, 730 * 3600      # one month


def cost_per_million(utilization):
    """Self-hosted cost of a million tokens: the GPU bills for idle hours too."""
    tokens_per_hour = TOKENS_PER_S * 3600 * utilization
    return GPU_HOUR / tokens_per_hour * 1e6


print("utilization   USD per million tokens")
for u in (1.0, 0.6, 0.3, 0.1):
    print(f"   {u:4.0%}           {cost_per_million(u):.2f}")

# PayFlow's assistant: 40,000 requests a day, 1,700 tokens in and 300 out.
requests_per_day, tokens_per_request = 40_000, 2000
monthly_tokens = requests_per_day * tokens_per_request * 30
price_in, price_out = 2.00, 10.00      # hosted API, USD per million tokens
api_price = (1700 * price_in + 300 * price_out) / tokens_per_request   # blended
gpus, ops = 2, 4000        # two GPUs for redundancy; engineering share per month
fixed = gpus * GPU_HOUR * HOURS + ops
capacity = gpus * TOKENS_PER_S * SECONDS

api_bill = monthly_tokens / 1e6 * api_price
break_even = fixed / api_price * 1e6
print(f"monthly volume: {monthly_tokens / 1e9:.2f} billion tokens")
print(f"hosted API: USD {api_price:.2f} per million blended, "
      f"bill USD {api_bill:,.0f}")
print(f"self-hosting: USD {fixed:,.0f} fixed "
      f"(USD {fixed / monthly_tokens * 1e6:.2f} per million at this volume)")
print(f"break-even volume: {break_even / 1e9:.2f} billion tokens a month, "
      f"which needs {break_even / capacity:.0%} utilization")
print(f"utilization at PayFlow's volume: {monthly_tokens / capacity:.0%}")

# Per-request view, which is the number a product review needs.
print(f"cost per 1,000 requests: API USD "
      f"{api_bill / (requests_per_day * 30) * 1000:.2f}, self-hosted USD "
      f"{fixed / (requests_per_day * 30) * 1000:.2f}")

# Checks against the hand calculation in the chapter.
assert np.isclose(cost_per_million(1.0), 2.50 / 5.4)
assert np.isclose(cost_per_million(0.3), 2.50 / 1.62)
assert monthly_tokens == 2_400_000_000 and np.isclose(api_price, 3.20)
assert np.isclose(api_bill, 7680) and np.isclose(fixed, 7650)
assert np.isclose(break_even, 7650 / 3.20 * 1e6)
assert np.isclose(capacity, 7.884e9)
