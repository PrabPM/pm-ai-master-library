"""Chapter 70: sizing a reviewer queue with the Erlang C formula.
Illustrative volumes.
"""
from math import factorial


def erlang_c(arrivals_per_hour, handled_per_hour, reviewers):
    """Probability that a new item has to wait (all reviewers busy)."""
    load = arrivals_per_hour / handled_per_hour           # offered load, in erlangs
    if reviewers <= load:
        return 1.0                                        # the queue grows forever
    top = load ** reviewers / factorial(reviewers) * reviewers / (reviewers - load)
    return top / (sum(load ** k / factorial(k) for k in range(reviewers)) + top)


def mean_wait_min(arrivals_per_hour, handled_per_hour, reviewers):
    p_wait = erlang_c(arrivals_per_hour, handled_per_hour, reviewers)
    spare = reviewers * handled_per_hour - arrivals_per_hour
    return float("inf") if spare <= 0 else 60 * p_wait / spare


def staff_for(arrivals_per_hour, handle_min, target_wait_min):
    rate, c = 60 / handle_min, 1
    while mean_wait_min(arrivals_per_hour, rate, c) > target_wait_min:
        c += 1
    return c


print(f"hand case, 10 per hour, 6 min each, 2 reviewers: P(wait) "
      f"{erlang_c(10, 10, 2):.3f}, mean wait {mean_wait_min(10, 10, 2):.1f} min")
arrivals = 4000 * 0.03                      # 4,000 decisions an hour, 3% escalated
print(f"escalations per hour: {arrivals:.0f}; offered load at 6 min: "
      f"{arrivals / 10:.0f} reviewers' worth")
for c in (13, 14, 15, 16):
    print(f"  {c} reviewers: utilization {arrivals / (c * 10):.0%}, P(wait) "
          f"{erlang_c(arrivals, 10, c):.2f}, mean wait "
          f"{mean_wait_min(arrivals, 10, c):.1f} min")
slow, fast = staff_for(arrivals, 6, 1.0), staff_for(arrivals, 4, 1.0)
saving = (slow - fast) * 40 * 12 * 365      # USD 40 an hour, 12-hour day
print(f"reviewers for a 1-minute mean wait: {slow} at 6 min a case, "
      f"{fast} at 4 min a case")
print(f"yearly saving from the faster review screen: USD {saving:,}")

# ---- checks against the hand-worked numbers ----
assert abs(erlang_c(10, 10, 2) - 1 / 3) < 1e-12
assert abs(mean_wait_min(10, 10, 2) - 2.0) < 1e-9
assert arrivals == 120 and erlang_c(arrivals, 10, 12) == 1.0
assert slow > fast
