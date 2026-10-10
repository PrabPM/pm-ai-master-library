"""Lab 7 (chapter 64): target a retention offer by uplift, not by risk."""
import numpy as np

# segment: (churn without offer, churn with offer), from a randomized test.
# Each segment has 5,000 merchants.
SEGMENTS = {"A low risk": (0.02, 0.02), "B wavering": (0.10, 0.06),
            "C leaving anyway": (0.30, 0.28), "D do not disturb": (0.05, 0.08)}
VALUE, OFFER_COST, SIZE = 400, 12, 5000      # USD margin per year, USD per offer


def profit_per_merchant(control, treated):
    uplift = control - treated               # churn avoided by the offer
    return uplift * VALUE - OFFER_COST


if __name__ == "__main__":
    profit = {}
    for name, (control, treated) in SEGMENTS.items():
        profit[name] = profit_per_merchant(control, treated)
        print(f"{name:<18} uplift {control - treated:+.2f}  "
              f"profit per merchant USD {profit[name]:+6.2f}")
    everyone = SIZE * sum(profit.values())
    highest_risk = SIZE * profit["C leaving anyway"]
    by_uplift = SIZE * sum(p for p in profit.values() if p > 0)
    print(f"offer to everyone:       USD {everyone:+,.0f}")
    print(f"offer to highest risk:   USD {highest_risk:+,.0f}")
    print(f"offer where uplift pays: USD {by_uplift:+,.0f}")

    assert np.isclose(profit["B wavering"], 4) and np.isclose(by_uplift, 20_000)
    assert np.isclose(everyone, -180_000) and np.isclose(highest_risk, -20_000)
