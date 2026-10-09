"""Chapter 18: data processing with Polars and Parquet."""
import os
import random
import tempfile
from datetime import UTC, datetime, timedelta
from pathlib import Path

import polars as pl

CURRENCY = {"m_harbor": "USD", "m_kumo": "JPY", "m_dune": "KWD"}
METHODS = ["card", "wallet"]


def make_partition(day: str, rows: int, seed: int) -> pl.DataFrame:
    """Invent one day of payment attempts. Seeded, so every run is identical."""
    rng = random.Random(seed)
    start = datetime.fromisoformat(day).replace(tzinfo=UTC)
    merchants = [rng.choice(list(CURRENCY)) for _ in range(rows)]
    return pl.DataFrame({
        "attempt_id": [f"att_{day[-2:]}_{i:05d}" for i in range(rows)],
        "merchant_id": merchants,
        "currency": [CURRENCY[m] for m in merchants],
        "method": [rng.choices(METHODS, weights=[8, 2])[0] for _ in range(rows)],
        "status": [rng.choices(["succeeded", "declined", "failed"],
                               weights=[85, 12, 3])[0] for _ in range(rows)],
        "amount_minor": [rng.randrange(300, 20_000) for _ in range(rows)],
        "created_at": [start + timedelta(seconds=rng.randrange(86_400))
                       for _ in range(rows)],
    })


def write_lake(root: Path) -> dict[str, dict]:
    """Write two daily partitions and return the sender's control totals."""
    manifest = {}
    for day, seed in (("2026-07-12", 1), ("2026-07-13", 2)):
        frame = make_partition(day, rows=5_000, seed=seed)
        folder = root / f"day={day}"
        folder.mkdir(parents=True)
        frame[:2_500].write_parquet(folder / "part-0.parquet")
        frame[2_500:].write_parquet(folder / "part-1.parquet")
        manifest[day] = {"rows": frame.height,
                         "amount_minor": int(frame["amount_minor"].sum())}
    return manifest


def daily_summary(root: Path, day: str) -> pl.LazyFrame:
    """Describe the work. Nothing is read until .collect()."""
    return (
        pl.scan_parquet(root / f"day={day}" / "*.parquet")
        .filter(pl.col("status") == "succeeded")
        .group_by("merchant_id", "currency")
        .agg(pl.col("amount_minor").sum().alias("volume_minor"),
             pl.len().alias("payments"))
        .sort("merchant_id")
    )


def check_control_totals(root: Path, day: str, expected: dict) -> None:
    """Refuse to publish numbers built on an incomplete or altered input."""
    actual = (pl.scan_parquet(root / f"day={day}" / "*.parquet")
              .select(pl.len().alias("rows"), pl.col("amount_minor").sum())
              .collect().row(0, named=True))
    if actual != expected:
        raise ValueError(f"control totals differ for {day}: file says {actual}, "
                         f"sender says {expected}")


def write_atomically(frame: pl.DataFrame, target: Path) -> None:
    temporary = target.with_suffix(".tmp")
    frame.write_parquet(temporary)
    os.replace(temporary, target)   # readers see the old file or the new, never half


if __name__ == "__main__":
    pl.Config.set_tbl_formatting("ASCII_FULL_CONDENSED")
    pl.Config.set_tbl_hide_dataframe_shape(True)
    with tempfile.TemporaryDirectory() as folder:
        root = Path(folder) / "attempts"
        manifest = write_lake(root)
        day = "2026-07-13"

        print("-- the plan Polars will run")
        query = daily_summary(root, day)
        for line in query.explain().splitlines():
            if any(word in line for word in ("SCAN", "PROJECT", "SELECTION")):
                text = line.strip().replace(str(root) + "/", "")
                print(text if len(text) <= 60 else text[:56] + " ...")

        print("-- the result")
        check_control_totals(root, day, manifest[day])
        summary = query.collect(engine="streaming")
        print(summary)
        print("money column type:", summary.schema["volume_minor"])

        print("-- a file goes missing")
        (root / f"day={day}" / "part-1.parquet").unlink()
        try:
            check_control_totals(root, day, manifest[day])
        except ValueError as exc:
            print("refused:", str(exc).replace(": file", ":\n  file").replace(
                ", sender", ",\n  sender"))

        write_atomically(summary, Path(folder) / "summary.parquet")
        print("summary written:", sorted(p.name for p in Path(folder).glob("summary*")))
