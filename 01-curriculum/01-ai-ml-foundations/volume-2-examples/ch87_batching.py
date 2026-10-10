"""Chapter 87: static versus continuous batching, and paged KV-cache allocation.

Time is counted in decode steps: one step writes one token for every request in
the running batch. Step time is held constant to keep the comparison simple.
Run: python ch87_batching.py
"""
import numpy as np


def simulate(requests, batch_size, continuous):
    """requests: list of (arrival_step, output_tokens). Returns finish steps and
    the share of batch slots that did useful work."""
    waiting = sorted(range(len(requests)), key=lambda i: requests[i][0])
    running, finish, t, busy, slots = {}, {}, 0, 0, 0
    while waiting or running:
        can_admit = continuous or not running      # static: only when batch is empty
        while (can_admit and waiting and len(running) < batch_size
               and requests[waiting[0]][0] <= t):
            i = waiting.pop(0)
            running[i] = requests[i][1]            # tokens still to write
        if not running:
            t = requests[waiting[0]][0]            # idle until the next arrival
            continue
        t += 1                                     # one decode step for the batch
        slots += batch_size
        for i in running:
            if running[i] > 0:
                running[i] -= 1
                busy += 1
        done = [i for i in running if running[i] == 0]
        if continuous or len(done) == len(running):
            for i in done:                         # static: only when all are done
                finish[i] = t
                del running[i]
    latency = np.array([finish[i] - requests[i][0] for i in range(len(requests))])
    return latency, busy / slots


hand = [(0, 10), (0, 20), (0, 30), (0, 100), (5, 20), (15, 10)]
print("six requests, 4 slots")
for name, mode in (("static", False), ("continuous", True)):
    latency, _ = simulate(hand, batch_size=4, continuous=mode)
    print(f"  {name:10s} latency {latency.tolist()}  mean {latency.mean():.1f}")

rng = np.random.default_rng(42)
n = 2000
arrivals = np.cumsum(rng.exponential(scale=40.0, size=n)).astype(int)   # Poisson
lengths = np.minimum(rng.lognormal(mean=4.0, sigma=0.8, size=n).astype(int) + 1, 600)
workload = list(zip(arrivals.tolist(), lengths.tolist()))
print(f"{n} simulated requests, 8 slots, mean output {lengths.mean():.0f} tokens")
for name, mode in (("static", False), ("continuous", True)):
    latency, _ = simulate(workload, batch_size=8, continuous=mode)
    backlog = [(0, tokens) for _, tokens in workload]      # everyone already waiting
    _, saturated = simulate(backlog, batch_size=8, continuous=mode)
    p95 = np.percentile(latency, 95)
    print(f"  {name:10s} mean latency {latency.mean():3.0f} steps, p95 {p95:3.0f}; "
          f"slots used under backlog {saturated:.0%}")

# Paged allocation: reserve KV memory in 16-token blocks as each request grows.
context_tokens = [120, 300, 80, 950, 40, 610, 200, 100]
max_len, block = 2048, 16
reserved = len(context_tokens) * max_len
paged = sum(-(-t // block) * block for t in context_tokens)       # round up
used = sum(context_tokens)
print(f"KV slots in use {used}: contiguous reserves {reserved} "
      f"({1 - used / reserved:.0%} idle), paged {paged} ({1 - used / paged:.1%} idle)")

# Checks against the hand calculation in the chapter.
lat_s, use_s = simulate(hand, 4, False)
lat_c, use_c = simulate(hand, 4, True)
assert lat_s.tolist() == [100, 100, 100, 100, 115, 105]
assert lat_c.tolist() == [10, 20, 30, 100, 25, 15] and np.isclose(lat_c.mean(), 100 / 3)
assert np.isclose(use_s, 190 / 480) and np.isclose(use_c, 190 / 400)
assert reserved == 16384 and paged == 2464 and used == 2400
