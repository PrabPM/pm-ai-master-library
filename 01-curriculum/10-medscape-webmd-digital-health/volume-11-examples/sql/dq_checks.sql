-- Four data-quality rules as one result set: rule, rows checked, failures.
SELECT 'validity: target-list NPI passes check digit' AS rule,
       COUNT(*) AS checked, SUM(1 - npi_valid(npi)) AS failed
FROM target_list
UNION ALL
SELECT 'uniqueness: one row per engagement event_id',
       COUNT(*), COUNT(*) - COUNT(DISTINCT event_id)
FROM engagement_event
UNION ALL
SELECT 'completeness: consent state is known',
       COUNT(*), SUM(consent_state = 'unknown')
FROM hcp_profile
UNION ALL
SELECT 'referential integrity: exposure has an assignment',
       COUNT(*), SUM(a.hcp_id IS NULL)
FROM exposure e
LEFT JOIN journey_assignment a USING (hcp_id);
