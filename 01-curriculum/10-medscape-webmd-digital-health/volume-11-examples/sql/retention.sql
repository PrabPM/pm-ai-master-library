-- Among members who reached first value: who came back, and when?
WITH activated AS (
  SELECT visitor_id, variant, event_at AS activated_at
  FROM registration_event
  WHERE step = 'first_value'
), returned AS (
  SELECT a.visitor_id,
         MAX(l.login_at <  datetime(a.activated_at, '+8 days'))  AS week_1,
         MAX(l.login_at >= datetime(a.activated_at, '+8 days'))  AS days_8_30
  FROM activated a
  JOIN login_event l USING (visitor_id)
  GROUP BY a.visitor_id
)
SELECT
  a.variant,
  COUNT(*)                                                      AS activated,
  ROUND(100.0 * SUM(COALESCE(r.week_1, 0)) / COUNT(*), 1)       AS pct_back_week_1,
  ROUND(100.0 * SUM(COALESCE(r.days_8_30, 0)) / COUNT(*), 1)    AS pct_back_days_8_30
FROM activated a
LEFT JOIN returned r USING (visitor_id)
GROUP BY a.variant
ORDER BY a.variant;
