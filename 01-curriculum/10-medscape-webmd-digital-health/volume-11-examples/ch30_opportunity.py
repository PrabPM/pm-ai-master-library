"""Chapter 30: a service-line opportunity model where capacity binds."""
from common import heading, table

# region: opportunity
# Fictional Elkhaven Health inputs for one quarter.
# demand = people in the service area likely to need the service
# open_slots = new-patient appointments available in the quarter
lines = [
    # name, demand, reachable share, conversion, open slots, contribution each
    ("Cardiology, North campus", 9_400, 0.55, 0.035, 60, 410.0),
    ("Cardiology, River campus", 7_800, 0.50, 0.035, 420, 410.0),
    ("Orthopedics, North campus", 11_200, 0.48, 0.028, 380, 520.0),
]
rows = []
for name, demand, reach, conv, slots, value in lines:
    wanted = demand * reach * conv           # appointments marketing could create
    served = min(wanted, slots)              # appointments operations can honor
    rows.append((name, round(wanted), slots, round(served),
                 served * value, "capacity" if wanted > slots else "demand"))
# endregion

heading("Service-line opportunity, one quarter")
table(["service_line", "requests", "open_slots", "appointments", "contribution",
       "binds"], rows, {"contribution": ",.0f"})
