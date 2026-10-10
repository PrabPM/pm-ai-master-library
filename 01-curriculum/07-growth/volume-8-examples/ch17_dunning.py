"""Chapter 17: how much involuntary churn a recovery sequence prevents."""
SUBSCRIBERS, PRICE = 12_000, 25
failed = 240  # renewal charges declined on the first attempt this month

STEPS = {  # step: subscribers recovered by it (PayFlow Plus, September 2026)
    "Automatic retry on day 3": 60,
    "Email and dashboard prompt to update card": 54,
    "Final retry on day 7": 21,
}

print(f"Failed first attempt: {failed} ({failed / SUBSCRIBERS:.1%} of subscribers)")
left = failed
for step, recovered in STEPS.items():
    left -= recovered
    print(f"  {step:<44}{recovered:>4} recovered, {left:>3} left")
saved = failed - left
print(f"Involuntary churn: {failed / SUBSCRIBERS:.1%} with no recovery, "
      f"{left / SUBSCRIBERS:.1%} with it")
print(f"Kept this month: {saved} subscribers, ${saved * PRICE:,} of monthly revenue")
