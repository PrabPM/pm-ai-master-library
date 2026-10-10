-- Did anyone in the holdout see the campaign? Did everyone in treatment?
SELECT
  a.variant,
  COUNT(*)                                        AS assigned_hcps,
  COUNT(x.hcp_id)                                 AS exposed_hcps,
  ROUND(100.0 * COUNT(x.hcp_id) / COUNT(*), 1)    AS pct_exposed
FROM journey_assignment a
LEFT JOIN (SELECT DISTINCT hcp_id FROM exposure) x USING (hcp_id)
GROUP BY a.variant
ORDER BY a.variant DESC;
