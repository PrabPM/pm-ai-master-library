"""Chapter 12: delivery, pacing and frequency for the Ritmora campaign."""
from common import connect, heading, read_sql, run_sql, table

db = connect()
heading("Delivery by line item")
run_sql(db, "delivery", {"viewable_rate": ".3f", "frequency": ".1f"})

# region: pacing
DAYS_TOTAL, DAYS_RUN = 84, 26
rows, tot = [], [0.0, 0.0, 0.0]
for line_item, budget, planned, spent in db.execute(read_sql("pacing")):
    days_left = DAYS_TOTAL - DAYS_RUN
    rows.append((line_item, budget, planned, spent, 100 * spent / planned,
                 spent / DAYS_RUN, (budget - spent) / days_left))
    tot = [tot[0] + budget, tot[1] + planned, tot[2] + spent]
rows.append(("TOTAL", tot[0], tot[1], tot[2], 100 * tot[2] / tot[1],
             tot[2] / DAYS_RUN, (tot[0] - tot[2]) / (DAYS_TOTAL - DAYS_RUN)))
# endregion

heading("Pacing after 26 of 84 days")
table(["line_item", "budget", "planned", "spent", "pace_pct", "daily_so_far",
       "daily_needed"], rows, {"pace_pct": ".1f"})

heading("Frequency across all line items")
run_sql(db, "frequency", {"pct_of_reached": ".1f"})
