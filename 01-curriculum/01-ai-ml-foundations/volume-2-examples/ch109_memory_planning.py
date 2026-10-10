"""Chapter 109: what memory costs per step, and when a workflow beats an agent.

All prices are illustrative, not any vendor's price list.
"""
import numpy as np

PRICE_IN = 3.00          # illustrative USD per million input tokens


def context_tokens(system=1200, session_summary=600, retrieved_chunks=5,
                   chunk=400, scratch=300, user=200):
    """Tokens the model re-reads on every step of the loop."""
    return system + session_summary + retrieved_chunks * chunk + scratch + user


def cost_per_task(tokens_per_step, steps):
    return tokens_per_step * steps * PRICE_IN / 1e6


def resolved_share(coverage, p_step, steps):
    """Share of all tickets a design resolves: it must cover the ticket type
    and then get every step right."""
    return coverage * p_step ** steps


if __name__ == "__main__":
    # 1. Memory budget for PayFlow's operations agent.
    full = context_tokens()
    lean = context_tokens(session_summary=300, retrieved_chunks=2)
    for name, tok in (("full memory", full), ("lean memory", lean)):
        c = cost_per_task(tok, steps=6)
        print(f"{name}: {tok:,} tokens a step, USD {c:.4f} a task, "
              f"USD {c * 200_000:,.0f} a month")

    # 2. Workflow, agent or both? 80% of tickets are one of four known types.
    workflow = resolved_share(coverage=0.80, p_step=0.99, steps=3)
    agent = resolved_share(coverage=1.00, p_step=0.95, steps=6)
    known = 0.99 ** 3                       # workflow on the types it covers
    unknown = 0.95 ** 6                     # agent on everything else
    hybrid = 0.80 * known + 0.20 * unknown
    print(f"workflow only: {workflow:.3f}")
    print(f"agent only:    {agent:.3f}")
    print(f"hybrid:        {hybrid:.3f}")

    # 3. A supervisor with a cost cap stops before the call that would break it.
    cap, spent, calls = 0.10, 0.01, []      # 0.01 is the supervisor's own call
    for worker, cost in (("billing", 0.02), ("risk", 0.05), ("kyb", 0.03)):
        if spent + cost > cap:
            calls.append(f"{worker}: skipped")
            continue
        spent += cost
        calls.append(f"{worker}: called")
    print("; ".join(calls), f"| spent USD {spent:.2f} of {cap:.2f}")

    assert full == 4300 and lean == 2800
    assert np.isclose(cost_per_task(full, 6), 0.0774)
    assert np.isclose(cost_per_task(full, 6) * 200_000, 15_480)
    assert np.isclose(workflow, 0.7762, atol=1e-4)
    assert np.isclose(agent, 0.7351, atol=1e-4)
    assert np.isclose(hybrid, 0.9233, atol=1e-4)
    assert np.isclose(spent, 0.08)
