"""Chapter 3: precision, recall and F1 on 40 labeled tickets, at three thresholds."""

# Risk score from the takeover model for 40 tickets Priya's team labeled by hand.
TAKEOVER = [0.95, 0.88, 0.81, 0.74, 0.62, 0.55, 0.41, 0.22]            # 8 real cases
HONEST = [0.78, 0.66, 0.58, 0.52, 0.47, 0.44, 0.39, 0.36, 0.33, 0.31, 0.28,
          0.27, 0.24, 0.21, 0.19, 0.18, 0.16, 0.15, 0.13, 0.12, 0.11, 0.10,
          0.09, 0.08, 0.07, 0.06, 0.05, 0.05, 0.04, 0.03, 0.02, 0.02]   # 32 honest
MISS_COST = 900     # average loss when a takeover is missed, dollars
REVIEW_COST = 6     # eight minutes of a risk analyst's time, dollars


# [listing]
def confusion(threshold):
    tp = sum(score >= threshold for score in TAKEOVER)   # flagged, and real
    fp = sum(score >= threshold for score in HONEST)     # flagged, but honest
    fn = len(TAKEOVER) - tp                              # real, but missed
    tn = len(HONEST) - fp
    return tp, fp, fn, tn


def metrics(threshold):
    tp, fp, fn, tn = confusion(threshold)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    f1 = 2 * precision * recall / (precision + recall)
    accuracy = (tp + tn) / (tp + fp + fn + tn)
    cost = fn * MISS_COST + (tp + fp) * REVIEW_COST
    return precision, recall, f1, accuracy, cost
# [end listing]


def main():
    print("Threshold  TP  FP  FN  TN  Precision  Recall    F1  Accuracy    Cost")
    for threshold in (0.7, 0.5, 0.3):
        tp, fp, fn, tn = confusion(threshold)
        p, r, f1, acc, cost = metrics(threshold)
        print(f"{threshold:>9}{tp:>4}{fp:>4}{fn:>4}{tn:>4}{p:>11.2f}{r:>8.2f}"
              f"{f1:>6.2f}{acc:>10.1%}{cost:>8,}")
    never = len(HONEST) / (len(HONEST) + len(TAKEOVER))
    print(f"Flag nothing at all: accuracy {never:.1%}, "
          f"cost {len(TAKEOVER) * MISS_COST:,}")


if __name__ == "__main__":
    main()
