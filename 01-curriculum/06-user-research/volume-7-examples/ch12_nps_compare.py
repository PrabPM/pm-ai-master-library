"""Chapter 12: is a change in NPS real, and what does the blend hide?"""
import math

from ch12_nps import nps

print("quarter to quarter")
last, last_half = nps(85, 52, 38)        # last quarter, n = 175
this, this_half = nps(81, 54, 45)        # this quarter, n = 180
change = this - last
change_half = math.hypot(last_half, this_half)
print(f"last {last:+.0f}, this {this:+.0f}, change {change:+.0f} points")
print(f"95% interval for the change: {change - change_half:+.0f} to "
      f"{change + change_half:+.0f}")

print("\nthis quarter, split by how long the merchant has been with PayFlow")
SEGMENTS = {"Joined in the last 90 days": (18, 18, 24),
            "Joined more than 90 days ago": (63, 36, 21)}
for name, mix in SEGMENTS.items():
    score, half = nps(*mix)
    print(f"{name:<29} n = {sum(mix):>3}  NPS = {score:+4.0f}  "
          f"({score - half:+.0f} to {score + half:+.0f})")
