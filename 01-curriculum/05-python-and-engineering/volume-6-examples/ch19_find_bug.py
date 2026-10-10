"""Chapter 19: let Hypothesis find the payment nobody thought to test."""
from decimal import ROUND_HALF_EVEN, Decimal

from hypothesis import given, settings
from hypothesis import strategies as st


def fee_minor_v1(amount_minor: int) -> int:
    """The first version of PayFlow's fee: 2.9% + 30 cents. It looks right."""
    raw = Decimal(amount_minor) * Decimal("0.029") + 30
    return int(raw.quantize(Decimal("1"), rounding=ROUND_HALF_EVEN))


def test_examples() -> None:
    """The tests written by hand. All three pass."""
    assert fee_minor_v1(12_000) == 378
    assert fee_minor_v1(4_500) == 160
    assert fee_minor_v1(1_500) == 74


@settings(derandomize=True, database=None)
@given(st.integers(min_value=1, max_value=10_000_000))
def test_fee_never_exceeds_amount(amount_minor: int) -> None:
    """A rule that must hold for EVERY amount, not just the ones we thought of."""
    assert 0 <= fee_minor_v1(amount_minor) <= amount_minor


if __name__ == "__main__":
    test_examples()
    print("three hand-written examples: pass")
    try:
        test_fee_never_exceeds_amount()
        print("property: pass")
    except AssertionError as failure:
        print("property: FAIL")
        for note in failure.__notes__:
            print(note)
    print("fee on a 1-cent payment:", fee_minor_v1(1), "cents")
    print("fee on a 20-cent payment:", fee_minor_v1(20), "cents")
