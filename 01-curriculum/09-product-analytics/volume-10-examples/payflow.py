"""Shared PayFlow numbers and a small seeded simulation for Volume 10.

PayFlow is fictional. Every constant here was invented for teaching.
"""
import numpy as np

# ---- one average active small merchant, one month -------------------------
VOLUME = 8_000.00            # dollars of successful payments
PAYMENTS = 160               # successful payments (average payment $50)
FEE_PCT, FEE_FIXED = 0.029, 0.30      # PayFlow's price: 2.9% + $0.30
COST_PCT, COST_FIXED = 0.018, 0.10    # interchange, network and processor fees
LOSS_PCT = 0.001             # fraud and dispute losses, share of volume
SUPPORT = 0.5 * 14.00        # 0.5 tickets a month at $14 a ticket
PAYOUTS = 20 * 0.25          # 20 payouts a month at $0.25 each


def unit_economics(volume=VOLUME, payments=PAYMENTS):
    """Return the monthly money lines for one active merchant, in dollars."""
    revenue = FEE_PCT * volume + FEE_FIXED * payments
    processing = COST_PCT * volume + COST_FIXED * payments
    losses = LOSS_PCT * volume
    net_revenue = revenue - processing
    contribution = net_revenue - losses - SUPPORT - PAYOUTS
    return {"volume": volume, "revenue": revenue, "processing": processing,
            "net_revenue": net_revenue, "losses": losses, "support": SUPPORT,
            "payouts": PAYOUTS, "contribution": contribution}


MARGIN = unit_economics()["contribution"]      # $100.00 a month

# ---- how small merchants leave --------------------------------------------
COHORTS = ["2025-10", "2025-11", "2025-12", "2026-01", "2026-02", "2026-03",
           "2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
SIZES = [412, 438, 395, 451, 467, 480, 502, 489, 515, 498, 521, 506]
REASONS = ["business closed", "switched provider", "closed by PayFlow risk"]


SPRING_PUSH = 6     # cohort index of April 2026, when the partner bonus began


def hazard(age, cohort=0):
    """True chance that a merchant active at age-1 months is gone by age.

    Merchants activated from April 2026 on leave faster in their first three
    months. The analyst does not know this; the cohort table has to show it.
    """
    if age == 1:
        h = 0.12
    elif age == 2:
        h = 0.08
    elif age == 3:
        h = 0.06
    elif age <= 6:
        h = 0.04
    elif age <= 12:
        h = 0.025
    else:
        h = 0.015
    if cohort >= SPRING_PUSH and age <= 3:
        h *= 1.4
    return h


def simulate(seed=10):
    """One row per activated merchant: cohort index, last active age, churned,
    reason.

    last_age is the last month-since-activation with a successful payment.
    A merchant still active in September 2026 is censored: we have not seen it
    leave, so churned is False and last_age is its current age.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for c, size in enumerate(SIZES):
        max_age = len(COHORTS) - 1 - c          # months we can observe
        for _ in range(size):
            age, churned = 0, False
            while age < max_age:
                if rng.random() < hazard(age + 1, c):
                    churned = True
                    break
                age += 1
            reason = rng.choice(REASONS, p=[0.50, 0.32, 0.18]) if churned else ""
            rows.append((c, age, churned, str(reason)))
    return rows


def survival_table(rows):
    """Kaplan-Meier style table: for each age, who was at risk and who left."""
    max_age = len(COHORTS) - 1
    table, surv = [], 1.0
    for age in range(1, max_age + 1):
        # at risk: active at age-1 and old enough for us to observe month `age`
        at_risk = sum(1 for c, last, _, _ in rows
                      if last >= age - 1 and max_age - c >= age)
        left = sum(1 for c, last, churned, _ in rows
                   if churned and last == age - 1 and max_age - c >= age)
        if at_risk == 0:
            break                             # nobody old enough to observe
        h = left / at_risk
        surv *= 1 - h
        table.append((age, at_risk, left, h, surv))
    return table
