"""Chapter 21. Three attribution models and one experiment on the same merchants."""
from math import sqrt
from statistics import NormalDist

from payflow import TYPICAL_CONTRIBUTION, payback_month

CHANNELS = ["Paid social", "Paid search", "Organic", "Bookkeepers", "Sales team"]
SOCIAL_SPEND = 42_000

# The 1,000 merchants activated in August 2026, grouped by the marketing touches
# recorded before sign-up, in order. Columns: touches, merchants.
JOURNEYS = [
    (["Paid social", "Paid search"], 110),
    (["Paid social", "Organic"], 90),
    (["Organic", "Paid search"], 120),
    (["Paid search"], 70),
    (["Organic"], 250),
    (["Paid social"], 60),
    (["Bookkeepers"], 80),
    (["Organic", "Bookkeepers"], 40),
    (["Paid social", "Organic", "Sales team"], 50),
    (["Paid search", "Sales team"], 40),
    (["Bookkeepers", "Organic"], 90),
]

# Conversion lift test, August 31 to September 27, 2026. The ad platform withheld
# PayFlow's ads from a random 20% of the target audience.
# Columns: people, merchants activated (from any channel).
SAW_ADS = (320_000, 608)
HELD_OUT = (80_000, 104)


def credit(model):
    """Merchants credited to each channel under one attribution model."""
    totals = dict.fromkeys(CHANNELS, 0.0)
    for touches, merchants in JOURNEYS:
        if model == "first":
            totals[touches[0]] += merchants
        elif model == "last":
            totals[touches[-1]] += merchants
        else:                               # linear: equal shares
            for channel in touches:
                totals[channel] += merchants / len(touches)
    return totals


def lift(treated, control):
    """Incremental merchants among the treated group, with a 95% interval."""
    (n1, k1), (n0, k0) = treated, control
    p1, p0 = k1 / n1, k0 / n0
    se = sqrt(p1 * (1 - p1) / n1 + p0 * (1 - p0) / n0)
    z = NormalDist().inv_cdf(0.975)
    diff = p1 - p0
    pooled = (k1 + k0) / (n1 + n0)
    z_test = diff / sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n0))
    p_value = 2 * (1 - NormalDist().cdf(abs(z_test)))
    return diff * n1, (diff - z * se) * n1, (diff + z * se) * n1, p_value


def main():
    models = {name: credit(name) for name in ("first", "last", "linear")}
    print(f"{'Channel':<14}{'First touch':>12}{'Last touch':>12}{'Linear':>9}")
    for channel in CHANNELS:
        print(f"{channel:<14}{models['first'][channel]:>12,.0f}"
              f"{models['last'][channel]:>12,.0f}{models['linear'][channel]:>9,.0f}")
    print()
    print("Paid social: merchants credited, and cost per merchant")
    labels = {"first": "First touch", "last": "Last touch", "linear": "Linear"}
    for name, label in labels.items():
        merchants = models[name]["Paid social"]
        cost = SOCIAL_SPEND / merchants
        print(f"  {label:<12}{merchants:>5,.0f}   ${cost:,.0f} each")
    extra, low, high, p_value = lift(SAW_ADS, HELD_OUT)
    print(f"  {'Holdout':<12}{extra:>5,.0f}   ${SOCIAL_SPEND / extra:,.0f} each")
    print(f"  Holdout 95% interval: {low:,.0f} to {high:,.0f} merchants, "
          f"${SOCIAL_SPEND / high:,.0f} to ${SOCIAL_SPEND / low:,.0f} each")
    print(f"  Chance of a gap this large if the ads did nothing: p = {p_value:.4f}")
    by_last = payback_month(SOCIAL_SPEND / models["last"]["Paid social"],
                            TYPICAL_CONTRIBUTION)
    by_test = payback_month(SOCIAL_SPEND / extra, TYPICAL_CONTRIBUTION)
    print(f"  Payback month: {by_last} at the last-touch cost, "
          f"{by_test} at the holdout cost")


if __name__ == "__main__":
    main()
