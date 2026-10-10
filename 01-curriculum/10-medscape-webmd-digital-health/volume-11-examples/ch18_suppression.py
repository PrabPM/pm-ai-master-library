"""Chapter 18: minimum cell size suppression in an aggregate report."""
from common import connect, heading, run_sql

db = connect()
heading("Engaged HCPs by specialty and state (cells under 11 hidden)")
run_sql(db, "suppression")
