"""Chapter 24: tests for the lab model answers."""
from datetime import datetime

import polars as pl
import pytest

from ch04_time_ids import NEW_YORK
from labs import (CircuitBreaker, CircuitOpen, Refund, TokenBucket, add_refund,
                  allocate, misreported, naive_window, quality_problems, refund_state,
                  true_window)


def test_allocate_examples():
    assert allocate(9_003, [50, 30, 20]) == [4_501, 2_701, 1_801]
    assert allocate(1_000, [1, 1, 1]) == [334, 333, 333]
    assert allocate(0, [1, 2]) == [0, 0]
    with pytest.raises(ValueError):
        allocate(100, [0, 0])


def test_naive_window_misreports_summer_midnight_sales():
    sale = datetime(2026, 7, 14, 0, 30, tzinfo=NEW_YORK)
    assert misreported([sale], naive_window) == [sale.isoformat()]
    assert misreported([sale], true_window) == []


def test_refund_states():
    refunds = add_refund(12_000, [], Refund("rf_1", 2_000))
    assert refund_state(12_000, refunds) == "partial"
    refunds = add_refund(12_000, refunds, Refund("rf_2", 10_000))
    assert refund_state(12_000, refunds) == "full"
    assert refund_state(12_000, []) == "none"


def test_token_bucket_refills_at_its_rate():
    bucket = TokenBucket(rate_per_second=2, burst=5)
    assert [bucket.allow(0.0)[0] for _ in range(6)] == [True] * 5 + [False]
    assert bucket.allow(0.0)[1] == pytest.approx(0.5)
    assert bucket.allow(0.5)[0] is True


def test_circuit_breaker_opens_then_recovers():
    breaker = CircuitBreaker(failure_threshold=2, reset_after=10)

    def fail():
        raise ConnectionError

    for now in (0, 1):
        with pytest.raises(ConnectionError):
            breaker.call(fail, now)
    with pytest.raises(CircuitOpen):
        breaker.call(lambda: "ok", 5)
    assert breaker.state(11) == "half-open"
    assert breaker.call(lambda: "ok", 11) == "ok"
    assert breaker.state(12) == "closed"


def test_quality_gate_passes_a_clean_file():
    clean = pl.DataFrame({"ref": ["nb_1", "nb_2"], "amount_minor": [100, 200],
                          "currency": ["USD", "JPY"]})
    assert quality_problems(clean) == {}
