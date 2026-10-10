"""Chapter 51: the skeleton of an operations assistant: retrieve, call a read-only
tool, answer with citations or abstain. Illustrative policies and numbers.
"""
import math
import re
import textwrap
from collections import Counter

POLICIES = {
    "P1": "Payouts are sent on the next business day after settlement.",
    "P2": "A payout is placed on hold while a changed bank account is verified.",
    "P3": "Bank account verification usually takes up to two business days.",
    "P4": "A dispute must be contested with evidence before the network deadline.",
    "P5": "Refunds return the payment amount; the fixed fee is not returned.",
    "P6": "Rolling reserves hold ten percent of volume for ninety days.",
}
PAYOUTS = {"PO-8850": {"status": "on hold", "reason": "bank account verification",
                       "amount_usd": 1284.40, "hold_started": "2026-10-12"}}


STOP = set("a an the is are in on of for to and with while how why does can".split())


def tokens(text):
    """Lower-case words cut to five letters, a crude way to match word forms."""
    return [w[:5] for w in re.findall(r"[a-z]+", text.lower()) if w not in STOP]


N_DOCS = len(POLICIES)
DF = Counter(w for text in POLICIES.values() for w in set(tokens(text)))


def vector(text):
    """TF-IDF weights: words that are rare across the policies count for more."""
    tf = Counter(tokens(text))
    return {w: c * math.log((N_DOCS + 1) / (DF[w] + 1)) for w, c in tf.items()}


def cosine(a, b):
    dot = sum(a[w] * b[w] for w in a if w in b)
    return dot / (math.hypot(*a.values()) * math.hypot(*b.values()) or 1.0)


def get_payout(payout_id):
    """Read-only tool. The assistant has no tool that moves money."""
    return PAYOUTS.get(payout_id)


def assist(question, min_score=0.15, k=2):
    q = vector(question)
    ranked = sorted(((cosine(q, vector(t)), pid) for pid, t in POLICIES.items()),
                    reverse=True)[:k]
    support = [(pid, round(score, 2)) for score, pid in ranked if score >= min_score]
    found = re.search(r"PO-\d+", question)
    record = get_payout(found.group()) if found else None
    if not support and not record:
        return "No supported answer found. Offer: escalate to payments operations."
    facts = [f"{POLICIES[pid]} [{pid} {score}]" for pid, score in support]
    if record:
        facts.insert(0, f"{found.group()} is {record['status']} for "
                        f"{record['reason']} since {record['hold_started']}. [tool]")
    return " ".join(facts)


for question in ["Why is payout PO-8850 on hold, and how long does verification "
                 "usually take?", "Can a merchant pay a supplier in euros?"]:
    print("Q:", question)
    print(textwrap.fill(assist(question), 84, initial_indent="A: ",
                        subsequent_indent="   "))

# Handle-time arithmetic for one month.
tickets, manual_min, assisted_min, used = 9000, 12.0, 5.0, 0.70
new_aht = used * assisted_min + (1 - used) * manual_min
hours_saved = tickets * (manual_min - new_aht) / 60
net = hours_saved * 40.0 - tickets * 0.04          # USD 40 per hour, 4 cents a call
print(f"average handle time {manual_min:.1f} -> {new_aht:.1f} min; "
      f"{hours_saved:.0f} hours saved; net USD {net:,.0f} per month")

# ---- checks ----
assert "[P2 " in assist("Why is payout PO-8850 on hold?")
assert assist("Can a merchant pay a supplier in euros?").startswith("No supported")
assert math.isclose(new_aht, 7.1) and math.isclose(hours_saved, 735.0)
assert math.isclose(net, 29_040.0)
