"""Chapter 10: idempotency. Charge twice by accident, then make it impossible."""
import hashlib
import json
import sqlite3

from fake_provider import FakeProvider, ProviderTimeout

LOCK_SECONDS = 30


# --- The failure -----------------------------------------------------------
def pay_without_key(bank: FakeProvider, payload: dict) -> str:
    result = bank.authorize(payload["amount_minor"], payload["currency"],
                            payload["card_token"])
    return result.provider_ref


# --- The fix ---------------------------------------------------------------
class IdempotencyConflict(Exception):
    """Same key, different request. The caller has a bug; refuse loudly."""


class RequestInProgress(Exception):
    """Same key, and the first attempt has not finished yet."""


def payload_hash(payload: dict) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


class PaymentsApi:
    def __init__(self, bank: FakeProvider) -> None:
        self.bank = bank
        self.db = sqlite3.connect(":memory:")
        self.db.execute("""CREATE TABLE idempotency_keys (
            merchant_id TEXT NOT NULL, key TEXT NOT NULL, payload_hash TEXT NOT NULL,
            locked_until REAL NOT NULL, response TEXT,
            PRIMARY KEY (merchant_id, key))""")

    def claim(self, merchant_id: str, key: str, digest: str, now: float) -> dict | None:
        """Return a stored response to replay, or None if the caller should proceed."""
        try:
            with self.db:  # short transaction: try to be the first
                self.db.execute(
                    "INSERT INTO idempotency_keys VALUES (?, ?, ?, ?, NULL)",
                    (merchant_id, key, digest, now + LOCK_SECONDS))
            return None
        except sqlite3.IntegrityError:
            pass  # someone used this key before: decide which case this is
        stored_hash, locked_until, response = self.db.execute(
            "SELECT payload_hash, locked_until, response FROM idempotency_keys"
            " WHERE merchant_id = ? AND key = ?", (merchant_id, key)).fetchone()
        if stored_hash != digest:
            raise IdempotencyConflict("key reused with a different payload")
        if response is not None:
            return json.loads(response) | {"replayed": True}
        if now < locked_until:
            raise RequestInProgress("first attempt still running")
        self.set_lock(merchant_id, key, now + LOCK_SECONDS)  # take over a dead attempt
        return None

    def set_lock(self, merchant_id: str, key: str, until: float) -> None:
        with self.db:
            self.db.execute("UPDATE idempotency_keys SET locked_until = ?"
                            " WHERE merchant_id = ? AND key = ?",
                            (until, merchant_id, key))

    def create_payment(self, merchant_id: str, key: str, payload: dict,
                       now: float = 0.0) -> dict:
        replay = self.claim(merchant_id, key, payload_hash(payload), now)
        if replay is not None:
            return replay
        try:
            result = self.bank.authorize(  # no database transaction is open here
                payload["amount_minor"], payload["currency"], payload["card_token"],
                idempotency_key=f"{merchant_id}:{key}")
        except ProviderTimeout:
            self.set_lock(merchant_id, key, now)  # unlock so a retry can take over
            raise
        response = {"status": "authorized" if result.approved else "declined",
                    "provider_ref": result.provider_ref}
        with self.db:  # short transaction: store the answer for future retries
            self.db.execute("UPDATE idempotency_keys SET response = ?"
                            " WHERE merchant_id = ? AND key = ?",
                            (json.dumps(response), merchant_id, key))
        return response


if __name__ == "__main__":
    order = {"amount_minor": 12_000, "currency": "USD", "card_token": "tok_visa_4242"}

    print("-- without an idempotency key")
    bank = FakeProvider(plan=["timeout_after_work"])
    try:
        pay_without_key(bank, order)
    except ProviderTimeout as exc:
        print("attempt 1:", exc, "-> the checkout page retries")
    print("attempt 2:", pay_without_key(bank, order))
    print("charges at the bank:", [c["ref"] for c in bank.charges])

    print("-- with an idempotency key")
    bank = FakeProvider(plan=["timeout_after_work"])
    api = PaymentsApi(bank)
    try:
        api.create_payment("m_harbor", "order-7781", order, now=0)
    except ProviderTimeout as exc:
        print("attempt 1:", exc, "-> the checkout page retries")
    print("attempt 2:", api.create_payment("m_harbor", "order-7781", order, now=3))
    print("attempt 3:", api.create_payment("m_harbor", "order-7781", order, now=9))
    print("charges at the bank:", [c["ref"] for c in bank.charges])

    print("-- same key, different amount")
    try:
        api.create_payment("m_harbor", "order-7781", order | {"amount_minor": 99_000})
    except IdempotencyConflict as exc:
        print("refused:", exc)

    print("-- same key arrives again while the first attempt is at the bank")
    def impatient_double_click() -> None:
        try:
            api.create_payment("m_harbor", "order-7782", order, now=20.5)
        except RequestInProgress as exc:
            print("second request refused:", exc)
    bank.on_call = impatient_double_click
    print("first request:", api.create_payment("m_harbor", "order-7782", order, now=20))

    print("-- same key, different merchant")
    print(api.create_payment("m_kumo", "order-7781",
                             {"amount_minor": 1_500, "currency": "JPY",
                              "card_token": "tok_jcb_3530"}))
    print("charges at the bank:", [c["ref"] for c in bank.charges])
