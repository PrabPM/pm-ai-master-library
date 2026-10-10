"""Chapter 31: from campaign to completed encounter, and honest ROI."""
from common import heading, table

# region: funnel
# Fictional Elkhaven cardiology campaign, 45-day matured cohort.
stages = [("Provider-finder sessions from campaign", 6_200),
          ("Scheduling started", 1_010), ("Appointments scheduled", 640),
          ("Appointments kept (completed encounters)", 512),
          ("Encounters matched to finance records", 468)]
# endregion
heading("Campaign-to-encounter funnel")
rows, prev = [], None
for name, n in stages:
    rows.append((name, n, None if prev is None else 100.0 * n / prev))
    prev = n
table(["stage", "count", "pct_of_previous"], rows, {"pct_of_previous": ".1f"})

# region: roi
matched = 468
gross_charges_each, net_revenue_each = 1_480.00, 505.00
variable_cost_each = 185.00
campaign_cost = 58_000.00
incremental_share = 0.40          # from a geo holdout, not from attribution

gross = matched * gross_charges_each
net = matched * net_revenue_each
contribution = matched * (net_revenue_each - variable_cost_each)
incremental = contribution * incremental_share
# endregion
heading("Three ways to state the result")
out = [("Gross charges, all attributed", gross, (gross - campaign_cost)
        / campaign_cost),
       ("Net revenue, all attributed", net, (net - campaign_cost) / campaign_cost),
       ("Contribution, incremental only", incremental,
        (incremental - campaign_cost) / campaign_cost)]
table(["basis", "value", "roi"], out, {"value": ",.0f", "roi": "+.2f"})
