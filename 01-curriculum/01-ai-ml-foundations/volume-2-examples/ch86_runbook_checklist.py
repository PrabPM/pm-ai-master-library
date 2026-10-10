"""Chapter 86. A release checklist and an incident timeline as code: the checklist
blocks a release with a named reason, and the timeline yields time to detect, time
to mitigate and customer impact."""
from datetime import datetime

# ---- 1. The release checklist as data --------------------------------------------
CHECKLIST = [   # (item, the evidence that satisfies it, chapter)
    ("run recorded", lambda r: all(r.get(k) for k in ("code", "data", "env")), 81),
    ("data and model gates passed", lambda r: r.get("gates") == "pass", 82),
    ("golden set: no hard failures", lambda r: r.get("golden_hard_failures") == 0, 83),
    ("metamorphic tests passed", lambda r: r.get("renamed_flips") == 0, 83),
    ("shadow p99 latency within 50 ms", lambda r: r.get("shadow_p99_ms", 99) <= 50, 84),
    ("rollback triggers configured", lambda r: bool(r.get("triggers")), 84),
    ("named approver", lambda r: bool(r.get("approver")), 81),
]


def review(release):
    """Returns the checklist items this release does not satisfy."""
    return [(item, ch) for item, check, ch in CHECKLIST if not check(release)]


fraud_v24 = {
    "code": "25a2cc4d1c", "data": "4cae3d8e34", "env": "lockfile 7c1e",
    "gates": "pass", "golden_hard_failures": 0, "renamed_flips": 0,
    "shadow_p99_ms": 62, "triggers": ["decline rate z >= 3"], "approver": None,
}
missing = review(fraud_v24)
print(f"fraud_v24: {len(CHECKLIST) - len(missing)} of {len(CHECKLIST)} items satisfied")
for item, ch in missing:
    print(f"  BLOCKED by: {item} (Chapter {ch})")
assert [m[0] for m in missing] == ["shadow p99 latency within 50 ms", "named approver"]

fraud_v24.update(shadow_p99_ms=41, approver="risk lead")
assert review(fraud_v24) == []
print("after the fix:", "READY" if not review(fraud_v24) else "BLOCKED")

# ---- 2. An incident timeline -----------------------------------------------------
timeline = {           # the stale-feature incident of Chapter 85
    "started": "02:10", "alert fired": "02:22", "acknowledged": "02:27",
    "fallback engaged": "02:41", "feature fresh again": "03:35",
}
t = {k: datetime.strptime(v, "%H:%M") for k, v in timeline.items()}


def minutes(a, b):
    return int((t[b] - t[a]).total_seconds() // 60)


detect = minutes("started", "alert fired")
mitigate = minutes("started", "fallback engaged")
resolve = minutes("started", "feature fresh again")
payments = mitigate * 600                       # 600 payments a minute
missed_fraud = payments * 0.004                 # extra fraud approved while exposed
print(f"\ntime to detect {detect} min, to mitigate {mitigate} min, "
      f"to resolve {resolve} min")
print(f"exposed payments {payments:,}, extra fraud approved about {missed_fraud:.0f}, "
      f"about USD {missed_fraud * 85:,.0f}")
assert (detect, mitigate, resolve) == (12, 31, 85)
assert payments == 18_600 and round(missed_fraud) == 74

