"""Chapter 10: compare candidate activation events on the June 2026 cohort."""
SIGNUPS, RETAINED = 7_000, 3_150  # retained = paid again in days 61 to 90

CANDIDATES = {
    # event in the first 14 days: (merchants who did it, how many were retained)
    "Connected a bank account": (5_390, 3_100),
    "First live payment": (4_340, 2_950),
    "Five live payments": (2_800, 2_380),
    "Invited a teammate": (630, 580),
}

print(f"{'Event in first 14 days':<26}{'Did it':>8}{'Kept if yes':>13}"
      f"{'Kept if no':>12}{'Coverage':>10}")
for event, (did, kept) in CANDIDATES.items():
    kept_if_no = (RETAINED - kept) / (SIGNUPS - did)
    print(f"{event:<26}{did / SIGNUPS:>8.0%}{kept / did:>13.0%}"
          f"{kept_if_no:>12.0%}{kept / RETAINED:>10.0%}")
