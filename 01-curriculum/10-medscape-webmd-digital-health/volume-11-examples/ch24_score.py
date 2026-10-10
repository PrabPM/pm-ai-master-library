"""Chapter 24: a transparent HCP engagement score."""
from common import heading, table

# region: score
WEIGHTS = {"article_view": 1, "video_complete": 3, "tool_use": 4,
           "brand_site_depth": 3, "cross_channel_bonus": 2}
HALF_LIFE_DAYS = 14
CAP_PER_SIGNAL = 3                 # repeated identical events stop counting


def score(events, identity_confidence):
    """events: (signal, days_ago, quality_factor between 0 and 1)."""
    total, seen = 0.0, {}
    for signal, days_ago, quality in sorted(events, key=lambda e: e[1]):
        seen[signal] = seen.get(signal, 0) + 1
        if seen[signal] > CAP_PER_SIGNAL:
            continue
        decay = 0.5 ** (days_ago / HALF_LIFE_DAYS)
        total += WEIGHTS[signal] * decay * quality * identity_confidence
    return total
# endregion


hcps = [
    ("HCP A: three education videos, a tool, two channels", 1.00,
     [("video_complete", 2, 1.0), ("video_complete", 6, 1.0),
      ("video_complete", 11, 1.0), ("tool_use", 4, 1.0),
      ("cross_channel_bonus", 2, 1.0)]),
    ("HCP B: ten article views in one day", 1.00,
     [("article_view", 1, 1.0)] * 10),
    ("HCP C: same as A, but five weeks ago", 1.00,
     [("video_complete", 37, 1.0), ("video_complete", 41, 1.0),
      ("video_complete", 46, 1.0), ("tool_use", 39, 1.0),
      ("cross_channel_bonus", 37, 1.0)]),
    ("HCP D: same as A, weaker identity link", 0.60,
     [("video_complete", 2, 1.0), ("video_complete", 6, 1.0),
      ("video_complete", 11, 1.0), ("tool_use", 4, 1.0),
      ("cross_channel_bonus", 2, 1.0)]),
]
heading("Engagement score")
table(["hcp", "identity_confidence", "score"],
      [(name, conf, score(ev, conf)) for name, conf, ev in hcps],
      {"identity_confidence": ".2f", "score": ".2f"})
