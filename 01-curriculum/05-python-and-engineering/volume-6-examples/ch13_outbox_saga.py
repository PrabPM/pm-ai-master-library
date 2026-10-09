"""Chapter 13: the transactional outbox and sagas."""
import json
import sqlite3
from collections.abc import Callable
from dataclasses import dataclass


class Crash(Exception):
    """Stands in for the process dying at the worst moment."""


def new_db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE payments (id TEXT PRIMARY KEY, status TEXT)")
    db.execute("""CREATE TABLE outbox (event_id TEXT PRIMARY KEY, payload TEXT,
                  published INTEGER NOT NULL DEFAULT 0)""")
    db.execute("INSERT INTO payments VALUES ('pay_1001', 'authorized')")
    db.commit()
    return db


# --- The failure: write to the database, then publish, as two separate steps
def capture_dual_write(db: sqlite3.Connection, queue: list, crash: bool) -> None:
    with db:
        db.execute("UPDATE payments SET status = 'captured' WHERE id = 'pay_1001'")
    if crash:
        raise Crash("process died after commit, before publish")
    queue.append({"event_id": "evt_501", "type": "payment.captured"})


# --- The fix: record the event in the SAME transaction as the state change --
def capture_with_outbox(db: sqlite3.Connection) -> None:
    event = {"event_id": "evt_501", "type": "payment.captured", "payment": "pay_1001"}
    with db:  # both rows commit together or not at all
        db.execute("UPDATE payments SET status = 'captured' WHERE id = 'pay_1001'")
        db.execute("INSERT INTO outbox (event_id, payload) VALUES (?, ?)",
                   (event["event_id"], json.dumps(event)))


def relay(db: sqlite3.Connection, queue: list, crash_before_mark: bool = False) -> int:
    """A separate loop: publish unpublished rows, then mark them. Returns count."""
    rows = db.execute("SELECT event_id, payload FROM outbox"
                      " WHERE published = 0 ORDER BY rowid").fetchall()
    for event_id, payload in rows:
        queue.append(json.loads(payload))
        if crash_before_mark:
            raise Crash("relay died after publish, before marking")
        with db:
            db.execute("UPDATE outbox SET published = 1 WHERE event_id = ?",
                       (event_id,))
    return len(rows)


class LedgerConsumer:
    """Downstream service. Remembers event IDs so a repeat does nothing."""

    def __init__(self) -> None:
        self.seen: set[str] = set()
        self.postings = 0

    def handle(self, event: dict) -> None:
        if event["event_id"] in self.seen:
            return
        self.seen.add(event["event_id"])
        self.postings += 1


# --- Sagas -----------------------------------------------------------------
@dataclass
class Step:
    name: str
    action: Callable[[], None]
    compensate: Callable[[], None] | None = None


def run_saga(steps: list[Step], log: list[str]) -> bool:
    done: list[Step] = []
    for step in steps:
        try:
            step.action()
            log.append(f"did          {step.name}")
            done.append(step)
        except Exception as exc:
            log.append(f"FAILED       {step.name}: {exc}")
            for finished in reversed(done):
                if finished.compensate is not None:
                    finished.compensate()
                    log.append(f"compensated  {finished.name}")
            return False
    return True


def catering_order_saga(courier_available: bool) -> tuple[list[str], list[str]]:
    """A $120.00 catering order: capture the payment, book a courier, confirm."""
    statement: list[str] = []  # what the shopper's card statement will show

    def capture() -> None:
        statement.append("charge $120.00")

    def refund() -> None:  # a new business action, not a deletion
        statement.append("refund $120.00")

    def book_courier() -> None:
        if not courier_available:
            raise RuntimeError("no courier available")

    log: list[str] = []
    run_saga([Step("capture payment", capture, compensate=refund),
              Step("book courier", book_courier),
              Step("confirm order", lambda: None)], log)
    return log, statement


if __name__ == "__main__":
    print("-- dual write, with a crash between the two steps")
    db, queue = new_db(), []
    try:
        capture_dual_write(db, queue, crash=True)
    except Crash as exc:
        print("crash:", exc)
    status = db.execute("SELECT status FROM payments").fetchone()[0]
    print("database says:", status, "| events published:", len(queue))

    print("-- outbox, with the relay crashing once")
    db, queue, ledger = new_db(), [], LedgerConsumer()
    capture_with_outbox(db)
    try:
        relay(db, queue, crash_before_mark=True)
    except Crash as exc:
        print("crash:", exc)
    print("relay restarts and publishes", relay(db, queue), "event(s)")
    for event in queue:
        ledger.handle(event)
    print("deliveries:", len(queue), "| ledger postings:", ledger.postings)

    for available in (True, False):
        print(f"-- catering order saga, courier available: {available}")
        log, statement = catering_order_saga(courier_available=available)
        print("\n".join(log))
        print("card statement:", statement)
