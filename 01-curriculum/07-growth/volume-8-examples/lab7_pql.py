"""Lab 7: where should 400 sales calls a month go?"""
# tier: (merchants a month, upgrade rate alone, with a call, monthly profit if won)
TIERS = {
    "$10k-$25k a month": (900, 0.04, 0.07, 150),
    "$25k-$100k a month": (350, 0.05, 0.16, 600),
    "Over $100k a month": (60, 0.03, 0.30, 2_500),
}
CALLS = 400

rows = []
for tier, (merchants, alone, with_call, profit) in TIERS.items():
    rows.append(((with_call - alone) * profit, tier, merchants))
left, total = CALLS, 0
for per_call, tier, merchants in sorted(rows, reverse=True):
    calls = min(left, merchants)
    left -= calls
    total += calls * per_call
    print(f"{tier:<20} ${per_call:>6.2f} a month per call, {calls:>3} calls")
print(f"Added monthly gross profit from 400 calls: ${total:,.0f}")
