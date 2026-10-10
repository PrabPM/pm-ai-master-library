"""Chapter 15: what one extra minute per visit costs a clinic."""
from common import heading

# region: minute
clinicians, visits_per_day, clinic_days = 24, 18, 230     # fictional Elkhaven
extra_minutes = 1
hours = clinicians * visits_per_day * clinic_days * extra_minutes / 60
visits_lost = hours * 60 / 20                # a follow-up visit takes 20 minutes
# endregion

heading("One extra minute per visit")
print(f"{clinicians} cardiology clinicians x {visits_per_day} visits x "
      f"{clinic_days} days = {clinicians * visits_per_day * clinic_days:,} visits")
print(f"One extra minute each = {hours:,.0f} clinician hours a year")
print(f"That is {visits_lost:,.0f} twenty-minute visits that cannot happen")
