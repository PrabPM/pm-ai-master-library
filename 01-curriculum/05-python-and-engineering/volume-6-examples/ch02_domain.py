"""Chapter 2: a payment that cannot be put into an illegal state."""
from dataclasses import FrozenInstanceError, dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum


class PaymentStatus(StrEnum):
    CREATED = "created"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    SETTLED = "settled"
    DECLINED = "declined"
    VOIDED = "voided"
    REFUNDED = "refunded"
    CHARGED_BACK = "charged_back"


S = PaymentStatus
ALLOWED: dict[PaymentStatus, frozenset[PaymentStatus]] = {
    S.CREATED: frozenset({S.AUTHORIZED, S.DECLINED}),
    S.AUTHORIZED: frozenset({S.CAPTURED, S.VOIDED}),
    S.CAPTURED: frozenset({S.SETTLED, S.REFUNDED}),
    S.SETTLED: frozenset({S.REFUNDED, S.CHARGED_BACK}),
    S.DECLINED: frozenset(),
    S.VOIDED: frozenset(),
    S.REFUNDED: frozenset(),
    S.CHARGED_BACK: frozenset(),
}


class IllegalTransition(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Payment:
    payment_id: str
    merchant_id: str
    amount_minor: int
    currency: str
    created_at: datetime
    status: PaymentStatus = PaymentStatus.CREATED

    def __post_init__(self) -> None:
        if self.amount_minor <= 0:
            raise ValueError("amount_minor must be positive")
        if self.created_at.tzinfo is None:
            raise ValueError("created_at must be timezone-aware")


def transition(payment: Payment, new: PaymentStatus) -> Payment:
    if new not in ALLOWED[payment.status]:
        raise IllegalTransition(
            f"{payment.payment_id}: {payment.status} -> {new} is not allowed")
    return replace(payment, status=new)


def loose_demo() -> None:
    """The loose version: a dict accepts anything, including nonsense."""
    payment = {"id": "pay_1001", "amount": -120.0, "status": "captrued"}
    payment["status"] = "authorized"  # a settled payment could go backwards too
    print("dict accepted:", payment)


if __name__ == "__main__":
    loose_demo()
    created = datetime(2026, 7, 13, 14, 5, tzinfo=UTC)
    p = Payment("pay_1001", "m_harbor", 12_000, "USD", created)
    for step in (S.AUTHORIZED, S.CAPTURED, S.SETTLED):
        p = transition(p, step)
        print("now", p.status)
    try:
        transition(p, S.AUTHORIZED)
    except IllegalTransition as exc:
        print("refused:", exc)
    try:
        PaymentStatus("captrued")
    except ValueError as exc:
        print("refused:", exc)
    try:
        p.status = S.CREATED  # type: ignore[misc]
    except FrozenInstanceError as exc:
        print("refused:", exc)
    try:
        Payment("pay_1002", "m_harbor", -500, "USD", created)
    except ValueError as exc:
        print("refused:", exc)
