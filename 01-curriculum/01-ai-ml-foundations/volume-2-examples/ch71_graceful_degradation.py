"""Chapter 71: a fallback chain with a timeout and a circuit breaker.
Seeded simulation; illustrative failure rates.
"""
from collections import Counter

import numpy as np

rng = np.random.default_rng(71)
TIMEOUT = 4.0                                   # seconds allowed for the main model


def call_main(down):
    """Returns (succeeded, seconds). When down, every call hangs to the timeout."""
    if down:
        return False, TIMEOUT
    if rng.random() < 0.005:
        return False, 0.2                       # a fast error
    seconds = rng.lognormal(np.log(1.2), 0.5)
    return seconds <= TIMEOUT, min(seconds, TIMEOUT)


def call_small():
    return rng.random() >= 0.01, rng.lognormal(np.log(0.4), 0.4)


def serve(down=False, skip_main=False):
    """Main model, then the small model, then help articles and a human handoff."""
    waited = 0.0
    if not skip_main:
        ok, seconds = call_main(down)
        waited += seconds
        if ok:
            return "main model", waited
    ok, seconds = call_small()
    waited += seconds
    return ("small model", waited) if ok else ("articles + handoff", waited + 0.05)


normal = [serve() for _ in range(100_000)]
share = Counter(tier for tier, _ in normal)
print("normal day:", ", ".join(f"{t} {c / 1000:.2f}%" for t, c in share.most_common()))
print("hand check, both models fail on the same request:", 0.005 * 0.01)

outage = [serve(down=True)[1] for _ in range(2_000)]
failures, with_breaker = 0, []
for _ in range(2_000):                          # the same outage with a breaker
    tripped = failures >= 5                     # open after 5 failures in a row
    tier, seconds = serve(down=True, skip_main=tripped)
    failures += 1                               # the main model stays down here
    with_breaker.append(seconds)
print(f"outage, no breaker:   p95 wait {np.percentile(outage, 95):.2f}s")
print(f"outage, with breaker: p95 wait {np.percentile(with_breaker, 95):.2f}s")

# ---- checks ----
assert np.isclose(0.005 * 0.01, 0.00005)
assert share["main model"] > 98_000 and share["articles + handoff"] < 100
assert np.percentile(outage, 95) > TIMEOUT > np.percentile(with_breaker, 95)
