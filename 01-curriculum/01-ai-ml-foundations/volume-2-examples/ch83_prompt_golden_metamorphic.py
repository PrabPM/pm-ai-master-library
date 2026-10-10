"""Chapter 83. A prompt as a versioned artifact, a golden-set regression test and a
metamorphic test. The "model" is a small ticket router standing in for an LLM call:
the test harness is the same either way."""
import hashlib
import json

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# ---- 1. The prompt is an artifact with an id -------------------------------------
prompt = {
    "name": "support_router",
    "system": "Route the merchant's ticket to payouts, disputes or account.",
    "examples": [["My payout is late", "payouts"], ["I got a chargeback", "disputes"]],
    "model": "router-llm-2026-06",
    "temperature": 0.0,
    "max_tokens": 5,
}


def prompt_id(artifact):
    canonical = json.dumps(artifact, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()[:12]


v_a = prompt_id(prompt)
v_b = prompt_id(dict(prompt, temperature=0.2))
print("prompt id", v_a, "| with temperature 0.2:", v_b)
assert v_a == prompt_id(dict(reversed(list(prompt.items())))) and v_a != v_b

# ---- 2. A stand-in model with a flaw to find -------------------------------------
TEMPLATES = {
    "payouts": ["{m} says the payout has not arrived", "payout to {m} is delayed again",
                "{m} asks when the transfer reaches the bank",
                "{m} wants a different payout schedule"],
    "disputes": ["{m} received a chargeback and wants to respond",
                 "a customer disputed a charge at {m}",
                 "{m} asks how to upload dispute evidence",
                 "{m} lost a dispute and asks why"],
    "account": ["{m} cannot log in to the dashboard",
                "{m} needs to update the bank details",
                "{m} asks to add a team member",
                "{m} wants to change the business address"],
}
MERCHANTS = ["Northwind", "Bluebird", "Cascade", "Larkspur"]
# In the training tickets each merchant mostly writes about one thing.
HABIT = {"Northwind": "payouts", "Bluebird": "disputes", "Cascade": "account"}

rng = np.random.default_rng(83)
train_text, train_route = [], []
for _ in range(400):
    m = MERCHANTS[rng.integers(4)]
    routes = list(TEMPLATES)
    p = [0.9 if HABIT.get(m) == r else 0.05 for r in routes] if m in HABIT else None
    route = routes[rng.choice(3, p=p)]
    train_text.append(TEMPLATES[route][rng.integers(4)].format(m=m))
    train_route.append(route)


def mask_names(text):
    for m in MERCHANTS:
        text = text.replace(m, "MERCHANT")
    return text


def build_router(preprocess):
    vec = CountVectorizer()
    clf = LogisticRegression(max_iter=500)
    clf.fit(vec.fit_transform([preprocess(t) for t in train_text]), train_route)
    return lambda text: clf.predict(vec.transform([preprocess(text)]))[0]


# ---- 3. Golden set: fixed inputs, expected outputs, severities -------------------
GOLDEN = [   # (ticket, expected route, severity)
    ("Northwind says the payout never arrived", "payouts", "hard"),
    ("Bluebird received a chargeback yesterday", "disputes", "hard"),
    ("Cascade cannot log in", "account", "hard"),
    ("Larkspur lost a dispute", "disputes", "hard"),
    ("Northwind asks why it is delayed", "payouts", "soft"),
    ("Bluebird asks why the charge was reversed", "disputes", "soft"),
    ("Cascade asks when the dashboard updates", "account", "soft"),
    ("Cascade needs a team login", "account", "soft"),
    ("Larkspur needs to update the bank details", "account", "soft"),
    ("Bluebird wants to respond", "disputes", "soft"),
]


def golden_test(router, max_soft_failures=1):
    fails = [(sev, t) for t, want, sev in GOLDEN if router(t) != want]
    hard = sum(sev == "hard" for sev, _ in fails)
    return hard == 0 and len(fails) - hard <= max_soft_failures, hard, len(fails) - hard


# ---- 4. Metamorphic test: renaming the merchant must not change the route --------
def invariance_test(router):
    pairs, flips = 0, []
    for ticket, _, _ in GOLDEN:
        name = next(m for m in MERCHANTS if m in ticket)
        for other in MERCHANTS:
            if other != name:
                pairs += 1
                swapped = ticket.replace(name, other)
                if router(swapped) != router(ticket):
                    flips.append(swapped)
    return pairs, flips


results = {}
for label, pre in [("raw text", lambda t: t), ("names masked", mask_names)]:
    router = build_router(pre)
    ok, hard, soft = golden_test(router)
    pairs, flips = invariance_test(router)
    results[label] = (ok, len(flips))
    print(f"\n{label}: golden {'pass' if ok else 'FAIL'} "
          f"(hard failures {hard}, soft failures {soft})")
    print(f"   {len(flips)} of {pairs} renamed tickets change route "
          f"({len(flips) / pairs:.1%})")
    for f in flips[:3]:
        print(f"   {f!r} -> {router(f)}")
assert results["raw text"][0] and results["raw text"][1] > 0
assert results["names masked"][1] == 0
