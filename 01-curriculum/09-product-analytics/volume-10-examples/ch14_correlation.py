"""Chapter 14: Simpson's paradox on real counts, then a confounded correlation."""
import numpy as np

# Small merchants active in March 2026. Did they still pay in September?
# segment: (Assist users, of whom retained, non-users, of whom retained)
SEGMENTS = {"New (under 3 months)": (1_400, 728, 600, 288),
            "Established": (400, 344, 2_600, 2_080)}
ALL = tuple(sum(column) for column in zip(*SEGMENTS.values()))


def gap(users, kept, non, non_kept):
    """Retention of Assist users minus retention of non-users."""
    return kept / users - non_kept / non


def weighted_gap():
    """Average the within-segment gaps, weighting each segment by its size."""
    everyone = ALL[0] + ALL[2]
    return sum(gap(*s) * (s[0] + s[2]) / everyone for s in SEGMENTS.values())


def confounded(seed=14):
    """Staff headcount drives both dashboard logins and payment volume."""
    rng = np.random.default_rng(seed)
    staff = rng.choice([1, 3, 10], size=600, p=[0.5, 0.35, 0.15])
    logins = rng.poisson(4 * staff)                    # weekly dashboard logins
    volume = rng.normal(8_000 * staff, 2_000 * staff)  # monthly volume, dollars
    print(f"All 600 merchants: r = {np.corrcoef(logins, volume)[0, 1]:.2f}")
    for s in (1, 3, 10):
        pick = staff == s
        r = np.corrcoef(logins[pick], volume[pick])[0, 1]
        print(f"  merchants with {s:>2} staff ({pick.sum()}): r = {r:+.2f}")


if __name__ == "__main__":
    for name, s in list(SEGMENTS.items()) + [("All merchants", ALL)]:
        users, kept, non, non_kept = s
        print(f"{name:<22} users {kept / users:.0%} of {users:,}   "
              f"non-users {non_kept / non:.0%} of {non:,}   gap {gap(*s):+.0%}")
    print(f"Gap after weighting each segment by its size: {weighted_gap():+.1%}")
    print()
    confounded()
