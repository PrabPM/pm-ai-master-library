-- Rates by ASSIGNED variant (intention to treat), not by who was exposed.
WITH assigned AS (
  SELECT hcp_id, variant, assigned_at
  FROM journey_assignment
  WHERE journey_id = 'J-CARDIO'
), outcomes AS (
  SELECT DISTINCT a.hcp_id
  FROM assigned a
  JOIN engagement_event e
    ON e.hcp_id = a.hcp_id
   AND e.event_type = 'qualified_conversion'
   AND e.event_at >= a.assigned_at
   AND e.event_at < datetime(a.assigned_at, '+14 days')
)
SELECT
  a.variant,
  COUNT(*)                                  AS assigned_hcps,
  COUNT(o.hcp_id)                           AS converted_hcps,
  ROUND(1.0 * COUNT(o.hcp_id) / COUNT(*), 4) AS conversion_rate
FROM assigned a
LEFT JOIN outcomes o USING (hcp_id)
GROUP BY a.variant
ORDER BY a.variant DESC;
