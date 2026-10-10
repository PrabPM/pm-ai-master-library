"""Case 1 (chapter 124): ship or hold a fraud model whose offline metrics improved.

Per 1,000,000 payments. All numbers are illustrative PayFlow figures.
"""
import numpy as np

PAYMENTS, FRAUD_RATE = 1_000_000, 0.005
FRAUD_LOSS, AVG_TICKET = 120.0, 80.0
FEE = 0.029 * AVG_TICKET + 0.30                 # PayFlow's revenue on one payment


def outcome(block_rate, recall):
    frauds = PAYMENTS * FRAUD_RATE
    blocked = PAYMENTS * block_rate
    caught = frauds * recall
    good_blocked = blocked - caught
    cost = (frauds - caught) * FRAUD_LOSS + good_blocked * FEE
    good_block_rate = good_blocked / (PAYMENTS - frauds)
    return caught, good_blocked, good_block_rate, cost


OPTIONS = {"current model": (0.010, 0.62),
           "new model, same score threshold": (0.016, 0.74),
           "new model, block rate matched": (0.010, 0.70)}

if __name__ == "__main__":
    print(f"fee per payment: USD {FEE:.2f}")
    costs = {}
    for name, (block_rate, recall) in OPTIONS.items():
        caught, good_blocked, gbr, cost = outcome(block_rate, recall)
        costs[name] = cost
        print(f"{name}")
        print(f"   fraud caught {caught:,.0f}  good blocked {good_blocked:,.0f} "
              f"({gbr:.2%} of good)  cost USD {cost:,.0f}")
    extra = outcome(0.016, 0.74)[1] - outcome(0.010, 0.62)[1]
    print(f"same threshold: {extra:,.0f} more good payments blocked, "
          f"USD {extra * AVG_TICKET:,.0f} of merchants' sales")
    saving = costs["current model"] - costs["new model, block rate matched"]
    print(f"matched block rate saves USD {saving:,.0f} per million payments")

    assert np.isclose(FEE, 2.62)
    assert np.isclose(costs["current model"], 246_078)
    assert np.isclose(costs["new model, same score threshold"], 188_226)
    assert np.isclose(costs["new model, block rate matched"], 197_030)
    assert np.isclose(extra, 5_400) and np.isclose(saving, 49_048)
