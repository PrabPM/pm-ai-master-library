"""Chapter 21: data-quality rules run as queries."""
from common import connect, heading, read_sql, table

db = connect()
heading("Data-quality rules")
rows = [(rule, checked, failed, 100.0 * (checked - failed) / checked)
        for rule, checked, failed in db.execute(read_sql("dq_checks"))]
table(["rule", "checked", "failed", "pass_pct"], rows, {"pass_pct": ".2f"})
