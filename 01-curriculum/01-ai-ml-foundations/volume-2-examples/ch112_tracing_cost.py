"""Chapter 112: one request as a tree of spans, with cost attributed per span.

The run is simulated with a fake clock, so the numbers are the same every time.
Prices are illustrative, not any vendor's price list.
"""
from contextlib import contextmanager

import numpy as np

# Illustrative USD per million tokens: (input, output).
PRICES = {"embed-s": (0.10, 0.00), "small": (0.50, 1.50), "large": (3.00, 15.00)}


class Tracer:
    def __init__(self):
        self.clock_ms, self.spans, self.open = 0, [], []

    @contextmanager
    def span(self, name, **attrs):
        s = {"id": len(self.spans) + 1, "name": name, "start": self.clock_ms,
             "parent": self.open[-1] if self.open else None, **attrs}
        self.spans.append(s)
        self.open.append(s["id"])
        yield s
        self.open.pop()
        s["end"] = self.clock_ms

    def work(self, ms):
        self.clock_ms += ms


def cost(span):
    p_in, p_out = PRICES.get(span.get("model"), (0.0, 0.0))
    return (span.get("tokens_in", 0) * p_in + span.get("tokens_out", 0) * p_out) / 1e6


def simulated_request(t):
    with t.span("request", tenant="m_juniper"):
        with t.span("retrieve", model="embed-s", tokens_in=800):
            t.work(120)
        with t.span("plan", model="small", tokens_in=1200, tokens_out=150):
            t.work(400)
        with t.span("tool get_payout_status"):
            t.work(180)
        with t.span("tool get_merchant_profile"):
            t.work(140)
        with t.span("synthesize", model="large", tokens_in=3200, tokens_out=400):
            t.work(1800)
    return t.spans


def trace_cost(loops):
    """Cost of a run that goes around plan -> tools -> synthesize `loops` times.
    Each extra round re-reads a context that has grown by 400 tokens."""
    embed = 800 * 0.10 / 1e6
    plan = (1200 * 0.50 + 150 * 1.50) / 1e6
    rounds = sum(plan + ((3200 + 400 * t) * 3.00 + 400 * 15.00) / 1e6
                 for t in range(loops))
    return embed + rounds


if __name__ == "__main__":
    spans = simulated_request(Tracer())
    total = sum(cost(s) for s in spans)
    print(f"{'span':<28}{'parent':>6}{'ms':>6}{'in':>6}{'out':>5}"
          f"{'cost USD':>10}{'share':>7}")
    for s in spans:
        name = ("  " if s["parent"] else "") + s["name"]
        print(f"{name:<28}{s['parent'] or '-':>6}{s['end'] - s['start']:>6}"
              f"{s.get('tokens_in', 0):>6}{s.get('tokens_out', 0):>5}"
              f"{cost(s):>10.6f}{cost(s) / total:>7.1%}")
    print(f"trace total: USD {total:.6f}; at 2,000,000 requests a month: "
          f"USD {total * 2e6:,.0f}")

    # Many runs: most go around once, a few get stuck and loop many times.
    rng = np.random.default_rng(11)
    loops = np.minimum(rng.geometric(0.7, size=10_000), 14)
    costs = np.array([trace_cost(k) for k in loops])
    top = np.sort(costs)[-100:]                       # the costliest 1%
    print(f"stuck run with 14 rounds: USD {trace_cost(14):.4f} "
          f"({trace_cost(14) / total:.0f}x a normal run)")
    print(f"10,000 runs: median USD {np.median(costs):.4f}, "
          f"p99 USD {np.percentile(costs, 99):.4f}, "
          f"costliest 1% = {top.sum() / costs.sum():.1%} of spend")

    by_name = {s["name"]: cost(s) for s in spans}
    assert np.isclose(by_name["retrieve"], 0.00008)
    assert np.isclose(by_name["plan"], 0.000825)
    assert np.isclose(by_name["synthesize"], 0.0156)
    assert np.isclose(total, 0.016505)
    assert np.isclose(total * 2e6, 33_010)
    assert np.isclose(trace_cost(1), total)
    assert np.isclose(trace_cost(14), 0.33923)
    assert spans[0]["end"] == 2640 and spans[-1]["end"] - spans[-1]["start"] == 1800
