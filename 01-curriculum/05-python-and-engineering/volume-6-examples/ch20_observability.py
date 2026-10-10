"""Chapter 20: observability. RED metrics, an SLI, an error budget and a trace."""
import random
from contextlib import contextmanager
from dataclasses import dataclass

WINDOW_SECONDS = 300          # five minutes of traffic
SLO_TARGET = 0.995            # 99.5% of valid requests answered well
SLOW_MS = 2_000


@dataclass(frozen=True)
class RequestEvent:
    http_status: int
    latency_ms: int


def make_traffic(count: int = 2_000, seed: int = 20) -> list[RequestEvent]:
    """Invented traffic for payments-api: mostly fine, a few declines and failures."""
    rng = random.Random(seed)
    events = []
    for _ in range(count):
        status = rng.choices([200, 402, 503, 500], weights=[860, 124, 12, 4])[0]
        latency = int(rng.lognormvariate(5.1, 0.45))
        if status == 503 or rng.random() < 0.006:
            latency += rng.randrange(1_900, 4_000)     # timeouts and slow outliers
        events.append(RequestEvent(status, latency))
    return events


def percentile(sorted_values: list[int], fraction: float) -> int:
    index = min(len(sorted_values) - 1, int(fraction * len(sorted_values)))
    return sorted_values[index]


def is_good(event: RequestEvent) -> bool:
    """Good = the caller got a correct answer in time. A decline is a correct answer."""
    return event.http_status < 500 and event.latency_ms <= SLOW_MS


class Tracer:
    """A toy tracer: nested spans with a fake clock, printed as a tree."""

    def __init__(self) -> None:
        self.clock, self.depth, self.lines = 0, 0, []

    @contextmanager
    def span(self, name: str, own_ms: int = 0):
        start, slot = self.clock, len(self.lines)
        self.lines.append("")
        self.depth += 1
        self.clock += own_ms
        try:
            yield
        finally:
            self.depth -= 1
            label = "  " * self.depth + name
            self.lines[slot] = f"{label:<40}{self.clock - start:>5} ms"


if __name__ == "__main__":
    events = make_traffic()
    latencies = sorted(e.latency_ms for e in events)
    declines = sum(e.http_status == 402 for e in events)
    server_errors = sum(e.http_status >= 500 for e in events)

    print("-- RED for payments-api, 14:00 to 14:05 UTC")
    print(f"rate:     {len(events) / WINDOW_SECONDS:.1f} requests per second")
    print(f"errors:   {server_errors / len(events):.1%} server errors"
          f" (declines, not errors: {declines / len(events):.1%})")
    print(f"duration: mean {sum(latencies) // len(latencies)} ms | "
          f"p50 {percentile(latencies, 0.50)} ms | p95 {percentile(latencies, 0.95)} ms"
          f" | p99 {percentile(latencies, 0.99)} ms")

    print("-- SLI and error budget")
    naive = sum(e.http_status == 200 for e in events) / len(events)
    good = sum(is_good(e) for e in events)
    sli = good / len(events)
    allowed_bad = (1 - SLO_TARGET) * len(events)
    print(f"if every non-200 counted as bad: {naive:.1%}")
    print(f"SLI, correct answer within 2 s:  {sli:.2%} (target {SLO_TARGET:.1%})")
    print(f"bad requests: {len(events) - good}, "
          f"budget for this window: {allowed_bad:.0f}")
    print(f"burn rate: {(1 - sli) / (1 - SLO_TARGET):.1f}x")

    print("-- one slow request, as a trace (trace_id 4bf92f3577b34da6)")
    tracer = Tracer()
    with tracer.span("payments-api POST /payments", own_ms=4):
        with tracer.span("db: claim idempotency key", own_ms=6):
            pass
        with tracer.span("northbank: authorize", own_ms=2_310):
            pass
        with tracer.span("db: store result + outbox row", own_ms=9):
            pass
    print("\n".join(tracer.lines))
