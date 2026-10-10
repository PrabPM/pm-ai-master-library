"""Case 4 (chapter 124): sizing a drift incident after a large merchant joins."""
import numpy as np

WEEKLY, NEW_SHARE = 2_000_000, 0.12            # payments a week; new merchant's share
BASE_BLOCK, NEW_BLOCK = 0.022, 0.09            # block rates
TICKET = 95.0                                  # new merchant's average payment, USD

# Merchant-category mix: training vs this week (five groups).
TRAINED = np.array([0.40, 0.25, 0.20, 0.14, 0.01])
NOW = np.array([0.35, 0.22, 0.18, 0.12, 0.13])


def psi(expected, actual):
    return float(((actual - expected) * np.log(actual / expected)).sum())


if __name__ == "__main__":
    new_volume = WEEKLY * NEW_SHARE
    blocked = (WEEKLY - new_volume) * BASE_BLOCK + new_volume * NEW_BLOCK
    print(f"approval rate: before {1 - BASE_BLOCK:.2%}, now {1 - blocked / WEEKLY:.2%}")
    print(f"PSI on merchant category: {psi(TRAINED, NOW):.2f}")

    extra = new_volume * (NEW_BLOCK - BASE_BLOCK)
    fee = 0.029 * TICKET + 0.30
    print(f"extra payments blocked at the new merchant: {extra:,.0f} a week")
    print(f"merchant sales lost: USD {extra * TICKET:,.0f}; "
          f"PayFlow fees lost: USD {extra * fee:,.0f}")
    hours = extra * 2 / 60
    print(f"reviewing all of them by hand at 2 minutes each: {hours:,.0f} hours, "
          f"{hours / 40:.0f} people")

    sample = 0.05 * extra
    print(f"reviewing a random 5% instead: {sample:,.0f} payments, "
          f"{sample * 2 / 60:.0f} hours a week")

    assert np.isclose(new_volume, 240_000)
    assert np.isclose(sample, 816) and np.isclose(sample * 2 / 60, 27.2)
    assert np.isclose(1 - blocked / WEEKLY, 0.96984)
    assert np.isclose(extra, 16_320) and np.isclose(fee, 3.055)
    assert np.isclose(extra * TICKET, 1_550_400)
    assert np.isclose(extra * fee, 49_857.6)
    assert psi(TRAINED, NOW) > 0.25
