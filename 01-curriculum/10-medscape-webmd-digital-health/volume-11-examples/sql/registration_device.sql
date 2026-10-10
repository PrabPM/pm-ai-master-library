SELECT
  variant,
  device,
  SUM(step = 'start')                                           AS started,
  ROUND(100.0 * SUM(step = 'submit') / SUM(step = 'start'), 1)  AS pct_submitted
FROM registration_event
GROUP BY variant, device
ORDER BY variant, device;
