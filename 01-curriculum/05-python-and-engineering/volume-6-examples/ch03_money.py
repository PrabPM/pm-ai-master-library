"""Chapter 3: money. Watch float lose a cent, then do it exactly."""
from dataclasses import dataclass
from decimal import (ROUND_DOWN, ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_HALF_UP,
                     ROUND_UP, Decimal)

# How many decimal places each currency uses (its "exponent", from ISO 4217).
EXPONENT = {"USD": 2, "EUR": 2, "JPY": 0, "KWD": 3}


# --- The failure -----------------------------------------------------------
def fee_float(amount: float) -> float:
    """PayFlow's price is 2.9% + $0.30. This version uses float. Do not."""
    return round(amount * 0.029 + 0.30, 2)


# --- The fix ---------------------------------------------------------------
def fee_minor(amount_minor: int, rate: Decimal = Decimal("0.029"),
              fixed_minor: int = 30) -> int:
    """Fee in minor units (cents for USD), rounded half-even, never above amount."""
    raw = Decimal(amount_minor) * rate + fixed_minor
    fee = int(raw.quantize(Decimal("1"), rounding=ROUND_HALF_EVEN))
    return min(fee, amount_minor)


def to_minor(text: str, currency: str) -> int:
    """'120.00' USD -> 12000. Refuses more decimals than the currency has."""
    amount = Decimal(text)  # from a string, never from a float
    scaled = amount.scaleb(EXPONENT[currency])
    if scaled != scaled.to_integral_value():
        raise ValueError(f"{text} has too many decimals for {currency}")
    return int(scaled)


def format_minor(amount_minor: int, currency: str) -> str:
    exp = EXPONENT[currency]
    return f"{Decimal(amount_minor).scaleb(-exp):.{exp}f} {currency}"


@dataclass(frozen=True)
class Money:
    amount_minor: int
    currency: str

    def __add__(self, other: "Money") -> "Money":
        if other.currency != self.currency:
            raise ValueError(f"cannot add {self.currency} and {other.currency}")
        return Money(self.amount_minor + other.amount_minor, self.currency)


def split_minor(total_minor: int, parts: int) -> list[int]:
    """Split so the pieces add back to the total. Early pieces get the extra."""
    base, extra = divmod(total_minor, parts)
    return [base + 1 if i < extra else base for i in range(parts)]


def rounding_table() -> None:
    modes = [ROUND_HALF_EVEN, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_DOWN, ROUND_UP]
    values = ["0.125", "0.135", "0.145", "0.1451", "-0.125"]
    print(f"{'value':>8}" + "".join(f"{m[6:]:>11}" for m in modes))
    for v in values:
        cells = [Decimal(v).quantize(Decimal("0.01"), rounding=m) for m in modes]
        print(f"{v:>8}" + "".join(f"{c!s:>11}" for c in cells))


if __name__ == "__main__":
    print("-- float surprises")
    print("0.1 + 0.2 =", 0.1 + 0.2)
    print("int(19.99 * 100) =", int(19.99 * 100))
    print("Decimal(0.1) =", Decimal(0.1))
    print("Decimal('0.1') =", Decimal("0.1"))

    print("-- one $15.00 breakfast combo")
    print("exact fee: 15.00 * 0.029 + 0.30 =", Decimal("15.00") * Decimal("0.029")
          + Decimal("0.30"))
    print("float fee:", fee_float(15.00))
    print("exact fee, rounded:", format_minor(fee_minor(1500), "USD"))

    print("-- 200 combos in a day")
    float_total = sum(fee_float(15.00) for _ in range(200))
    exact_total = sum(fee_minor(1500) for _ in range(200))
    print("float total:", float_total)
    print("exact total:", format_minor(exact_total, "USD"))
    print("missing:", format_minor(exact_total - round(float_total * 100), "USD"))

    print("-- rounding modes, to 2 places")
    rounding_table()

    print("-- currency exponents")
    for text, cur in [("120.00", "USD"), ("1500", "JPY"), ("4.250", "KWD")]:
        minor = to_minor(text, cur)
        print(f"{text:>7} {cur} -> {minor:>6} minor units -> "
              f"{format_minor(minor, cur)}")
    try:
        to_minor("1500.50", "JPY")
    except ValueError as exc:
        print("refused:", exc)
    try:
        Money(12_000, "USD") + Money(1500, "JPY")
    except ValueError as exc:
        print("refused:", exc)

    print("-- split 100.00 USD three ways")
    naive = [round(100.00 / 3, 2)] * 3
    print("naive:", naive, "sum =", round(sum(naive), 2))
    exact = split_minor(10_000, 3)
    print("exact:", exact, "sum =", sum(exact))
