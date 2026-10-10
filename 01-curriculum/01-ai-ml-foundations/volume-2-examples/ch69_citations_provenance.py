"""Chapter 69: checking claim-level citations in code and measuring how much of
a draft the agent kept. Illustrative records.
"""
import re
from difflib import SequenceMatcher

SOURCES = {
    "S1": "Payout PO-8850: amount USD 1,284.40, status on hold since 2026-10-12.",
    "S2": "Bank account changed 2026-10-12. Verification started 2026-10-12.",
    "S3": "Help article: verification usually takes up to 2 business days.",
}
DRAFT = [  # (claim, cited source or None)
    ("Payout PO-8850 for USD 1,284.40 is on hold.", "S1"),
    ("The hold began on 2026-10-12 with a bank account change.", "S2"),
    ("Verification usually takes up to 2 business days.", "S3"),
    ("The payout will arrive on 2026-10-16.", "S3"),
    ("Nothing else is needed from you.", None),
]
FACT = r"PO-\d+|\d{4}-\d{2}-\d{2}|\d[\d,]*\.\d+|\d+"     # ids, dates, amounts, counts


def verdict(claim, source_id):
    """A claim passes only if every id, date and number it states is in its source."""
    if source_id is None:
        return "uncited"
    if source_id not in SOURCES:
        return "citation does not exist"
    missing = [f for f in re.findall(FACT, claim) if f not in SOURCES[source_id]]
    return "supported" if not missing else "not in source: " + ", ".join(missing)


results = [verdict(c, s) for c, s in DRAFT]
for (claim, s), r in zip(DRAFT, results):
    print(f"[{s or '--'}] {r:25s} {claim}")
cited = [r for r in results if r != "uncited"]
coverage = len(cited) / len(results)
support = sum(r == "supported" for r in cited) / len(cited)
print(f"citation coverage {coverage:.2f}   support rate {support:.2f}")

draft_text = " ".join(c for c, _ in DRAFT)
sent_text = "Hi Maya. " + " ".join(c for (c, _), r in zip(DRAFT, results)
                                   if r == "supported")
kept = SequenceMatcher(None, draft_text, sent_text).ratio()
print(f"similarity of the sent reply to the draft: {kept:.2f}")

# ---- checks against the hand-worked numbers ----
assert results[:3] == ["supported"] * 3 and results[4] == "uncited"
assert results[3] == "not in source: 2026-10-16"
assert coverage == 0.80 and support == 0.75
