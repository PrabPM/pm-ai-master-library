"""Chapter 110: an approval gate with a quorum, and a tamper-evident audit log.

Standard library only. The log is a hash chain: each entry's hash covers the
entry and the previous hash, so changing any old entry breaks every later link.
"""
import hashlib
import json


def digest(obj):
    """SHA-256 of a canonical JSON encoding, as hex."""
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def needs_quorum(amount_usd, threshold=10_000):
    return 2 if amount_usd > threshold else 1


def gate(action, approvals, approvers=("finance_lead", "risk_lead", "ops_manager")):
    """Approve only if enough named approvers signed THIS exact action."""
    h = digest(action)
    valid = {who for who, signed_hash in approvals
             if who in approvers and signed_hash == h}
    return len(valid) >= needs_quorum(action["amount_usd"]), h


class AuditLog:
    GENESIS = "0" * 64

    def __init__(self):
        self.entries = []                       # (entry, chain_hash)

    def append(self, entry):
        prev = self.entries[-1][1] if self.entries else self.GENESIS
        self.entries.append((entry, digest({"prev": prev, "entry": entry})))

    def first_broken_link(self):
        prev = self.GENESIS
        for i, (entry, chain_hash) in enumerate(self.entries, start=1):
            if digest({"prev": prev, "entry": entry}) != chain_hash:
                return i
            prev = chain_hash
        return None


if __name__ == "__main__":
    action = {"tool": "retry_payout", "payout_id": "po_207", "amount_usd": 18_400}
    h = digest(action)
    print("action hash:", h[:12])
    ok1, _ = gate(action, [("finance_lead", h)])
    ok2, _ = gate(action, [("finance_lead", h), ("risk_lead", h)])
    changed = dict(action, amount_usd=81_400)
    ok3, _ = gate(changed, [("finance_lead", h), ("risk_lead", h)])
    print("one approval:", ok1, "| two approvals:", ok2)
    print("two approvals, amount changed after signing:", ok3)

    log = AuditLog()
    log.append({"event": "proposed", "action": h[:12], "by": "ops_agent"})
    log.append({"event": "approved", "action": h[:12], "by": "finance_lead"})
    log.append({"event": "approved", "action": h[:12], "by": "risk_lead"})
    log.append({"event": "executed", "action": h[:12], "key": "idem-" + h[:8]})
    for i, (entry, chain_hash) in enumerate(log.entries, start=1):
        print(i, entry["event"], chain_hash[:12])
    print("first broken link:", log.first_broken_link())

    log.entries[1][0]["by"] = "ops_agent"       # someone edits entry 2
    print("after editing entry 2, first broken link:", log.first_broken_link())

    # Approval load: gate everything, or only retries above USD 10,000?
    retries, seconds_each, share_large = 400, 30, 0.06
    all_minutes = retries * seconds_each / 60
    tiered_minutes = retries * share_large * seconds_each / 60
    print(f"approval minutes per day: all {all_minutes:.0f}, "
          f"tiered {tiered_minutes:.0f}")

    assert (ok1, ok2, ok3) == (False, True, False)
    assert log.first_broken_link() == 2
    assert all_minutes == 200 and tiered_minutes == 12
    assert needs_quorum(9_999) == 1 and needs_quorum(18_400) == 2
