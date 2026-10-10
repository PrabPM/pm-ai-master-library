"""Chapter 24: measuring PayFlow Assist. Offline accuracy, online signals that
disagree, cost and latency per task, and how many answers to review."""
from math import ceil

import numpy as np
from statsmodels.stats.proportion import proportion_confint

# offline evaluation set: category -> (questions, graded correct)
EVAL_SET = {"Payout timing": (140, 131), "Fees and pricing": (100, 91),
            "Disputes": (90, 64), "Account and KYB": (70, 58)}
# September 2026, live traffic
ANSWERS = 42_000
RATED, THUMBS_UP = 2_520, 2_293           # merchants who clicked a thumb
REVIEWED, ACCEPTABLE = 300, 243           # random sample graded by staff
RESOLVED = 28_560                         # no ticket on the topic within 48 hours
# per answer: 3.2 model calls on average; prices are invented, per million tokens
TOKENS_IN, TOKENS_OUT = 12_800, 1_120
PRICE_IN, PRICE_OUT = 0.80, 4.00


def wilson(successes, n):
    low, high = proportion_confint(successes, n, alpha=0.05, method="wilson")
    return f"{successes / n:.1%} (95% CI {low:.1%} to {high:.1%})"


def review_sample(margin, expected=0.8, z=1.96):
    """Answers to grade so the 95% interval is +/- margin around `expected`."""
    return ceil(z ** 2 * expected * (1 - expected) / margin ** 2)


if __name__ == "__main__":
    print("Offline evaluation set")
    for name, (n, correct) in EVAL_SET.items():
        print(f"  {name:<18}{n:>4}  {wilson(correct, n)}")
    n = sum(q for q, _ in EVAL_SET.values())
    correct = sum(c for _, c in EVAL_SET.values())
    print(f"  {'All':<18}{n:>4}  {wilson(correct, n)}")

    print()
    print(f"Thumbs-up rate:        {wilson(THUMBS_UP, RATED)}")
    print(f"  ...from {RATED / ANSWERS:.0%} of answers; the other "
          f"{1 - RATED / ANSWERS:.0%} said nothing")
    print(f"Random human review:   {wilson(ACCEPTABLE, REVIEWED)}")
    print(f"Resolved, no ticket:   {RESOLVED / ANSWERS:.0%} of {ANSWERS:,} answers")

    print()
    cost = (TOKENS_IN * PRICE_IN + TOKENS_OUT * PRICE_OUT) / 1_000_000
    print(f"Cost per answer ${cost:.4f}; per resolved question "
          f"${cost * ANSWERS / RESOLVED:.4f}; per month ${cost * ANSWERS:,.0f}")
    seconds = np.random.default_rng(24).lognormal(np.log(2.1), 0.8, size=ANSWERS)
    p50, p95 = np.percentile(seconds, [50, 95])
    print(f"Latency: mean {seconds.mean():.1f} s, p50 {p50:.1f} s, p95 {p95:.1f} s")

    print()
    for margin in (0.05, 0.03, 0.02):
        print(f"Review {review_sample(margin):>5,} answers for +/- {margin:.0%}")
