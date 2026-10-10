"""Chapter 15: liquidity of PayFlow Experts, September 2026, by category."""

# category: (requests posted, matched within 48 hours, median hours to first
#            quote, experts who quoted at least once, jobs rated 4 stars or more)
CATEGORIES = {
    "Store setup": (620, 558, 3, 85, 502),
    "Accounting sync": (410, 328, 9, 48, 279),
    "Tax and compliance": (150, 105, 20, 21, 86),
    "Custom API integration": (340, 139, 41, 19, 97),
}

if __name__ == "__main__":
    print(f"{'category':<24}{'requests':>9}{'fill':>6}{'hours':>7}"
          f"{'req/expert':>12}{'good':>6}")
    tot_req = tot_match = tot_good = tot_experts = 0
    for name, (req, matched, hours, experts, good) in CATEGORIES.items():
        print(f"{name:<24}{req:>9,}{matched / req:>6.0%}{hours:>7}"
              f"{req / experts:>12.1f}{good / req:>6.0%}")
        tot_req, tot_match = tot_req + req, tot_match + matched
        tot_good, tot_experts = tot_good + good, tot_experts + experts
    print(f"{'All categories':<24}{tot_req:>9,}{tot_match / tot_req:>6.0%}"
          f"{'':>7}{tot_req / tot_experts:>12.1f}{tot_good / tot_req:>6.0%}")
    api = CATEGORIES["Custom API integration"]
    print(f"Unfilled API requests: {api[0] - api[1]} of "
          f"{tot_req - tot_match} unfilled in total")
