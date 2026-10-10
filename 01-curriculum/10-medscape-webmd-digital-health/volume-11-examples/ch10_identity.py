"""Chapter 10: NPI check digits and the match-rate funnel."""
from common import connect, heading, read_sql, table
from seed import npi_check_digit, npi_is_valid

heading("NPI check digit")
print("123456789 ->", "123456789" + str(npi_check_digit("123456789")))
for npi in ("1234567893", "1234567894", "123456789"):
    print(f"{npi:11s} valid: {npi_is_valid(npi)}")

db = connect()
heading("Match-rate funnel")
cur = db.execute(read_sql("match_funnel"))
names = [d[0] for d in cur.description]
counts = cur.fetchone()
rows, prev = [], None
for name, count in zip(names, counts):
    step = None if prev is None else 100.0 * count / prev
    rows.append((name, count, step, 100.0 * count / counts[0]))
    prev = count
table(["stage", "npis", "pct_of_previous", "pct_of_list"], rows,
      {"pct_of_previous": ".1f", "pct_of_list": ".1f"})
