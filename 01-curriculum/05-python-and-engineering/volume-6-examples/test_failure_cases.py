"""Chapter 19: one test per failure that payment systems meet in production."""
import json
import sqlite3
from datetime import datetime

import pytest

from ch02_domain import IllegalTransition, Payment, PaymentStatus, transition
from ch03_money import to_minor
from ch04_time_ids import settlement_date
from ch10_idempotency import IdempotencyConflict, PaymentsApi, RequestInProgress
from ch11_webhooks import SECRET, RejectedWebhook, WebhookReceiver, sign, verify
from ch13_outbox_saga import LedgerConsumer, capture_with_outbox, new_db, relay
from ch15_ledger import HARBOR, Ledger, capture, reverse
from ch23_deploy import contract, expand, new_code_reads, old_code_reads
from ch23_deploy import new_db as new_payments_db
from fake_provider import FakeProvider, ProviderTimeout
from labs import Refund, RefundRejected, add_refund

ORDER = {"amount_minor": 12_000, "currency": "USD", "card_token": "tok_visa_4242"}
NOW = 1_783_951_509


def event(event_id: str, status: str) -> bytes:
    return json.dumps({"id": event_id, "payment_id": "pay_1001",
                       "status": status}).encode()


def test_duplicate_delivery_is_applied_once():
    receiver, raw = WebhookReceiver(), event("evt_1", "captured")
    assert receiver.receive(sign(SECRET, NOW, raw), raw, NOW) == 200
    assert receiver.receive(sign(SECRET, NOW, raw), raw, NOW) == 200
    assert sum("applied" in line for line in receiver.log) == 1


def test_timeout_after_provider_success_charges_once():
    bank = FakeProvider(plan=["timeout_after_work"])
    api = PaymentsApi(bank)
    with pytest.raises(ProviderTimeout):
        api.create_payment("m_harbor", "order-1", ORDER, now=0)
    retry = api.create_payment("m_harbor", "order-1", ORDER, now=5)
    assert retry["status"] == "authorized"
    assert len(bank.charges) == 1


def test_out_of_order_webhooks_never_move_a_payment_backwards():
    receiver = WebhookReceiver()
    for raw in (event("evt_2", "captured"), event("evt_1", "authorized")):
        receiver.receive(sign(SECRET, NOW, raw), raw, NOW)
    assert receiver.status["pay_1001"] == "captured"


def test_partial_refunds_cannot_exceed_the_payment():
    refunds = add_refund(12_000, [], Refund("rf_1", 7_000))
    with pytest.raises(RefundRejected):
        add_refund(12_000, refunds, Refund("rf_2", 5_001))
    assert add_refund(12_000, refunds, Refund("rf_1", 7_000)) == refunds


def test_reversal_restores_balances_without_deleting_history():
    ledger, journal = Ledger(), capture("pay_1001", 12_000, 378)
    ledger.post(journal)
    ledger.post(reverse(journal, "posted in error"))
    assert ledger.balance(HARBOR) == 0
    assert len(ledger.journal_ids()) == 2


def test_clock_boundary_one_second_either_side_of_cutoff():
    before = datetime.fromisoformat("2026-07-13T20:59:59+00:00")
    at_cutoff = datetime.fromisoformat("2026-07-13T21:00:00+00:00")
    assert settlement_date(before).isoformat() == "2026-07-13"
    assert settlement_date(at_cutoff).isoformat() == "2026-07-14"


def test_currency_scale_is_enforced():
    assert to_minor("1500", "JPY") == 1500
    assert to_minor("4.250", "KWD") == 4250
    with pytest.raises(ValueError):
        to_minor("10.999", "USD")


def test_concurrent_same_key_requests_do_not_both_run():
    bank = FakeProvider()
    api = PaymentsApi(bank)
    outcomes = []

    def second_request():
        with pytest.raises(RequestInProgress):
            api.create_payment("m_harbor", "order-2", ORDER, now=0.5)
        outcomes.append("second refused")

    bank.on_call = second_request
    api.create_payment("m_harbor", "order-2", ORDER, now=0)
    assert outcomes == ["second refused"] and len(bank.charges) == 1
    with pytest.raises(IdempotencyConflict):
        api.create_payment("m_harbor", "order-2", ORDER | {"amount_minor": 1}, now=1)


def test_migration_can_be_rolled_back_until_contract():
    db = new_payments_db()
    expand(db)
    assert old_code_reads(db) == new_code_reads(db) == 12_000   # rollback is safe
    contract(db)
    with pytest.raises(sqlite3.OperationalError):
        old_code_reads(db)                                      # now it is not


def test_replayed_events_and_webhooks_do_no_extra_work():
    db, queue, ledger = new_db(), [], LedgerConsumer()
    capture_with_outbox(db)
    relay(db, queue)
    for delivered in queue * 3:
        ledger.handle(delivered)
    assert ledger.postings == 1
    raw = event("evt_9", "captured")
    with pytest.raises(RejectedWebhook):
        verify(SECRET, sign(SECRET, NOW, raw), raw, NOW + 3600)


def test_state_machine_refuses_to_revive_a_settled_payment():
    created = datetime.fromisoformat("2026-07-13T14:05:00+00:00")
    payment = Payment("pay_1001", "m_harbor", 12_000, "USD", created)
    for step in ("authorized", "captured", "settled"):
        payment = transition(payment, PaymentStatus(step))
    with pytest.raises(IllegalTransition):
        transition(payment, PaymentStatus.AUTHORIZED)
