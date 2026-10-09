"""Chapter 19: properties that must hold for every input, checked by Hypothesis."""
from hypothesis import given, settings
from hypothesis import strategies as st

from ch02_domain import ALLOWED, PaymentStatus
from ch03_money import EXPONENT, fee_minor, format_minor, split_minor, to_minor
from ch15_ledger import Ledger, capture, refund
from labs import allocate

amounts = st.integers(min_value=1, max_value=10_000_000)
settings.register_profile("book", derandomize=True, database=None, max_examples=200)
settings.load_profile("book")


@given(amounts)
def test_fee_is_never_negative_and_never_exceeds_the_amount(amount_minor):
    assert 0 <= fee_minor(amount_minor) <= amount_minor


@given(amounts, amounts)
def test_a_bigger_payment_never_has_a_smaller_fee(a, b):
    low, high = sorted((a, b))
    assert fee_minor(low) <= fee_minor(high)


@given(st.integers(min_value=0, max_value=10_000_000),
       st.integers(min_value=1, max_value=50))
def test_split_keeps_every_cent_and_is_fair(total_minor, parts):
    pieces = split_minor(total_minor, parts)
    assert sum(pieces) == total_minor
    assert max(pieces) - min(pieces) <= 1


@given(st.integers(min_value=0, max_value=10_000_000),
       st.lists(st.integers(min_value=0, max_value=1_000), min_size=1, max_size=8)
       .filter(lambda weights: sum(weights) > 0))
def test_allocate_keeps_every_cent(total_minor, weights):
    shares = allocate(total_minor, weights)
    assert sum(shares) == total_minor
    assert all(share >= 0 for share in shares)


@given(st.integers(min_value=0, max_value=10**12), st.sampled_from(sorted(EXPONENT)))
def test_minor_units_survive_a_round_trip_through_text(amount_minor, currency):
    text = format_minor(amount_minor, currency).split()[0]
    assert to_minor(text, currency) == amount_minor


@given(st.lists(st.tuples(amounts, st.booleans()), max_size=30))
def test_ledger_always_balances(events):
    ledger = Ledger()
    for number, (amount, is_refund) in enumerate(events):
        journal = (refund(f"rf_{number}", amount) if is_refund
                   else capture(f"pay_{number}", amount, fee_minor(amount)))
        ledger.post(journal)
    debits, credits = ledger.trial_balance()
    assert debits == credits


@given(st.lists(st.sampled_from(list(PaymentStatus)), max_size=12))
def test_no_path_leaves_a_terminal_state(attempts):
    status = PaymentStatus.CREATED
    for target in attempts:
        if target in ALLOWED[status]:
            status = target
    if not ALLOWED[status]:
        assert all(target not in ALLOWED[status] for target in PaymentStatus)
