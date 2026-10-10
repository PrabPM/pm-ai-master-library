"""Numbers used in Chapter 22's packaging example, the labs (Chapter 27) and the
filled-in vendor matrix (Template 4)."""
from ch13_eval_sample_size import cases_per_version, wilson_interval
from ch18_unit_economics import answer_cost
from payflow import MERCHANT_QUESTIONS


def chapter22():
    print("Chapter 22: packaging Release 2")
    per_merchant = MERCHANT_QUESTIONS * answer_cost() / 30_000
    payments = 18_000 / 60
    fee = 18_000 * 0.029 + payments * 0.30
    print(f"  AI cost per merchant per month: ${per_merchant:.3f}")
    print(f"  PayFlow fee on $18,000 in $60 payments: ${fee:,.2f}")


def lab1():
    print("Lab 1: dispute evidence packets, 900 a month")
    def ev(p_right, gain, harm, fixed, n=900):
        return n * (p_right * gain - (1 - p_right) * harm) - fixed
    print(f"  X checklist template:           {ev(0.95, 2.80, 1.40, 800):>8,.0f}")
    print(f"  Y AI draft, light review:       {ev(0.88, 10.50, 36.20, 3_000):>8,.0f}")
    print(f"  Y AI draft, full review:        {ev(0.88, 10.50, 4.20, 3_000):>8,.0f}")
    need = (3_000 / 900 + 36.20) / (10.50 + 36.20)
    print(f"  Y light review breaks even at {need:.1%} right")


def lab2():
    print("Lab 2: the claim check on 500 reviewed answers, 40 truly unsupported")
    for name, tp, fp in (("A strict", 32, 28), ("B loose", 38, 82)):
        fn = 40 - tp
        cost = fn * 40 + fp * 3.78
        print(f"  {name}: precision {tp / (tp + fp):.2f}, recall {tp / 40:.2f}, "
              f"abstains on {(tp + fp) / 500:.0%}, cost ${cost:,.2f}")


def lab5():
    print("Lab 5: 172/200 versus 181/200")
    for passed in (172, 181):
        low, high = wilson_interval(passed, 200)
        print(f"  {passed}/200 = {passed / 200:.1%}, interval {low:.1%} to {high:.1%}")
    print(f"  cases needed per version: {cases_per_version(0.86, 0.905):,}")


def vendor_matrix():
    print("Template 4: weighted vendor scores (1 to 5)")
    weights = {"Golden-set quality": 30, "Worst-slice quality": 15, "Data terms": 15,
               "Latency at our context": 10, "Cost per successful task": 10,
               "Change policy and support": 10, "Exit time": 10}
    scores = {"A, hosted API": [5, 4, 4, 4, 3, 4, 3],
              "B, via our cloud": [4, 4, 5, 3, 4, 4, 4],
              "C, self-hosted open": [3, 2, 5, 3, 2, 2, 5]}
    for name, row in scores.items():
        total = sum(w * s for w, s in zip(weights.values(), row)) / 100
        print(f"  {name:<22}{total:.2f}")


def main():
    for part in (chapter22, lab1, lab2, lab5, vendor_matrix):
        part()
        print()


if __name__ == "__main__":
    main()
