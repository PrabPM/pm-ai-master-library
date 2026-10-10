"""Chapter 6: CPM arithmetic and where an advertiser's dollar goes."""
from common import heading, table

# region: cpm
def media_cost(impressions, cpm):
    return impressions / 1000 * cpm


impressions, cpm = 2_400_000, 28.00
gross = media_cost(impressions, cpm)
# endregion

heading("CPM arithmetic")
print(f"{impressions:,} impressions at a ${cpm:.2f} CPM cost ${gross:,.2f}")

# region: waterfall
# Fictional fee schedule, as shares of gross advertiser spend.
fees = [("DSP platform fee", 0.12), ("Audience data fee", 0.08),
        ("Verification and measurement", 0.03)]
rows, left = [("Gross advertiser spend", gross)], gross
for name, share in fees:
    rows.append((name, -gross * share))
    left -= gross * share
rows.append(("Working media (clears the auction)", left))
ssp_fee = left * 0.15                    # fictional SSP take rate on media
rows.append(("SSP fee", -ssp_fee))
rows.append(("Publisher revenue", left - ssp_fee))
# endregion

heading("Where the money goes")
table(["line", "amount"], rows, {"amount": ",.2f"})
publisher = left - ssp_fee
print(f"\nPublisher receives {publisher / gross:.1%} of gross spend.")
print(f"Advertiser pays ${cpm:.2f} CPM; publisher earns "
      f"${publisher / impressions * 1000:.2f} eCPM.")
