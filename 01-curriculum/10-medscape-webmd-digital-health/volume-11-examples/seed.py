"""Build the fictional Wrenfield practice database (SQLite).

Everything here is invented for teaching. No row describes a real person,
provider, company or campaign. Fictional NPIs start with 9, a first digit that
real NPIs do not use, so none of them can belong to a real provider.

Only Random.random() is used, because that method's sequence is guaranteed to
stay the same across Python versions.
"""
import math
import os
import sqlite3
from datetime import datetime, timedelta
from random import Random

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "wrenfield.db")

CAMPAIGN_START = datetime(2026, 9, 14)
TODAY = datetime(2026, 10, 9)          # last full day of data
DAYS_RUN = (TODAY - CAMPAIGN_START).days + 1   # 26


class Rng:
    """Deterministic helper built only on Random.random()."""

    def __init__(self, seed):
        self._r = Random(seed)

    def u(self):
        return self._r.random()

    def n(self, k):
        return int(self._r.random() * k)

    def hit(self, p):
        return self._r.random() < p

    def pick(self, seq):
        return seq[self.n(len(seq))]

    def weighted(self, pairs):
        x, acc = self._r.random(), 0.0
        for value, weight in pairs:
            acc += weight
            if x < acc:
                return value
        return pairs[-1][0]

    def normal(self):
        u1 = max(self._r.random(), 1e-12)
        u2 = self._r.random()
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)


# region: npi
def npi_check_digit(first_nine):
    """Luhn check digit for an NPI, using the 80840 health-industry prefix."""
    total = 24                      # what the constant prefix 80840 contributes
    for i, ch in enumerate(reversed(first_nine)):
        d = int(ch)
        if i % 2 == 0:              # every second digit, starting from the right
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return (10 - total % 10) % 10


def npi_is_valid(npi):
    return (len(npi) == 10 and npi.isdigit()
            and npi_check_digit(npi[:9]) == int(npi[9]))
# endregion


def fake_npi(i):
    nine = f"9{i:08d}"
    return nine + str(npi_check_digit(nine))


SCHEMA = """
CREATE TABLE target_list (npi TEXT, client TEXT, list_version TEXT);
CREATE TABLE hcp_profile (
  hcp_id INTEGER PRIMARY KEY, npi TEXT, profession TEXT, specialty TEXT,
  state TEXT, consent_state TEXT, verified INTEGER, last_seen TEXT);
CREATE TABLE journey_assignment (
  hcp_id INTEGER, journey_id TEXT, variant TEXT, assigned_at TEXT);
CREATE TABLE exposure (
  hcp_id INTEGER, day TEXT, line_item TEXT, impressions INTEGER,
  viewable INTEGER);
CREATE TABLE line_item (
  line_item TEXT PRIMARY KEY, name TEXT, buy_type TEXT, cpm REAL,
  budget REAL, start_day TEXT, end_day TEXT);
CREATE TABLE engagement_event (
  event_id TEXT, hcp_id INTEGER, event_type TEXT, content_class TEXT,
  event_at TEXT, qualified INTEGER);
CREATE TABLE decision_event (
  decision_id INTEGER PRIMARY KEY, hcp_id INTEGER, journey_id TEXT,
  action TEXT, reason_code TEXT, model_version TEXT, policy_version TEXT,
  decided_at TEXT);
CREATE TABLE activation_event (
  decision_id INTEGER, channel TEXT, status TEXT, activated_at TEXT);
CREATE TABLE integration_event (
  partner_id TEXT, endpoint TEXT, status_code INTEGER, latency_ms INTEGER,
  event_at TEXT);
CREATE TABLE registration_event (
  visitor_id INTEGER, variant TEXT, device TEXT, step TEXT, event_at TEXT);
CREATE TABLE login_event (visitor_id INTEGER, login_at TEXT);
"""

CARDIO = [("Cardiovascular Disease", 0.52), ("Interventional Cardiology", 0.14),
          ("Clinical Cardiac Electrophysiology", 0.08),
          ("Advanced Heart Failure", 0.06), ("Cardiology NP/PA", 0.20)]
OTHER = [("Family Medicine", 0.40), ("Internal Medicine", 0.35),
         ("Endocrinology", 0.15), ("Nephrology", 0.10)]
STATES = [("CA", 0.16), ("TX", 0.13), ("FL", 0.11), ("NY", 0.11), ("PA", 0.08),
          ("OH", 0.08), ("IL", 0.08), ("GA", 0.07), ("NC", 0.07), ("WA", 0.05),
          ("CO", 0.04), ("VT", 0.01), ("WY", 0.01)]


def ts(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def build(path=DB_PATH):
    if os.path.exists(path):
        os.remove(path)
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    rng = Rng(20261009)

    # ---- the client's target list and Wrenfield's member profiles --------
    profiles, targets, hcp_id = [], [], 0
    for i in range(12000):
        npi = fake_npi(i)
        listed = npi
        if rng.hit(0.015):                      # typo in the client's file
            listed = npi[:9] + str((int(npi[9]) + 1 + rng.n(8)) % 10)
        targets.append((listed, "Aldermoor", "2026-09-01"))
        if not rng.hit(0.82):                   # not a Wrenfield member
            continue
        hcp_id += 1
        spec = rng.weighted(CARDIO)
        prof = "NP/PA" if spec == "Cardiology NP/PA" else "MD/DO"
        consent = rng.weighted([("granted", 0.90), ("opted_out", 0.06),
                                ("unknown", 0.04)])
        verified = 1 if rng.hit(0.93) else 0
        seen = TODAY - timedelta(days=rng.n(20) if rng.hit(0.85) else 31 + rng.n(200))
        profiles.append((hcp_id, npi, prof, spec, rng.weighted(STATES), consent,
                         verified, ts(seen)))
    for i in range(12000, 15000):               # members who are not on the list
        hcp_id += 1
        profiles.append((hcp_id, fake_npi(i), "MD/DO", rng.weighted(OTHER),
                         rng.weighted(STATES), "granted", 1,
                         ts(TODAY - timedelta(days=rng.n(40)))))
    db.executemany("INSERT INTO target_list VALUES (?,?,?)", targets)
    db.executemany("INSERT INTO hcp_profile VALUES (?,?,?,?,?,?,?,?)", profiles)

    # ---- line items -------------------------------------------------------
    end = CAMPAIGN_START + timedelta(days=83)
    items = [("LI-DIRECT", "Wrenfield Clinical endemic display", "guaranteed",
              120.0, 20000.0),
             ("LI-PMP", "Endemic network private marketplace", "pmp",
              85.0, 16000.0),
             ("LI-OPEN", "HCP-addressable open auction", "open", 50.0, 12000.0)]
    db.executemany("INSERT INTO line_item VALUES (?,?,?,?,?,?,?)",
                   [(a, b, c, d, e, ts(CAMPAIGN_START)[:10], ts(end)[:10])
                    for a, b, c, d, e in items])

    # ---- eligibility, random assignment, exposure, outcomes ---------------
    listed_valid = {t[0] for t in targets if npi_is_valid(t[0])}
    cutoff = ts(CAMPAIGN_START - timedelta(days=30))
    assign, expo, eng, eid = [], [], [], 0
    for (hid, npi, prof, spec, state, consent, verified, seen) in profiles:
        if npi not in listed_valid or consent != "granted" or not verified:
            continue
        if seen < cutoff:
            continue
        variant = "holdout" if rng.hit(0.10) else "treatment"
        assign.append((hid, "J-CARDIO", variant, ts(CAMPAIGN_START)))
        reached = rng.hit(0.78) if variant == "treatment" else rng.hit(0.015)
        if reached:
            for _ in range(3 + rng.n(18)):
                day = CAMPAIGN_START + timedelta(days=rng.n(DAYS_RUN))
                li = rng.weighted([("LI-DIRECT", 0.34), ("LI-PMP", 0.15),
                                   ("LI-OPEN", 0.51)])
                imps = 1 + rng.n(4)
                view = sum(1 for _ in range(imps)
                           if rng.hit(0.72 if li != "LI-OPEN" else 0.55))
                expo.append((hid, ts(day)[:10], li, imps, view))
        p = 0.060 if variant == "holdout" else 0.060 + (0.036 if reached else 0.0)
        if rng.hit(p):
            eid += 1
            when = CAMPAIGN_START + timedelta(days=rng.n(14), hours=rng.n(24))
            eng.append((f"e{eid:06d}", hid, "qualified_conversion", "sponsored",
                        ts(when), 1))
        for _ in range(rng.n(4)):
            eid += 1
            etype, cls = rng.pick([("content_viewed", "editorial"),
                                   ("video_completed", "education"),
                                   ("tool_used", "editorial"),
                                   ("content_viewed", "sponsored")])
            when = CAMPAIGN_START + timedelta(days=rng.n(DAYS_RUN),
                                              minutes=rng.n(1440))
            eng.append((f"e{eid:06d}", hid, etype, cls, ts(when),
                        1 if rng.hit(0.8) else 0))
    for row in eng[:40]:                         # duplicates from a retried batch
        eng.append(row)
    db.executemany("INSERT INTO journey_assignment VALUES (?,?,?,?)", assign)
    db.executemany("INSERT INTO exposure VALUES (?,?,?,?,?)", expo)
    db.executemany("INSERT INTO engagement_event VALUES (?,?,?,?,?,?)", eng)

    # ---- journey decisions and activations --------------------------------
    dec, act, did = [], [], 0
    treated = [a[0] for a in assign if a[2] == "treatment"]
    for hid in treated:
        if not rng.hit(0.45):
            continue
        did += 1
        journey = rng.weighted([("J-EDU", 0.5), ("J-EVENT", 0.2), ("J-COMM", 0.3)])
        action, reason = rng.weighted([
            (("offer", "eligible_top_ranked"), 0.62),
            (("no_action", "frequency_cap"), 0.17),
            (("no_action", "no_eligible_candidate"), 0.09),
            (("suppress", "consent_changed"), 0.04),
            (("no_action", "already_completed"), 0.08)])
        when = CAMPAIGN_START + timedelta(days=rng.n(DAYS_RUN), minutes=rng.n(1440))
        dec.append((did, hid, journey, action, reason, "rank-v3", "pol-2026-09",
                    ts(when)))
        if action != "offer":
            continue
        channel = rng.weighted([("site", 0.45), ("email", 0.35), ("crm", 0.20)])
        median = {"site": 2.0, "email": 9.0, "crm": 35.0}[channel]
        spread = {"site": 0.5, "email": 0.7, "crm": 1.3}[channel]
        minutes = median * math.exp(spread * rng.normal())
        status = "delivered" if rng.hit(0.96 if channel != "crm" else 0.88) \
            else "failed"
        act.append((did, channel, status, ts(when + timedelta(minutes=minutes))))
    db.executemany("INSERT INTO decision_event VALUES (?,?,?,?,?,?,?,?)", dec)
    db.executemany("INSERT INTO activation_event VALUES (?,?,?,?)", act)

    # ---- partner API calls (seven days) -----------------------------------
    calls = []
    partners = {"elkhaven-crm": (0.985, 180), "aldermoor-crm": (0.93, 420),
                "campus-lms": (0.97, 260)}
    for partner, (ok, base) in partners.items():
        for endpoint in ("POST /activations", "GET /audiences", "POST /events"):
            for _ in range(700):
                when = TODAY - timedelta(minutes=rng.n(7 * 1440))
                if rng.hit(ok):
                    code = 200
                elif partner == "aldermoor-crm" and rng.hit(0.6):
                    code = 429
                else:
                    code = rng.pick([400, 401, 500, 503])
                slow = 6.0 if (partner == "aldermoor-crm" and rng.hit(0.08)) else 1.0
                latency = int(base * slow * math.exp(0.35 * rng.normal()))
                calls.append((partner, endpoint, code, latency, ts(when)))
    db.executemany("INSERT INTO integration_event VALUES (?,?,?,?,?)", calls)

    # ---- registration experiment on Wrenfield Clinical --------------------
    steps = ["start", "submit", "email_verified", "professional_verified",
             "first_value"]
    rates = {"A_long_form": [0.52, 0.80, 0.70, 0.60],
             "B_short_form": [0.68, 0.78, 0.62, 0.63]}
    reg, logins = [], []
    reg_start = datetime(2026, 8, 3)
    for vid in range(1, 8001):
        variant = "A_long_form" if rng.hit(0.5) else "B_short_form"
        device = "mobile" if rng.hit(0.62) else "desktop"
        when = reg_start + timedelta(days=rng.n(14), minutes=rng.n(1440))
        reg.append((vid, variant, device, "start", ts(when)))
        alive = True
        for step, rate in zip(steps[1:], rates[variant]):
            if device == "mobile" and step == "submit" and variant == "A_long_form":
                rate -= 0.08               # long forms hurt most on a phone
            alive = alive and rng.hit(rate)
            if not alive:
                break
            when += timedelta(minutes=2 + rng.n(600))
            reg.append((vid, variant, device, step, ts(when)))
        if alive:                          # reached first value: may come back
            if rng.hit(0.58):
                logins.append((vid, ts(when + timedelta(days=1 + rng.n(7)))))
            if rng.hit(0.41):
                logins.append((vid, ts(when + timedelta(days=8 + rng.n(23)))))
    db.executemany("INSERT INTO registration_event VALUES (?,?,?,?,?)", reg)
    db.executemany("INSERT INTO login_event VALUES (?,?)", logins)

    db.commit()
    return db


if __name__ == "__main__":
    conn = build()
    print("Built", os.path.basename(DB_PATH), "on SQLite", sqlite3.sqlite_version)
    for (name,) in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        (count,) = conn.execute(f"SELECT COUNT(*) FROM {name}").fetchone()
        print(f"  {name:20s} {count:>7,d} rows")
