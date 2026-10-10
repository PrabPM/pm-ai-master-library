-- Engaged HCPs by specialty and state, with small cells hidden.
SELECT
  p.specialty,
  p.state,
  CASE WHEN COUNT(DISTINCT p.hcp_id) < 11 THEN 'suppressed'
       ELSE CAST(COUNT(DISTINCT p.hcp_id) AS TEXT) END AS engaged_hcps
FROM hcp_profile p
JOIN engagement_event e USING (hcp_id)
WHERE e.qualified = 1
  AND p.specialty IN ('Advanced Heart Failure',
                      'Clinical Cardiac Electrophysiology')
  AND p.state IN ('CA', 'CO', 'VT', 'WY')
GROUP BY p.specialty, p.state
ORDER BY p.specialty, p.state;
