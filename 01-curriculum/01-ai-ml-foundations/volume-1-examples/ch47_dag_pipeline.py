"""Chapter 47: PayFlow's nightly fraud-model pipeline as a DAG.

Each step lists the steps it needs first and how many minutes it takes.
"""
from collections import deque

steps = {   # step: (minutes, steps it depends on)
    "payments": (10, []),                       # ingest yesterday's payments
    "disputes": (5, []),                        # ingest new disputes (the labels)
    "features": (30, ["payments"]),
    "labels": (10, ["payments", "disputes"]),
    "train": (40, ["features", "labels"]),
    "evaluate": (10, ["train"]),
    "publish": (5, ["evaluate"]),
}


def topological_order(steps):
    """Kahn's algorithm: repeatedly run a step whose inputs are all done."""
    waiting_on = {s: len(deps) for s, (_, deps) in steps.items()}   # in-degree
    unlocks = {s: [] for s in steps}
    for s, (_, deps) in steps.items():
        for d in deps:
            unlocks[d].append(s)
    ready = deque(s for s in steps if waiting_on[s] == 0)
    order = []
    while ready:
        s = ready.popleft()
        order.append(s)
        for nxt in unlocks[s]:
            waiting_on[nxt] -= 1
            if waiting_on[nxt] == 0:
                ready.append(nxt)
    if len(order) < len(steps):          # some steps never became ready
        stuck = sorted(set(steps) - set(order))
        raise ValueError("cycle: " + ", ".join(stuck) + " wait on each other")
    return order


def schedule(steps):
    """Earliest finish time of every step, and the chain that sets the total."""
    finish, blocker = {}, {}
    for s in topological_order(steps):
        minutes, deps = steps[s]
        blocker[s] = max(deps, key=lambda d: finish[d], default=None)
        finish[s] = minutes + (finish[blocker[s]] if deps else 0)
    last = max(finish, key=finish.get)
    chain = [last]
    while blocker[chain[-1]] is not None:
        chain.append(blocker[chain[-1]])
    return finish, chain[::-1]


order = topological_order(steps)
print("run order:", " -> ".join(order))
finish, critical = schedule(steps)
print("finish:", " ".join(f"{s}:{t}" for s, t in finish.items()))
print(f"critical path ({finish[critical[-1]]} min):", " -> ".join(critical))
slack = finish["features"] - finish["labels"]
print(f"slack: labels could take {slack} minutes longer and delay nothing")

assert order.index("features") < order.index("train")
assert finish == {"payments": 10, "disputes": 5, "features": 40, "labels": 20,
                  "train": 80, "evaluate": 90, "publish": 95}
assert critical == ["payments", "features", "train", "evaluate", "publish"]
assert slack == 20

# a faster non-critical step changes nothing; a faster critical step does
faster_labels = dict(steps, labels=(1, steps["labels"][1]))
faster_features = dict(steps, features=(15, ["payments"]))
print("labels in 1 min instead of 10    -> total",
      schedule(faster_labels)[0]["publish"])
print("features in 15 min instead of 30 -> total",
      schedule(faster_features)[0]["publish"])
assert schedule(faster_labels)[0]["publish"] == 95
assert schedule(faster_features)[0]["publish"] == 80

# someone makes ingestion wait for the scores this same run will publish
broken = dict(steps, payments=(10, ["publish"]))
try:
    topological_order(broken)
except ValueError as error:
    print(error)
    assert "cycle" in str(error)
