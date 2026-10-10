"""Chapter 37: queries a PM in this role should be able to write."""
from common import connect, heading, run_sql

db = connect()
heading("Time from decision to activation")
run_sql(db, "latency", {"p50_minutes": ".1f", "p95_minutes": ".1f"})

heading("Weekly activation funnel")
run_sql(db, "weekly_activation", {"pct_offers_delivered": ".1f"})
