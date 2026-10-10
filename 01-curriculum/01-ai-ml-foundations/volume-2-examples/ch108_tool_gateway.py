"""Chapter 108: a tiny tool gateway.

Every tool call the model asks for goes through `Gateway.call`, which enforces
an allowlist, argument validation, server-side ownership, a human approval for
writes and a per-run budget. Chapter 114 imports this file and attacks it.
"""
import re

# What each tool accepts, whether it changes anything, and what it costs.
TOOLS = {
    "get_payout_status": {"args": {"payout_id": r"po_\d{3}"}, "write": False,
                          "cost": 1},
    "list_failed_payouts": {"args": {"limit": range(1, 51)}, "write": False,
                            "cost": 1},
    "retry_payout": {"args": {"payout_id": r"po_\d{3}"}, "write": True,
                     "cost": 5},
    "export_merchants": {"args": {}, "write": False, "cost": 50},
}
ALLOWLIST = {"ops_agent": {"get_payout_status", "list_failed_payouts",
                           "retry_payout"}}
PAYOUT_OWNER = {"po_207": "m_juniper", "po_208": "m_juniper", "po_311": "m_harbor"}


def validate(args, spec):
    """Return None if args match the spec exactly, else the reason they do not."""
    if set(args) != set(spec):
        return f"arguments must be exactly {sorted(spec)}"
    for name, rule in spec.items():
        value = args[name]
        if isinstance(rule, range):
            if not isinstance(value, int) or value not in rule:
                return f"{name} must be {rule.start} to {rule.stop - 1}"
        elif not isinstance(value, str) or not re.fullmatch(rule, value):
            return f"{name} has the wrong format"
    return None


class Gateway:
    def __init__(self, budget):
        self.budget, self.spent, self.log = budget, 0, []

    def call(self, role, session, tool, args, approved_by=None):
        verdict = self._decide(role, session, tool, args, approved_by)
        self.log.append((tool, args, verdict))
        return verdict

    def _decide(self, role, session, tool, args, approved_by):
        if tool not in ALLOWLIST.get(role, set()):
            return "DENY  tool not on the allowlist"
        spec = TOOLS[tool]
        problem = validate(args, spec["args"])
        if problem:
            return "DENY  " + problem
        payout = args.get("payout_id")
        if payout and PAYOUT_OWNER.get(payout) != session["merchant_id"]:
            return "DENY  payout is not in this session's merchant"
        if spec["write"] and approved_by is None:
            return "HOLD  needs a human approval"
        if self.spent + spec["cost"] > self.budget:
            return "DENY  run budget exhausted"
        self.spent += spec["cost"]
        return "ALLOW"


if __name__ == "__main__":
    gw = Gateway(budget=7)
    session = {"merchant_id": "m_juniper"}       # set by login, never by the model
    requests = [
        ("get_payout_status", {"payout_id": "po_207"}, None),
        ("export_merchants", {}, None),
        ("list_failed_payouts", {"limit": 5000}, None),
        ("get_payout_status", {"payout_id": "po_311"}, None),
        ("retry_payout", {"payout_id": "po_207"}, None),
        ("retry_payout", {"payout_id": "po_207"}, "dana@payflow"),
        ("get_payout_status", {"payout_id": "po_207"}, None),
        ("get_payout_status", {"payout_id": "po_208"}, None),
    ]
    for n, (tool, args, approver) in enumerate(requests, start=1):
        verdict = gw.call("ops_agent", session, tool, args, approved_by=approver)
        print(f"{n}. {tool:<20} {verdict}")
    allowed = sum(v == "ALLOW" for _, _, v in gw.log)
    print(f"allowed {allowed} of {len(gw.log)}; budget used {gw.spent} of {gw.budget}")

    verdicts = [v.split()[0] for _, _, v in gw.log]
    assert verdicts == ["ALLOW", "DENY", "DENY", "DENY", "HOLD", "ALLOW", "ALLOW",
                        "DENY"]
    assert allowed == 3 and gw.spent == 7
    # Hand count of reachable rows: free SQL reaches every row; the narrow tool
    # reaches at most 50 rows of one merchant.
    rows_total, rows_narrow = 12 * 2_000_000, 50
    print(f"rows reachable: free SQL {rows_total:,}   narrow tool {rows_narrow}")
    assert rows_total // rows_narrow == 480_000
