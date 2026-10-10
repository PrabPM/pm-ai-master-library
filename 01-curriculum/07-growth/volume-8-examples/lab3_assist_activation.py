"""Lab 3: candidate activation events for PayFlow Assist (June 2026 cohort)."""
TRIED, RETAINED = 5_000, 600  # retained = still using Assist weekly in week 8

# event in the first 7 days: (merchants who did it, of whom retained in week 8)
CANDIDATES = {
    "Asked one question": (3_400, 560),
    "Asked three or more": (1_100, 380),
    "Pinned an answer": (400, 260),
    "Connected accounting": (250, 200),
}

print(f"{'Event in first 7 days':<24}{'Did it':>8}{'Kept if yes':>13}"
      f"{'Kept if no':>12}{'Coverage':>10}")
for event, (did, kept) in CANDIDATES.items():
    kept_if_no = (RETAINED - kept) / (TRIED - did)
    print(f"{event:<24}{did / TRIED:>8.0%}{kept / did:>13.0%}"
          f"{kept_if_no:>12.0%}{kept / RETAINED:>10.0%}")
