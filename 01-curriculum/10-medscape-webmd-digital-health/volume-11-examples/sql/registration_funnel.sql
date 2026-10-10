-- Grain of registration_event: one row per visitor per step reached.
SELECT
  variant,
  SUM(step = 'start')                  AS started,
  SUM(step = 'submit')                 AS submitted,
  SUM(step = 'email_verified')         AS email_verified,
  SUM(step = 'professional_verified')  AS prof_verified,
  SUM(step = 'first_value')            AS first_value
FROM registration_event
GROUP BY variant
ORDER BY variant;
