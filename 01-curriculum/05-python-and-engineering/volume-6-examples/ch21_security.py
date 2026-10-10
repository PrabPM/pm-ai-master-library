"""Chapter 21: three small security failures and their fixes."""
import ipaddress
import random
import sqlite3
from urllib.parse import urlsplit


# --- 1. SQL injection ------------------------------------------------------
def new_db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE payments (id TEXT, merchant_id TEXT, amount_minor INT)")
    db.executemany("INSERT INTO payments VALUES (?, ?, ?)", [
        ("pay_1001", "m_harbor", 12_000), ("pay_1002", "m_harbor", 4_500),
        ("pay_0999", "m_kumo", 1_500), ("pay_0998", "m_dune", 4_250)])
    return db


def list_payments_unsafe(db: sqlite3.Connection, merchant_id: str) -> list[str]:
    query = f"SELECT id FROM payments WHERE merchant_id = '{merchant_id}'"
    return [row[0] for row in db.execute(query)]


def list_payments_safe(db: sqlite3.Connection, merchant_id: str) -> list[str]:
    query = "SELECT id FROM payments WHERE merchant_id = ?"
    return [row[0] for row in db.execute(query, (merchant_id,))]


# --- 2. Server-side request forgery through a merchant's webhook URL --------
def webhook_url_problem(url: str) -> str | None:
    """Return why PayFlow must not call this URL, or None if it looks acceptable."""
    parts = urlsplit(url)
    if parts.scheme != "https":
        return "must use https"
    try:
        address = ipaddress.ip_address(parts.hostname or "")
    except ValueError:
        return None  # a hostname: production must also check what it resolves to
    if not address.is_global:
        return f"{address} is not a public address"
    return None


# --- 3. Tokenization: keep the card number in exactly one place ------------
class TokenVault:
    """The only component allowed to hold card numbers."""

    def __init__(self, seed: int = 21) -> None:
        self._rng = random.Random(seed)   # repeatable demo; production uses a CSPRNG
        self._pans: dict[str, str] = {}

    def tokenize(self, pan: str) -> dict:
        token = f"tok_{self._rng.getrandbits(64):016x}"
        self._pans[token] = pan
        return {"token": token, "last4": pan[-4:]}


if __name__ == "__main__":
    db = new_db()
    attack = "m_harbor' OR '1'='1"
    print("-- SQL injection")
    print("query built by string formatting:", list_payments_unsafe(db, attack))
    print("parameterized query:             ", list_payments_safe(db, attack))
    print("parameterized, honest input:     ", list_payments_safe(db, "m_harbor"))

    print("-- merchant-supplied webhook URLs")
    for url in ("https://hooks.harborcoffee.example/payflow",
                "http://hooks.harborcoffee.example/payflow",
                "https://169.254.169.254/latest/meta-data/",
                "https://10.0.4.17/admin", "https://127.0.0.1:8443/"):
        print(f"{url:<44} {webhook_url_problem(url) or 'ok'}")

    print("-- tokenization")
    vault = TokenVault()
    card = vault.tokenize("4111111111111111")
    print("what every other service stores:", card)
