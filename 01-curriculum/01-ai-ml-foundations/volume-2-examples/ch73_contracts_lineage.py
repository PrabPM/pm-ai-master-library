"""Chapter 73. Data as a product: a contract check, a completeness gate,
a freshness budget and a lineage blast radius for PayFlow's payment_events."""
import numpy as np

# ---- 1. The contract and three proposed changes --------------------------------
V1 = {
    "payment_id": {"type": "string"},
    "merchant_id": {"type": "string"},
    "amount_cents": {"type": "int"},
    "status": {"type": "enum", "values": ["approved", "declined"]},
}


def breaking_changes(old, new):
    """Reasons the change breaks an old reader or a new one."""
    why = []
    for name, spec in old.items():
        if name not in new and "default" not in spec:
            why.append(f"removed {name}")
        elif name in new and new[name] != spec:       # type or allowed values
            why.append(f"changed {name}")
    for name, spec in new.items():
        if name not in old and "default" not in spec:
            why.append(f"added {name} with no default")
    return why


add_optional = dict(V1, mcc={"type": "int", "default": None})
rename = {k: v for k, v in V1.items() if k != "amount_cents"}
rename["amount_minor"] = {"type": "int"}
new_status = dict(V1, status={"type": "enum",
                              "values": ["approved", "declined", "pending_review"]})

results = {}
for label, proposal in [("add optional mcc", add_optional),
                        ("rename amount_cents", rename),
                        ("add a status value", new_status)]:
    why = breaking_changes(V1, proposal)
    results[label] = why
    print(f"{label:20s}", "BREAKING: " + "; ".join(why) if why else "compatible")

assert results["add optional mcc"] == []
assert len(results["rename amount_cents"]) == 2
assert len(results["add a status value"]) == 1

# ---- 2. Completeness gate and freshness error budget ----------------------------
active, with_kyb, target = 10_000, 9_930, 0.995
completeness = with_kyb / active
assert np.isclose(completeness, 0.993)
print(f"\ncompleteness {completeness:.3f} vs target {target} ->",
      "pass" if completeness >= target else "FAIL")

minutes = 30 * 24 * 60                      # a 30-day window, measured per minute
budget = round(minutes * (1 - 0.99))        # SLO: lag <= 60 s in 99% of minutes
bad_minutes = 130
assert (minutes, budget) == (43_200, 432)
print(f"error budget {budget} bad minutes, used {bad_minutes} "
      f"({bad_minutes / budget:.0%})")

# ---- 3. Lineage: blast radius and the freshness budget along one path -----------
EDGES = {                                   # producer -> consumers
    "payment_events": ["payments_clean"],
    "payments_clean": ["velocity_5m", "merchant_daily"],
    "velocity_5m": ["online_store"],
    "online_store": ["fraud_model"],
    "merchant_daily": ["churn_model", "dashboard"],
    "kyb_documents": ["merchant_profile"],
    "merchant_profile": ["onboarding_risk_model"],
}
HOP_P99 = {"payment_events": 3, "payments_clean": 4, "velocity_5m": 12,
           "online_store": 5}               # seconds each hop may add, at its p99


def blast_radius(node):
    """Everything downstream of `node`: its transitive consumers."""
    seen, stack = set(), [node]
    while stack:
        for child in EDGES.get(stack.pop(), []):
            if child not in seen:
                seen.add(child)
                stack.append(child)
    return seen


print(f"blast radius of payment_events: {len(blast_radius('payment_events'))} assets")
assert len(blast_radius("payment_events")) == 7
assert blast_radius("kyb_documents") == {"merchant_profile", "onboarding_risk_model"}

path = ["payment_events", "payments_clean", "velocity_5m", "online_store"]
budget_s = sum(HOP_P99[n] for n in path)
assert budget_s == 24
print(f"sum of hop limits {budget_s} s vs the model's 30 s need: "
      f"margin {30 - budget_s} s")

# Percentiles do not add. Simulate independent hop lags whose p99 equals each limit.
rng = np.random.default_rng(73)
lags = []
for n in path:
    raw = rng.lognormal(mean=0.0, sigma=0.8, size=200_000)
    lags.append(raw * HOP_P99[n] / np.quantile(raw, 0.99))
total = np.sum(lags, axis=0)
within = np.mean(total <= budget_s)
print(f"simulated end-to-end p99 {np.quantile(total, 0.99):.1f} s; "
      f"{within:.2%} of events within {budget_s} s")
assert within >= 1 - 4 * 0.01               # the union bound: at least 96%
