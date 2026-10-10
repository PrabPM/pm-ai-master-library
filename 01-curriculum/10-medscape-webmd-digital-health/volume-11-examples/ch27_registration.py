"""Chapters 27 and 28: the registration experiment and who came back."""
from common import connect, heading, read_sql, run_sql, table

db = connect()
heading("Registration funnel by variant")
headers, rows = run_sql(db, "registration_funnel")

heading("Step rates per 100 starts")
out = []
for r in rows:
    out.append((r[0],) + tuple(100.0 * v / r[1] for v in r[2:]))
table(["variant", "submitted", "email_verified", "prof_verified", "first_value"],
      out, {h: ".1f" for h in headers[2:]})
a, b = out[0], out[1]
print(f"\nB versus A: registrations {b[1] / a[1] - 1:+.1%}, "
      f"verified and activated members {b[4] / a[4] - 1:+.1%}")

heading("Submit rate by device")
run_sql(db, "registration_device", {"pct_submitted": ".1f"})

heading("Retention of activated members")
run_sql(db, "retention", {"pct_back_week_1": ".1f", "pct_back_days_8_30": ".1f"})
