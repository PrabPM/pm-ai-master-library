"""Chapter 42: mutual information versus correlation.

Feature A: amount bucket (small, medium, large). Fraud is high at both ends:
card testing uses tiny amounts, cash-out uses large ones.
Feature B: new-device flag, with a small, steady lift in fraud.
Writes volume-1-assets/ch42-u-shaped-fraud.svg.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)


def H(p):
    p = np.asarray(p, dtype=float).ravel()
    p = p[p > 0]
    return float(np.sum(p * np.log2(1 / p)))


def mutual_information(joint):
    """I(X;Y) = H(X) + H(Y) - H(X,Y), in bits, from a joint table."""
    joint = np.asarray(joint, dtype=float)
    return H(joint.sum(axis=1)) + H(joint.sum(axis=0)) - H(joint)


def correlation(joint, x_values, y_values):
    px, py = joint.sum(axis=1), joint.sum(axis=0)
    ex, ey = px @ x_values, py @ y_values
    cov = x_values @ joint @ y_values - ex * ey
    sx = np.sqrt(px @ (x_values - ex) ** 2)
    sy = np.sqrt(py @ (y_values - ey) ** 2)
    return cov / (sx * sy)


# ---- exact tables: rows = feature value, columns = (legitimate, fraud) -----
share = np.array([0.25, 0.50, 0.25])            # small, medium, large
fraud_rate = np.array([0.08, 0.01, 0.08])
amount = np.column_stack([share * (1 - fraud_rate), share * fraud_rate])
device = np.array([[0.80 * 0.96, 0.80 * 0.04],     # known device: 4% fraud
                   [0.20 * 0.935, 0.20 * 0.065]])  # new device: 6.5% fraud
labels = np.array([0.0, 1.0])
for name, table, codes in [("amount bucket", amount, np.array([0.0, 1.0, 2.0])),
                           ("new device", device, np.array([0.0, 1.0]))]:
    mi = mutual_information(table)
    h_y = H(table.sum(axis=0))
    print(f"{name:13}: correlation = {correlation(table, codes, labels):+.4f}, "
          f"I = {mi:.4f} bits = {mi / h_y:.1%} of H(fraud)")

# hand result for the amount bucket
h_fraud = H([0.045, 0.955])
h_given = 0.25 * H([0.08, 0.92]) + 0.50 * H([0.01, 0.99]) + 0.25 * H([0.08, 0.92])
print(f"H(fraud) = {h_fraud:.4f}, H(fraud | bucket) = {h_given:.4f}, "
      f"difference = {h_fraud - h_given:.4f}")
assert np.isclose(mutual_information(amount), h_fraud - h_given)
assert np.isclose(round(h_fraud - h_given, 4), 0.0233)
assert abs(correlation(amount, np.array([0.0, 1.0, 2.0]), labels)) < 1e-12
assert mutual_information(amount) > 5 * mutual_information(device)

# ---- the same thing estimated from 20,000 sampled payments -----------------
rng = np.random.default_rng(42)
n = 20_000
bucket = rng.choice(3, size=n, p=share)
fraud = (rng.random(n) < fraud_rate[bucket]).astype(int)


def estimate(x, y):
    table = np.zeros((x.max() + 1, 2))
    np.add.at(table, (x, y), 1)
    return mutual_information(table / len(x))


shuffled = [estimate(bucket, rng.permutation(fraud)) for _ in range(200)]
print(f"sample of {n:,}: correlation = {np.corrcoef(bucket, fraud)[0, 1]:+.4f}, "
      f"estimated I = {estimate(bucket, fraud):.4f} bits")
print(f"same feature, labels shuffled 200 times: I = {np.mean(shuffled):.5f} bits "
      f"on average, {np.max(shuffled):.5f} at most")
assert abs(np.corrcoef(bucket, fraud)[0, 1]) < 0.02
assert estimate(bucket, fraud) > 10 * np.max(shuffled)


def draw():
    plt.rcParams.update({
        "svg.fonttype": "none", "svg.hashsalt": "ch42", "font.family": "Helvetica",
        "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
        "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
    fig, ax = plt.subplots(figsize=(5.6, 3.2), dpi=100)
    x = np.arange(3)
    ax.bar(x, fraud_rate * 100, 0.55, color="#4f46e5")
    for xi, rate in zip(x, fraud_rate):
        ax.text(xi, rate * 100 + 0.25, f"{rate:.0%}", ha="center", fontsize=10,
                color="#1f2937")
    ax.plot([-0.45, 2.45], [4.5, 4.5], "--", color="#b91c1c", linewidth=1.4)
    ax.text(0.42, 4.85, "best straight line is flat:", color="#b91c1c",
            fontsize=10)
    ax.text(0.42, 3.55, "correlation = 0", color="#b91c1c", fontsize=10)
    ax.set_xticks(x, ["small\n(under USD 5)", "medium", "large\n(over USD 500)"])
    ax.set_ylabel("fraud rate (%)")
    ax.set_ylim(0, 9.5)
    fig.tight_layout()
    fig.savefig(ASSETS / "ch42-u-shaped-fraud.svg", bbox_inches="tight",
                metadata={"Date": None})
    plt.close(fig)


draw()
