"""Part VI: the calculations behind the labs and cases."""
from ch13_lift import lift, report
from common import heading, table

# ---- Lab 1: latency budget ------------------------------------------------
# region: latency
budget = [("Request validation and consent", 15),
          ("Identity and context enrichment", 20),
          ("Partner selection and serialization", 10),
          ("Network and DSP bidding", 150),
          ("Bid validation and auction", 20),
          ("Response and safety margin", 35)]
total = sum(ms for _, ms in budget)
assert total == 250
slow_lookup = 100                       # enrichment at its p95 on a bad day
dsp_time_left = 150 - (slow_lookup - 20)
# endregion
heading("Lab 1: auction latency budget")
table(["component", "budget_ms"], budget + [("Total", total)])
print(f"\nIf enrichment takes {slow_lookup} ms, DSPs get {dsp_time_left} ms "
      f"instead of 150 ms.")

# ---- Lab 5: the prescribing decision -------------------------------------
heading("Lab 5: new-prescriber lift, 10,000 per arm, $800,000 campaign")
r = lift(620, 10_000, 540, 10_000)
report(r, 10_000, cost=800_000)
print(f"cost range from the interval  ${800_000 / (r['high'] * 10_000):,.0f} "
      f"to ${800_000 / (r['low'] * 10_000):,.0f}")

# ---- Lab 8: revenue forecast as a range ----------------------------------
# region: forecast
def monthly_revenue(requests, match, bid_rate, win_rate, net_cpm):
    return requests * match * bid_rate * win_rate * net_cpm / 1000


base = {"requests": 40_000_000, "match": 0.10, "bid_rate": 0.65,
        "win_rate": 0.42, "net_cpm": 78.0}
low = {"requests": 36_000_000, "match": 0.08, "bid_rate": 0.60,
       "win_rate": 0.38, "net_cpm": 70.0}
high = {"requests": 44_000_000, "match": 0.12, "bid_rate": 0.70,
        "win_rate": 0.46, "net_cpm": 85.0}
# endregion
heading("Lab 8: monthly revenue forecast")
print(f"all low   ${monthly_revenue(**low):>10,.0f}")
print(f"base      ${monthly_revenue(**base):>10,.0f}")
print(f"all high  ${monthly_revenue(**high):>10,.0f}")
swings = []
for key in base:
    lo = monthly_revenue(**{**base, key: low[key]})
    hi = monthly_revenue(**{**base, key: high[key]})
    swings.append((key, lo, hi, hi - lo))
swings.sort(key=lambda s: -s[3])
print()
table(["input_moved_alone", "revenue_low", "revenue_high", "swing"], swings,
      {"revenue_low": ",.0f", "revenue_high": ",.0f", "swing": ",.0f"})

# ---- Case 2: the underdelivering private marketplace ---------------------
# region: deal
funnel = [("Eligible ad opportunities", 1_024_000, None),
          ("Matched to the target list", 87_040, 0.30),
          ("Bid requests sent with the deal", 85_300, 0.98),
          ("Bids returned", 55_445, 0.70),
          ("Bids at or above the deal floor", 52_670, 0.93),
          ("Auctions won", 22_120, 0.45),
          ("Rendered impressions", 21_454, 0.97),
          ("Viewable impressions", 15_425, 0.70)]
rows, prev = [], None
for name, count, planned in funnel:
    actual = None if prev is None else count / prev
    gap = None if prev is None else actual / planned
    rows.append((name, count, planned, actual, gap))
    prev = count
# endregion
heading("Case 2: deal funnel, forecast rate against actual rate")
table(["stage", "count", "planned_rate", "actual_rate", "actual_vs_plan"], rows,
      {"planned_rate": ".0%", "actual_rate": ".1%", "actual_vs_plan": ".2f"})
match_fix = 21_454 * 0.30 / (87_040 / 1_024_000)
floor_fix = 21_454 * 1.0 / (52_670 / 55_445)
print(f"\nImpressions if match rate reached plan:      {match_fix:,.0f}")
print(f"Impressions if every bid cleared the floor:  {floor_fix:,.0f}")
