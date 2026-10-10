"""Chapter 75. A streaming window count with a watermark, late events, and an
online/offline parity test, all in plain Python."""
import numpy as np


def tumbling_counts(events, width, bound):
    """Count (event_time, arrival_time) events per window, as a stream engine does."""
    counts, closed, late = {}, set(), []
    max_seen = float("-inf")
    for event_time, _ in sorted(events, key=lambda e: e[1]):   # arrival order
        start = int(event_time // width) * width
        if start in closed:
            late.append(event_time)                            # too late to count
        else:
            counts[start] = counts.get(start, 0) + 1
        max_seen = max(max_seen, event_time)
        watermark = max_seen - bound
        closed.update(s for s in counts if s + width <= watermark)   # window ends
    return counts, late


def batch_counts(events, width):
    """The offline answer: every event, placed by its event time."""
    counts = {}
    for event_time, _ in events:
        start = int(event_time // width) * width
        counts[start] = counts.get(start, 0) + 1
    return counts


def parity_skew(online, offline, tol=0):
    """Share of keys whose online value differs from offline by more than tol."""
    miss = sum(abs(online.get(k, 0) - v) > tol for k, v in offline.items())
    return miss / len(offline)


# ---- 1. The hand example: one merchant, 60-second windows ------------------------
hand = [(10, 11), (25, 26), (50, 51), (63, 64), (40, 66), (68, 69), (56, 72)]
offline = batch_counts(hand, width=60)
for bound in (5, 15):
    online, late = tumbling_counts(hand, width=60, bound=bound)
    print(f"bound {bound:2d} s: online {online}, late {late}, offline {offline}")
online5, late5 = tumbling_counts(hand, 60, 5)
assert online5 == {0: 4, 60: 2} and late5 == [56]
assert tumbling_counts(hand, 60, 15) == ({0: 5, 60: 2}, [])
assert offline == {0: 5, 60: 2}
assert parity_skew(online5, offline) == 0.5

# ---- 2. One hour of payments with realistic delays, seeded -----------------------
rng = np.random.default_rng(75)
n = 20_000
event_time = np.sort(rng.uniform(0, 3600, n))
slow = rng.random(n) < 0.10                       # 10% come through a slow path
delay = np.where(slow, rng.exponential(20.0, n), rng.exponential(1.0, n))
stream = list(zip(event_time, event_time + delay))
truth = batch_counts(stream, width=60)
assert sum(truth.values()) == n

print("\nbound   late events   windows off by any   windows off by more than 3")
shares = []
for bound in (0, 5, 15, 60):
    online, late = tumbling_counts(stream, width=60, bound=bound)
    shares.append(len(late) / n)
    print(f"{bound:3d} s   {shares[-1]:10.2%}   {parity_skew(online, truth):16.0%}"
          f"   {parity_skew(online, truth, tol=3):24.0%}")
assert shares == sorted(shares, reverse=True)     # a longer wait loses fewer events
