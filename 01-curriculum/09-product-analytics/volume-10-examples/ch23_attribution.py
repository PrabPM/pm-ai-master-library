"""Chapter 23: four rule-based attribution models next to measured incrementality.

Each path is the ordered list of marketing touches before one merchant's first
payment: (channel, days before the first payment). Q3 2026, 800 merchants.
"""
from collections import defaultdict

PATHS = [
    ([("Search", 1)], 250),
    ([("Social", 12), ("Search", 1)], 200),
    ([("Social", 20), ("Email", 6), ("Search", 1)], 90),
    ([("Partner", 2)], 110),
    ([("Social", 3)], 70),
    ([("Partner", 15), ("Search", 2)], 80),
]
SPEND = {"Search": 230_000, "Social": 130_000, "Partner": 60_000, "Email": 0}
INCREMENTAL = {"Search": 250, "Social": 185, "Partner": 45, "Email": 0}  # holdouts
HALF_LIFE = 7.0     # days: a touch 7 days earlier gets half the weight


def first_touch(path):
    return {path[0][0]: 1.0}


def last_touch(path):
    return {path[-1][0]: 1.0}


def linear(path):
    credit = defaultdict(float)
    for channel, _ in path:
        credit[channel] += 1 / len(path)
    return credit


def time_decay(path):
    weights = [0.5 ** (days / HALF_LIFE) for _, days in path]
    credit = defaultdict(float)
    for (channel, _), w in zip(path, weights):
        credit[channel] += w / sum(weights)
    return credit


MODELS = {"first": first_touch, "last": last_touch, "linear": linear,
          "decay": time_decay}


def attribute(model):
    totals = defaultdict(float)
    for path, merchants in PATHS:
        for channel, share in model(path).items():
            totals[channel] += share * merchants
    return totals


if __name__ == "__main__":
    credit = {name: attribute(model) for name, model in MODELS.items()}
    print(f"{'channel':<9}" + "".join(f"{name:>8}" for name in MODELS)
          + f"{'holdout':>9}{'$/last':>9}{'$/incr.':>9}")
    for channel, spend in SPEND.items():
        row = "".join(f"{credit[name][channel]:>8.0f}" for name in MODELS)
        last, incr = credit["last"][channel], INCREMENTAL[channel]
        per_last = f"{spend / last:>9,.0f}" if last and spend else f"{'-':>9}"
        per_incr = f"{spend / incr:>9,.0f}" if incr else f"{'-':>9}"
        print(f"{channel:<9}{row}{incr:>9}{per_last}{per_incr}")
    total = sum(n for _, n in PATHS)
    print(f"{'Total':<9}" + f"{total:>8}" * 4 + f"{sum(INCREMENTAL.values()):>9}")
