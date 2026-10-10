"""Chapter 54: a compliance gate for generated marketing copy, a ticket topic
classifier, and a spike alert. Synthetic text and counts; illustrative numbers.
"""
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score

ASSETS = Path(__file__).resolve().parent.parent / "volume-2-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})
rng = np.random.default_rng(54)

# ---- 1. Voice of the customer: topic classifier on synthetic tickets ----
words = {
    "payout delay": "payout late delayed bank arrive waiting deposit missing days",
    "fees": "fee charge rate percent pricing invoice cost statement higher",
    "dispute": "dispute chargeback customer evidence bank claim lost deadline",
    "login": "login password code locked reset account access phone email",
}
filler = "hello please help thanks my the is not still today again urgent".split()
texts, labels = [], []
for topic, vocab in words.items():
    for _ in range(150):
        own = rng.choice(vocab.split(), 3)
        noise = rng.choice(filler + " ".join(words.values()).split(), 4)
        texts.append(" ".join(rng.permutation(np.concatenate([own, noise]))))
        labels.append(topic)
order = rng.permutation(len(texts))
texts, labels = np.array(texts)[order], np.array(labels)[order]
vec = TfidfVectorizer().fit(texts[:400])
clf = LogisticRegression(max_iter=500).fit(vec.transform(texts[:400]), labels[:400])
macro_f1 = f1_score(labels[400:], clf.predict(vec.transform(texts[400:])),
                    average="macro")
print(f"topic classifier macro-F1 on 200 held-out tickets: {macro_f1:.2f}")

# ---- 2. Generated copy: the disclosure is a locked template, never generated ----
DISCLOSURE = "2.9% + USD 0.30 per successful card payment"
BANNED = r"\b(guaranteed|risk-free|no fees|instant approval)\b"
variants = [
    f"Get paid the day you sell. {DISCLOSURE}.",
    f"Guaranteed next-day payouts. {DISCLOSURE}.",
    "Sell today, get paid tomorrow. Just 2.5% per payment.",
    f"One dashboard for every sale. {DISCLOSURE}.",
]


def gate(text):
    if DISCLOSURE not in text:
        return "blocked: disclosure missing or altered"
    if re.search(BANNED, text, flags=re.I):
        return "blocked: banned claim"
    return "to human review"


for i, v in enumerate(variants, 1):
    print(f"variant {i}: {gate(v)}")

# ---- 3. Spike alert on hourly 'payout delay' tickets ----
hours = 96
counts = rng.poisson(40, hours)
counts[80:84] = rng.poisson([75, 95, 110, 90])        # an outage starts at hour 80


def z_score(history, value):
    return (value - history.mean()) / history.std(ddof=1)


alerts = [h for h in range(48, hours) if z_score(counts[h - 48:h], counts[h]) > 3]
first = alerts[0]
z_first = z_score(counts[first - 48:first], counts[first])
print(f"hand check: (75 - 40) / 6.3 = {(75 - 40) / 6.3:.1f}")
print(f"first alert at hour {first}: {counts[first]} tickets, z = {z_first:.1f}; "
      f"alerts in 48 hours: {len(alerts)}")

# ---- 4. Money for the campaign ----
sends, ctr_old, ctr_new = 200_000, 0.020, 0.026       # click rate before and after
signup_rate, value, review = 0.05, 150, 20            # USD per signup, per review
gain = sends * (ctr_new - ctr_old) * signup_rate * value - len(variants) * review
print(f"campaign gain: USD {gain:,.0f}")

# ---- checks ----
assert [gate(v)[:7] for v in variants] == ["to huma", "blocked", "blocked", "to huma"]
assert np.isclose(gain, 8_920.0)
assert np.isclose((75 - 40) / 6.3, 5.6, atol=0.05)
assert first == 80 and macro_f1 > 0.8

# ---- figure ----
fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=100)
ax.plot(range(hours), counts, color="#4f46e5", lw=1.5)
mu, sd = counts[32:80].mean(), counts[32:80].std(ddof=1)
ax.axhline(mu + 3 * sd, color="#b91c1c", ls="--", lw=1.5)
ax.text(1, mu + 3 * sd + 3, "alert line: mean + 3 standard deviations", color="#b91c1c")
ax.plot(alerts, counts[alerts], "o", color="#b91c1c")
ax.annotate("outage begins", (80, counts[80]), textcoords="offset points",
            xytext=(-88, 8), color="#1f2937")
ax.set_xlabel("hour")
ax.set_ylabel("'payout delay' tickets per hour")
ax.grid(axis="y")
fig.savefig(ASSETS / "ch54-ticket-spike.svg", bbox_inches="tight",
            metadata={"Date": None})
