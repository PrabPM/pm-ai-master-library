"""Chapter 11: a latency budget for one Assist answer, simulated stage by stage."""
import math
import random
import statistics

# Stage, typical (median) milliseconds, spread. A larger spread means a longer tail.
STAGES = [
    ("Sign-in and permission check", 40, 0.30),
    ("Rewrite the question (small model)", 250, 0.35),
    ("Search with permission check", 180, 0.45),
    ("Rerank the passages", 120, 0.30),
    ("Tool calls: payout and bank records", 350, 0.60),
    ("Model: wait for the first token", 700, 0.40),
    ("Model: stream 320 tokens", 4_000, 0.25),
    ("Check each claim against its source", 300, 0.35),
]
FIRST_TOKEN_STAGES = 6      # the user sees text after the first six stages
RUNS = 20_000


# [listing]
def percentile(values, pct):
    return statistics.quantiles(values, n=100)[pct - 1]


def simulate(seed=7):
    rng = random.Random(seed)
    runs = []
    for _ in range(RUNS):
        runs.append([rng.lognormvariate(math.log(median), spread)
                     for _, median, spread in STAGES])
    return runs
# [end listing]


def summary():
    runs = simulate()
    stage_p50 = [percentile([r[i] for r in runs], 50) for i in range(len(STAGES))]
    stage_p95 = [percentile([r[i] for r in runs], 95) for i in range(len(STAGES))]
    first = [sum(r[:FIRST_TOKEN_STAGES]) for r in runs]
    total = [sum(r) for r in runs]
    # Variant: start the tool calls at the same time as search and rerank.
    parallel = [r[0] + r[1] + max(r[2] + r[3], r[4]) + r[5] for r in runs]
    return stage_p50, stage_p95, first, total, parallel


def main():
    stage_p50, stage_p95, first, total, parallel = summary()
    print(f"{'Stage':<38}{'P50 ms':>8}{'P95 ms':>8}")
    for (name, _, _), p50, p95 in zip(STAGES, stage_p50, stage_p95):
        print(f"{name:<38}{p50:>8,.0f}{p95:>8,.0f}")
    print(f"{'Time to first token':<38}{percentile(first, 50):>8,.0f}"
          f"{percentile(first, 95):>8,.0f}")
    print(f"{'Whole answer':<38}{percentile(total, 50):>8,.0f}"
          f"{percentile(total, 95):>8,.0f}")
    print(f"Sum of the eight stage P95s: {sum(stage_p95):,.0f} ms "
          f"(overstates the real P95)")
    print(f"{'First token, tools run beside search':<38}"
          f"{percentile(parallel, 50):>8,.0f}{percentile(parallel, 95):>8,.0f}")


if __name__ == "__main__":
    main()
