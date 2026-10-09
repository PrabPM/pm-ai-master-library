"""The Python you need for this book: seven features in one small file."""
import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum
from functools import wraps


# 1. Type hints: say what goes in and what comes out.
def net_minor(amount_minor: int, fee_minor: int) -> int:
    return amount_minor - fee_minor


# 2. Enum: a closed list of allowed values.
class Currency(StrEnum):
    USD = "USD"
    JPY = "JPY"


# 3. Dataclass: a record with named, typed fields. frozen=True means read-only.
@dataclass(frozen=True)
class Charge:
    merchant_id: str
    amount_minor: int
    currency: Currency


# 4. Exception: a named way to stop and say what went wrong.
class ChargeRejected(Exception):
    pass


def check(charge: Charge) -> Charge:
    if charge.amount_minor <= 0:
        raise ChargeRejected("amount must be positive")
    return charge


# 5. Context manager: setup, then cleanup that runs even if the body fails.
@contextmanager
def step(name: str):
    print(f"begin {name}")
    try:
        yield
    finally:
        print(f"end   {name}")


# 6. Decorator: wrap a function to add behavior without editing it.
def announced(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}{args}")
        return func(*args, **kwargs)
    return wrapper


@announced
def double(x: int) -> int:
    return x * 2


# 7. async/await: a function that can pause while it waits.
async def ask_bank(payment_id: str) -> str:
    await asyncio.sleep(0.01)  # pretend to wait for the network
    return f"{payment_id}: approved"


async def ask_two() -> list[str]:
    return await asyncio.gather(ask_bank("pay_1001"), ask_bank("pay_1002"))


if __name__ == "__main__":
    print("1.", net_minor(12_000, 378))
    print("2.", Currency("USD"), [c.value for c in Currency])
    try:
        Currency("usd")
    except ValueError as exc:
        print("   ", exc)
    charge = Charge("m_harbor", 12_000, Currency.USD)
    print("3.", charge)
    try:
        check(Charge("m_harbor", 0, Currency.USD))
    except ChargeRejected as exc:
        print("4. rejected:", exc)
    print("5.")
    with step("capture"):
        print("   working")
    print("6.", double(21))
    print("7.", asyncio.run(ask_two()))
