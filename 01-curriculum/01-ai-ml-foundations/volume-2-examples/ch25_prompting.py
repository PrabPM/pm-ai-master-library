"""Chapter 25: test a prompt instead of admiring it, and the price of voting.

No API is called. fake_model is a deterministic stand-in so the harness runs
offline; in a real project that one function is the call to your model.
Run: python ch25_prompting.py
"""
from math import comb

import numpy as np

LABELS = ["PAYOUT", "REFUND", "DISPUTE"]
ZERO_SHOT = "Classify this PayFlow support ticket.\nTicket: {ticket}"
WITH_LABELS = ("Classify this PayFlow support ticket. Answer with one word: "
               "PAYOUT, REFUND or DISPUTE.\nTicket: {ticket}")
FEW_SHOT = (WITH_LABELS.replace("Ticket: {ticket}", "") +
            "Ticket: The bank reversed a charge the customer says is fraud.\n"
            "Answer: DISPUTE\nTicket: {ticket}\nAnswer:")

TESTS = [                                   # (ticket, expected label)
    ("My payout has not arrived.", "PAYOUT"),
    ("Where is this week's payout?", "PAYOUT"),
    ("Customer wants a refund for order 88.", "REFUND"),
    ("How do I refund half of a payment?", "REFUND"),
    ("I got a chargeback notice from the bank.", "DISPUTE"),
    ("A customer filed a dispute, what now?", "DISPUTE"),
]


def fake_model(prompt):
    """Stand-in for an API call. It mimics two habits of real models: it chats
    unless told the format, and it learns unfamiliar words from examples."""
    ticket = prompt.rsplit("Ticket:", 1)[1].lower()
    topic = next((lab for lab in LABELS if lab.lower() in ticket), None)
    if topic is None and "chargeback" in ticket and "Answer: DISPUTE" in prompt:
        topic = "DISPUTE"                   # only the few-shot prompt teaches this
    if "one word" not in prompt:
        return f"This ticket looks like it is about a {topic or 'billing'} problem."
    return topic or "PAYOUT"


def pass_rate(template):
    passed = sum(fake_model(template.format(ticket=t)) == want for t, want in TESTS)
    return passed, len(TESTS)


for name, template in [("zero-shot", ZERO_SHOT), ("zero-shot + labels", WITH_LABELS),
                       ("few-shot", FEW_SHOT)]:
    passed, n = pass_rate(template)
    print(f"{name:19s} passed {passed}/{n}")


def majority_correct(p, n):
    """P(more than half of n independent samples are right), each right w.p. p."""
    need = n // 2 + 1
    return sum(comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(need, n + 1))


print("self-consistency, each sample right with probability 0.7:")
for n in (1, 3, 5, 9):
    print(f"  {n} samples: P(majority right) = {majority_correct(0.7, n):.4f}, "
          f"cost x{n}")
rng = np.random.default_rng(0)
votes = rng.random((200_000, 5)) < 0.7
print(f"  simulated, 5 samples: {np.mean(votes.sum(axis=1) >= 3):.4f}")

# Checks against the hand calculation in the chapter.
assert [pass_rate(t)[0] for t in (ZERO_SHOT, WITH_LABELS, FEW_SHOT)] == [0, 5, 6]
assert np.isclose(majority_correct(0.7, 5), 0.3087 + 0.36015 + 0.16807)
assert abs(np.mean(votes.sum(axis=1) >= 3) - 0.83692) < 0.005
