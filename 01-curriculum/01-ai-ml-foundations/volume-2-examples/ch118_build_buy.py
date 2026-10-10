"""Chapter 118: build, buy or adapt as positioning, with break-even arithmetic.

All prices and scores are illustrative.
"""
import numpy as np


def position(centrality, data_advantage):
    """Scores from 1 (low) to 5 (high)."""
    if centrality >= 4 and data_advantage >= 4:
        return "build"
    if data_advantage >= 3:
        return "adapt"          # buy the model, add your data (retrieval, tuning)
    return "buy"


def break_even_volume(fixed_per_year, price_buy, cost_own):
    """Yearly volume above which owning is cheaper than paying per call."""
    return fixed_per_year / (price_buy - cost_own)


def three_year_cost(one_time, fixed_per_year, unit_cost, volume_per_year):
    return one_time + 3 * (fixed_per_year + unit_cost * volume_per_year)


if __name__ == "__main__":
    capabilities = {                       # (centrality, data advantage)
        "fraud scoring": (5, 5),
        "dispute evidence summaries": (3, 4),
        "support reply drafts": (2, 3),
        "sales call transcription": (1, 1),
    }
    for name, (c, d) in capabilities.items():
        print(f"{name:<28} centrality {c}  data advantage {d}  -> {position(c, d)}")

    # Dispute summaries: pay per call, or tune and host a small model?
    volume = 6_000_000                               # summaries per year
    v_star = break_even_volume(180_000, 0.012, 0.003)
    buy = three_year_cost(40_000, 0, 0.012, volume)
    own = three_year_cost(150_000, 180_000, 0.003, volume)
    print(f"break-even volume: {v_star:,.0f} summaries a year (PayFlow: {volume:,})")
    print(f"three-year cost: buy USD {buy:,.0f}   own USD {own:,.0f}")

    assert np.isclose(v_star, 20_000_000)
    assert np.isclose(buy, 256_000) and np.isclose(own, 744_000)
    assert [position(*s) for s in capabilities.values()] == ["build", "adapt",
                                                             "adapt", "buy"]
