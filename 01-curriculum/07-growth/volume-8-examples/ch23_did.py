"""Chapter 23: difference-in-differences on a go-dark geo test of paid social."""
import pandas as pd
import statsmodels.formula.api as smf

ON = [941, 935, 955, 955, 941, 978, 971, 985, 1006, 993, 983, 994]  # ads all 12 weeks
DARK = [923, 900, 926, 934, 921, 943, 886, 876, 885, 904, 887, 898]  # off from week 7
CLAIMED = 115  # weekly sign-ups the ad platform credited itself in the dark states
REPORTED_CAC = 450  # dollars per activated merchant, on the platform's count

data = pd.DataFrame({
    "signups": ON + DARK,
    "dark": [0] * 12 + [1] * 12,
    "after": ([0] * 6 + [1] * 6) * 2,
})
means = data.groupby(["dark", "after"])["signups"].mean().unstack()
change_on = means.loc[0, 1] - means.loc[0, 0]
change_dark = means.loc[1, 1] - means.loc[1, 0]
fit = smf.ols("signups ~ dark * after", data).fit()
low, high = fit.conf_int().loc["dark:after"]

print(f"States with ads on: {means.loc[0, 0]:.0f} -> {means.loc[0, 1]:.0f} "
      f"({change_on:+.0f} a week)")
print(f"States gone dark:   {means.loc[1, 0]:.0f} -> {means.loc[1, 1]:.0f} "
      f"({change_dark:+.0f} a week)")
print(f"Difference-in-differences: {change_dark - change_on:+.0f} a week "
      f"(95% CI {low:+.0f} to {high:+.0f})")
share = (change_on - change_dark) / CLAIMED
print(f"Platform's claim: {CLAIMED} a week. Share that was incremental: {share:.0%}")
print(f"Cost per activated merchant: ${REPORTED_CAC} as reported, "
      f"${REPORTED_CAC / share:,.0f} per incremental one")
