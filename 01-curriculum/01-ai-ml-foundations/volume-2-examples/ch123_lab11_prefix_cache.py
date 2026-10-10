"""Lab 11 (chapters 29, 88 and 92): what a cached prompt prefix saves.

Prices are illustrative, not any vendor's price list.
"""
import numpy as np

P_IN, P_CACHED, P_OUT = 2.00, 0.20, 10.00     # USD per million tokens
PREFIX, VARIABLE, OUTPUT = 3000, 1500, 400    # tokens per request
REQUESTS = 1_200_000                          # per month


def cost_per_request(hit_rate):
    prefix = PREFIX * (hit_rate * P_CACHED + (1 - hit_rate) * P_IN)
    return (prefix + VARIABLE * P_IN + OUTPUT * P_OUT) / 1e6


if __name__ == "__main__":
    for hit in (0.0, 0.9):
        c = cost_per_request(hit)
        print(f"prefix cache hit rate {hit:.0%}: USD {c:.5f} a request, "
              f"USD {c * REQUESTS:,.0f} a month")
    saved = (cost_per_request(0) - cost_per_request(0.9)) * REQUESTS
    print(f"saved: USD {saved:,.0f} a month "
          f"({saved / (cost_per_request(0) * REQUESTS):.0%})")

    assert np.isclose(cost_per_request(0), 0.013)
    assert np.isclose(cost_per_request(0.9), 0.00814)
    assert np.isclose(saved, 5_832)
