"""Chapter 22: a geo holdout read with difference-in-differences.

Twelve metro regions, sixteen weeks. Paid media ran everywhere for eight weeks
(6 Apr to 31 May 2026), then was paused in six randomly chosen regions for
eight weeks (1 Jun to 26 Jul 2026). The data is simulated with a known truth:
ads cause 30% of activations, while the ad platforms claim 49% of them.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

from ch17_ltv import LTV_36
from ch18_cac import CAC, NEW, payback_month

rng = np.random.default_rng(223)
BASE_RATE = [24, 31, 28, 40, 35, 22, 45, 30, 26, 38, 33, 29]   # weekly, ads on
SUMMER = 1.12                              # every region is busier in June-July
holdout_regions = set(rng.choice(12, size=6, replace=False).tolist())

records = []
for region, base in enumerate(BASE_RATE):
    for week in range(16):
        post = week >= 8
        level = base * (SUMMER if post else 1.0)
        ads_on = not (post and region in holdout_regions)
        organic = rng.poisson(level * 0.70)
        from_ads = rng.poisson(level * 0.30) if ads_on else 0
        claimed = rng.poisson(level * 0.49) if ads_on else 0
        records.append({"region": region, "week": week, "post": int(post),
                        "holdout": int(region in holdout_regions),
                        "activated": organic + from_ads, "claimed": claimed})
df = pd.DataFrame(records)


def did(df):
    cell = df.groupby(["holdout", "post"])["activated"].mean()
    change_holdout = cell[1, 1] - cell[1, 0]
    change_control = cell[0, 1] - cell[0, 0]
    return cell, change_holdout, change_control, change_holdout - change_control


if __name__ == "__main__":
    cell, change_h, change_c, effect = did(df)
    print("Average activated merchants per region-week")
    print(f"{'':<22}{'before':>8}{'after':>8}{'change':>8}")
    print(f"{'ads paused (holdout)':<22}{cell[1, 0]:>8.1f}{cell[1, 1]:>8.1f}"
          f"{change_h:>+8.1f}")
    print(f"{'ads kept on':<22}{cell[0, 0]:>8.1f}{cell[0, 1]:>8.1f}{change_c:>+8.1f}")
    print(f"Difference-in-differences: {effect:+.1f} per region-week")

    model = smf.ols("activated ~ holdout:post + C(region) + C(week)", data=df).fit(
        cov_type="cluster", cov_kwds={"groups": df["region"]})
    low, high = model.conf_int().loc["holdout:post"]
    print(f"Regression with region and week effects: "
          f"{model.params['holdout:post']:+.1f} (95% CI {low:+.1f} to {high:+.1f})")

    print()
    region_weeks = 6 * 8
    claimed = df[(df.holdout == 1) & (df.post == 0)]["claimed"].sum()
    print(f"Ad platforms claimed {claimed:,} activations in the paused regions "
          f"in the 8 weeks before")
    for label, per_week in [("estimate", effect), ("low end", high),
                            ("high end", low)]:
        lost = -per_week * region_weeks
        print(f"  {label:<9} {lost:>4.0f} activations lost  ->  "
              f"{lost / claimed:.0%} of claimed were incremental")

    print()
    share = round(-effect * region_weeks / claimed, 2)
    real = share * NEW["paid"]
    cac = CAC["paid, fully loaded"] / share
    print(f"Applied to Q3: {NEW['paid']} claimed x {share:.0%} = {real:.0f} "
          f"merchants the ads caused")
    print(f"  fully loaded paid CAC per incremental merchant: ${cac:,.0f}")
    print(f"  payback month {payback_month(cac)}, LTV:CAC {LTV_36 / cac:.1f}")
