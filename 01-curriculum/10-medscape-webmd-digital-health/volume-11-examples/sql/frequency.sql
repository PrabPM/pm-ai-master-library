-- Grain: one row per exposed HCP, then bucketed. Counts all line items
-- together, which is what a global frequency cap has to do.
WITH per_hcp AS (
  SELECT hcp_id, SUM(impressions) AS imps
  FROM exposure
  GROUP BY hcp_id
)
SELECT
  CASE WHEN imps <= 10 THEN '01-10'
       WHEN imps <= 25 THEN '11-25'
       WHEN imps <= 40 THEN '26-40'
       ELSE '41+' END           AS impressions_in_26_days,
  COUNT(*)                      AS hcps,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_reached
FROM per_hcp
GROUP BY 1
ORDER BY 1;
