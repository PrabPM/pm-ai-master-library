"""Chapter 7: a first-price auction with floors, and yield as expected value."""
from common import heading, table

# region: auction
def run_auction(bids, open_floor, deal_floors):
    """First-price: the highest eligible bid wins and pays what it bid."""
    eligible = []
    for bidder, price, deal in bids:
        floor = deal_floors[deal] if deal else open_floor
        status = "eligible" if price >= floor else f"below floor ${floor:.2f}"
        eligible.append((bidder, price, deal or "open", status))
    live = [b for b in eligible if b[3] == "eligible"]
    winner = max(live, key=lambda b: b[1]) if live else None
    return eligible, winner


bids = [("DSP-A", 21.50, None), ("DSP-B", 26.00, "cardio-endemic-pmp"),
        ("DSP-C", 23.75, "cardio-endemic-pmp"), ("DSP-D", 17.90, None)]
rows, winner = run_auction(bids, open_floor=18.00,
                           deal_floors={"cardio-endemic-pmp": 24.00})
# endregion

heading("One auction")
table(["bidder", "bid_cpm", "path", "status"], rows, {"bid_cpm": ".2f"})
print(f"\nWinner: {winner[0]} pays ${winner[1]:.2f} CPM (first price).")

# region: yield
def revenue_per_1000_requests(eligible, fill, net_cpm, render):
    """Expected publisher revenue for every 1,000 ad requests."""
    return eligible * fill * net_cpm * render


options = [("Floor $8, 900 ms timeout", 0.94, 0.86, 14.20, 0.97),
           ("Floor $14, 900 ms timeout", 0.94, 0.61, 19.80, 0.97),
           ("Floor $14, 2,500 ms timeout", 0.94, 0.70, 20.60, 0.78)]
out = []
for name, eligible, fill, net_cpm, render in options:
    out.append((name, fill, net_cpm, render,
                revenue_per_1000_requests(eligible, fill, net_cpm, render)))
# endregion

heading("Yield for three settings of one placement")
table(["setting", "fill", "net_cpm", "render", "revenue_per_1000_requests"], out,
      {"fill": ".0%", "net_cpm": ".2f", "render": ".0%",
       "revenue_per_1000_requests": ".2f"})
