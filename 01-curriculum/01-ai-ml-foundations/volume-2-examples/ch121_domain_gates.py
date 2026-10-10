"""Chapter 121: the same approval-gate rule in four kinds of product.

Ask a person to review an automated action when the expected loss from acting
wrongly is larger than the cost of the review:  p_wrong * loss > review_cost.
All numbers are illustrative.
"""
import numpy as np


def gate_threshold(p_wrong, review_cost):
    """Loss above which a human review pays for itself."""
    return review_cost / p_wrong


def review_cost(seconds, hourly_rate=72.0):
    return seconds / 3600 * hourly_rate


DOMAINS = [
    # name, action, P(wrong), review seconds, loss per unit, unit
    ("payments", "retry a failed payout", 0.02, 30, 1.0, "USD of payout"),
    ("marketplace", "refund a return", 0.05, 45, 1.0, "USD of refund"),
    ("B2B SaaS", "send a drafted email", 0.03, 60, 4.0, "recipients"),
    ("consumer app", "post for the user", 0.01, 5, 1.0, "USD of harm"),
]

if __name__ == "__main__":
    for name, action, p, secs, loss_per_unit, unit in DOMAINS:
        cost = review_cost(secs)
        limit = gate_threshold(p, cost) / loss_per_unit
        print(f"{name:<13} {action:<22} review USD {cost:.2f}  "
              f"gate above {limit:,.0f} {unit}")

    # Payments, by hand: review costs 30 s at USD 72 an hour = USD 0.60.
    assert np.isclose(review_cost(30), 0.60)
    assert np.isclose(gate_threshold(0.02, 0.60), 30)
    # A retry to a long-verified account can lose only the USD 1.50 return fee.
    assert 0.02 * 1.50 < 0.60
    assert np.isclose(gate_threshold(0.05, review_cost(45)), 18)
    assert np.isclose(gate_threshold(0.03, review_cost(60)) / 4.0, 10)
    assert np.isclose(gate_threshold(0.01, review_cost(5)), 10)
