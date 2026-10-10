"""Chapter 18: what one Assist answer, one ticket and one resolved ticket cost."""
from payflow import (AGENT_COST_PER_MIN, ANSWERS_PER_SESSION, ANSWERS_PER_TICKET,
                     CACHE_HIT_RATE, COMPLEX_TICKETS, EVIDENCE, HISTORY, LARGE,
                     MERCHANT_QUESTIONS, MINUTES_AFTER, MINUTES_BEFORE, OUTPUT,
                     PREFIX, QUESTION, RESOLVED_AFTER, RESOLVED_BEFORE, RETRY_RATE,
                     SEARCH_COST, SESSIONS_RESOLVED, SMALL, TASK_SUCCESS,
                     TOOL_RESULTS, dollars)


# [listing]
def answer_cost(evidence=EVIDENCE, history=HISTORY, output=OUTPUT, reasoning=0,
                cache_hit=CACHE_HIT_RATE, model=LARGE, lines=False):
    """Dollars for one answer: main model, two small helper calls, search."""
    cached = PREFIX * cache_hit
    fresh = PREFIX - cached + history + evidence + TOOL_RESULTS + QUESTION
    helper_in = 300 + evidence + TOOL_RESULTS + output   # rewrite + claim check
    ledger = [
        ("Main model, fresh input", fresh, dollars(fresh, model["input"])),
        ("Main model, cached input", cached, dollars(cached, model["cached"])),
        ("Main model, output", output + reasoning,
         dollars(output + reasoning, model["output"])),
        ("Small model, input", helper_in, dollars(helper_in, SMALL["input"])),
        ("Small model, output", 100, dollars(100, SMALL["output"])),
        ("Search, rerank, tool calls", 0, SEARCH_COST),
    ]
    total = sum(cost for _, _, cost in ledger) * (1 + RETRY_RATE)
    return (total, ledger) if lines else total


def ticket_cost(per_answer, minutes=MINUTES_AFTER, resolved=RESOLVED_AFTER):
    ai = per_answer * ANSWERS_PER_TICKET
    return ai, (ai + minutes * AGENT_COST_PER_MIN) / resolved
# [end listing]


def main():
    total, ledger = answer_cost(lines=True)
    print(f"{'One Assist answer':<28}{'Tokens':>8}{'Dollars':>10}")
    for name, tokens, cost in ledger:
        shown = f"{tokens:,.0f}" if tokens else ""
        print(f"{name:<28}{shown:>8}{cost:>10.5f}")
    print(f"{'Total with 4% retries':<28}{'':>8}{total:>10.5f}")
    print(f"{'Per successful answer':<28}{'':>8}{total / TASK_SUCCESS:>10.5f}")
    print()
    before = MINUTES_BEFORE * AGENT_COST_PER_MIN / RESOLVED_BEFORE
    ai, after = ticket_cost(total)
    print(f"Resolved ticket before Assist: ${before:.2f}")
    print(f"Resolved ticket with Assist:   ${after:.2f}  (AI share ${ai:.3f})")
    session = total * ANSWERS_PER_SESSION / SESSIONS_RESOLVED
    print(f"Resolved merchant session:     ${session:.3f}  (no agent involved)")
    answers = COMPLEX_TICKETS * ANSWERS_PER_TICKET + MERCHANT_QUESTIONS
    tokens = sum(t for _, t, _ in ledger) * (1 + RETRY_RATE) * answers
    print(f"Month: {answers:,.0f} answers, {tokens / 1e6:,.0f} million tokens, "
          f"AI bill ${answers * total:,.0f}")
    print()
    print(f"{'What changes':<36}{'Per answer':>11}{'Resolved ticket':>17}")
    scenarios = [
        ("Base case", {}, {}),
        ("Prompt cache switched off", {"cache_hit": 0}, {}),
        ("20 passages instead of 5", {"evidence": 8_000}, {}),
        ("Long conversation (6,000 tokens)", {"history": 6_000}, {}),
        ("Reasoning on (+1,500 tokens)", {"reasoning": 1_500}, {}),
        ("All three of the above (P95 load)",
         {"evidence": 8_000, "history": 6_000, "reasoning": 1_500}, {}),
        ("Agent one minute slower", {}, {"minutes": MINUTES_AFTER + 1}),
        ("Resolution falls to 74%", {}, {"resolved": 0.74}),
    ]
    for name, answer_args, ticket_args in scenarios:
        per_answer = answer_cost(**answer_args)
        print(f"{name:<36}{per_answer:>11.4f}"
              f"{ticket_cost(per_answer, **ticket_args)[1]:>17.2f}")


if __name__ == "__main__":
    main()
