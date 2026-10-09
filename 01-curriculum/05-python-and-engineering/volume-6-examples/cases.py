"""Chapter 25: the worked cases, built from the chapter modules."""
from datetime import datetime

from ch03_money import fee_minor, format_minor
from ch04_time_ids import settlement_date
from ch10_idempotency import PaymentsApi
from ch14_workers import Queue
from ch15_ledger import HARBOR, Journal, Entry, Ledger, capture
from ch16_reconciliation import Record, reconcile
from fake_provider import FakeProvider, ProviderTimeout, ProviderUnavailable


# --- Case 1: recover after a provider timeout -------------------------------
def case_timeout_recovery() -> None:
    plan = ["ok", "timeout_after_work", "timeout_before_work", "ok",
            "timeout_after_work", "unavailable"]
    orders = {f"order-78{n:02d}": {"amount_minor": amount, "currency": "USD",
                                   "card_token": "tok_visa_4242"}
              for n, amount in enumerate([12_000, 4_500, 1_500, 8_900, 2_500, 6_000])}
    bank = FakeProvider(plan=list(plan))
    api = PaymentsApi(bank)
    unknown: list[str] = []
    for key, order in orders.items():           # 14:05, NorthBank starts timing out
        try:
            api.create_payment("m_harbor", key, order, now=0)
        except (ProviderTimeout, ProviderUnavailable):
            unknown.append(key)
    print("answered at 14:05:", len(orders) - len(unknown), "of", len(orders))
    print("outcome unknown:", ", ".join(unknown))
    print("charges at the bank so far:", len(bank.charges))

    for key in unknown:                         # 14:20, the recovery sweep
        result = api.create_payment("m_harbor", key, orders[key], now=900)
        print(f"sweep {key}: {result['status']} {result['provider_ref']}")
    print("charges at the bank after the sweep:", len(bank.charges), "for",
          len(orders), "orders")

    careless = FakeProvider(plan=list(plan))    # the same afternoon without keys
    failed = []
    for order in orders.values():
        try:
            careless.authorize(order["amount_minor"], "USD", order["card_token"])
        except (ProviderTimeout, ProviderUnavailable):
            failed.append(order)
    for order in failed:                        # "just retry the failures"
        careless.authorize(order["amount_minor"], "USD", order["card_token"])
    print("same afternoon without keys:", len(careless.charges), "charges for",
          len(orders), "orders")


# --- Case 2: run a daily settlement and reconcile it ------------------------
CAPTURES = [   # (payment, NorthBank reference, amount, captured at, UTC)
    ("pay_1001", "nb_0001", 12_000, "2026-07-13T14:05:09+00:00"),
    ("pay_1002", "nb_0002", 4_500, "2026-07-13T14:20:41+00:00"),
    ("pay_1003", "nb_0003", 8_900, "2026-07-13T20:59:58+00:00"),   # 16:59:58 local
    ("pay_1004", "nb_0004", 2_500, "2026-07-13T21:00:03+00:00"),   # 17:00:03 local
]
BANK_FILE = [Record("nb_0001", 12_000, ""), Record("nb_0002", 4_500, ""),
             Record("nb_0003", 8_900, "")]


def in_batch(captured_at: str, business_date: str) -> bool:
    instant = datetime.fromisoformat(captured_at)
    return settlement_date(instant).isoformat() == business_date


def settle(ledger: Ledger, business_date: str, bank_file: list[Record]) -> dict:
    """Post one business date: captures, bank receipt, payout. Safe to run twice."""
    batch = [c for c in CAPTURES if in_batch(c[3], business_date)]
    gross = fees = 0
    for payment_id, _, amount, _ in batch:
        fee = fee_minor(amount)
        ledger.post(capture(payment_id, amount, fee))      # no-op if posted before
        gross, fees = gross + amount, fees + fee
    breaks = reconcile([Record(ref, amount, at) for _, ref, amount, at in batch],
                       bank_file)
    summary = {"payments": len(batch), "gross": gross, "fees": fees,
               "net": gross - fees, "breaks": breaks, "payout_posted": False}
    if breaks:
        return summary                                     # hold the payout
    ledger.post(Journal(f"stl:northbank:{business_date}", "bank receipt", (
        Entry("cash", debit_minor=gross),
        Entry("due_from_northbank", credit_minor=gross))))
    summary["payout_posted"] = ledger.post(Journal(
        f"po:m_harbor:{business_date}", "payout", (
            Entry(HARBOR, debit_minor=gross - fees),
            Entry("cash", credit_minor=gross - fees))))
    return summary


def case_daily_settlement() -> None:
    short_file = BANK_FILE[:2] + [Record("nb_0003", 8_890, "")]
    held = settle(Ledger(), "2026-07-13", short_file)
    print("bank file ten cents short:", held["breaks"])
    print("  payout posted:", held["payout_posted"])

    ledger = Ledger()
    first = settle(ledger, "2026-07-13", BANK_FILE)
    print("payments in the 2026-07-13 batch:", first["payments"], "of", len(CAPTURES))
    for name in ("gross", "fees", "net"):
        print(f"  {name:<6}{format_minor(first[name], 'USD'):>12}")
    print("breaks:", first["breaks"], "| payout posted:", first["payout_posted"])
    again = settle(ledger, "2026-07-13", BANK_FILE)
    print("second run posted a payout:", again["payout_posted"])
    print("cash:", ledger.balance("cash"), "| owed to Harbor:", ledger.balance(HARBOR),
          "| fee revenue:", ledger.balance("fee_revenue"))


# --- Case 3: trace a stuck payout --------------------------------------------
def case_stuck_payout() -> None:
    queue = Queue(visibility_timeout=30, max_receives=3)
    queue.send("send payout po_0714 to Harbor Coffee")
    now, errors = 0.0, []
    while (message := queue.receive(now)) is not None:
        errors.append("bank rejected: account closed")   # will never succeed
        now += 31
    queue.receive(now)
    print("payout status in the database: processing (for six hours)")
    print("outbox row for po_0714: published")
    print("main queue depth:", len(queue.messages))
    print("dead-letter queue:", [m.body for m in queue.dead_letters])
    print("attempts:", len(errors), "| every error:", set(errors))


if __name__ == "__main__":
    for title, case in (("Case 1", case_timeout_recovery),
                        ("Case 2", case_daily_settlement),
                        ("Case 3", case_stuck_payout)):
        print(f"== {title}")
        case()
