"""Chapter 14: contribution margin for one managed campaign."""
from common import heading, table

# region: contribution
# Fictional figures for the 12-week Ritmora campaign.
gross_spend = 48_000.00
lines = [
    ("Gross media spend billed to the client", gross_spend),
    ("Publisher and media cost", -31_200.00),
    ("Third-party data and identity", -2_900.00),
    ("Verification and measurement", -1_450.00),
    ("Variable cloud and serving cost", -1_150.00),
    ("Campaign operations labor (62 h at $95)", -62 * 95.00),
    ("Credits and makegoods", -1_200.00),
]
net_revenue = gross_spend - 31_200.00            # if booked as an agent
contribution = sum(amount for _, amount in lines)
# endregion

heading("Contribution model")
table(["line", "amount"], lines + [("Contribution margin", contribution)],
      {"amount": ",.2f"})
print(f"\nNet revenue (gross minus media cost): ${net_revenue:,.2f}")
print(f"Take rate on gross spend:             {net_revenue / gross_spend:.1%}")
print(f"Contribution as share of gross:       {contribution / gross_spend:.1%}")
print(f"Contribution as share of net revenue: {contribution / net_revenue:.1%}")
