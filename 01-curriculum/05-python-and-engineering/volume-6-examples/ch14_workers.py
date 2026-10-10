"""Chapter 14: queues, workers and schedulers."""
import sqlite3
from dataclasses import dataclass, field


@dataclass
class Message:
    body: str
    receives: int = 0
    invisible_until: float = 0.0


@dataclass
class Queue:
    """An at-least-once queue with a visibility timeout and a dead-letter queue."""
    visibility_timeout: float = 30.0
    max_receives: int = 3
    messages: list[Message] = field(default_factory=list)
    dead_letters: list[Message] = field(default_factory=list)

    def send(self, body: str) -> None:
        self.messages.append(Message(body))

    def receive(self, now: float) -> Message | None:
        for message in list(self.messages):
            if message.invisible_until > now:
                continue                      # another worker is holding it
            if message.receives >= self.max_receives:
                self.messages.remove(message)
                self.dead_letters.append(message)
                continue
            message.receives += 1
            message.invisible_until = now + self.visibility_timeout
            return message
        return None

    def ack(self, message: Message) -> None:
        if message in self.messages:
            self.messages.remove(message)


def new_billing_db() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE subscriptions (id TEXT PRIMARY KEY, due_date TEXT)")
    db.execute("""CREATE TABLE charge_commands (subscription_id TEXT, due_date TEXT,
                  status TEXT DEFAULT 'pending',
                  PRIMARY KEY (subscription_id, due_date))""")
    db.executemany("INSERT INTO subscriptions VALUES (?, ?)",
                   [("sub_101", "2026-07-13"), ("sub_102", "2026-07-13"),
                    ("sub_103", "2026-07-14")])
    db.commit()
    return db


def create_due_charges(db: sqlite3.Connection, business_date: str) -> int:
    """Safe to run any number of times for the same date. Returns new commands."""
    with db:
        cursor = db.execute(
            """INSERT INTO charge_commands (subscription_id, due_date)
               SELECT id, due_date FROM subscriptions WHERE due_date = ?
               ON CONFLICT (subscription_id, due_date) DO NOTHING""", (business_date,))
    return cursor.rowcount


if __name__ == "__main__":
    print("-- a slow worker and the visibility timeout")
    queue = Queue(visibility_timeout=30)
    queue.send("capture pay_1001")
    first = queue.receive(now=0)
    print("t=0   worker A receives:", first.body)
    print("t=10  worker B receives:", queue.receive(now=10))
    second = queue.receive(now=31)
    print("t=31  worker B receives:", second.body, f"(receive #{second.receives})")
    queue.ack(first)
    print("t=45  worker A finishes and acks; B is already doing the same work")

    print("-- a message that always fails")
    queue = Queue(visibility_timeout=30, max_receives=3)
    queue.send("capture pay_9999 (malformed)")
    now = 0.0
    while (message := queue.receive(now)) is not None:
        print(f"t={now:<4.0f} attempt {message.receives} fails")
        now += 31
    queue.receive(now)
    print("dead-letter queue:", [m.body for m in queue.dead_letters])

    print("-- the daily billing job runs twice")
    db = new_billing_db()
    print("first run created: ", create_due_charges(db, "2026-07-13"), "commands")
    print("second run created:", create_due_charges(db, "2026-07-13"), "commands")
    total = db.execute("SELECT COUNT(*) FROM charge_commands").fetchone()[0]
    print("charge commands in total:", total)
