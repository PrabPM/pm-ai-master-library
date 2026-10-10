"""Chapter 103. Document understanding: validation rules and review routing for
extracted business-verification fields, and the straight-through arithmetic.

Run: python ch103_document_understanding.py
"""
import numpy as np

# [listing]
def iban_ok(iban):
    """ISO 13616 check: move 4 characters to the end, letters to numbers, mod 97."""
    s = iban.replace(" ", "").upper()
    return int("".join(str(int(c, 36)) for c in s[4:] + s[:4])) % 97 == 1


def review_reasons(app, threshold=0.90):
    reasons = [f"low confidence: {k}" for k, c in app["confidence"].items()
               if c < threshold]
    if not iban_ok(app["iban"]):
        reasons.append("IBAN fails its checksum")
    if sum(app["owner_shares"]) > 100:
        reasons.append("ownership adds up to more than 100%")
    if app["legal_name"].lower() != app["account_holder"].lower():
        reasons.append("bank account holder differs from the legal name")
    return reasons


apps = [dict(legal_name="Alder Goods Ltd", account_holder="Alder Goods Ltd",
             iban="GB82 WEST 1234 5698 7654 32", owner_shares=[60, 40],
             confidence={"legal_name": 0.99, "iban": 0.97}),
        dict(legal_name="Birch Supply LLC", account_holder="J. Birch",
             iban="GB82 WEST 1234 5698 7654 23", owner_shares=[70, 45],
             confidence={"legal_name": 0.98, "iban": 0.71})]
for app in apps:
    reasons = review_reasons(app)
    print(app["legal_name"], "->", "human review" if reasons else "auto-accept")
    for reason in reasons:
        print("   ", reason)

p_field, fields, volume = 0.85, 6, 1000
stp = p_field ** fields
print(f"straight-through rate {stp:.1%}; reviewer hours per month "
      f"{volume * (1 - stp) * 4 / 60:.1f} instead of {volume * 12 / 60:.0f}")
# [/listing]

# Hand-worked: 0.85 squared is 0.7225, cubed 0.614125, to the sixth 0.3771
assert np.isclose(0.85 ** 2, 0.7225) and np.isclose(0.85 ** 3, 0.614125)
assert round(stp, 4) == 0.3771
assert round(volume * (1 - stp) * 4 / 60, 1) == 41.5 and volume * 12 / 60 == 200
# Rules behave as described
assert iban_ok("GB82 WEST 1234 5698 7654 32")
assert not iban_ok("GB82 WEST 1234 5698 7654 23")       # two digits swapped
assert review_reasons(apps[0]) == []
assert len(review_reasons(apps[1])) == 4

# Field-level scores used in the chapter: 50 fields that have a true value,
# the model returns 48 values, 45 of them correct
precision, recall = 45 / 48, 45 / 50
f1 = 2 * precision * recall / (precision + recall)
assert np.isclose(precision, 0.9375) and np.isclose(recall, 0.90)
assert round(f1, 3) == 0.918

# Q103.1: 95% of fields pass, 8 fields
assert round(0.95 ** 8, 3) == 0.663
# Q103.2: 5,100 auto-accepted fields with 1% wrong; rules catch 30 of the 51
assert round(5100 * 0.01) == 51 and round((51 - 30) / 5100, 4) == 0.0041
