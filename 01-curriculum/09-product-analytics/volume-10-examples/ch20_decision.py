"""Chapter 20: expected value, a sensitivity table, Monte Carlo and the value of
information, all on the Quickstart model from Chapter 19."""
import numpy as np

from ch19_projection import BASE, SCENARIOS, cash_flows, npv, project

PROBABILITY = {"Downside": 0.25, "Base": 0.50, "Upside": 0.25}
RANGES = {      # one driver at a time: (pessimistic value, optimistic value)
    "lift": (0.02, 0.08), "approved": (800, 1_200), "margin": (80, 120),
    "churn": (1.25, 0.80), "build": (1_000_000, 700_000), "launch": (9, 6)}


def value(**changes):
    return npv(cash_flows(project(**{**BASE, **changes})))


def tornado():
    bars = [(name, value(**{name: low}), value(**{name: high}))
            for name, (low, high) in RANGES.items()]
    return sorted(bars, key=lambda bar: bar[2] - bar[1], reverse=True)


def break_even_lift():
    """The activation lift at which NPV is exactly zero, by bisection."""
    low, high = 0.0, 0.10
    for _ in range(60):
        mid = (low + high) / 2
        low, high = (mid, high) if value(lift=mid) < 0 else (low, mid)
    return high


def monte_carlo(draws=5_000, seed=20):
    rng = np.random.default_rng(seed)
    results = np.empty(draws)
    for i in range(draws):
        results[i] = value(
            lift=rng.triangular(0.00, 0.05, 0.10),
            approved=rng.normal(1_000, 80),
            margin=rng.normal(100, 8),
            churn=rng.uniform(0.85, 1.15),
            build=rng.triangular(700_000, 800_000, 1_100_000),
            launch=int(rng.choice([6, 9, 12], p=[0.60, 0.30, 0.10])))
    return results


if __name__ == "__main__":
    outcomes = {name: npv(cash_flows(project(**d))) for name, d in SCENARIOS.items()}
    expected = sum(PROBABILITY[n] * v for n, v in outcomes.items())
    for name, v in outcomes.items():
        print(f"{name:<9} p = {PROBABILITY[name]:.2f}   NPV {v:>10,.0f}")
    print(f"Expected NPV if we build now: {expected:,.0f}")

    print()
    print(f"{'driver':<10}{'pessimistic':>13}{'optimistic':>12}{'swing':>12}")
    for name, low, high in tornado():
        print(f"{name:<10}{low:>13,.0f}{high:>12,.0f}{high - low:>12,.0f}")
    print(f"NPV is zero at a lift of {break_even_lift() * 100:+.1f} points")

    print()
    sims = monte_carlo()
    p10, p50, p90 = np.percentile(sims, [10, 50, 90])
    print(f"Monte Carlo, {len(sims):,} draws: mean {sims.mean():,.0f}")
    print(f"  P10 {p10:,.0f}   P50 {p50:,.0f}   P90 {p90:,.0f}")
    print(f"  chance NPV is below zero: {(sims < 0).mean():.0%}")

    print()
    informed = sum(PROBABILITY[n] * max(v, 0) for n, v in outcomes.items())
    print(f"Decide now:          best of build ({expected:,.0f}) or skip (0) "
          f"= {max(expected, 0):,.0f}")
    print(f"Know the lift first: build only when NPV > 0     = {informed:,.0f}")
    print(f"Expected value of perfect information: {informed - max(expected, 0):,.0f}")
