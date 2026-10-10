"""Chapter 27: the agent loop with typed tools, a step cap and an approval gate.

No API is called. fake_model is a scripted stand-in for the model so the loop
runs offline; everything around it is what your application owns.
Run: python ch27_agent.py
"""
import json
import textwrap

PAYOUTS = {"M-17": {"status": "held", "reason": "reserve", "amount_usd": 1840.00}}
POLICY = {"reserve": "A reserve holds 10% of each payout for 90 days."}

TOOLS = {   # name -> argument types, the function, and whether it changes anything
    "get_payout": {"args": {"merchant_id": str}, "side_effect": False,
                   "fn": lambda merchant_id: PAYOUTS.get(merchant_id, "not found")},
    "get_policy": {"args": {"topic": str}, "side_effect": False,
                   "fn": lambda topic: POLICY.get(topic, "not found")},
    "release_payout": {"args": {"merchant_id": str}, "side_effect": True,
                       "fn": lambda merchant_id: "released"},
}


def fake_model(messages):
    """Scripted policy: what a model would plausibly propose at each step."""
    seen = [m["content"] for m in messages if m["role"] == "tool"]
    if len(seen) == 0:
        return {"tool": "get_payout", "args": {"merchant_id": "M-17"}}
    if len(seen) == 1:
        return {"tool": "get_policy", "args": {"topic": "reserve"}}
    if len(seen) == 2:
        return {"tool": "release_payout", "args": {"merchant_id": "M-17"}}
    return {"final": "The payout of USD 1,840.00 is held by a reserve. Releasing it "
                     "needs a risk analyst's approval, which I have requested."}


def run_agent(question, max_steps=5, approved=False):
    messages, trace = [{"role": "user", "content": question}], []
    for step in range(1, max_steps + 1):
        action = fake_model(messages)                 # 1. the model proposes
        if "final" in action:
            return action["final"], trace
        spec, args = TOOLS.get(action["tool"]), action["args"]
        if spec is None or any(not isinstance(args.get(k), t)   # 2. you validate
                               for k, t in spec["args"].items()):
            result = "error: unknown tool or bad arguments"
        elif spec["side_effect"] and not approved:              # 3. you gate
            result = "blocked: needs human approval"
        else:
            result = spec["fn"](**args)                          # 4. you execute
        trace.append((step, action["tool"], result))
        messages.append({"role": "tool", "content": json.dumps(result)})
    return "Stopped: step limit reached.", trace


answer, trace = run_agent("Why is merchant M-17's payout late? Release it if you can.")
for step, tool, result in trace:
    print(f"step {step}: {tool:15s} -> {result}")
print(textwrap.fill("final: " + answer, width=80))
print("with max_steps=2:", run_agent("same question", max_steps=2)[0])

# Input tokens grow with every step, because each call re-reads the whole history.
base, per_step, calls = 1000, 300, len(trace) + 1
per_call = [base + i * per_step for i in range(calls)]
print(f"input tokens per model call: {per_call} -> total {sum(per_call):,}")

# Checks against the hand calculation in the chapter.
assert sum(per_call) == calls * base + per_step * calls * (calls - 1) // 2 == 5800
assert trace[-1][2] == "blocked: needs human approval"
assert run_agent("q", approved=True)[1][-1][2] == "released"
