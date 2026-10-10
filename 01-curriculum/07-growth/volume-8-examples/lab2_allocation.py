"""Lab 2: spend $300,000 in $50,000 blocks, always buying the best next block."""
# Activated merchants a month at $50k, $100k, ... of monthly spend (measured).
CURVES = {
    "Paid search": [315, 574, 785, 958, 1100, 1216],
    "Partner co-marketing": [310, 420, 470],
    "Podcast sponsorships": [150, 290, 420],
}
BLOCK = 50_000

blocks = []  # (extra merchants, channel, block number)
for channel, totals in CURVES.items():
    previous = 0
    for i, total in enumerate(totals, start=1):
        blocks.append((total - previous, channel, i))
        previous = total

bought = sorted(blocks, reverse=True)[:6]
for extra, channel, i in bought:
    print(f"{channel:<22} block {i}: {extra:>3} merchants, ${BLOCK / extra:,.0f} each")
print(f"Total: {sum(b[0] for b in bought):,} activated merchants a month")
best_unbought = sorted(blocks, reverse=True)[6]
print(f"Best block not bought: {best_unbought[1]} block {best_unbought[2]}, "
      f"${BLOCK / best_unbought[0]:,.0f} each")
