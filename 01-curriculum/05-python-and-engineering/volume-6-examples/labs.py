"""Chapter 24: model answers for the code labs. Run this file to see every output."""
from dataclasses import dataclass, field, replace
from datetime import UTC, date, datetime, time, timedelta, timezone

import polars as pl

from ch04_time_ids import NEW_YORK, local_day_in_utc
from ch15_ledger import HARBOR, Ledger, capture, reverse


# --- Lab 1: split a payment by weights -------------------------------------
def allocate(total_minor: int, weights: list[int]) -> list[int]:
    """Largest-remainder split: floors first, then leftover units to the largest
    remainders. The parts always add back to the total."""
    if total_minor < 0 or not weights or min(weights) < 0 or sum(weights) == 0:
        raise ValueError("need a non-negative total and positive total weight")
    weight_sum = sum(weights)
    shares = [total_minor * w // weight_sum for w in weights]
    leftover = total_minor - sum(shares)
    by_remainder = sorted(range(len(weights)),
                          key=lambda i: (-(total_minor * weights[i] % weight_sum), i))
    for index in by_remainder[:leftover]:
        shares[index] += 1
    return shares


# --- Lab 2: the test that catches the 24-hour bug --------------------------
FIXED_EST = timezone(timedelta(hours=-5))


def naive_window(day: date) -> tuple[datetime, datetime]:
    """The buggy job: assumes New York is always UTC-5 and every day has 24 hours."""
    start = datetime.combine(day, time.min, tzinfo=FIXED_EST).astimezone(UTC)
    return start, start + timedelta(hours=24)


def true_window(day: date) -> tuple[datetime, datetime]:
    return local_day_in_utc(day, NEW_YORK)


def report_day(instant: datetime, window) -> date:
    """Which report day does `window` put this instant in?"""
    guess = instant.astimezone(UTC).date()
    for offset in (-1, 0, 1):
        day = guess + timedelta(days=offset)
        start, end = window(day)
        if start <= instant < end:
            return day
    raise AssertionError("no window contains the instant")


def misreported(sales: list[datetime], window) -> list[str]:
    """The test: every sale must be reported on its New York calendar date."""
    return [sale.isoformat() for sale in sales
            if report_day(sale, window) != sale.astimezone(NEW_YORK).date()]


# --- Lab 3: partial refunds ------------------------------------------------
class RefundRejected(Exception):
    pass


@dataclass(frozen=True)
class Refund:
    refund_id: str
    amount_minor: int


def add_refund(payment_minor: int, refunds: list[Refund], new: Refund) -> list[Refund]:
    """Return the new refund list. A repeated refund_id changes nothing."""
    if any(r.refund_id == new.refund_id for r in refunds):
        return refunds
    already = sum(r.amount_minor for r in refunds)
    if new.amount_minor <= 0:
        raise RefundRejected("refund must be positive")
    if already + new.amount_minor > payment_minor:
        raise RefundRejected(
            f"only {payment_minor - already} left to refund, asked {new.amount_minor}")
    return refunds + [new]


def refund_state(payment_minor: int, refunds: list[Refund]) -> str:
    refunded = sum(r.amount_minor for r in refunds)
    if refunded == 0:
        return "none"
    return "full" if refunded == payment_minor else "partial"


# --- Lab 5: a token-bucket rate limiter ------------------------------------
@dataclass
class TokenBucket:
    rate_per_second: float
    burst: int
    tokens: float = field(init=False)
    updated: float = 0.0

    def __post_init__(self) -> None:
        self.tokens = float(self.burst)

    def allow(self, now: float) -> tuple[bool, float]:
        """Returns (allowed, seconds to wait before the next token)."""
        elapsed = now - self.updated
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate_per_second)
        self.updated = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True, 0.0
        return False, (1 - self.tokens) / self.rate_per_second


# --- Lab 6: a circuit breaker ----------------------------------------------
class CircuitOpen(Exception):
    pass


@dataclass
class CircuitBreaker:
    failure_threshold: int = 3
    reset_after: float = 30.0
    failures: int = 0
    opened_at: float | None = None

    def state(self, now: float) -> str:
        if self.opened_at is None:
            return "closed"
        return "half-open" if now - self.opened_at >= self.reset_after else "open"

    def call(self, action, now: float):
        if self.state(now) == "open":
            raise CircuitOpen("failing fast; the bank is not being called")
        try:
            result = action()
        except Exception:
            self.failures += 1
            if self.failures >= self.failure_threshold or self.opened_at is not None:
                self.opened_at = now          # open, or re-open after a failed trial
            raise
        self.failures, self.opened_at = 0, None
        return result


# --- Lab 8: a data-quality gate for a settlement file ----------------------
def quality_problems(frame: pl.DataFrame) -> dict[str, int]:
    problems = {
        "duplicate_refs": frame.height - frame["ref"].n_unique(),
        "null_amounts": frame["amount_minor"].null_count(),
        "non_positive_amounts": frame.filter(pl.col("amount_minor") <= 0).height,
        "unknown_currencies": frame.filter(
            ~pl.col("currency").is_in(["USD", "JPY", "KWD"])).height,
        "money_not_integer": 0 if frame.schema["amount_minor"].is_integer() else 1,
    }
    return {name: count for name, count in problems.items() if count}


if __name__ == "__main__":
    print("== Lab 1")
    naive = [round(90.03 * share, 2) for share in (0.5, 0.3, 0.2)]
    print("naive floats:", naive, "sum =", round(sum(naive), 2))
    parts = allocate(9_003, [50, 30, 20])
    print("allocate:    ", parts, "sum =", sum(parts))
    print("1000 JPY three ways:", allocate(1_000, [1, 1, 1]))

    print("== Lab 2")
    sales = [datetime(2026, 1, 15, 0, 30, tzinfo=NEW_YORK),
             datetime(2026, 3, 8, 0, 30, tzinfo=NEW_YORK),
             datetime(2026, 7, 14, 0, 30, tzinfo=NEW_YORK),
             datetime(2026, 11, 1, 0, 30, tzinfo=NEW_YORK),
             datetime(2026, 11, 1, 23, 30, tzinfo=NEW_YORK)]
    print("naive job misreports:", misreported(sales, naive_window))
    print("fixed job misreports:", misreported(sales, true_window))
    print("2026-07-14T00:30 New York is reported by the naive job on",
          report_day(sales[2], naive_window))

    print("== Lab 3")
    refunds: list[Refund] = []
    for refund in (Refund("rf_2001", 2_000), Refund("rf_2002", 5_000),
                   Refund("rf_2001", 2_000), Refund("rf_2003", 6_000),
                   Refund("rf_2004", 5_000)):
        try:
            refunds = add_refund(12_000, refunds, refund)
            print(refund.refund_id, "ok      ->", refund_state(12_000, refunds),
                  f"({sum(r.amount_minor for r in refunds)} refunded)")
        except RefundRejected as exc:
            print(refund.refund_id, "refused:", exc)

    print("== Lab 5")
    bucket = TokenBucket(rate_per_second=2, burst=5)
    arrivals = [0.0] * 7 + [0.5, 1.0, 3.5]
    for now in arrivals:
        allowed, wait = bucket.allow(now)
        print(f"t={now:<4}", "200 ok" if allowed else f"429, retry after {wait:.2f}s")

    print("== Lab 6")
    breaker = CircuitBreaker()

    def bank_call(now: float) -> str:
        if now < 32:
            raise ConnectionError("NorthBank is down")
        return "authorized"

    for now in range(0, 55, 5):
        before = breaker.state(now)
        try:
            outcome = breaker.call(lambda: bank_call(now), now)
        except CircuitOpen:
            outcome = "skipped, failed fast"
        except ConnectionError:
            outcome = "called, failed"
        print(f"t={now:<3} breaker {before:<10} {outcome}")

    print("== Lab 7")
    ledger = Ledger()
    wrong = capture("pay_1001", 12_000, 387)          # fee typed as 3.87, not 3.78
    ledger.post(wrong)
    print("before: owed to Harbor", ledger.balance(HARBOR),
          "| fee revenue", ledger.balance("fee_revenue"))
    ledger.post(reverse(wrong, "fee was 387, should be 378"))
    ledger.post(replace(capture("pay_1001", 12_000, 378),
                        journal_id="pay_1001:capture:v2"))
    print("after:  owed to Harbor", ledger.balance(HARBOR),
          "| fee revenue", ledger.balance("fee_revenue"))
    print("journals kept:", ledger.journal_ids())

    print("== Lab 8")
    bank_file = pl.DataFrame({
        "ref": ["nb_0001", "nb_0002", "nb_0002", "nb_0003", "nb_0004"],
        "amount_minor": [12_000, 4_500, 4_500, None, -900],
        "currency": ["USD", "USD", "USD", "usd", "USD"],
    })
    for name, count in quality_problems(bank_file).items():
        print(f"{name}: {count}")
    print("a file with float money:", quality_problems(pl.DataFrame({
        "ref": ["nb_0001"], "amount_minor": [120.0], "currency": ["USD"]})))
