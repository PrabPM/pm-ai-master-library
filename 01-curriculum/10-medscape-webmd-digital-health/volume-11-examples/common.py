"""Shared helpers: open the practice database, run a .sql file, print a table."""
import os
import sqlite3

import seed

HERE = os.path.dirname(os.path.abspath(__file__))


def connect():
    """Open wrenfield.db, building it first if it does not exist."""
    if not os.path.exists(seed.DB_PATH):
        seed.build().close()
    db = sqlite3.connect(seed.DB_PATH)
    db.create_function("npi_valid", 1, lambda s: int(seed.npi_is_valid(s or "")))
    return db


def heading(text):
    print(f"\n-- {text} --")


def fmt(value, spec=None):
    if value is None:
        return "-"
    if spec:
        return format(value, spec)
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,d}"
    return str(value)


def table(headers, rows, specs=None):
    """Print rows as an aligned text table. Numbers are right-aligned."""
    specs = specs or {}
    cells = [[fmt(v, specs.get(h)) for h, v in zip(headers, r)] for r in rows]
    widths = [max(len(h), *(len(c[i]) for c in cells)) if cells else len(h)
              for i, h in enumerate(headers)]
    numeric = [bool(rows) and all(isinstance(r[i], (int, float)) or r[i] is None
                                  for r in rows) for i in range(len(headers))]
    def line(vals):
        out = [v.rjust(w) if numeric[i] else v.ljust(w)
               for i, (v, w) in enumerate(zip(vals, widths))]
        return "  ".join(out).rstrip()
    print(line(headers))
    print("  ".join("-" * w for w in widths))
    for c in cells:
        print(line(c))


def read_sql(name):
    with open(os.path.join(HERE, "sql", name + ".sql")) as f:
        return f.read()


def run_sql(db, name, specs=None):
    """Run sql/<name>.sql, print the result, and return (headers, rows)."""
    cur = db.execute(read_sql(name))
    headers = [d[0] for d in cur.description]
    rows = cur.fetchall()
    table(headers, rows, specs)
    return headers, rows
