"""Chapter 23: a rename that breaks a rollout, the safe way, and measuring first."""
import sqlite3


def new_db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE payments (id TEXT PRIMARY KEY, amount INTEGER)")
    db.execute("INSERT INTO payments VALUES ('pay_1001', 12000)")
    db.execute("CREATE TABLE refunds (id TEXT, payment_id TEXT, amount_minor INTEGER)")
    db.commit()
    return db


# Two versions of the service run side by side while a rollout is in progress.
def old_code_reads(db: sqlite3.Connection) -> int:
    return db.execute("SELECT amount FROM payments WHERE id = 'pay_1001'").fetchone()[0]


def new_code_reads(db: sqlite3.Connection) -> int:
    return db.execute(
        "SELECT amount_minor FROM payments WHERE id = 'pay_1001'").fetchone()[0]


def try_read(label: str, reader, db: sqlite3.Connection) -> str:
    try:
        return f"{label}: {reader(db)}"
    except sqlite3.OperationalError as exc:
        return f"{label}: BROKEN ({exc})"


def expand(db: sqlite3.Connection) -> None:
    """Step 1, before any new code ships: add the new column and fill it."""
    with db:
        db.execute("ALTER TABLE payments ADD COLUMN amount_minor INTEGER")
        db.execute("UPDATE payments SET amount_minor = amount")


def contract(db: sqlite3.Connection) -> None:
    """Last step, after no running code reads the old column: remove it."""
    with db:
        db.execute("ALTER TABLE payments DROP COLUMN amount")


class CountingConnection:
    """Wraps a connection and counts round trips to the database."""

    def __init__(self, db: sqlite3.Connection) -> None:
        self.db, self.queries = db, 0

    def execute(self, sql: str, params: tuple = ()):
        self.queries += 1
        return self.db.execute(sql, params)


def refund_totals_one_by_one(conn: CountingConnection, payment_ids: list[str]) -> dict:
    return {pid: conn.execute("SELECT COALESCE(SUM(amount_minor), 0) FROM refunds"
                              " WHERE payment_id = ?", (pid,)).fetchone()[0]
            for pid in payment_ids}


def refund_totals_in_one_query(conn: CountingConnection,
                               payment_ids: list[str]) -> dict:
    marks = ",".join("?" * len(payment_ids))
    rows = conn.execute(f"SELECT payment_id, SUM(amount_minor) FROM refunds"
                        f" WHERE payment_id IN ({marks}) GROUP BY payment_id",
                        tuple(payment_ids)).fetchall()
    return {pid: 0 for pid in payment_ids} | dict(rows)


if __name__ == "__main__":
    print("-- rename the column in one step, mid-rollout")
    db = new_db()
    db.execute("ALTER TABLE payments RENAME COLUMN amount TO amount_minor")
    print(try_read("old code", old_code_reads, db))
    print(try_read("new code", new_code_reads, db))

    print("-- expand, roll out, then contract")
    db = new_db()
    expand(db)
    print("after expand   |", try_read("old code", old_code_reads, db), "|",
          try_read("new code", new_code_reads, db))
    print("rollout: every server now runs the new code; rollback is still possible")
    contract(db)
    print("after contract |", try_read("new code", new_code_reads, db))

    print("-- measure before optimizing: round trips for 200 payments")
    db = new_db()
    ids = [f"pay_{n}" for n in range(1001, 1201)]
    db.executemany("INSERT INTO refunds VALUES (?, ?, ?)",
                   [(f"rf_{i}", pid, 500) for i, pid in enumerate(ids[::10])])
    slow, fast = CountingConnection(db), CountingConnection(db)
    same = refund_totals_one_by_one(slow, ids) == refund_totals_in_one_query(fast, ids)
    print("one query per payment:", slow.queries, "round trips")
    print("one query for the page:", fast.queries, "round trip")
    print("same answers:", same)
