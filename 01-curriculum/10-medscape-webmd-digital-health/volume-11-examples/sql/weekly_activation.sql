-- Grain: one row per campaign week. Week 1 starts September 14, 2026.
SELECT
  1 + CAST((julianday(date(d.decided_at)) - julianday('2026-09-14')) / 7 AS INT)
                                                          AS campaign_week,
  COUNT(*)                                                AS decisions,
  SUM(d.action = 'offer')                                 AS offers,
  SUM(a.status = 'delivered')                             AS delivered,
  ROUND(100.0 * SUM(a.status = 'delivered')
        / SUM(d.action = 'offer'), 1)                     AS pct_offers_delivered
FROM decision_event d
LEFT JOIN activation_event a USING (decision_id)
GROUP BY campaign_week
ORDER BY campaign_week;
