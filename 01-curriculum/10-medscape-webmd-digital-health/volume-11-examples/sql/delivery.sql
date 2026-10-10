-- Grain: one row per line item, campaign to date.
SELECT
  li.line_item,
  li.buy_type,
  SUM(e.impressions)                                        AS impressions,
  ROUND(1.0 * SUM(e.viewable) / SUM(e.impressions), 3)      AS viewable_rate,
  ROUND(SUM(e.impressions) * li.cpm / 1000.0, 2)            AS spend,
  ROUND(SUM(e.impressions) * li.cpm / SUM(e.viewable), 2)   AS vcpm,
  COUNT(DISTINCT e.hcp_id)                                  AS reach,
  ROUND(1.0 * SUM(e.impressions) / COUNT(DISTINCT e.hcp_id), 1) AS frequency
FROM line_item li
JOIN exposure e USING (line_item)
GROUP BY li.line_item
ORDER BY spend DESC;
