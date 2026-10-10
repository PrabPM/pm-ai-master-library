-- Minutes from decision to delivered activation, by channel.
-- SQLite has no PERCENTILE_CONT, so this uses the nearest-rank method.
WITH lat AS (
  SELECT a.channel,
         (julianday(a.activated_at) - julianday(d.decided_at)) * 1440.0 AS minutes
  FROM decision_event d
  JOIN activation_event a USING (decision_id)
  WHERE a.status = 'delivered'
), ranked AS (
  SELECT channel, minutes,
         ROW_NUMBER() OVER (PARTITION BY channel ORDER BY minutes) AS rn,
         COUNT(*)     OVER (PARTITION BY channel)                  AS n
  FROM lat
)
SELECT
  channel,
  MAX(n)                                                         AS delivered,
  ROUND(MAX(CASE WHEN rn = (n + 1) / 2 THEN minutes END), 1)     AS p50_minutes,
  ROUND(MAX(CASE WHEN rn = (95 * n + 99) / 100 THEN minutes END), 1)
                                                                 AS p95_minutes
FROM ranked
GROUP BY channel
ORDER BY p95_minutes;
