"""Chapter 13: test-versus-control lift with a confidence interval."""
from math import sqrt
from statistics import NormalDist

from common import connect, heading, read_sql, run_sql, table

Z95 = NormalDist().inv_cdf(0.975)


# region: lift
def lift(conv_t, n_t, conv_c, n_c):
    """Absolute lift between two proportions with a 95% interval."""
    p_t, p_c = conv_t / n_t, conv_c / n_c
    se = sqrt(p_t * (1 - p_t) / n_t + p_c * (1 - p_c) / n_c)
    diff = p_t - p_c
    return {"p_t": p_t, "p_c": p_c, "abs": diff, "rel": diff / p_c,
            "low": diff - Z95 * se, "high": diff + Z95 * se}
# endregion


def srm_p_value(n_t, n_c, share_t):
    """Chi-square test (1 degree of freedom) that the split matches the plan."""
    total = n_t + n_c
    exp_t, exp_c = total * share_t, total * (1 - share_t)
    chi2 = (n_t - exp_t) ** 2 / exp_t + (n_c - exp_c) ** 2 / exp_c
    return chi2, 2 * (1 - NormalDist().cdf(sqrt(chi2)))


def holdout_needed(p_c, p_t, power=0.80):
    """Equal-size arms needed to detect p_t versus p_c at 5% two-sided."""
    z_b = NormalDist().inv_cdf(power)
    var = p_t * (1 - p_t) + p_c * (1 - p_c)
    return (Z95 + z_b) ** 2 * var / (p_t - p_c) ** 2


def report(r, n_t, cost=None):
    print(f"treatment rate   {r['p_t']:.2%}")
    print(f"control rate     {r['p_c']:.2%}")
    print(f"absolute lift    {r['abs'] * 100:.2f} points "
          f"(95% CI {r['low'] * 100:.2f} to {r['high'] * 100:.2f})")
    print(f"relative lift    {r['rel']:.1%}")
    print(f"incremental      {r['abs'] * n_t:,.0f} "
          f"(95% CI {r['low'] * n_t:,.0f} to {r['high'] * n_t:,.0f})")
    if cost:
        print(f"cost per incremental outcome  ${cost / (r['abs'] * n_t):,.0f}")


if __name__ == "__main__":
    db = connect()
    heading("Conversion by assigned variant")
    _, rows = run_sql(db, "lift", {"conversion_rate": ".4f"})
    by = {r[0]: r for r in rows}
    t, c = by["treatment"], by["holdout"]

    heading("Sample ratio check (planned 90/10)")
    chi2, p = srm_p_value(t[1], c[1], 0.90)
    print(f"treatment share {t[1] / (t[1] + c[1]):.2%}, chi-square {chi2:.2f}, "
          f"p = {p:.2f}")

    heading("Lift on qualified engagement within 14 days")
    report(lift(t[2], t[1], c[2], c[1]), t[1])

    heading("Who was actually exposed")
    run_sql(db, "contamination", {"pct_exposed": ".1f"})

    heading("Same lift, two holdout sizes (prescribing outcome)")
    out = []
    for label, n_t, n_c in [("10% holdout", 10_000, 1_111),
                            ("50% holdout", 10_000, 10_000)]:
        r = lift(round(0.062 * n_t), n_t, round(0.054 * n_c), n_c)
        out.append((label, n_t, n_c, r["abs"] * 100, r["low"] * 100,
                    r["high"] * 100,
                    "yes" if r["low"] > 0 else "no"))
    table(["design", "treated", "control", "lift_pts", "ci_low", "ci_high",
           "excludes_zero"], out,
          {"lift_pts": ".2f", "ci_low": ".2f", "ci_high": ".2f"})
    need = holdout_needed(0.054, 0.062)
    print(f"\nEqual arms needed for 80% power at 5.4% vs 6.2%: "
          f"{need:,.0f} HCPs per arm")
