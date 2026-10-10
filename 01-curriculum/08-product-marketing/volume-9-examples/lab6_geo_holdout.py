"""Lab 6. Brand search ads paused in half the metro areas: what did they add?"""

# Activated merchants in 40 metro areas, split at random into two groups of 20.
# Four-week periods. Ads ran everywhere except in OFF during the test period.
ON = {"earlier": 995, "before": 1_020, "test": 1_050}
OFF = {"earlier": 960, "before": 980, "test": 965}
BRAND_SPEND_ON = 4_500     # brand search spend in the ON metros during the test ($)
LAST_CLICK_ON = 230        # merchants last-click credited to brand search there


def diff_in_diff(first, second):
    """Change in the ON group minus change in the OFF group."""
    return (ON[second] - ON[first]) - (OFF[second] - OFF[first])


def main():
    wobble = diff_in_diff("earlier", "before")   # nothing changed: a noise check
    extra = diff_in_diff("before", "test")
    print(f"Noise check, two periods with ads on everywhere: {wobble:+d} merchants")
    print(f"Test, ads paused in the OFF metros:               {extra:+d} merchants")
    print(f"Share of last-click credit that was incremental:  "
          f"{extra / LAST_CLICK_ON:.1%}")
    print(f"Reported cost per merchant:     ${BRAND_SPEND_ON / LAST_CLICK_ON:,.2f}")
    print(f"Incremental cost per merchant:  ${BRAND_SPEND_ON / extra:,.2f}")


if __name__ == "__main__":
    main()
