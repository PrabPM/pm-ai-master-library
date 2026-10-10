"""Chapter 107: an agent is a loop. What the loop costs and how errors compound.

Runs a scripted version of PayFlow's operations agent (no model call is made:
the "model" is a fixed list of choices) and checks the two hand calculations
in the chapter.
"""
import numpy as np

READ = {"get_payout_status", "get_merchant_profile"}
WRITE = {"retry_payout"}


def guard(tool):
    """The rule that sits between the model's choice and the real system."""
    if tool in READ:
        return "allow"
    if tool in WRITE:
        return "ask"                 # a person must approve first
    return "deny"                    # anything unknown is refused


def run(choices, max_steps=6, approve=lambda tool, args: True):
    trace = []
    for step, (tool, args) in enumerate(choices, start=1):
        if step > max_steps:
            trace.append((step, "stop", "step budget reached"))
            break
        if tool == "final_answer":
            trace.append((step, tool, "done"))
            break
        verdict = guard(tool)
        if verdict == "ask":
            verdict = "approved" if approve(tool, args) else "rejected"
        trace.append((step, tool, verdict))
    return trace


def task_success(p_step, steps):
    """Chance that every one of `steps` independent steps is right."""
    return p_step ** steps


def input_tokens(steps, base=1500, added_per_step=400):
    """Each step re-reads the whole context, which grows by `added_per_step`."""
    return sum(base + t * added_per_step for t in range(steps))


if __name__ == "__main__":
    # The model's choices for the ticket "payout po_207 to Juniper Bakery failed".
    choices = [
        ("get_payout_status", {"payout_id": "po_207"}),
        ("get_merchant_profile", {"merchant_id": "m_juniper"}),
        ("retry_payout", {"payout_id": "po_207"}),
        ("final_answer", {}),
    ]
    for step, tool, verdict in run(choices):
        print(f"step {step}: {tool:<22} {verdict}")

    print()
    for steps in (1, 3, 6, 10):
        print(f"{steps:>2} steps at 95% each -> task success "
              f"{task_success(0.95, steps):.3f}")
    need = 0.95 ** (1 / 6)
    print(f"per-step accuracy needed for 95% over 6 steps: {need:.4f}")

    one, six = input_tokens(1), input_tokens(6)
    print(f"input tokens: 1 step {one:,}   6 steps {six:,}   ratio {six / one:.0f}x")

    # A simulation agrees with the formula.
    rng = np.random.default_rng(7)
    ok = (rng.random((20_000, 6)) < 0.95).all(axis=1).mean()
    print(f"simulated 6-step success over 20,000 runs: {ok:.3f}")

    assert np.isclose(task_success(0.95, 6), 0.7351, atol=1e-4)
    assert np.isclose(task_success(0.95, 3), 0.8574, atol=1e-4)
    assert np.isclose(need, 0.9915, atol=1e-4)
    assert six == 6 * 1500 + 400 * 15 == 15_000 and one == 1500
    assert abs(ok - 0.7351) < 0.01
    assert [v for _, _, v in run(choices)] == ["allow", "allow", "approved", "done"]
    assert run(choices, approve=lambda t, a: False)[2][2] == "rejected"
    assert run([("delete_ledger", {})])[0][2] == "deny"
