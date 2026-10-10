"""Chapter 119: cost per action, gross margin under three pricing models, and
the return on a cache.

Every price below is illustrative, not any vendor's price list.
"""
import numpy as np

P_IN, P_OUT = 2.00, 10.00        # illustrative USD per million tokens


def cost_per_ticket(tokens_in=5000, tokens_out=500, other=0.005, loops=1):
    return loops * (tokens_in * P_IN + tokens_out * P_OUT) / 1e6 + other * loops


def margin(price, cost):
    return (price - cost) / price


def effective_cost(hit_rate, cost_hit, cost_miss):
    return hit_rate * cost_hit + (1 - hit_rate) * cost_miss


def payback_months(build, volume, cost, cost_with_cache, run):
    """Months for a cache to repay its build cost from net monthly savings."""
    return build / (volume * (cost - cost_with_cache) - run)


if __name__ == "__main__":
    base = cost_per_ticket()
    tail = cost_per_ticket(loops=12)
    blended = 0.96 * base + 0.04 * tail
    capped = 0.96 * base + 0.04 * cost_per_ticket(loops=4)
    print(f"cost per ticket: typical USD {base:.4f}, runaway USD {tail:.4f}")
    print(f"blended USD {blended:.4f}; with a 4-loop cap USD {capped:.4f}")

    # Outcome pricing: USD 0.50 per resolved ticket.
    print(f"outcome price 0.50: margin {margin(0.50, blended):.1%}")

    # Seat pricing: USD 30 per support agent per month, AI included.
    for tickets in (300, 600, 1500):
        ai_cost = tickets * blended
        print(f"seat price 30, {tickets:>5} tickets: AI cost USD {ai_cost:>5.2f}, "
              f"margin {margin(30, ai_cost):.1%}")
    print(f"seat break-even: {30 / blended:,.0f} tickets per seat per month")

    # Usage pricing: cost plus a markup, sold as credits.
    print(f"usage price at 4x cost: USD {4 * blended:.3f} per ticket, "
          f"margin {margin(4 * blended, blended):.0%}")

    # Cache: 30% of tickets answered from a semantic cache at USD 0.001.
    volume, build, run = 800_000, 45_000, 1_000
    eff = effective_cost(0.30, 0.001, blended)
    saving = volume * (blended - eff) - run
    months = payback_months(build, volume, blended, eff, run)
    print(f"effective cost with cache USD {eff:.5f}; net saving USD {saving:,.0f} "
          f"a month; payback {months:.1f} months")

    assert np.isclose(base, 0.020) and np.isclose(tail, 0.240)
    assert np.isclose(blended, 0.0288) and np.isclose(capped, 0.0224)
    assert np.isclose(margin(0.50, blended), 0.9424)
    assert np.isclose(600 * blended, 17.28) and np.isclose(margin(30, 17.28), 0.424)
    assert np.isclose(30 / blended, 1041.67, atol=0.01)
    assert np.isclose(eff, 0.02046) and np.isclose(saving, 5_672)
    assert np.isclose(months, 7.93, atol=0.01) and np.isclose(months, build / saving)
