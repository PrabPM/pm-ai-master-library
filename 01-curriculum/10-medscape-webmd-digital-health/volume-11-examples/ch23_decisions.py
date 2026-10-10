"""Chapter 23: what the next-best-action engine decided."""
from common import connect, heading, run_sql

db = connect()
heading("Decisions by journey")
run_sql(db, "decisions", {"pct_offer": ".1f", "pct_no_action": ".1f",
                          "pct_suppress": ".1f", "pct_frequency_cap": ".1f"})
