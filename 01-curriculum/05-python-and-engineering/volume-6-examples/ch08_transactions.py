"""Chapter 8: transactions. A race the application loses and the database wins."""
import tempfile
from pathlib import Path

from sqlalchemy import Engine, String, UniqueConstraint, create_engine, func, select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from fake_provider import FakeProvider


class Base(DeclarativeBase):
    pass


class LooseCommand(Base):
    """A payment command table with no uniqueness rule."""
    __tablename__ = "loose_commands"
    id: Mapped[int] = mapped_column(primary_key=True)
    merchant_id: Mapped[str] = mapped_column(String(32))
    idempotency_key: Mapped[str] = mapped_column(String(64))
    amount_minor: Mapped[int]


class PaymentCommand(Base):
    """The same table, with the rule written into the database."""
    __tablename__ = "payment_commands"
    __table_args__ = (UniqueConstraint("merchant_id", "idempotency_key"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    merchant_id: Mapped[str] = mapped_column(String(32))
    idempotency_key: Mapped[str] = mapped_column(String(64))
    amount_minor: Mapped[int]
    status: Mapped[str] = mapped_column(String(16), default="received")
    provider_ref: Mapped[str] = mapped_column(String(32), default="")


def found(engine: Engine, merchant_id: str, key: str) -> bool:
    """The application-level check: is there already a command with this key?"""
    with Session(engine) as session:
        query = select(LooseCommand).where(LooseCommand.merchant_id == merchant_id,
                                           LooseCommand.idempotency_key == key)
        return session.scalar(query) is not None


def insert_loose(engine: Engine, merchant_id: str, key: str, amount_minor: int) -> None:
    with Session(engine) as session, session.begin():
        session.add(LooseCommand(merchant_id=merchant_id, idempotency_key=key,
                                 amount_minor=amount_minor))


def count(engine: Engine, table) -> int:
    with Session(engine) as session:
        return session.scalar(select(func.count()).select_from(table))


def record_command(engine: Engine, merchant_id: str, key: str,
                   amount_minor: int) -> tuple[int, bool]:
    """Insert first and let the database referee. Returns (row id, created)."""
    with Session(engine) as session:
        row = PaymentCommand(merchant_id=merchant_id, idempotency_key=key,
                             amount_minor=amount_minor)
        session.add(row)
        try:
            session.commit()
            return row.id, True
        except IntegrityError:
            session.rollback()
            winner = session.scalars(select(PaymentCommand).where(
                PaymentCommand.merchant_id == merchant_id,
                PaymentCommand.idempotency_key == key)).one()
            return winner.id, False


def hold_lock_across_network_call(engine: Engine) -> None:
    """Request A keeps its transaction open while it waits for the bank."""
    with Session(engine) as a, Session(engine) as b:
        a.add(PaymentCommand(merchant_id="m_harbor", idempotency_key="order-7790",
                             amount_minor=4_500))
        a.flush()  # A now holds a write lock ... and goes off to call the bank
        b.add(PaymentCommand(merchant_id="m_kumo", idempotency_key="order-0042",
                             amount_minor=1_500))
        try:
            b.commit()
        except OperationalError as exc:
            print("request B failed while A waited:", exc.orig)
            b.rollback()
        a.rollback()


def pay_in_three_steps(engine: Engine, provider: FakeProvider, merchant_id: str,
                       key: str, amount_minor: int) -> str:
    """Short transaction, network call with no transaction, short transaction."""
    row_id, created = record_command(engine, merchant_id, key, amount_minor)  # 1
    if not created:
        return "duplicate request: returning the first result"
    result = provider.authorize(amount_minor, "USD", "tok_visa_4242", key)    # 2
    with Session(engine) as session, session.begin():                         # 3
        row = session.get(PaymentCommand, row_id)
        row.status = "authorized" if result.approved else "declined"
        row.provider_ref = result.provider_ref
        return f"{row.status} ({row.provider_ref})"


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as folder:
        engine = create_engine(f"sqlite:///{Path(folder) / 'payflow.db'}",
                               connect_args={"timeout": 0})
        Base.metadata.create_all(engine)

        print("-- check, then insert (no constraint)")
        a_found = found(engine, "m_harbor", "order-7781")   # request A looks
        b_found = found(engine, "m_harbor", "order-7781")   # request B looks
        print("A found a row:", a_found, "| B found a row:", b_found)
        if not a_found:
            insert_loose(engine, "m_harbor", "order-7781", 12_000)
        if not b_found:
            insert_loose(engine, "m_harbor", "order-7781", 12_000)
        print("rows for one order:", count(engine, LooseCommand))

        print("-- insert, and let the unique constraint decide")
        id_a, created_a = record_command(engine, "m_harbor", "order-7781", 12_000)
        id_b, created_b = record_command(engine, "m_harbor", "order-7781", 12_000)
        print("A created:", created_a, "| B created:", created_b,
              "| same row:", id_a == id_b)
        print("rows for one order:", count(engine, PaymentCommand))

        print("-- a transaction held open across a network call")
        hold_lock_across_network_call(engine)

        print("-- the right shape: three short steps")
        bank = FakeProvider()
        print(pay_in_three_steps(engine, bank, "m_harbor", "order-7791", 4_500))
        print(pay_in_three_steps(engine, bank, "m_harbor", "order-7791", 4_500))
        print("charges at the bank:", len(bank.charges))
        engine.dispose()
