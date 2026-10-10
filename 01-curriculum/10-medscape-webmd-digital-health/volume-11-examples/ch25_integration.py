"""Chapter 25: which partner integration is struggling?"""
from common import connect, heading, run_sql

db = connect()
heading("Integration friction by partner, last seven days")
run_sql(db, "integration", {"success_rate": ".3f"})
