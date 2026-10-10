"""Chapter 20: deterministic assignment by hashing the merchant ID."""
import hashlib


def variant(merchant_id, experiment, treatment_share=0.50):
    """The same merchant in the same experiment always gets the same answer."""
    digest = hashlib.sha256(f"{experiment}:{merchant_id}".encode()).hexdigest()
    bucket = int(digest[:8], 16) / 16**8  # a number from 0 up to, not including, 1
    return "treatment" if bucket < treatment_share else "control"


ids = [f"m_{i:05d}" for i in range(1, 10_001)]
first = [variant(m, "guided-setup") for m in ids]
again = [variant(m, "guided-setup") for m in ids]
other = [variant(m, "plus-trial-length") for m in ids]
both = sum(a == b == "treatment" for a, b in zip(first, other))

print("m_00001 ->", variant("m_00001", "guided-setup"))
print(f"In treatment: {first.count('treatment'):,} of {len(ids):,}")
print("Same answers on a second call:", first == again)
print(f"In treatment in both experiments: {both / len(ids):.1%}")
