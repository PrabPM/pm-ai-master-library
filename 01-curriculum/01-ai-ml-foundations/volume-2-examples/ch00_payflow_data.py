"""PayFlow's synthetic tables, used by every example in Parts I and II.

PayFlow is fictional. Every number here is generated from a fixed seed, so each
run of each script prints the same thing. Import the functions from another
script in this folder, or run this file to print the first rows of each table.
"""
import numpy as np

PAYMENT_FEATURES = ["amount", "hour", "new_card", "foreign_card", "velocity_1h"]
MERCHANT_FEATURES = ["tenure_months", "monthly_volume", "avg_ticket", "refund_rate",
                     "dispute_rate", "tickets_90d"]
CATEGORIES = ["retail", "food", "software", "services"]


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def payments(n=20000, seed=114):
    """One row per card payment. is_fraud is the label (about 2% of rows)."""
    rng = np.random.default_rng(seed)
    amount = np.round(rng.lognormal(np.log(40.0), 0.9, n), 2)
    hour = rng.integers(0, 24, n)
    new_card = rng.binomial(1, 0.25, n)
    foreign_card = rng.binomial(1, 0.10, n)
    velocity_1h = rng.poisson(0.3, n)
    night = (hour < 6).astype(float)
    z = (-5.5 + 1.0 * velocity_1h + 1.5 * new_card + 1.3 * foreign_card
         + 0.6 * np.log(amount / 40.0) + 0.7 * night)
    is_fraud = rng.binomial(1, sigmoid(z))
    return {"amount": amount, "hour": hour, "new_card": new_card,
            "foreign_card": foreign_card, "velocity_1h": velocity_1h,
            "is_fraud": is_fraud}


def merchants(n=2000, seed=1):
    """One row per merchant. churned is the label (left within 90 days)."""
    rng = np.random.default_rng(seed)
    category = rng.choice(len(CATEGORIES), n, p=[0.4, 0.3, 0.1, 0.2])
    tenure_months = rng.integers(1, 61, n)
    monthly_volume = np.round(rng.lognormal(np.log(18.0), 0.8, n), 1)   # USD thousands
    avg_ticket = np.round(rng.lognormal(np.log(45.0), 0.5, n), 2)       # USD
    refund_rate = np.round(rng.gamma(2.0, 1.2, n), 1)                   # percent
    dispute_rate = np.round(rng.gamma(1.5, 0.2, n), 2)                  # percent
    tickets_90d = rng.poisson(1.5 + 0.4 * refund_rate)
    z = (-1.6 - 0.03 * tenure_months - 0.35 * np.log(monthly_volume / 18.0)
         + 0.18 * tickets_90d + 0.9 * dispute_rate)
    churned = rng.binomial(1, sigmoid(z))
    return {"category": category, "tenure_months": tenure_months,
            "monthly_volume": monthly_volume, "avg_ticket": avg_ticket,
            "refund_rate": refund_rate, "dispute_rate": dispute_rate,
            "tickets_90d": tickets_90d, "churned": churned}


def payouts(n=400, seed=7):
    """One row per payout. delay_hours is the number to forecast."""
    rng = np.random.default_rng(seed)
    amount_k = np.round(rng.uniform(0.2, 8.0, n), 2)                    # USD thousands
    weekend = rng.binomial(1, 2 / 7, n)
    new_bank = rng.binomial(1, 0.15, n)
    delay_hours = np.round(2.0 + 1.5 * amount_k + 12.0 * weekend + 6.0 * new_bank
                           + rng.normal(0.0, 2.0, n), 1)
    return {"amount_k": amount_k, "weekend": weekend, "new_bank": new_bank,
            "delay_hours": delay_hours}


def review_sample(n=300, seed=5):
    """A small hand-labeled sample with two features, so it can be drawn.

    Columns: amount in USD hundreds and card age in days (both 0 to 4), then the
    label. Fraud concentrates on new cards at mid-to-high amounts, so the region
    is curved and no straight line separates it. 5% of labels are flipped.
    """
    rng = np.random.default_rng(seed)
    X = rng.uniform(0.0, 4.0, (n, 2))
    inside = ((X[:, 0] - 2.4) / 1.4) ** 2 + (X[:, 1] / 2.4) ** 2 < 1
    flip = rng.random(n) < 0.05
    return X, np.where(flip, ~inside, inside).astype(int)


def fresh_review_sample(n=2000):
    """New payments from the same process, for testing."""
    return review_sample(n, seed=105)


TICKETS = [
    ("payout late", "payouts"),
    ("payout missing", "payouts"),
    ("chargeback dispute", "disputes"),
    ("dispute late", "disputes"),
]

DOCUMENTS = [
    ("D-101", "registration certificate", "legal_name", "Northwind Outfitters LLC",
     0.98, 1),
    ("D-101", "registration certificate", "registration_no", "4471-2209", 0.91, 1),
    ("D-102", "bank letter", "account_holder", "Northwind Outfiters", 0.62, 0),
    ("D-103", "owner ID", "date_of_birth", "1988-04-17", 0.95, 1),
]


def matrix(table, columns):
    """Stack the named columns into an (n, d) float matrix."""
    return np.column_stack([table[c] for c in columns]).astype(float)


def split(X, y, test_share=0.25, seed=0):
    """Shuffle once, then cut into train and test parts."""
    order = np.random.default_rng(seed).permutation(len(y))
    cut = int(len(y) * (1 - test_share))
    return X[order[:cut]], X[order[cut:]], y[order[:cut]], y[order[cut:]]


def head(table, columns, rows=4):
    """The first rows as a list of lists, header first."""
    out = [list(columns)]
    for i in range(rows):
        row = [table[c][i].item() for c in columns]
        if "category" in columns:
            row[columns.index("category")] = CATEGORIES[table["category"][i]]
        out.append(row)
    return out


SHOW = {
    "payments": (payments, PAYMENT_FEATURES + ["is_fraud"], 5),
    "merchants": (merchants, ["category", "tenure_months", "monthly_volume",
                              "refund_rate", "tickets_90d", "churned"], 4),
    "payouts": (payouts, ["amount_k", "weekend", "new_bank", "delay_hours"], 4),
}

if __name__ == "__main__":
    for name, (make, cols, rows) in SHOW.items():
        table = make()
        print(f"{name} ({len(table[cols[-1]])} rows)")
        for row in head(table, cols, rows):
            print("  " + " ".join(f"{v!s:>14}" for v in row))
    pay, mer, po = payments(), merchants(), payouts()
    print(f"fraud rate {pay['is_fraud'].mean():.3f}   "
          f"churn rate {mer['churned'].mean():.3f}   "
          f"mean payout delay {po['delay_hours'].mean():.1f} h")
    assert 0.015 < pay["is_fraud"].mean() < 0.025
