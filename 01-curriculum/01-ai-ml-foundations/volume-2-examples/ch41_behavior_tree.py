"""Chapter 41. A finite state machine and a behavior tree for PayFlow's refund flow."""

# --- Finite state machine: the life of one refund request.
TRANSITIONS = {("received", "identity_ok"): "verified",
               ("received", "identity_failed"): "rejected",
               ("verified", "auto_approved"): "refunded",
               ("verified", "sent_to_human"): "in_review",
               ("in_review", "human_approved"): "refunded",
               ("in_review", "human_denied"): "rejected"}


def run_fsm(events, state="received"):
    for event in events:
        if (state, event) not in TRANSITIONS:
            return f"{state} (illegal event: {event})"
        state = TRANSITIONS[(state, event)]
    return state


# --- Behavior tree: what the support assistant does with a refund request.
SUCCESS, FAILURE, RUNNING = "SUCCESS", "FAILURE", "RUNNING"
LOG = []


def leaf(name, fn):
    def tick(ctx):
        status = fn(ctx)
        LOG.append(f"{name} {status}")
        return status
    return tick


def ok(flag):
    return SUCCESS if flag else FAILURE


def sequence(*children):                  # all children must succeed, in order
    def tick(ctx):
        for child in children:
            status = child(ctx)
            if status != SUCCESS:
                return status             # stop at the first FAILURE or RUNNING
        return SUCCESS
    return tick


def selector(*children):                  # try children until one does not fail
    def tick(ctx):
        for child in children:
            status = child(ctx)
            if status != FAILURE:
                return status
        return FAILURE
    return tick


tree = sequence(
    leaf("verified?", lambda c: ok(c["verified"])),
    selector(
        sequence(leaf("amount <= 50?", lambda c: ok(c["amount"] <= 50)),
                 leaf("auto-refund", lambda c: SUCCESS)),
        leaf("to human", lambda c: SUCCESS if c["human_done"] else RUNNING)),
    leaf("confirm", lambda c: SUCCESS))

if __name__ == "__main__":
    print("FSM:", run_fsm(["identity_ok", "sent_to_human", "human_approved"]))
    print("FSM:", run_fsm(["auto_approved"]))
    waiting = dict(human_done=False)
    cases = [("USD 30, verified", dict(verified=True, amount=30, **waiting)),
             ("USD 120, verified", dict(verified=True, amount=120, **waiting)),
             ("USD 30, not verified", dict(verified=False, amount=30, **waiting))]
    results = []
    for name, ctx in cases:
        LOG.clear()
        results.append(tree(ctx))
        print(f"BT  {name}: {results[-1]}")
        print("    " + " | ".join(LOG))

    # Checks against the hand trace in the chapter.
    assert run_fsm(["identity_ok", "sent_to_human", "human_approved"]) == "refunded"
    assert run_fsm(["auto_approved"]).startswith("received (illegal")
    assert results == [SUCCESS, RUNNING, FAILURE]
    assert len({s for s, _ in TRANSITIONS} | set(TRANSITIONS.values())) == 5
    # Check yourself: once the human finishes, the next tick completes the flow.
    LOG.clear()
    assert tree(dict(verified=True, amount=120, human_done=True)) == SUCCESS
    assert LOG[-1] == "confirm SUCCESS"
