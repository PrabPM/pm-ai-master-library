"""Chapter 72: a tamper-evident audit trail and a color-contrast check."""
import hashlib
import json


def add_record(trail, record):
    """Append a record whose hash covers its content and the previous hash."""
    previous = trail[-1]["hash"] if trail else "0" * 64
    body = json.dumps(record, sort_keys=True)
    digest = hashlib.sha256((previous + body).encode()).hexdigest()
    trail.append({"record": record, "previous": previous, "hash": digest})


def first_broken(trail):
    """Index of the first record that no longer matches its hash, or None."""
    previous = "0" * 64
    for i, entry in enumerate(trail):
        body = json.dumps(entry["record"], sort_keys=True)
        if entry["previous"] != previous or entry["hash"] != hashlib.sha256(
                (previous + body).encode()).hexdigest():
            return i
        previous = entry["hash"]
    return None


def luminance(hex_color):
    """Relative luminance of an sRGB color, as defined by WCAG."""
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
           for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    hi, lo = sorted([luminance(a), luminance(b)], reverse=True)
    return (hi + 0.05) / (lo + 0.05)


trail = []
add_record(trail, {"at": "2026-10-13T09:02:11Z", "actor": "assist-v4.1", "payment":
                   "PY-20931", "score": 0.07, "action": "approve", "sources": []})
add_record(trail, {"at": "2026-10-13T09:02:40Z", "actor": "assist-v4.1", "payout":
                   "PO-8850", "action": "draft reply", "sources": ["S1", "S2", "S3"]})
add_record(trail, {"at": "2026-10-13T09:04:02Z", "actor": "sam.whitfield", "payout":
                   "PO-8850", "action": "edit and send", "kept": 0.79})
print("records:", len(trail), " first broken record:", first_broken(trail))
trail[1]["record"]["action"] = "release payout"        # someone edits history
print("after tampering, first broken record:", first_broken(trail))

print("black on white:", round(contrast("#000000", "#ffffff"), 1))
for name, color in [("ink #1f2937", "#1f2937"), ("muted #6b7280", "#6b7280"),
                    ("line #cbd5e1", "#cbd5e1")]:
    ratio = contrast(color, "#ffffff")
    print(f"{name:14s} on white {ratio:5.2f}:1  "
          f"{'passes' if ratio >= 4.5 else 'fails'} 4.5:1 for body text")

# ---- checks against the hand-worked numbers ----
assert abs(contrast("#000000", "#ffffff") - 21.0) < 1e-9
assert first_broken(trail) == 1
assert contrast("#6b7280", "#ffffff") >= 4.5 > contrast("#cbd5e1", "#ffffff")
