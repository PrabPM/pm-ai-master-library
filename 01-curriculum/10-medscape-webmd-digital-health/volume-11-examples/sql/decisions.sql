-- What the decision engine chose, and why. "No action" is a real outcome.
SELECT
  journey_id,
  COUNT(*)                                                  AS decisions,
  ROUND(100.0 * SUM(action = 'offer') / COUNT(*), 1)        AS pct_offer,
  ROUND(100.0 * SUM(action = 'no_action') / COUNT(*), 1)    AS pct_no_action,
  ROUND(100.0 * SUM(action = 'suppress') / COUNT(*), 1)     AS pct_suppress,
  ROUND(100.0 * SUM(reason_code = 'frequency_cap') / COUNT(*), 1)
                                                            AS pct_frequency_cap
FROM decision_event
GROUP BY journey_id
ORDER BY journey_id;
