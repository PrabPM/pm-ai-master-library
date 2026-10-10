"""Chapter 25: turn an incident's event log into the durations that matter."""
from datetime import datetime

EVENTS = [  # (time, key, what happened). All times Eastern, 2026.
    ("2026-09-04 02:10", "fault", "Knowledge sync job starts failing"),
    ("2026-09-08 09:00", "change", "Help article HC-112 updated: up to 2 days"),
    ("2026-09-08 09:14", "first_bad", "First answer cites the old 1-day text"),
    ("2026-09-15 10:12", "signal", "Sam flags an answer as wrong"),
    ("2026-09-15 11:20", "declared", "Incident declared, severity 2"),
    ("2026-09-15 11:32", "contained", "Payout-timing answers switched to abstain"),
    ("2026-09-15 14:10", "fixed", "Sync repaired and index rebuilt"),
    ("2026-09-15 15:45", "restored", "Evals pass, normal answers restored"),
]
AFFECTED = {"agent-facing answers": 212, "merchant-facing answers": 96}


# [listing]
def durations(events):
    at = {key: datetime.strptime(when, "%Y-%m-%d %H:%M") for when, key, _ in events}
    spans = {
        "Bad answers before anyone noticed": at["signal"] - at["first_bad"],
        "First signal to incident declared": at["declared"] - at["signal"],
        "Declared to contained": at["contained"] - at["declared"],
        "Contained to restored": at["restored"] - at["contained"],
    }
    unnoticed = spans["Bad answers before anyone noticed"]
    share = unnoticed / (at["restored"] - at["first_bad"])
    return spans, share
# [end listing]


def pretty(delta):
    minutes = int(delta.total_seconds() // 60)
    days, rest = divmod(minutes, 1440)
    hours, mins = divmod(rest, 60)
    return (f"{days} d " if days else "") + f"{hours} h {mins:02d} min"


def main():
    for when, _, what in EVENTS:
        stamp = datetime.strptime(when, "%Y-%m-%d %H:%M")
        print(f"{stamp:%a %b %d %H:%M}  {what}")
    print()
    spans, share = durations(EVENTS)
    for name, delta in spans.items():
        print(f"{name:<36}{pretty(delta):>14}")
    print(f"Share of the incident spent undetected: {share:.0%}")
    print(f"Answers affected: {sum(AFFECTED.values())} "
          f"({', '.join(f'{v} {k}' for k, v in AFFECTED.items())})")


if __name__ == "__main__":
    main()
