"""Chapter 15: a double-entry ledger that refuses to lose money."""
from collections import defaultdict
from dataclasses import dataclass

# Which side makes each kind of account grow.
NORMAL_SIDE = {"asset": "debit", "expense": "debit",
               "liability": "credit", "revenue": "credit"}
ACCOUNTS = {
    "cash": "asset",                            # money in PayFlow's bank account
    "due_from_northbank": "asset",              # captured, not yet settled to us
    "merchant_payable:m_harbor": "liability",   # what we owe Harbor Coffee
    "fee_revenue": "revenue",                   # what PayFlow has earned
}


class LedgerError(Exception):
    pass


@dataclass(frozen=True)
class Entry:
    account: str
    debit_minor: int = 0
    credit_minor: int = 0


@dataclass(frozen=True)
class Journal:
    journal_id: str
    description: str
    entries: tuple[Entry, ...]


class Ledger:
    def __init__(self) -> None:
        self._journals: dict[str, Journal] = {}   # append-only: no update, no delete

    def post(self, journal: Journal) -> bool:
        """Returns True if posted, False if this journal_id was posted before."""
        if journal.journal_id in self._journals:
            return False
        debits = sum(e.debit_minor for e in journal.entries)
        credits = sum(e.credit_minor for e in journal.entries)
        if debits != credits:
            raise LedgerError(f"unbalanced journal {journal.journal_id}: "
                              f"debits {debits} != credits {credits}")
        for entry in journal.entries:
            if entry.account not in ACCOUNTS:
                raise LedgerError(f"unknown account {entry.account}")
            one_sided = (entry.debit_minor > 0) != (entry.credit_minor > 0)
            if not one_sided or min(entry.debit_minor, entry.credit_minor) < 0:
                raise LedgerError("each entry is one positive debit or credit")
        self._journals[journal.journal_id] = journal
        return True

    def balance(self, account: str) -> int:
        """Balance on the account's normal side, derived from entries every time."""
        total = 0
        for journal in self._journals.values():
            for entry in journal.entries:
                if entry.account == account:
                    total += entry.debit_minor - entry.credit_minor
        return total if NORMAL_SIDE[ACCOUNTS[account]] == "debit" else -total

    def journal_ids(self) -> list[str]:
        return list(self._journals)

    def trial_balance(self) -> tuple[int, int]:
        entries = [e for j in self._journals.values() for e in j.entries]
        return (sum(e.debit_minor for e in entries),
                sum(e.credit_minor for e in entries))


HARBOR = "merchant_payable:m_harbor"


def journal(journal_id: str, description: str, *entries: Entry) -> Journal:
    """Build a journal, dropping zero-value lines (a 1-cent payment has no net)."""
    kept = tuple(e for e in entries if e.debit_minor or e.credit_minor)
    return Journal(journal_id, description, kept)


def capture(payment_id: str, amount: int, fee: int) -> Journal:
    return journal(f"{payment_id}:capture", "payment captured",
                   Entry("due_from_northbank", debit_minor=amount),
                   Entry(HARBOR, credit_minor=amount - fee),
                   Entry("fee_revenue", credit_minor=fee))


def settlement(batch_id: str, amount: int) -> Journal:
    return journal(f"{batch_id}:settle", "NorthBank settled to PayFlow",
                   Entry("cash", debit_minor=amount),
                   Entry("due_from_northbank", credit_minor=amount))


def payout(payout_id: str, amount: int) -> Journal:
    return journal(f"{payout_id}:payout", "paid out to Harbor Coffee",
                   Entry(HARBOR, debit_minor=amount),
                   Entry("cash", credit_minor=amount))


def refund(refund_id: str, amount: int) -> Journal:
    return journal(f"{refund_id}:refund", "refund to shopper",
                   Entry(HARBOR, debit_minor=amount),
                   Entry("due_from_northbank", credit_minor=amount))


def chargeback(dispute_id: str, amount: int, dispute_fee: int) -> Journal:
    return journal(f"{dispute_id}:chargeback", "chargeback lost",
                   Entry(HARBOR, debit_minor=amount + dispute_fee),
                   Entry("due_from_northbank", credit_minor=amount),
                   Entry("fee_revenue", credit_minor=dispute_fee))


def reverse(journal: Journal, reason: str) -> Journal:
    """Corrections are new journals: the mirror image of the one being corrected."""
    flipped = tuple(Entry(e.account, debit_minor=e.credit_minor,
                          credit_minor=e.debit_minor) for e in journal.entries)
    return Journal(f"{journal.journal_id}:reversal", reason, flipped)


def show(ledger: Ledger, event: str) -> None:
    cells = "".join(f"{ledger.balance(name) / 100:>15,.2f}" for name in ACCOUNTS)
    print(f"{event:<22}{cells}")


if __name__ == "__main__":
    ledger = Ledger()
    print("-- a journal that does not balance")
    try:
        ledger.post(Journal("pay_1001:capture", "typo in the fee", (
            Entry("due_from_northbank", debit_minor=12_000),
            Entry(HARBOR, credit_minor=11_622),
            Entry("fee_revenue", credit_minor=377))))
    except LedgerError as exc:
        print("refused:", exc)

    print("-- three days at Harbor Coffee (balances in USD)")
    print(f"{'after':<22}{'cash':>15}{'due from bank':>15}{'owed to Harbor':>15}"
          f"{'fee revenue':>15}")
    ledger.post(capture("pay_1001", 12_000, 378))
    show(ledger, "capture pay_1001")
    ledger.post(capture("pay_1002", 4_500, 160))
    show(ledger, "capture pay_1002")
    ledger.post(refund("rf_2001", 2_000))
    show(ledger, "refund $20.00")
    ledger.post(settlement("stl_0713", 14_500))
    show(ledger, "settlement")
    ledger.post(payout("po_0714", 13_962))
    show(ledger, "payout")
    ledger.post(chargeback("dp_3001", 4_500, 1_500))
    show(ledger, "chargeback pay_1002")

    print("-- posting the same journal again")
    print("posted:", ledger.post(capture("pay_1001", 12_000, 378)))
    debits, credits = ledger.trial_balance()
    print("trial balance: debits", debits, "| credits", credits)
