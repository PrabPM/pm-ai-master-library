"""Chapter 90: replicas, a warm pool, and a fair split of capacity among tenants.

Rates and the hourly price are illustrative, not quotes.
Run: python ch90_capacity.py
"""
from math import ceil

import numpy as np

per_replica = 4.0        # requests per second one replica serves within the latency SLO
baseline, burst = 20.0, 10.0          # steady arrivals, and a sudden extra load
cold_start_s = 180                    # time to start a replica and load its weights
gpu_hour_usd = 2.50

steady = ceil(baseline / per_replica)
warm = ceil(burst / per_replica)
print(f"steady replicas: {steady}; warm replicas to absorb the burst: {warm} "
      f"(USD {warm * gpu_hour_usd * 730:,.0f} per month)")


def simulate_queue(warm_replicas, seconds=1500, burst_at=60):
    """Queue second by second. Autoscaled replicas arrive one cold start later."""
    queue, history = 0.0, []
    for t in range(seconds):
        arriving = baseline + (burst if t >= burst_at else 0.0)
        replicas = steady + warm_replicas
        if t >= burst_at + cold_start_s:
            replicas = steady + warm                 # the autoscaler has caught up
        queue = max(0.0, queue + arriving - replicas * per_replica)
        history.append(queue)
    q = np.array(history)
    if q.max() == 0:
        return 0.0, 0
    peak = int(np.argmax(q))
    empty_at = peak + int(np.argmax(q[peak:] == 0)) + 1
    return q.max(), empty_at - burst_at


for pool in (0, warm):
    peak, empty_after = simulate_queue(pool)
    print(f"warm pool of {pool}: peak queue {peak:,.0f} requests, "
          f"empty {empty_after:,} s after the burst starts")


def fair_share(capacity, demand):
    """Max-min fairness: split equally, capped at what each tenant asks for."""
    share = {tenant: 0.0 for tenant in demand}
    unmet = dict(demand)
    while unmet and capacity > 1e-9:
        slice_ = capacity / len(unmet)
        for tenant in list(unmet):
            give = min(slice_, unmet[tenant])
            share[tenant] += give
            unmet[tenant] -= give
            capacity -= give
            if unmet[tenant] <= 1e-9:
                del unmet[tenant]
    return share


demand = {"A (chat)": 3000, "B (documents)": 9000, "C (search)": 2000}
split = fair_share(10_000, demand)
print("tokens per second, capacity 10,000:")
for tenant, wanted in demand.items():
    print(f"  {tenant:14s} wants {wanted:5d}, gets {split[tenant]:5.0f}")

# Checks against the hand calculation in the chapter.
assert (steady, warm) == (5, 3)
assert burst * cold_start_s == 1800
spare = (steady + warm) * per_replica - (baseline + burst)      # 2 requests a second
assert simulate_queue(0) == (1800, cold_start_s + 1800 / spare)
assert simulate_queue(3) == (0, 0)
assert list(split.values()) == [3000, 5000, 2000]
