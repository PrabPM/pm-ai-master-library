-- Grain of integration_event: one row per API call, including retries.
WITH ranked AS (
  SELECT partner_id, status_code, latency_ms,
         ROW_NUMBER() OVER (PARTITION BY partner_id ORDER BY latency_ms) AS rn,
         COUNT(*)     OVER (PARTITION BY partner_id)                     AS n
  FROM integration_event
  WHERE event_at >= datetime('2026-10-09', '-7 days')
)
SELECT
  partner_id,
  COUNT(*)                                                        AS calls,
  ROUND(AVG(CASE WHEN status_code BETWEEN 200 AND 299
                 THEN 1.0 ELSE 0.0 END), 3)                       AS success_rate,
  MAX(CASE WHEN rn = (95 * n + 99) / 100 THEN latency_ms END)     AS p95_latency_ms,
  SUM(status_code = 429)                                          AS rate_limited,
  SUM(status_code >= 500)                                         AS server_errors
FROM ranked
GROUP BY partner_id
ORDER BY success_rate, calls DESC;
