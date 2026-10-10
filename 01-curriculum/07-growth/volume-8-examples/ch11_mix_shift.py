"""Chapter 11: split a drop in a rate into real change and mix shift."""
# channel: (August sign-ups, activated, September sign-ups, activated)
CHANNELS = {
    "Organic and direct": (2_500, 1_600, 2_500, 1_525),
    "Paid search": (2_000, 1_160, 2_000, 1_100),
    "Partner platforms": (1_500, 1_050, 1_500, 1_005),
    "Invoice loop, referrals": (1_000, 530, 1_000, 500),
    "Paid social (new)": (0, 0, 1_000, 270),
}

print(f"{'Channel':<26}{'August':>8}{'September':>11}")
for name, (s0, a0, s1, a1) in CHANNELS.items():
    august = f"{a0 / s0:.1%}" if s0 else "none"
    print(f"{name:<26}{august:>8}{a1 / s1:>11.1%}")


def rate(rows, signups, activated):
    return sum(r[activated] for r in rows) / sum(r[signups] for r in rows)


everyone = list(CHANNELS.values())
existing = [row for row in everyone if row[0] > 0]  # channels present in August
aug, sep = rate(everyone, 0, 1), rate(everyone, 2, 3)
sep_existing = rate(existing, 2, 3)
real, mix = (sep_existing - aug) * 100, (sep - sep_existing) * 100
print()
print(f"All sign-ups:            {aug:.1%} -> {sep:.1%}")
print(f"Same four channels only: {aug:.1%} -> {sep_existing:.1%}  "
      f"real change {real:+.1f} points")
print(f"Adding the new channel:  {sep_existing:.1%} -> {sep:.1%}  "
      f"mix shift   {mix:+.1f} points")
