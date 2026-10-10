"""Chapter 16: settlement and reconciliation. Find and name every difference."""
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Record:
    ref: str            # NorthBank's reference, present on both sides
    amount_minor: int
    captured_at: str    # ISO timestamp in UTC


# PayFlow's own records for business date 2026-07-13 (cutoff 21:00 UTC).
LEDGER = [
    Record("nb_0001", 12_000, "2026-07-13T14:05:09Z"),
    Record("nb_0002", 4_500, "2026-07-13T14:20:41Z"),
    Record("nb_0003", 1_500, "2026-07-13T15:02:10Z"),
    Record("nb_0004", 8_900, "2026-07-13T16:45:00Z"),
    Record("nb_0005", 2_500, "2026-07-13T20:59:58Z"),   # two seconds before cutoff
    Record("nb_0006", 6_000, "2026-07-13T18:30:00Z"),
]
# NorthBank's settlement file for the same date.
BANK_FILE = [
    Record("nb_0001", 12_000, "2026-07-13T14:05:09Z"),
    Record("nb_0002", 4_500, "2026-07-13T14:20:41Z"),
    Record("nb_0003", 1_490, "2026-07-13T15:02:10Z"),   # ten cents short
    Record("nb_0004", 8_900, "2026-07-13T16:45:00Z"),
    Record("nb_0004", 8_900, "2026-07-13T16:45:00Z"),   # listed twice
    Record("nb_0007", 12_000, "2026-07-13T17:10:03Z"),  # we have no such payment
]
TIMING_WINDOW_START = "2026-07-13T20:55:00Z"   # last five minutes before cutoff

Break = tuple[str, str, int]   # (reference, category, bank minus ledger in minor units)


def reconcile(ledger: list[Record], bank: list[Record],
              timing_from: str = TIMING_WINDOW_START) -> list[Break]:
    """Compare two independent lists and name every difference."""
    breaks: list[Break] = []
    ours = {r.ref: r for r in ledger}
    bank_counts = Counter(r.ref for r in bank)
    theirs = {r.ref: r for r in bank}
    for ref, record in sorted(ours.items()):
        if ref not in theirs:
            near_cutoff = record.captured_at >= timing_from
            category = "timing_next_file" if near_cutoff else "missing_at_bank"
            breaks.append((ref, category, -record.amount_minor))
        elif theirs[ref].amount_minor != record.amount_minor:
            diff = theirs[ref].amount_minor - record.amount_minor
            breaks.append((ref, "amount_mismatch", diff))
    for ref, record in sorted(theirs.items()):
        if bank_counts[ref] > 1:
            extra = (bank_counts[ref] - 1) * record.amount_minor
            breaks.append((ref, "duplicate_at_bank", extra))
        if ref not in ours:
            breaks.append((ref, "missing_in_ledger", record.amount_minor))
    return breaks


if __name__ == "__main__":
    ledger_total = sum(r.amount_minor for r in LEDGER)
    bank_total = sum(r.amount_minor for r in BANK_FILE)
    print("-- control totals")
    print(f"ledger: {len(LEDGER)} records, {ledger_total / 100:>9,.2f} USD")
    print(f"bank:   {len(BANK_FILE)} records, {bank_total / 100:>9,.2f} USD")
    print(f"difference to explain: {(bank_total - ledger_total) / 100:,.2f} USD")

    print("-- exceptions")
    breaks = reconcile(LEDGER, BANK_FILE)
    for ref, category, diff in breaks:
        print(f"{ref}  {category:<20}{diff / 100:>10,.2f}")
    explained = sum(diff for _, _, diff in breaks)
    print(f"explained by exceptions: {explained / 100:,.2f} USD")
    print("fully explained:", explained == bank_total - ledger_total)

    print("-- running it again changes nothing")
    print("same result:", reconcile(LEDGER, BANK_FILE) == breaks)
