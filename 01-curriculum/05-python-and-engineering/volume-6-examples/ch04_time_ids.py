"""Chapter 4: time and identifiers. Aware datetimes, DST, cutoffs, and IDs."""
import random
import uuid
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

NEW_YORK = ZoneInfo("America/New_York")
CUTOFF = time(17, 0)                 # Harbor Coffee's settlement cutoff, local time
HOLIDAYS = {date(2026, 7, 3)}        # Independence Day, observed


def local_day_in_utc(day: date, tz: ZoneInfo) -> tuple[datetime, datetime]:
    """The UTC start and end of one local calendar day."""
    start = datetime.combine(day, time.min, tzinfo=tz)
    end = datetime.combine(day + timedelta(days=1), time.min, tzinfo=tz)
    return start.astimezone(UTC), end.astimezone(UTC)


def is_business_day(day: date) -> bool:
    return day.weekday() < 5 and day not in HOLIDAYS


def settlement_date(instant: datetime, tz: ZoneInfo = NEW_YORK) -> date:
    """The business day a payment settles with: after cutoff rolls forward."""
    if instant.tzinfo is None:
        raise ValueError("instant must be timezone-aware")
    local = instant.astimezone(tz)
    day = local.date()
    if local.time() >= CUTOFF:
        day += timedelta(days=1)
    while not is_business_day(day):
        day += timedelta(days=1)
    return day


def uuid7_at(unix_ms: int, rng: random.Random) -> uuid.UUID:
    """A UUID version 7 for Python 3.13: 48 bits of time, then random bits."""
    value = (unix_ms & 0xFFFFFFFFFFFF) << 80
    value |= 0x7 << 76                       # version 7
    value |= rng.getrandbits(12) << 64
    value |= 0b10 << 62                      # RFC 9562 variant
    value |= rng.getrandbits(62)
    return uuid.UUID(int=value)


def uuid7_created_at(value: uuid.UUID) -> datetime:
    """Anyone holding a version 7 UUID can read when it was made."""
    return datetime.fromtimestamp((value.int >> 80) / 1000, tz=UTC)


if __name__ == "__main__":
    print("-- naive vs aware")
    naive = datetime(2026, 7, 13, 21, 30)                 # no timezone attached
    aware = datetime(2026, 7, 13, 21, 30, tzinfo=NEW_YORK)
    print("naive:", naive.isoformat(), "| aware:", aware.isoformat())
    try:
        print(naive < aware)
    except TypeError as exc:
        print("refused:", exc)
    wrong = naive.replace(tzinfo=UTC)        # stamps a label, converts nothing
    right = aware.astimezone(UTC)            # converts the instant
    print("label only:", wrong.isoformat())
    print("converted: ", right.isoformat(), "<- a different UTC date")

    print("-- the 23-hour day (clocks spring forward on 2026-03-08)")
    for day in (date(2026, 3, 7), date(2026, 3, 8), date(2026, 11, 1)):
        start, end = local_day_in_utc(day, NEW_YORK)
        print(day, "runs", start.strftime("%d %H:%M"), "to", end.strftime("%d %H:%M"),
              "UTC =", end - start)

    print("-- adding a day is not adding 24 hours")
    before = datetime(2026, 3, 7, 12, 0, tzinfo=NEW_YORK)
    plus_day = before + timedelta(days=1)                # same wall-clock time
    plus_24h = (before.astimezone(UTC) + timedelta(hours=24)).astimezone(NEW_YORK)
    print("+1 day:  ", plus_day.isoformat())
    print("+24 hours:", plus_24h.isoformat())

    print("-- 01:30 happens twice on 2026-11-01")
    first = datetime(2026, 11, 1, 1, 30, tzinfo=NEW_YORK, fold=0)
    second = datetime(2026, 11, 1, 1, 30, tzinfo=NEW_YORK, fold=1)
    print("first: ", first.astimezone(UTC).isoformat())
    print("second:", second.astimezone(UTC).isoformat())

    print("-- cutoff and business days")
    for stamp in ("2026-07-02T20:59:00+00:00", "2026-07-02T21:00:00+00:00",
                  "2026-07-10T23:15:00+00:00"):
        instant = datetime.fromisoformat(stamp)
        local = instant.astimezone(NEW_YORK)
        print(local.strftime("%a %Y-%m-%d %H:%M %Z"), "-> settles",
              settlement_date(instant).strftime("%a %Y-%m-%d"))

    print("-- what an ID gives away")
    rng = random.Random(6)
    made = int(datetime(2026, 7, 13, 14, 5, 9, tzinfo=UTC).timestamp() * 1000)
    ids = [uuid7_at(made + i, rng) for i in range(3)]
    for item in ids:
        print(item)
    print("sorted by time:", ids == sorted(ids))
    print("readable creation time:", uuid7_created_at(ids[0]).isoformat())
    random_id = uuid.UUID(int=rng.getrandbits(128), version=4)
    print("uuid4 (random, sorts nowhere):", random_id)
    print("uuid.uuid7 built in:", hasattr(uuid, "uuid7"))
